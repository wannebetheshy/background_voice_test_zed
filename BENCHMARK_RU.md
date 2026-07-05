# Результаты сравнения (Vosk vs Whisper vs Silero)

Прогон через `compare.py` на реальных тестовых аудио пользователя: русский набор лежит в [`ru_lvl/`](ru_lvl/), английский — в [`en_lvl/`](en_lvl/).

## Что такое WER и CER

**WER (Word Error Rate)** — доля ошибок на уровне *слов*. Считается как расстояние Левенштейна между эталонным и распознанным текстом, поделённое на число слов в эталоне:

```
WER = (Substitutions + Deletions + Insertions) / Total words in reference
```

Если модель написала "покое" вместо "покоя" — это одна замена (substitution), и всё слово целиком считается ошибкой, даже если разошлась одна буква. Из-за богатой морфологии русского (падежи, окончания) WER может выглядеть пугающе высоким, хотя смысл распознан почти верно.

**CER (Character Error Rate)** — то же самое, но на уровне *символов*, а не слов. Для языков с богатым словоизменением он честнее показывает реальное качество: опечатка в одном окончании даёт маленький вклад в CER, а не "убивает" всё слово, как в WER.

```
CER = (Substitutions + Deletions + Insertions) / Total characters in reference
```

Оба считаются через `jiwer` в `compare.py`, текст нормализуется (нижний регистр, схлопывание пробелов) перед сравнением. 0.0 = идеальное совпадение, 1.0 = разошлось всё.

## Тестовые файлы

### Русский (`ru_lvl/`)

| Файл | Длительность | Формат | Описание уровня |
|---|---|---|---|
| `ru_lvl/1lvl_ru.mp3` | 11.73с | mp3, 44100Hz, mono | Чистая речь, говорю прямо в микрофон |
| `ru_lvl/2lvl_ru.mp3` | 14.92с | mp3, 44100Hz, mono | Добавлен фоновый шум + отошёл от микрофона |
| `ru_lvl/3lvl_ru.mp3` | 20.90с | mp3, 44100Hz, stereo | Песня (Кино, "Группа крови") — не речь, стресс-тест не для этого продукта |

Silero STT не участвует в русском сравнении: модель не поддерживает русский язык (только en/de/es), падает с ошибкой при попытке — это ограничение самой модели, не бага.

### Английский (`en_lvl/`)

| Файл | Длительность | Формат | Описание уровня |
|---|---|---|---|
| `en_lvl/1lvl_en.mp3` | 13.61с | mp3, 44100Hz, mono | Чистая речь, говорю прямо в микрофон |
| `en_lvl/2lvl_en.mp3` | 13.43с | mp3, 44100Hz, mono | Добавлен фоновый шум + отошёл от микрофона |
| `en_lvl/3lvl_en.mp3` | 14.78с | mp3, 48000Hz, stereo | Песня (не речь, стресс-тест не для этого продукта) |

---

## Русский

### 1lvl — чистая речь

**Reference:**
> Съешь ещё этих мягких французских булок, да выпей чаю. Ведь утро сегодня на удивление прохладное, а впереди нас ждет еще столько дел. Пусть весь мир подождет, пока ты наслаждаешься этим простым моментом покоя

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small ru) | 0.42 | 0.12 | 1.87с | съешь ещё этих мягких французских блок до выпить чаю ведёт сегодня на удивление прохладное впереди нас ждёт ещё столько дел пусть весь мир подождёт пока наслаждаешься этим простым моментом покое |
| Whisper (tiny) | 0.52 | 0.17 | 1.21с | В следующей счет их мягких французских блок до выпеча. Вездюто сегодня на удивление прохладное, впереди на ждет еще столько дел. Пусть в смир подождет, пока наслаждаешься с этим простым моментом покоя. |

### 2lvl — шум + отдалился от микрофона

**Reference:** тот же текст, что и в 1lvl.

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small ru) | 0.36 | 0.11 | 1.78с | съешь ещё этих мягких французских буллок до выпей чаю ведь ветер сегодня на удивление прохладную впереди нас ждёт ещё столько дел пусть весь мир подождёт пока наслаждаешься этим простым моментом покое |
| Whisper (tiny) | 0.52 | 0.19 | 1.23с | Все шищают их мягких французских блок, до выпечают. И тут, вот сегодня, но удивление прохватно, а впереди нас ждет еще столько дел. Пусть весь мир подождет, пока нас вождает с этим простим моментом покоя. |

### 3lvl — песня (не рабочий сценарий, для справки)

**Reference:**
> Группа крови на рукаве
> Мой порядковый номер на рукаве
> Пожелай мне удачи в бою
> Пожелай мне
> Не остаться в этой траве

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small ru) | 0.95 | 0.96 | 2.41с | удачи |
| Whisper (tiny) | 1.00 | 1.00 | 4.42с | *(пусто)* |
| Whisper (base) | 0.71 | 0.40 | 12.30с | Группа, крови, армопарье, Ой, порядка, вытоня, армопарье. Парнала им не удачи в бою, Парнала им не остаться в этой траве. |

## Английский

### 1lvl — чистая речь

**Reference:**
> The morning dew still clings to the meadow grass, and the crisp air holds a promise of quiet adventures ahead. Let the restless world rush by, while you linger in this fleeting, peaceful moment.

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small en) | 0.62 | 0.30 | 1.85с | the money and do still clings to the metal girls and decreased a or holds the promise of quiet adventurous hat led the restless formal to by of i will linger in this fleet and peaceful moment |
| Silero (en) | 0.62 | 0.27 | 1.01с | the money jew still clinks to the medadw grross and the gpair holds the promise of quiet adventures a head and let the rest of worldal by viral linger in the split and peaceful moment |
| Whisper (tiny) | 0.29 | 0.10 | 1.11с | The morning dew still clinks to the metal grass, and the crisp air holds the promise of quite adventure's ahead. Let the rest of the world rush by while you linger in this fleeting peaceful moment. |

### 2lvl — шум + отдалился от микрофона

**Reference:** тот же текст, что и в 1lvl.

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small en) | 0.65 | 0.27 | 1.89с | the morning do still clings to the metal girls and decrease pair holds the promise of client adventurous had little restless for old as by wow your linger on this blatant a peaceful moment |
| Silero (en) | 0.71 | 0.31 | 0.76с | the mon deue still clinks to the mealw gross and decreaseed paayer calls the promise of quiet adventures head l there has to sp ho taash by while you' linger on the slat peaceful moment |
| Whisper (tiny) | 0.32 | 0.13 | 1.16с | The morning dew still clings to the metal grass, and the crisp air holds a promise of quiet adventure's head. Let the rest of the world rush by while you linger and sleep in a peaceful moment. |

### 3lvl — песня (не рабочий сценарий, для справки)

**Reference:**
> I couldn't even hear you on the phone
> We've been caught up in a one-note monotone
> I've been living with my head down, comatose
> Your memory walks as a roving ghost

| Движок | WER | CER | Время | Распознанный текст |
|---|---|---|---|---|
| Vosk (small en) | 1.00 | 0.98 | 2.35с | yeah |
| Silero (en) | 0.87 | 0.57 | 0.73с | i could't any you one for got i don't want know i don't know re when i had down tur yes ever what as a woman go |
| Whisper (tiny) | 0.58 | 0.36 | 1.26с | I couldn't even hear you on the phone, I've been caught up at a window I'm gonna turn over and live with my head down, go to hell I've never realized as a woman goes |

---

## Вывод

**Русский:** на боевых уровнях (1lvl, 2lvl) **Vosk точнее Whisper-tiny** и по WER, и по CER, при этом Whisper-tiny немного быстрее по чистому времени инференса. Ошибки у обоих движков в основном в падежных окончаниях и похожих по звучанию словах ("покоя"→"покое", "булок"→"блок") — CER (11-19%) честнее отражает реальное качество, чем формально высокий WER (36-52%).

**Английский:** картина обратная — **Whisper-tiny заметно точнее** и Vosk, и Silero на обоих боевых уровнях (WER 0.29-0.32 против 0.62-0.71 у альтернатив), при сопоставимом времени инференса. Silero чуть быстрее всех по чистому времени, но точность ниже Whisper.

На сильно деградированном/нерепрезентативном аудио (3lvl, песни) все tiny-модели заметно проседают; в русском случае `whisper-base` вытаскивает смысл заметно лучше ценой ~3x времени (в английском base не проверяли).

**Вывод по выбору движка — зависит от языка:**
- Для **русского** — Vosk (лучше на шуме/дистанции, изначально потоковый).
- Для **английского** — Whisper-tiny (заметно точнее обеих альтернатив).

Если фоновый слушатель должен работать на обоих языках сразу, есть развилка: либо гонять оба движка и выбирать по ожидаемому языку речи, либо взять один универсальный (Whisper) ценой просадки точности на русском.

Воспроизвести самому:
```bash
./.venv/bin/python compare.py --file ru_lvl/1lvl_ru.mp3 --reference-file ru_lvl/1lvl.txt --engines vosk,whisper --lang ru
./.venv/bin/python compare.py --file en_lvl/1lvl_en.mp3 --reference-file en_lvl/1lvl.txt --engines vosk,silero,whisper --lang en
```
