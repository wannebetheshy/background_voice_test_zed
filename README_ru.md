# background_voice

Быстрое сравнение STT-движков (Vosk / Silero / faster-whisper tiny|base) на своих аудио + фоновое прослушивание микрофона. English version: [`README.md`](README.md).

## Установка

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

Системные зависимости:
- `ffmpeg` — декодирование любых аудио (в т.ч. кривых) для Vosk/Silero.
- `libportaudio2` — для записи с микрофона через `sounddevice` (`sudo apt install libportaudio2` на Debian/Kali).

Модели:
- **Vosk** — скачивается автоматически при первом запуске в `models/` (`ru` или `en`, см. `download_models.py`).
- **Whisper** (`faster-whisper`) — скачивается автоматически через huggingface hub при первом запуске.
- **Silero STT** — качается через `torch.hub` при первом запуске. Поддерживает только `en`, `de`, `es` — **русского нет**, для ru используйте vosk или whisper.

## Транскрибация одного файла или микрофона

```bash
./.venv/bin/python transcribe.py --engine whisper --whisper-size tiny --lang ru --file audio.wav
./.venv/bin/python transcribe.py --engine vosk --lang ru --file audio.wav
./.venv/bin/python transcribe.py --engine silero --lang en --file audio.wav

# с микрофона (Enter — старт, Enter — стоп)
./.venv/bin/python transcribe.py --engine whisper --lang ru --mic
```

Печатает текст и, если движок отдаёт word-level таймстемпы (vosk, whisper), список слов с `start`/`end`/`conf`.

## Сравнение точности (WER/CER против твоей эталонной транскрибации)

```bash
./.venv/bin/python compare.py \
  --file broken_audio.wav \
  --reference "текст который реально был сказан" \
  --engines vosk,silero,whisper \
  --lang ru \
  --whisper-size tiny
```

Или эталон из файла: `--reference-file reference.txt`. На выходе — таблица: время инференса, WER, CER и распознанный текст по каждому движку. Движок, который упал с ошибкой (например Silero на `ru`), просто пропускается с сообщением об ошибке — остальные всё равно посчитаются.

## Фоновое прослушивание микрофона (черновой прототип для "start/end word")

```bash
./.venv/bin/python live_listen.py --whisper-size tiny --lang ru
```

Работает так: пишет с микрофона непрерывно, режет поток на сегменты речи простым energy-VAD (RMS-порог + гистерезис, без лишних моделей), на каждом законченном сегменте гоняет Whisper с `word_timestamps=True` и печатает слова с `start`/`end`. Пороги (`--threshold`, `--start-frames`, `--end-frames`) настраиваются под твой микрофон/шум — дефолты грубые, для продакшна лучше заменить energy-VAD на `silero-vad` (отдельная лёгкая модель именно под это), но для быстрой проверки идеи достаточно и этого.

## Тестовые аудио

Сами исходные mp3 (`ru_lvl/*.mp3`, `en_lvl/*.mp3`) не лежат в репозитории — только эталонные транскрибации (`.txt`) и результаты в [`BENCHMARK.md`](BENCHMARK.md). Файлы: https://drive.google.com/drive/folders/1CwY4lNiNfFNHEV4wUJGe_2DAizI22eGB?usp=sharing

## Структура

```
engines/
  base.py        # Word / Transcript / STTEngine
  vosk_engine.py
  silero_engine.py
  whisper_engine.py
audio_utils.py    # декодирование произвольного аудио в PCM16 16kHz через ffmpeg
download_models.py # автозагрузка vosk-моделей
mic_capture.py      # push-to-talk запись с микрофона
transcribe.py        # CLI: файл/микрофон -> текст (+слова)
compare.py            # CLI: файл + эталон -> WER/CER по всем движкам
live_listen.py         # фоновое прослушивание с сегментацией речи
```
