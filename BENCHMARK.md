# Comparison Results (Vosk vs Whisper vs Silero)

Run via `compare.py` on the user's real test audio: the Russian set lives in [`ru_lvl/`](ru_lvl/), the English set in [`en_lvl/`](en_lvl/). Русская версия: [`BENCHMARK_RU.md`](BENCHMARK_RU.md).

## What WER and CER mean

**WER (Word Error Rate)** — the error rate at the *word* level. Computed as the Levenshtein distance between the reference and recognized text, divided by the number of words in the reference:

```
WER = (Substitutions + Deletions + Insertions) / Total words in reference
```

If the model wrote "покое" instead of "покоя" (a single wrong case ending), that counts as one substitution — the whole word is scored as an error even if only one letter differs. Because of Russian's rich morphology (cases, endings), WER can look scarily high even when the meaning was recognized almost perfectly.

**CER (Character Error Rate)** — the same idea, but at the *character* level instead of words. For heavily-inflected languages it's a more honest quality signal: a typo in one ending contributes a small amount to CER instead of "killing" the whole word the way WER does.

```
CER = (Substitutions + Deletions + Insertions) / Total characters in reference
```

Both are computed via `jiwer` in `compare.py`; text is normalized (lowercased, whitespace collapsed) before comparison. 0.0 = perfect match, 1.0 = everything differs.

## Test files

### Russian (`ru_lvl/`)

| File | Duration | Format | Level description |
|---|---|---|---|
| `ru_lvl/1lvl_ru.mp3` | 11.73s | mp3, 44100Hz, mono | Clean speech, spoken directly into the mic |
| `ru_lvl/2lvl_ru.mp3` | 14.92s | mp3, 44100Hz, mono | Background noise added + moved away from the mic |
| `ru_lvl/3lvl_ru.mp3` | 20.90s | mp3, 44100Hz, stereo | A song (Kino, "Gruppa Krovi") — not speech, a stress test, not a real target scenario |

Silero STT is excluded from the Russian comparison: the model doesn't support Russian (only en/de/es), it raises an error if you try — a limitation of the model itself, not a bug.

### English (`en_lvl/`)

| File | Duration | Format | Level description |
|---|---|---|---|
| `en_lvl/1lvl_en.mp3` | 13.61s | mp3, 44100Hz, mono | Clean speech, spoken directly into the mic |
| `en_lvl/2lvl_en.mp3` | 13.43s | mp3, 44100Hz, mono | Background noise added + moved away from the mic |
| `en_lvl/3lvl_en.mp3` | 14.78s | mp3, 48000Hz, stereo | A song (not speech, a stress test, not a real target scenario) |

---

## Russian

### 1lvl — clean speech

**Reference:**
> Съешь ещё этих мягких французских булок, да выпей чаю. Ведь утро сегодня на удивление прохладное, а впереди нас ждет еще столько дел. Пусть весь мир подождет, пока ты наслаждаешься этим простым моментом покоя

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small ru) | 0.42 | 0.12 | 1.87s | съешь ещё этих мягких французских блок до выпить чаю ведёт сегодня на удивление прохладное впереди нас ждёт ещё столько дел пусть весь мир подождёт пока наслаждаешься этим простым моментом покое |
| Whisper (tiny) | 0.52 | 0.17 | 1.21s | В следующей счет их мягких французских блок до выпеча. Вездюто сегодня на удивление прохладное, впереди на ждет еще столько дел. Пусть в смир подождет, пока наслаждаешься с этим простым моментом покоя. |

### 2lvl — noise + moved away from the mic

**Reference:** same text as 1lvl.

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small ru) | 0.36 | 0.11 | 1.78s | съешь ещё этих мягких французских буллок до выпей чаю ведь ветер сегодня на удивление прохладную впереди нас ждёт ещё столько дел пусть весь мир подождёт пока наслаждаешься этим простым моментом покое |
| Whisper (tiny) | 0.52 | 0.19 | 1.23s | Все шищают их мягких французских блок, до выпечают. И тут, вот сегодня, но удивление прохватно, а впереди нас ждет еще столько дел. Пусть весь мир подождет, пока нас вождает с этим простим моментом покоя. |

### 3lvl — song (not a real scenario, for reference only)

**Reference:**
> Группа крови на рукаве
> Мой порядковый номер на рукаве
> Пожелай мне удачи в бою
> Пожелай мне
> Не остаться в этой траве

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small ru) | 0.95 | 0.96 | 2.41s | удачи |
| Whisper (tiny) | 1.00 | 1.00 | 4.42s | *(empty)* |
| Whisper (base) | 0.71 | 0.40 | 12.30s | Группа, крови, армопарье, Ой, порядка, вытоня, армопарье. Парнала им не удачи в бою, Парнала им не остаться в этой траве. |

## English

### 1lvl — clean speech

**Reference:**
> The morning dew still clings to the meadow grass, and the crisp air holds a promise of quiet adventures ahead. Let the restless world rush by, while you linger in this fleeting, peaceful moment.

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small en) | 0.62 | 0.30 | 1.85s | the money and do still clings to the metal girls and decreased a or holds the promise of quiet adventurous hat led the restless formal to by of i will linger in this fleet and peaceful moment |
| Silero (en) | 0.62 | 0.27 | 1.01s | the money jew still clinks to the medadw grross and the gpair holds the promise of quiet adventures a head and let the rest of worldal by viral linger in the split and peaceful moment |
| Whisper (tiny) | 0.29 | 0.10 | 1.11s | The morning dew still clinks to the metal grass, and the crisp air holds the promise of quite adventure's ahead. Let the rest of the world rush by while you linger in this fleeting peaceful moment. |

### 2lvl — noise + moved away from the mic

**Reference:** same text as 1lvl.

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small en) | 0.65 | 0.27 | 1.89s | the morning do still clings to the metal girls and decrease pair holds the promise of client adventurous had little restless for old as by wow your linger on this blatant a peaceful moment |
| Silero (en) | 0.71 | 0.31 | 0.76s | the mon deue still clinks to the mealw gross and decreaseed paayer calls the promise of quiet adventures head l there has to sp ho taash by while you' linger on the slat peaceful moment |
| Whisper (tiny) | 0.32 | 0.13 | 1.16s | The morning dew still clings to the metal grass, and the crisp air holds a promise of quiet adventure's head. Let the rest of the world rush by while you linger and sleep in a peaceful moment. |

### 3lvl — song (not a real scenario, for reference only)

**Reference:**
> I couldn't even hear you on the phone
> We've been caught up in a one-note monotone
> I've been living with my head down, comatose
> Your memory walks as a roving ghost

| Engine | WER | CER | Time | Recognized text |
|---|---|---|---|---|
| Vosk (small en) | 1.00 | 0.98 | 2.35s | yeah |
| Silero (en) | 0.87 | 0.57 | 0.73s | i could't any you one for got i don't want know i don't know re when i had down tur yes ever what as a woman go |
| Whisper (tiny) | 0.58 | 0.36 | 1.26s | I couldn't even hear you on the phone, I've been caught up at a window I'm gonna turn over and live with my head down, go to hell I've never realized as a woman goes |

---

## Conclusion

**Russian:** on the production-relevant levels (1lvl, 2lvl), **Vosk is more accurate than Whisper-tiny** on both WER and CER, while Whisper-tiny is slightly faster in raw inference time. Errors from both engines are mostly case-ending mismatches and similar-sounding words ("покоя"→"покое", "булок"→"блок") — CER (11-19%) reflects real quality more honestly than the formally high WER (36-52%).

**English:** the picture flips — **Whisper-tiny is noticeably more accurate** than both Vosk and Silero on both production levels (WER 0.29-0.32 vs. 0.62-0.71 for the alternatives), at comparable inference time. Silero is slightly the fastest in raw time, but less accurate than Whisper.

On heavily degraded/unrepresentative audio (3lvl, songs) all tiny models drop off sharply; for the Russian case, `whisper-base` recovers meaning noticeably better at ~3x the time (not tested for English 3lvl).

**Engine choice conclusion — depends on language:**
- For **Russian** — Vosk (better on noise/distance, natively streaming).
- For **English** — Whisper-tiny (clearly more accurate than both alternatives).

If the background listener needs to work in both languages at once, there's a fork: either run both engines and pick based on expected speech language, or take one universal engine (Whisper) at the cost of lower accuracy on Russian.

Reproduce yourself:
```bash
./.venv/bin/python compare.py --file ru_lvl/1lvl_ru.mp3 --reference-file ru_lvl/1lvl.txt --engines vosk,whisper --lang ru
./.venv/bin/python compare.py --file en_lvl/1lvl_en.mp3 --reference-file en_lvl/1lvl.txt --engines vosk,silero,whisper --lang en
```
