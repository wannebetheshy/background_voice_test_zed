from dataclasses import dataclass, field
from typing import List


@dataclass
class Word:
    text: str
    start: float
    end: float
    conf: float = 1.0


@dataclass
class Transcript:
    text: str
    words: List[Word] = field(default_factory=list)


class STTEngine:
    def transcribe(self, path: str) -> Transcript:
        raise NotImplementedError
