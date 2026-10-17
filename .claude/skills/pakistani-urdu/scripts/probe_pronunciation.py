#!/usr/bin/env python3
"""Compare how an Urdu TTS voice says different spellings of the same word.

Why: Urdu script leaves short vowels unwritten, so the voice has to guess them.
English loanwords that start with a consonant cluster (classic, frame, brake,
plate) often get an extra vowel ("ka-lassic"). Diacritics such as jazm/sukun
(U+0652) or writing the word in Latin script can stop that, but you cannot
know which works without testing, and you usually cannot listen yourself.

This script gives two kinds of evidence:
  1. Timing: each variant is spoken inside the same carrier sentence and the
     voice's own word timings are recorded. An inserted vowel adds roughly
     40-90 ms, so a variant that is clearly shorter than the plain spelling,
     and close to nothing-inserted, has probably lost the extra vowel.
     Include a control spelled WITH the vowel (e.g. کَلاسِک) to calibrate.
  2. A listening sheet (MP3): every variant is announced by number
     ("ایک", "دو", ...) and spoken in the carrier, so a native speaker can
     pick the right one in under a minute.

Usage:
  probe_pronunciation.py --out DIR spec.json
  probe_pronunciation.py --out DIR "classic=کلاسک|کْلاسِک|Classic|کَلاسِک"

spec.json: [{"word": "classic", "variants": ["کلاسک", "کْلاسِک", "Classic", "کَلاسِک"]}]
  Optional per group: "intro" (spoken before the group in the listening sheet).
  A variant can be {"text": "...", "voice": "ur-PK-UzmaNeural"} to compare voices.
  Use --carrier "{}" when each variant is already a full sentence.

Needs: edge-tts (pip install edge-tts), ffmpeg, and network access to
speech.platform.bing.com. Uses HTTPS_PROXY if set.
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile

import edge_tts

NUMBERS = ["ایک", "دو", "تین", "چار", "پانچ", "چھ", "سات", "آٹھ", "نو", "دس"]


async def speak(text, voice, rate, path, tries=5):
    """Synthesize text to path; return list of (text, start_ms, end_ms) word timings.

    The speech service drops connections now and then, so retry with backoff.
    """
    for attempt in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary",
                                        proxy=os.environ.get("HTTPS_PROXY"))
            words = []
            with open(path, "wb") as f:
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        start = chunk["offset"] / 10000
                        words.append((chunk["text"], start, start + chunk["duration"] / 10000))
            return words
        except Exception as e:  # network errors surface as several aiohttp/edge_tts types
            if attempt == tries - 1:
                raise
            wait = 2 ** (attempt + 1)
            print(f"  retry in {wait}s after: {type(e).__name__}", file=sys.stderr)
            await asyncio.sleep(wait)


def target_span(words):
    """Duration of everything between the first and last carrier word."""
    if len(words) < 3:
        return None
    return words[-2][2] - words[1][1]


def load_spec(args):
    groups = []
    for item in args.spec:
        if os.path.exists(item):
            groups += json.load(open(item, encoding="utf-8"))
        else:
            word, _, variants = item.partition("=")
            groups.append({"word": word, "variants": variants.split("|")})
    return groups


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="+", help="spec.json file(s) or word=v1|v2|v3")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--voice", default="ur-PK-AsadNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--carrier", default="یہ {} ہے۔", help="sentence with {} where the word goes")
    ap.add_argument("--no-sheet", action="store_true", help="skip the listening MP3")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    groups = load_spec(args)
    tmp = tempfile.mkdtemp(prefix="probe-")
    sheet_parts, report = [], []

    async def run():
        for gi, g in enumerate(groups):
            rows = []
            if g.get("intro") and not args.no_sheet:  # e.g. "پہلا لفظ۔" so the listener can keep track
                intro = os.path.join(tmp, f"g{gi}-intro.mp3")
                await speak(g["intro"], args.voice, args.rate, intro)
                sheet_parts.append(intro)
            for i, v in enumerate(g["variants"]):
                # a variant is a spelling, or {"text": ..., "voice": ...} to compare voices
                text = v if isinstance(v, str) else v["text"]
                voice = args.voice if isinstance(v, str) else v.get("voice", args.voice)
                clip = os.path.join(tmp, f"g{gi}-{i}.mp3")
                words = await speak(args.carrier.format(text), voice, args.rate, clip)
                span = target_span(words)
                rows.append({"n": i + 1, "variant": text, "voice": voice,
                             "ms": None if span is None else round(span),
                             "tokens": [w[0] for w in words[1:-1]]})
                if not args.no_sheet:
                    label = os.path.join(tmp, f"g{gi}-{i}-n.mp3")
                    await speak(NUMBERS[i] + "۔", args.voice, args.rate, label)
                    sheet_parts.extend([label, clip])  # extend, not +=, keeps the outer list
            report.append({"word": g["word"], "rows": rows})

    asyncio.run(run())

    for g in report:
        base = g["rows"][0]["ms"]
        print(f"\n{g['word']}")
        for r in g["rows"]:
            delta = "" if base is None or r["ms"] is None else f"{r['ms'] - base:+5d} ms vs plain"
            print(f"  {r['n']}. {r['variant']:<14} {str(r['ms']):>5} ms  {delta}  tokens={r['tokens']}")
    json.dump(report, open(os.path.join(args.out, "probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if sheet_parts:
        gap = os.path.join(tmp, "gap.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", "0.6", "-q:a", "9", gap], check=True)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as f:
            for p in sheet_parts:
                f.write(f"file '{p}'\nfile '{gap}'\n")
        sheet = os.path.join(args.out, "listening-sheet.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-ar", "24000", "-ac", "1", "-b:a", "64k", sheet], check=True)
        print(f"\nlistening sheet: {sheet}")


if __name__ == "__main__":
    sys.exit(main())
