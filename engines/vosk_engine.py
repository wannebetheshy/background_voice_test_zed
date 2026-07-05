import json

from vosk import KaldiRecognizer, Model, SetLogLevel

from audio_utils import load_audio
from engines.base import STTEngine, Transcript, Word

SetLogLevel(-1)  # silence vosk's C++ logging spam


class VoskEngine(STTEngine):
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def transcribe(self, path: str) -> Transcript:
        pcm = load_audio(path, 16000)
        rec = KaldiRecognizer(self.model, 16000)
        rec.SetWords(True)

        data = pcm.tobytes()
        chunk_bytes = 8000  # 4000 samples * 2 bytes
        for i in range(0, len(data), chunk_bytes):
            rec.AcceptWaveform(data[i:i + chunk_bytes])

        result = json.loads(rec.FinalResult())
        words = [
            Word(w["word"], w["start"], w["end"], w.get("conf", 1.0))
            for w in result.get("result", [])
        ]
        return Transcript(text=result.get("text", ""), words=words)
