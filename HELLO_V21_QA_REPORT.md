# HELLO! MEET ME — EDU Rebuild v2.1 · QA report

Status: release-candidate for a temporary preview only. Production remains on
`f8b0723af3d128f032d5bde4bd5b8d2f1ee27453`.

## Scope

- Topic Hello, L1, L2, Check, lesson Results and topic Result.
- Four-page Hello textbook.
- Two-page A4 worksheet.
- Reusable local speech-card audio and the minimal task renderers required by
  the accepted v2.1 payload.
- No ABC1, Family or other educational payload was changed.

## Educational contract

- L1: 3 theory, 6 scored tasks, 1 mandatory unscored speak training, 1 special
  listen task.
- L2: 3 theory, 6 scored tasks, 1 mandatory unscored speak training, 1 special
  listen task.
- Check: exactly 8 questions and exactly 1 special listen question.
- Lesson Result uses `X из 6`; speak completion is rendered separately.
- Canonical payload uses ASCII apostrophes. `How are you?` and all other
  excluded units are absent from the v2.1 runtime override.
- Speech-card audio is local, repeatable, secondary, and does not select an
  answer or affect scoring.

Automated source contract: `node scripts/check_hello_v21.mjs` — PASS.

## Browser QA

- Viewports: mobile 390×844 and desktop 1366×768.
- Required route completed: Topic → L1 → Result → L2 → Result → Check → topic
  Result.
- Check result: 8/8 in the control run; both diagnostic skill areas rendered.
- Match, scene sorting, function sorting and dialogue order accept tap→tap.
- Speech-card speaker click leaves the option unselected.
- Speak changes only `completed`; it does not add a correct answer or error.
- SAVED/resume restored L1 exactly at theory step 2/3 after a normal exit.
- Locks observed sequentially: L2 locked before L1; Check unlocked after L2;
  ABC1 unlocked after Hello Check; remaining topics retained their real locks.
- First completion awarded the real lesson reward. A completed L1 replay was
  repeated through the UI after the anti-farm guard: balance remained unchanged
  and Result stated that the reward had already been received.
- Topic → textbook → Topic return passed on mobile and desktop.
- JavaScript page-origin errors: 0. (Browser-extension diagnostics excluded.)
- Horizontal overflow: 0 at 390 px and 1366 px.
- Broken/missing images: 0 on inspected routes.
- External runtime URLs in the product source: 0.
- Local Manrope is declared and active on the mobile UX v2 shell; the accepted
  book spread retains its deliberate local serif reading face.

## Worksheet QA

- PDF: 2 pages, A4 (595.276 × 841.89 pt).
- Both pages rendered to PNG and inspected after the final layout change.
- No clipping or overlap; line endpoints, circle targets and 1–4 boxes are
  physically writable at print size.
- No independent English writing or mandatory Latin-name entry.

## Progress compatibility

- Stable IDs `hello`, `hello_l1`, `hello_l2`, `hello_check` are preserved.
- Existing child progress and reward history are not migrated or reset.
- If an older profile only has completed parent `PROG.hello`, the compatibility
  bridge creates completed child summaries with zero coins, preserving locks
  without awarding a second reward.
- Valid old L1/L2 SAVED steps remain addressable because both lessons retain
  three theory steps and seven practice screens. An obsolete parent-only save
  falls back to Topic through the existing resume validation.
- No destructive migration is performed.

## Known preview limitation

Audio is a deterministic offline synthetic QA track generated with two
distinguishable neutral `flite` voices. It is stable and has no runtime network
dependency, but it is not claimed to be final studio child-voice mastering.
