#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const worksheetSource = fs.readFileSync(path.join(root, "scripts/generate_hello_worksheet.py"), "utf8");
const qaReport = JSON.parse(fs.readFileSync(path.join(root, "docs/qa/HELLO-v2.2-qa-report.json"), "utf8"));
const failures = [];
const ok = (condition, label) => condition ? console.log(`ok  ${label}`) : failures.push(label);
const between = (start, end) => {
  const a = html.indexOf(start);
  const b = html.indexOf(end, a);
  ok(a >= 0 && b > a, `source block ${start}`);
  return a >= 0 && b > a ? html.slice(a, b) : "";
};
const count = (source, pattern) => [...source.matchAll(pattern)].length;

const audioBlock = between("const HELLO_AUDIO_KEYS", "function canonicalSpeechText");
ok(count(audioBlock, /:\s*"[a-z-]+"/g) === 12, "12 canonical speech units");
ok(fs.readdirSync(path.join(root, "assets/audio/hello")).filter(x => x.endsWith(".mp3")).length === 24,
  "24 local voice files (12 × 2)");

const l1 = between("const HELLO_V21_TASKS_L1", "const HELLO_V21_THEORY_L2");
const l2 = between("const HELLO_V21_TASKS_L2", "Object.assign(LESSONS.hello,");
const checkStart = html.lastIndexOf("LESSONS.hello_check={");
const checkEnd = html.indexOf('buildTopicLessons("abc1"', checkStart);
const check = html.slice(checkStart, checkEnd);
ok(count(l1, /\{t:"/g) === 7 && count(l2, /\{t:"/g) === 7, "each lesson has 6 scored + 1 speak");
ok(count(l1, /t:"helloSpeak"/g) === 1 && count(l2, /t:"helloSpeak"/g) === 1, "one speak per lesson");
ok(count(check, /\{t:"/g) === 8 && count(check, /t:"listen"/g) === 1, "Check is 8 questions with one listen");
ok(count(html, /scoredTotal:6/g) >= 2, "lesson denominator remains 6");
ok(html.includes("L.helloV21&&wasDone"), "Hello replay anti-farm guard preserved");

const sorting = between("function bSceneSort", "function bFunctionSort");
ok(sorting.includes("function resolvePlacement"), "single sorting answer resolver");
ok(sorting.includes('resolvePlacement(selected,zone,"tap")'), "tap→tap uses shared resolver");
ok(sorting.includes('resolvePlacement(card,zone,"drag")'), "pointer drag uses shared resolver");
for (const event of ["pointerdown", "pointermove", "pointerup", "pointercancel"])
  ok(sorting.includes(`"${event}"`), `${event} supported`);
ok(sorting.includes('card.dataset.placed="1"') && sorting.includes("zone.appendChild(card)"), "correct placement is fixed once");
ok(sorting.includes('card.dataset.placed==="1"'), "repeat placement is ignored");
ok(sorting.includes("Сценка вернулась на исходное место"), "wrong drag returns with feedback");

ok(html.includes('[["A","Ben","спрашивает"],["B","Mia","отвечает"]]'), "dialogue cast is A Ben / B Mia");
ok(count(check, /speaker:"B",voice:"b",text:"I'm Mia\."/g) === 1, "Check answer belongs to Mia");
ok(!html.includes('[["A","Mia","спрашивает"],["B","Ben","отвечает"]]'), "legacy reversed cast removed");

ok(html.includes('className="hello-theory-figure scene-wide"'), "theory uses scene-wide role");
ok(html.includes('className="hello-task-scene scene-card"'), "tasks use scene-card role");
ok(html.includes("lesson-hello-feedback-art character-reaction"), "feedback uses reaction role");
ok(html.includes("object-fit:contain"), "Hello scenes avoid hard cover crop");
ok(html.includes('morning:"assets/topics/hello/hello-morning-arrival-worksheet-v1.webp"'), "unambiguous morning scene active");
ok(html.includes('body:has(#s-chapter:not(.hidden)) nav') && html.includes('body:has(#s-chapter:not(.hidden)) #luma-root'),
  "reader mode hides bottom navigation and LUMA");

const normative = between("const HELLO_V21_THEORY_L1", 'buildTopicLessons("abc1"');
for (const forbidden of ["How are you?", "I'm fine.", "Good afternoon.", "Good evening.", "Good night.", "See you tomorrow.", "How old are you?"])
  ok(!normative.includes(forbidden), `runtime payload excludes ${forbidden}`);
ok(!/https?:\/\/(?!www\.w3\.org\/2000\/svg)/.test(html), "no external runtime URL");

for (const file of [
  "assets/topics/hello/hello-morning-arrival-worksheet-v1.webp",
  "worksheets/tema-01-znakomstvo.pdf",
  "scripts/generate_hello_worksheet.py",
  "docs/HELLO_EDU_REBUILD_v2.2.md",
]) ok(fs.existsSync(path.join(root, file)), `${file} exists`);

ok(worksheetSource.includes('"Соедини ситуацию и реплику."'), "worksheet Task 1 exact instruction");
ok(worksheetSource.includes('phrases = ["See you!", "Hello!", "Goodbye!", "Good morning!"]'),
  "worksheet Task 1 has exactly four normative phrases");
ok(!worksheetSource.includes("Проведи шесть линий") && !worksheetSource.includes("Несколько реплик могут подходить"),
  "worksheet Task 1 legacy multi-match wording removed");
ok(qaReport.worksheet?.task_1_lines === 4 && qaReport.worksheet?.task_1_one_to_one === true,
  "QA report records four one-to-one worksheet matches");
ok(qaReport.audio_mastering?.status === "temporary_qa_voiceover" && qaReport.audio_mastering?.commercial_mastering === false,
  "QA report marks flite audio as temporary, not commercial mastering");

if (failures.length) {
  console.error(`\n${failures.length} failed:`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log("\nHello v2.2 static contract: PASS");
