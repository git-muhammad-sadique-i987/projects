#!/usr/bin/env python3
"""Flag Urdu that will sound Indian, translated, or trip up a TTS voice.

Usage:
  urdu_lint.py FILE [FILE...]            display text (PDFs, slides, subtitles, messages)
  urdu_lint.py --speech FILE [FILE...]   text that a voice will read (adds speech checks)
  urdu_lint.py --json scenes.json --field narration_ur --speech

Every finding is a question to answer, not an automatic error: fix it, or know why it is
right in this context. Categories:
  indian   Hindi/Sanskrit vocabulary, Mumbai slang, Indian usage habits
  calque   English sentence structure copied into Urdu (translationese)
  word     a more natural Pakistani word exists for this context
  speech   problems for text-to-speech (only with --speech)
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from urdu_tts import DEFAULT_LEXICON, MARKS, load_lexicon, to_speech  # noqa: E402


def wb(p):
    """Whole-word pattern for Urdu (vowel marks count as part of the word)."""
    return rf"(?<![\w{MARKS}])(?:{p})(?![\w{MARKS}])"


HINDI = {
    "اپیوگ": "استعمال", "اُپیوگ": "استعمال", "پریوگ": "استعمال", "آوشیک": "ضروری",
    "جانکاری": "معلومات", "سرکشا": "حفاظت", "سُرکشا": "حفاظت", "سمسیا": "مسئلہ",
    "سمے": "وقت", "پرشن": "سوال", "کاریہ": "کام", "کیول": "صرف", "وشیش": "خاص",
    "ویکتی": "شخص / بندہ", "یاتری": "مسافر / سواری", "درگھٹنا": "حادثہ", "سہایتا": "مدد",
    "اپلبدھ": "دستیاب", "پرکار": "قسم / طرح", "پریاس": "کوشش", "پریوار": "گھر والے / خاندان",
    "نمستے": "السلام علیکم", "نمسکار": "السلام علیکم", "دھنیواد": "شکریہ", "سواگت": "خوش آمدید",
    "کرپیا": "مہربانی کر کے", "لگ بھگ": "تقریباً",
}
SLANG = ["بولے تو", "اپن", "بنداس", "جھکاس", "لفڑا", "واٹ لگ", "کھالی پیلی", "کائے کو", "چالو کر"]
PATTERNS = [
    ("indian", wb("ون ٹوئنٹی"), "Pakistanis say model numbers digit by digit: سی جی ون ٹو فائیو"),
    ("indian", r"نے بولا|بولا کہ|مجھے بولو|بولو کہ", "بولنا for 'say/tell' sounds Mumbai; use کہا / بتائیں"),
    ("word", wb("بائیک"), "for mechanics and most adults: موٹر سائیکل (بائیک is fine in casual text)"),
    ("word", wb("ٹینک"), "a motorcycle's tank is ٹینکی"),
    ("word", r"سینٹر اسٹینڈ|سنٹر اسٹینڈ", "Pakistanis call the centre stand ڈبل اسٹینڈ"),
    ("word", wb("اسپراکٹ|سپراکٹ"), "workshop word: گراری"),
    ("word", wb("کیبل|کیبلز"), "for bike cables mechanics say تار"),
    ("word", wb("تھروٹل"), "throttle is ریس in workshop Urdu"),
    ("word", wb("چیسس"), "usually written and said چیسز"),
    ("word", wb("اسٹاک"), "'stock' parts: کمپنی والا / اوریجنل / وہی رہے گا"),
    ("calque", r"(?:جانے|جانا|جانی) (?:چاہئیں|چاہیے|چاہییں|چاہیئے)", "English-style passive; say it actively (e.g. صاف نظر آنے چاہئیں)"),
    ("calque", r"(?:کیا|کیے|کی) جائے(?:ں)?(?![\w])", "passive instruction; prefer کریں / کرنا ہے"),
    ("calque", r"قدم\s*[0-9۰-۹]|پہلا قدم|دوسرا قدم|تیسرا قدم", "heading copied from 'Step N'; say پہلا کام / دوسرا کام"),
    ("calque", r"اہم نکات|خلاصہ", "English heading; say یاد رکھنے کی باتیں / مختصر یہ کہ"),
    ("calque", r"سخت اصول", "literal 'strict rules'; try یہ باتیں پکی ہیں"),
    ("calque", r"فل لاک", "say ہینڈل پورا دائیں بائیں گھما کر"),
    ("calque", r"آپ کو [^۔]{0,40}?چاہیے", "'you should'; vary with کریں / کر لیں / کرنا ہے"),
]
# English loanwords starting with two consonants: voices often insert a vowel ("ka-lassic").
CLUSTER_LOANS = [
    "کلاس", "کلاسک", "کلچ", "کلپ", "کلینر", "کلیئرنس", "کلب", "کلک", "کلیمپ", "فریم", "فرنٹ",
    "فلیٹ", "فلور", "فلیش", "فلائی", "پلیٹ", "پلگ", "پلاسٹک", "پلان", "پرنٹ", "پریشر",
    "پروگرام", "بریک", "بریکیں", "بریکٹ", "بریکر", "بلاک", "بلب", "براؤن", "برش", "گریس",
    "گرائنڈر", "گرپ", "گلاس", "گریڈ", "گرین", "ٹرک", "ٹریکٹر", "ٹرپل", "ٹرم", "ٹرین",
    "ٹریفک", "ٹرائی", "ڈرائیور", "ڈرائیو", "ڈرم", "ڈرل", "سوئچ", "سوئنگ", "کراس", "کریک",
    "کرین", "کریڈٹ",
]
TESTED_OK = {"بریک", "بریکیں", "بریکٹ", "کلیمپ", "کریک"}  # probed: plain spelling has no extra vowel
AMBIGUOUS = {
    "سوا": "sawa (1¼) or siwa (except)? lexicon marks سَوا for sizes",
    "کس": "kas (tighten) or kis (which)? write کَس for tighten",
    "گدی": "gaddi or guddi? say سیٹ in speech",
    "پتی": "patti (strip) or pati? write پَتّی",
    "کٹر": "voice reads kattar; write کَٹَر for cutter",
    "بتیاں": "say لائٹیں in speech",
}


def lint(text, speech, lexicon):
    findings = []
    lines = text.split("\n")
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        for word, fix in HINDI.items():
            if re.search(wb(re.escape(word)), line):
                findings.append((n, "indian", word, f"Hindi word; Pakistani Urdu: {fix}"))
        for s in SLANG:  # whole words only: اپن must not match اپنی
            if re.search(wb(re.escape(s)), line):
                findings.append((n, "indian", s, "Mumbai/Bollywood slang"))
        for cat, pat, msg in PATTERNS:
            m = re.search(pat, line)
            if m:
                findings.append((n, cat, m.group(0), msg))
        if not speech:
            for m in re.finditer(r"[A-Za-z][A-Za-z']+", line):
                findings.append((n, "word", m.group(0), "Latin script inside Urdu; write it in Urdu script unless it is a code"))
            continue
        # speech checks run on what the voice will actually receive
        spoken = to_speech(line, lexicon)
        for m in re.finditer(r"[0-9۰-۹]+", spoken):
            findings.append((n, "speech", m.group(0), "write numbers as words, the way people say them"))
        for m in re.finditer(r"[()\[\]{}/:;–—]", spoken):
            findings.append((n, "speech", m.group(0), "voices read this badly; use ، or ۔ or rephrase"))
        for sent in re.split(r"[۔؟!]", spoken):
            words = sent.split()
            if len(words) > 22:
                findings.append((n, "speech", " ".join(words[:5]) + " …", f"long sentence ({len(words)} words); split it"))
        for word, msg in AMBIGUOUS.items():
            if re.search(wb(word), spoken):
                findings.append((n, "speech", word, f"ambiguous without vowel marks: {msg}"))
        lex_values = set(lexicon.values())
        for word in CLUSTER_LOANS:
            if word in TESTED_OK or word in lexicon:
                continue
            if re.search(wb(word), spoken):
                findings.append((n, "speech", word, "untested loanword starting with two consonants; run probe_pronunciation.py"))
        for m in re.finditer(r"[A-Za-z][A-Za-z']+", spoken):
            if not any(m.group(0) in v for v in lex_values):
                findings.append((n, "speech", m.group(0), "Latin word not from the lexicon; test how the voice says it"))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--speech", action="store_true", help="also check speech-specific problems")
    ap.add_argument("--json", help="JSON list of objects to lint")
    ap.add_argument("--field", default="narration_ur")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON)
    args = ap.parse_args()

    lexicon = load_lexicon(args.lexicon) if os.path.exists(args.lexicon) else {}
    sources = []
    if args.json:
        for it in json.load(open(args.json, encoding="utf-8")):
            sources.append((f"{args.json}:{it.get(args.id_field, '?')}", it[args.field]))
    for f in args.files:
        sources.append((f, open(f, encoding="utf-8").read()))
    if not sources:
        sources.append(("stdin", sys.stdin.read()))

    total = 0
    for name, text in sources:
        for n, cat, hit, msg in lint(text, args.speech, lexicon):
            total += 1
            print(f"{name}:{n}: [{cat}] «{hit}» {msg}")
    print(f"{total} finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
