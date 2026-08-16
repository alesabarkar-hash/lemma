# HELLO! MEET ME v2.2 — QA report

Baseline: `f8b0723af3d128f032d5bde4bd5b8d2f1ee27453`  
Branch: `edu-rebuild/hello-v2.2`  
Production changed: no.

## Educational contract

- Lesson 1: 3 theory screens, 6 scored tasks, 1 required unscored speak training.
- Lesson 2: 3 theory screens, 6 scored tasks, 1 required unscored speak training.
- Check: 8 independent questions, including exactly one dedicated listen question.
- Lesson Result denominator: 6. Speak is recorded as completed and is never marked correct or incorrect.

## v2.2 corrections

- L1 sorting supports pointer drag-and-drop and tap-to-tap through the same answer resolver.
- A wrong drop returns the card to its source; a correct drop fixes it in the zone; repeats are ignored.
- Digital lesson, Check and worksheet consistently use A = Ben and B = Mia; Mia answers `I'm Mia.`
- Active Hello images use the `scene-wide`, `scene-card` and `character-reaction` roles with separate mobile/desktop focal points.
- The morning scene includes sunrise, school-arrival and backpack cues.
- Textbook reader mode hides global bottom navigation and LUMA while retaining return to Topic Hello.

## Scoring and compatibility

- First perfect lesson completion: 18 lemmas under the existing formula.
- Repeat completion: 0 lemmas for Hello because the existing anti-farm guard is retained.
- `SAVED`, resume format, scoring, rewards and anti-farm were not redesigned.

## Automated static verification

- `node scripts/check_hello_v21.mjs`: PASS.
- `node scripts/check_hello_v22.mjs`: PASS.
- JavaScript inline parse errors: 0.
- Missing local image/audio/document assets: 0.
- External runtime URLs: 0.

## Runtime browser verification

- 15 mobile QA states and 3 desktop QA states rendered.
- Correct pointer drag: accepted and fixed in its zone.
- Wrong pointer drag: returned to the source with feedback.
- Tap-to-tap: accepted through the same resolver.
- Repeated action: blocked; transition to the following task: passed.
- Page JavaScript errors: 0 (browser-extension diagnostics excluded).
- Horizontal overflow: 0.
- Visible missing images: 0.
- External runtime requests: 0.

## Worksheet correction

- Page 1, Task 1 has exactly four situations and four one-to-one lines.
- Mapping: meeting → `Hello!`; morning meeting → `Good morning!`; leaving → `Goodbye!`; farewell wave → `See you!`.
- `Hi!`, `Bye!`, multiple correct mappings and the former six-line instruction are absent from this task.

## Audio status

The current `flite` audio files are temporary QA voiceover. They are not final commercial mastering.
