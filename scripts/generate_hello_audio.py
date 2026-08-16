#!/usr/bin/env python3
"""Generate the checked-in, offline Hello v2.1 voice prompts with ffmpeg/flite."""

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "audio" / "hello"

PHRASES = {
    "hello": "Hello!",
    "hi": "Hi!",
    "good-morning": "Good morning!",
    "goodbye": "Goodbye!",
    "bye": "Bye!",
    "see-you": "See you!",
    "whats-your-name": "What's your name?",
    "my-name-is-mia": "My name is Mia.",
    "my-name-is-ben": "My name is Ben.",
    "im-mia": "I'm Mia.",
    "im-ben": "I'm Ben.",
    "nice-to-meet-you": "Nice to meet you.",
}

VOICES = {"a": "slt", "b": "rms"}


def flite_escape(text: str) -> str:
    return re.sub(r"([\\':])", r"\\\1", text)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, phrase in PHRASES.items():
        for speaker, voice in VOICES.items():
            dest = OUT / f"{key}-{speaker}.mp3"
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i",
                    f"flite=text='{flite_escape(phrase)}':voice={voice}",
                    "-af", "loudnorm=I=-19:LRA=7:TP=-2",
                    "-ar", "24000", "-ac", "1", "-b:a", "48k", str(dest),
                ],
                check=True,
            )


if __name__ == "__main__":
    main()
