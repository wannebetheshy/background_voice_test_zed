import argparse
import time

from jiwer import cer, wer

from download_models import ensure_vosk_model
from engines.silero_engine import SileroEngine
from engines.vosk_engine import VoskEngine
from engines.whisper_engine import WhisperEngine


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def run_engine(name: str, path: str, lang: str, whisper_size: str):
    t0 = time.time()
    if name == "vosk":
        engine = VoskEngine(ensure_vosk_model(lang))
    elif name == "silero":
        engine = SileroEngine(language=lang)
    elif name == "whisper":
        engine = WhisperEngine(model_size=whisper_size, language=None if lang == "auto" else lang)
    else:
        raise ValueError(f"Unknown engine: {name}")
    result = engine.transcribe(path)
    return result, time.time() - t0


def main():
    ap = argparse.ArgumentParser(description="Сравнить точность Vosk/Silero/Whisper на одном аудио")
    ap.add_argument("--file", required=True)
    ap.add_argument("--reference", help="Эталонный текст (что реально сказано)")
    ap.add_argument("--reference-file", help="Путь к .txt с эталонным текстом")
    ap.add_argument("--engines", default="vosk,silero,whisper")
    ap.add_argument("--lang", default="ru")
    ap.add_argument("--whisper-size", default="tiny", choices=["tiny", "base"])
    args = ap.parse_args()

    reference = args.reference
    if args.reference_file:
        with open(args.reference_file, encoding="utf-8") as f:
            reference = f.read().strip()

    rows = []
    for name in [n.strip() for n in args.engines.split(",") if n.strip()]:
        print(f"[{name}] обрабатываю...")
        try:
            result, dt = run_engine(name, args.file, args.lang, args.whisper_size)
        except Exception as e:
            print(f"[{name}] ОШИБКА: {e}")
            continue
        row = {"engine": name, "text": result.text, "time": dt}
        if reference:
            row["wer"] = wer(normalize(reference), normalize(result.text))
            row["cer"] = cer(normalize(reference), normalize(result.text))
        rows.append(row)

    print()
    if reference:
        print("REFERENCE:", reference)
        print()
    header = f"{'Engine':<10} {'Time(s)':<8} {'WER':<8} {'CER':<8}  Text"
    print(header)
    print("-" * len(header))
    for r in rows:
        wer_s = f"{r['wer']:.2f}" if "wer" in r else "-"
        cer_s = f"{r['cer']:.2f}" if "cer" in r else "-"
        print(f"{r['engine']:<10} {r['time']:<8.2f} {wer_s:<8} {cer_s:<8}  {r['text']}")


if __name__ == "__main__":
    main()
