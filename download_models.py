import os
import sys
import urllib.request
import zipfile

MODELS = {
    "ru": ("https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip", "vosk-model-small-ru-0.22"),
    "en": ("https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip", "vosk-model-small-en-us-0.15"),
}


def ensure_vosk_model(lang: str, models_dir: str = "models") -> str:
    if lang not in MODELS:
        raise ValueError(f"No vosk model mapping for lang={lang!r}. Known: {list(MODELS)}")
    url, dirname = MODELS[lang]
    target = os.path.join(models_dir, dirname)
    if os.path.isdir(target):
        return target

    os.makedirs(models_dir, exist_ok=True)
    zip_path = os.path.join(models_dir, dirname + ".zip")
    print(f"Скачиваю {url} ...")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(models_dir)
    os.remove(zip_path)
    return target


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "ru"
    path = ensure_vosk_model(lang)
    print("Модель готова:", path)
