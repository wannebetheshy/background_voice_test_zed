import subprocess

import numpy as np


def load_audio(path: str, sr: int = 16000) -> np.ndarray:
    """Decode any audio file (mp3/ogg/broken headers/whatever) to mono PCM16 via ffmpeg."""
    cmd = [
        "ffmpeg", "-nostdin", "-threads", "0", "-i", path,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr), "-",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed to decode {path}:\n{proc.stderr.decode(errors='ignore')}")
    return np.frombuffer(proc.stdout, np.int16)
