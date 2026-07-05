from typing import Optional

from faster_whisper import WhisperModel

from engines.base import STTEngine, Transcript, Word


class WhisperEngine(STTEngine):
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8",
        language: Optional[str] = None,
    ):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.language = language

    def transcribe(self, path: str) -> Transcript:
        segments, _info = self.model.transcribe(path, language=self.language, word_timestamps=True)
        words = []
        chunks = []
        for seg in segments:
            chunks.append(seg.text.strip())
            for w in seg.words or []:
                words.append(Word(w.word.strip(), w.start, w.end, w.probability))
        return Transcript(text=" ".join(chunks).strip(), words=words)
