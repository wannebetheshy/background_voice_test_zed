import argparse
import queue
import tempfile

import numpy as np
import sounddevice as sd
import soundfile as sf

from engines.whisper_engine import WhisperEngine

SAMPLE_RATE = 16000
BLOCK_SIZE = 512  # ~32ms at 16kHz

# Simple energy-based VAD with hysteresis: cheap, no extra model to load,
# good enough to chop continuous mic audio into speech segments before
# handing each segment to Whisper for transcription + word timestamps.


def main():
    ap = argparse.ArgumentParser(description="Фоновое прослушивание микрофона: VAD + транскрибация по словам")
    ap.add_argument("--whisper-size", default="tiny", choices=["tiny", "base"])
    ap.add_argument("--lang", default="ru", help="ru/en/auto")
    ap.add_argument("--threshold", type=float, default=0.02, help="Порог RMS энергии для речи")
    ap.add_argument("--start-frames", type=int, default=3, help="Сколько подряд 'громких' блоков считать началом речи")
    ap.add_argument("--end-frames", type=int, default=15, help="Сколько подряд 'тихих' блоков считать концом речи")
    args = ap.parse_args()

    print("Загружаю Whisper...")
    engine = WhisperEngine(model_size=args.whisper_size, language=None if args.lang == "auto" else args.lang)

    q: "queue.Queue[np.ndarray]" = queue.Queue()

    def callback(indata, frame_count, time_info, status):
        q.put(indata[:, 0].copy())

    in_speech = False
    loud_run = 0
    quiet_run = 0
    speech_buffer = []

    def flush_segment():
        nonlocal speech_buffer
        if not speech_buffer:
            return
        audio = np.concatenate(speech_buffer)
        speech_buffer = []
        if len(audio) < SAMPLE_RATE * 0.2:  # skip tiny blips
            return
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, audio, SAMPLE_RATE)
        result = engine.transcribe(tmp.name)
        if result.text.strip():
            print(">>>", result.text.strip())
            for w in result.words:
                print(f"    [{w.start:5.2f}-{w.end:5.2f}] {w.text}")

    print("Слушаю микрофон... Ctrl+C для выхода.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=BLOCK_SIZE, callback=callback):
        try:
            while True:
                frame = q.get()
                rms = float(np.sqrt(np.mean(frame.astype(np.float64) ** 2)))
                loud = rms > args.threshold

                if loud:
                    loud_run += 1
                    quiet_run = 0
                else:
                    quiet_run += 1
                    loud_run = 0

                if not in_speech and loud_run >= args.start_frames:
                    in_speech = True
                    speech_buffer = []

                if in_speech:
                    speech_buffer.append(frame)

                if in_speech and quiet_run >= args.end_frames:
                    in_speech = False
                    flush_segment()
        except KeyboardInterrupt:
            flush_segment()
            print("Стоп.")


if __name__ == "__main__":
    main()
