import numpy as np
import torch

from audio_utils import load_audio
from engines.base import STTEngine, Transcript

# Silero STT (snakers4/silero-models) natively supports: en, de, es.
# There is no Russian silero_stt model — use vosk or whisper for ru audio.
SUPPORTED_LANGUAGES = ("en", "de", "es")


class SileroEngine(STTEngine):
    def __init__(self, language: str = "en", device: str = "cpu"):
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"silero_stt does not support language={language!r}; "
                f"supported: {SUPPORTED_LANGUAGES}. Use --engine vosk or --engine whisper for other languages."
            )
        self.device = torch.device(device)
        self.model, self.decoder, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_stt",
            language=language,
            device=self.device,
            trust_repo=True,
        )
        self.model.to(self.device)
        (_, _, _, self.prepare_model_input) = utils

    def transcribe(self, path: str) -> Transcript:
        pcm = load_audio(path, 16000).astype(np.float32) / 32768.0
        wav = torch.from_numpy(pcm)
        inp = self.prepare_model_input([wav], device=self.device)
        output = self.model(inp)
        text = self.decoder(output[0].cpu())
        return Transcript(text=text, words=[])  # no word-level timestamps from silero_stt
