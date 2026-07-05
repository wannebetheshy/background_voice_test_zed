# background_voice

Quick comparison of STT engines (Vosk / Silero / faster-whisper tiny|base) on your own audio + background microphone listening. Русская версия: [`README_ru.md`](README_ru.md).

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

System dependencies:
- `ffmpeg` — decodes arbitrary (including broken) audio for Vosk/Silero.
- `libportaudio2` — for microphone recording via `sounddevice` (`sudo apt install libportaudio2` on Debian/Kali).

Models:
- **Vosk** — downloaded automatically on first run into `models/` (`ru` or `en`, see `download_models.py`).
- **Whisper** (`faster-whisper`) — downloaded automatically via the huggingface hub on first run.
- **Silero STT** — downloaded via `torch.hub` on first run. Only supports `en`, `de`, `es` — **no Russian**, use vosk or whisper for ru.

## Transcribing a single file or the microphone

```bash
./.venv/bin/python transcribe.py --engine whisper --whisper-size tiny --lang ru --file audio.wav
./.venv/bin/python transcribe.py --engine vosk --lang ru --file audio.wav
./.venv/bin/python transcribe.py --engine silero --lang en --file audio.wav

# from the microphone (Enter to start, Enter to stop)
./.venv/bin/python transcribe.py --engine whisper --lang ru --mic
```

Prints the text and, if the engine provides word-level timestamps (vosk, whisper), a list of words with `start`/`end`/`conf`.

## Accuracy comparison (WER/CER against your reference transcript)

```bash
./.venv/bin/python compare.py \
  --file broken_audio.wav \
  --reference "the text that was actually said" \
  --engines vosk,silero,whisper \
  --lang ru \
  --whisper-size tiny
```

Or a reference from a file: `--reference-file reference.txt`. Output is a table: inference time, WER, CER, and the recognized text for each engine. An engine that raises an error (e.g. Silero on `ru`) is simply skipped with an error message — the rest are still scored.

## Background microphone listening (rough prototype for "start/end word")

```bash
./.venv/bin/python live_listen.py --whisper-size tiny --lang ru
```

How it works: continuously records from the mic, chops the stream into speech segments with a simple energy-based VAD (RMS threshold + hysteresis, no extra models), runs Whisper with `word_timestamps=True` on each completed segment, and prints words with `start`/`end`. Thresholds (`--threshold`, `--start-frames`, `--end-frames`) need tuning for your mic/noise — the defaults are rough. For production, swap the energy-VAD for `silero-vad` (a small dedicated model for this), but for a quick sanity check this is enough.

## Test audio

The original mp3 source files (`ru_lvl/*.mp3`, `en_lvl/*.mp3`) aren't in the repository — only the reference transcripts (`.txt`) and results in [`BENCHMARK.md`](BENCHMARK.md). Files: https://drive.google.com/drive/folders/1CwY4lNiNfFNHEV4wUJGe_2DAizI22eGB?usp=sharing

## Structure

```
engines/
  base.py        # Word / Transcript / STTEngine
  vosk_engine.py
  silero_engine.py
  whisper_engine.py
audio_utils.py    # decode arbitrary audio to PCM16 16kHz via ffmpeg
download_models.py # auto-download vosk models
mic_capture.py      # push-to-talk microphone recording
transcribe.py        # CLI: file/mic -> text (+ words)
compare.py            # CLI: file + reference -> WER/CER across all engines
live_listen.py         # background listening with speech segmentation
```
