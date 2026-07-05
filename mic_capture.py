import tempfile

import numpy as np
import sounddevice as sd
import soundfile as sf


def record_until_enter(samplerate: int = 16000) -> str:
    """Simple push-to-talk style capture: Enter to start, Enter to stop."""
    input("Нажми Enter, чтобы начать запись...")
    print("Идёт запись... Нажми Enter, чтобы остановить.")

    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=samplerate, channels=1, dtype="int16", callback=callback):
        input()

    audio = np.concatenate(frames, axis=0) if frames else np.zeros((0, 1), dtype=np.int16)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, samplerate)
    print("Сохранено во", tmp.name)
    return tmp.name
