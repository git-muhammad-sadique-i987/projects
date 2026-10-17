#!/usr/bin/env python3
"""Speak Urdu with a Pakistani neural voice, fixing known mispronunciations first.

The speech text is passed through speech_lexicon.tsv (display spelling -> spelling the
voice says correctly, e.g. کلاسک -> کْلاسک so it stops saying "ka-lassic"), then sent to
Microsoft's ur-PK voice via edge-tts, with retries because the connection drops at times.

Usage:
  urdu_tts.py --text "..." --out file.mp3
  urdu_tts.py --in speech.txt --out file.mp3
  urdu_tts.py --json scenes.json --field narration_ur --id-field id --outdir audio/ur
  urdu_tts.py --in speech.txt --print-speech          # show what the voice will get; no audio

Options: --voice (ur-PK-AsadNeural | ur-PK-UzmaNeural), --rate (+0%), --lexicon PATH,
--timings (write word timings JSON beside each MP3), --force (redo existing files).

Needs: pip install edge-tts; network access to speech.platform.bing.com (HTTPS_PROXY honoured).
"""
import argparse
import asyncio
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEXICON = os.path.join(HERE, "speech_lexicon.tsv")
MARKS = "ً-ْٰ"  # Arabic-script vowel marks count as part of a word


def load_lexicon(path):
    pairs = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) >= 2 and cols[0].strip():
                pairs[cols[0].strip()] = cols[1].strip()
    return pairs


def to_speech(text, lexicon):
    """Apply the lexicon in one pass, longest entries first, whole words only."""
    if not lexicon:
        return text
    keys = sorted(lexicon, key=len, reverse=True)
    pattern = re.compile(
        rf"(?<![\w{MARKS}])(?:{'|'.join(re.escape(k) for k in keys)})(?![\w{MARKS}])")
    return pattern.sub(lambda m: lexicon[m.group(0)], text)


async def synthesize(text, out, voice, rate, timings=False, tries=5):
    import edge_tts  # imported here so --print-speech works without it

    for attempt in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary",
                                        proxy=os.environ.get("HTTPS_PROXY"))
            words = []
            with open(out, "wb") as f:
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        start = chunk["offset"] / 10000
                        words.append({"text": chunk["text"], "start_ms": round(start),
                                      "end_ms": round(start + chunk["duration"] / 10000)})
            if os.path.getsize(out) == 0:
                raise RuntimeError("empty audio")
            if timings:
                with open(os.path.splitext(out)[0] + ".words.json", "w", encoding="utf-8") as f:
                    json.dump(words, f, ensure_ascii=False, indent=1)
            return words
        except Exception as e:  # aiohttp and edge_tts raise several error types on drops
            if attempt == tries - 1:
                raise
            wait = 2 ** (attempt + 1)
            print(f"retry in {wait}s after {type(e).__name__}: {e}", file=sys.stderr)
            await asyncio.sleep(wait)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--in", dest="infile")
    src.add_argument("--json", help="JSON list of objects; one MP3 per object")
    ap.add_argument("--field", default="narration_ur", help="JSON field holding the speech text")
    ap.add_argument("--id-field", default="id", help="JSON field used for the file name")
    ap.add_argument("--out", help="output MP3 (with --text/--in)")
    ap.add_argument("--outdir", help="output folder (with --json)")
    ap.add_argument("--voice", default="ur-PK-AsadNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON)
    ap.add_argument("--timings", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print-speech", action="store_true")
    args = ap.parse_args()

    lexicon = load_lexicon(args.lexicon) if args.lexicon and os.path.exists(args.lexicon) else {}

    if args.json:
        items = json.load(open(args.json, encoding="utf-8"))
        jobs = [(str(it[args.id_field]), it[args.field]) for it in items]
    else:
        text = args.text if args.text is not None else open(args.infile, encoding="utf-8").read()
        jobs = [("out", text)]

    if args.print_speech:
        for name, text in jobs:
            print(f"[{name}] {to_speech(text, lexicon)}")
        return 0

    async def run():
        for name, text in jobs:
            if args.json:
                if not args.outdir:
                    sys.exit("--outdir is required with --json")
                os.makedirs(args.outdir, exist_ok=True)
                out = os.path.join(args.outdir, name + ".mp3")
            else:
                if not args.out:
                    sys.exit("--out is required")
                out = args.out
            if os.path.exists(out) and os.path.getsize(out) > 0 and not args.force:
                print(f"skip {out} (exists)")
                continue
            await synthesize(to_speech(text, lexicon), out, args.voice, args.rate, args.timings)
            print(f"wrote {out}")

    asyncio.run(run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
