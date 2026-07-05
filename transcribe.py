import argparse

from download_models import ensure_vosk_model
from engines.silero_engine import SileroEngine
from engines.vosk_engine import VoskEngine
from engines.whisper_engine import WhisperEngine


def build_engine(name: str, lang: str, whisper_size: str):
    if name == "vosk":
        model_path = ensure_vosk_model(lang)
        return VoskEngine(model_path)
    if name == "silero":
        return SileroEngine(language=lang)
    if name == "whisper":
        return WhisperEngine(model_size=whisper_size, language=None if lang == "auto" else lang)
    raise ValueError(f"Unknown engine: {name}")


def main():
    ap = argparse.ArgumentParser(description="Транскрибация файла или микрофона одним из движков")
    ap.add_argument("--engine", choices=["vosk", "silero", "whisper"], required=True)
    ap.add_argument("--lang", default="ru", help="ru/en/auto (auto только для whisper)")
    ap.add_argument("--whisper-size", default="tiny", choices=["tiny", "base"])
    ap.add_argument("--file", help="Путь к аудиофайлу")
    ap.add_argument("--mic", action="store_true", help="Записать с микрофона вместо файла")
    args = ap.parse_args()

    if not args.file and not args.mic:
        ap.error("нужно указать --file или --mic")

    engine = build_engine(args.engine, args.lang, args.whisper_size)

    path = args.file
    if args.mic:
        from mic_capture import record_until_enter
        path = record_until_enter()

    result = engine.transcribe(path)
    print()
    print("TEXT:", result.text)
    if result.words:
        print("WORDS:")
        for w in result.words:
            print(f"  [{w.start:6.2f} - {w.end:6.2f}] {w.text}  (conf={w.conf:.2f})")


if __name__ == "__main__":
    main()
