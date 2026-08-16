# HELLO! MEET ME — EDU REBUILD v2.2

Статус: кандидат на приёмку. База продукта: LEMMA v1.57.0 (`f8b0723af3d128f032d5bde4bd5b8d2f1ee27453`).

## Норматив модуля

- ID темы: `hello`.
- Lesson 1: 3 theory, 6 проверяемых заданий, 1 обязательная устная тренировка.
- Lesson 2: 3 theory, 6 проверяемых заданий, 1 обязательная устная тренировка.
- Check: ровно 8 самостоятельных вопросов, из них 1 специальный listen-вопрос.
- Результат урока: `Правильно: X из 6`; устная тренировка показывается отдельно.
- Speak получает `completed=true`, но не получает `correct/incorrect`, не входит в score, процент или ошибки.
- Support audio каждой английской speech-card не выбирает ответ и не влияет на score.
- Canonical строки используют ASCII apostrophe: `What's your name?`, `I'm Mia.`, `I'm...`.

## Речевые единицы

Lesson 1: `Hello.`, `Hi.`, `Good morning.`, `Goodbye.`, `Bye.`, `See you.`

Lesson 2: `What's your name?`, `My name is...`, `I'm...`, `Nice to meet you.`

Не входят в Hello: `How are you?`, `I'm fine.`, дополнительные приветствия по времени, возраст, страна, spelling имени и ADV.

## Идентичность диалога

- A — Ben — спрашивает.
- B — Mia — отвечает.
- Порядок: A `Hello!` → A `What's your name?` → B `I'm Mia.` → A `Nice to meet you.`
- Эта идентичность одинакова в Lesson 2 dialogue order, Check, textbook и worksheet.

## v2.2: функциональные инварианты

- L1 sorting использует один `resolvePlacement` для pointer drag-and-drop и tap→tap.
- Правильный drop фиксирует сцену в зоне ровно один раз.
- Неправильный drop оставляет сцену в исходном наборе, показывает короткий feedback и не создаёт второй scoring path.
- Повторное действие с уже размещённой сценой игнорируется.
- Reader mode скрывает глобальную нижнюю навигацию и LUMA-orb; возврат ведёт в Topic Hello.

## v2.2: визуальные роли

- `scene-wide` — широкая коммуникативная сцена theory/textbook.
- `scene-card` — компактная 4:3 сцена задания.
- `character-reaction` — небольшая feedback-реакция без тяжёлого квадратного фона.
- Для Hello-сцен заданы отдельные mobile/desktop focal points. Изображения не маскируются жёстким `cover`.
- Утренняя сцена использует вход в класс, рюкзаки, взаимное внимание и утренний свет.

## Защищённая логика

Не изменяются payload других тем, PROG, SAVED/resume, locks, rewards, anti-farm, общий router и production. Merge, production deployment, version bump, tag и release не входят в этот кандидат.
