#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const failures = [];
const ok = (condition, label) => condition ? console.log(`ok  ${label}`) : failures.push(label);
const between = (start, end) => {
  const a = html.indexOf(start);
  const b = html.indexOf(end, a);
  ok(a >= 0 && b > a, `source block ${start}`);
  return a >= 0 && b > a ? html.slice(a, b) : "";
};
const count = (source, pattern) => [...source.matchAll(pattern)].length;

ok(html.includes('const APP_VERSION="1.57.0-hello-v2.1-pilot"'), "pilot version marker");

const audioBlock = between("const HELLO_AUDIO_KEYS", "function canonicalSpeechText");
ok(count(audioBlock, /:\s*"[a-z-]+"/g) === 12, "12 canonical speech units");
const audioFiles = fs.readdirSync(path.join(root, "assets/audio/hello")).filter(x => x.endsWith(".mp3"));
ok(audioFiles.length === 24, "24 local voice files (12 × 2)");

const l1 = between("const HELLO_V21_TASKS_L1", "const HELLO_V21_THEORY_L2");
const l2 = between("const HELLO_V21_TASKS_L2", "Object.assign(LESSONS.hello,");
const checkStart = html.lastIndexOf("LESSONS.hello_check={");
const checkEnd = html.indexOf('buildTopicLessons("abc1"', checkStart);
ok(checkStart >= 0 && checkEnd > checkStart, "source block final Hello Check");
const check = html.slice(checkStart, checkEnd);
ok(count(l1, /\{t:"/g) === 7, "L1 has 7 screens");
ok(count(l2, /\{t:"/g) === 7, "L2 has 7 screens");
ok(count(l1, /t:"helloSpeak"/g) === 1 && count(l2, /t:"helloSpeak"/g) === 1,
  "one unscored speak screen per lesson");
ok(count(l1, /t:"listen"/g) === 1 && count(l2, /t:"listen"/g) === 1,
  "one special listen task per lesson");
ok(count(check, /\{t:"/g) === 8, "Check has exactly 8 questions");
ok(count(check, /t:"listen"/g) === 1, "Check has exactly one special listen question");
ok(html.includes("scoredTotal:6") && count(html, /scoredTotal:6/g) >= 2, "lesson denominator is 6");
ok(html.includes("L.helloV21&&wasDone"), "strict Hello replay anti-farm guard");

const normative = between("const HELLO_V21_THEORY_L1", 'buildTopicLessons("abc1"');
for (const forbidden of ["How are you?", "I'm fine.", "Good afternoon.", "Good evening.", "Good night.", "See you tomorrow.", "How old are you?"])
  ok(!normative.includes(forbidden), `runtime payload excludes ${forbidden}`);
ok(normative.includes("What's your name?") && normative.includes("I'm Mia.") && normative.includes("I'm Ben."),
  "canonical ASCII apostrophes in payload");

const book = between('{id:"b3",title:"Hello! Meet Me"', '{id:"b12",title:"Алфавит a–h"');
ok(count(book, /\{kind:"lemmaBook",spread:/g) === 4, "Hello textbook has 4 pages");
ok(!/https?:\/\/(?!www\.w3\.org\/2000\/svg)/.test(html), "no external runtime URL");

if (failures.length) {
  console.error(`\n${failures.length} failed:`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log("\nHello v2.1 static contract: PASS");
