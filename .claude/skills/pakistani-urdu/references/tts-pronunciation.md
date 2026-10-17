# Urdu text-to-speech: pronunciation

Contents
1. Why the voice gets Urdu wrong
2. Voices
3. Speech-text rules
4. Probing a word (method)
5. Results so far
6. What timing cannot tell you

## 1. Why the voice gets Urdu wrong

Urdu script writes consonants and long vowels; short vowels (zabar, zer, pesh) are normally
left out. A TTS voice has to predict them. Two predictable failures follow:

- **Inserted vowels in English loanwords.** Urdu words do not begin with two consonants, so
  the voice's letter-to-sound rules break up clusters: کلاسک becomes "ka-laa-sik" instead of
  "klaa-sik", فریم becomes "fa-reem". Pakistanis say these words with the cluster intact, so
  the inserted vowel sounds rural or foreign, which is how listeners describe "an accent that
  feels off".
- **The wrong word among homographs.** کس is both "kis" (which) and "kas" (tighten); کٹر is
  "kaṭar" (cutter) and "kaṭṭar" (fanatic). Context does not always save it.

The voice does honour vowel marks. A jazm/sukun (ْ U+0652) on the first letter removes an
inserted vowel; a zabar (َ) forces one. That gives a way to steer it, and a way to measure it.

## 2. Voices

| Voice | Use |
|---|---|
| `ur-PK-AsadNeural` | Pakistani male. Default for workshop and instructional content |
| `ur-PK-UzmaNeural` | Pakistani female |
| `ur-IN-SalmanNeural`, `ur-IN-GulNeural` | Indian Urdu. Do not use for Pakistani listeners |

Rate +0%. Slowing to -5% or below makes Urdu sound robotic. If the listener says the accent
is off, first fix the text (most "accent" complaints are translationese or inserted vowels),
then offer the other Pakistani voice as an A/B comparison.

## 3. Speech-text rules

1. Numbers as words in the spoken style: "سوا سے دو انچ", "پندرہ ملی میٹر", model names as
   Pakistanis say them ("سی جی ون ٹو فائیو").
2. No brackets, slashes, colons, semicolons or dashes. "،" gives a short breath, "۔" a full stop.
3. At most about 20 words per sentence.
4. Prefer a word that cannot be misread over a word that needs vowel marks (سیٹ over گدی,
   لائٹیں over بتیاں).
5. Loanwords go through `speech_lexicon.tsv`. A new loanword starting with two consonants
   gets probed before it is trusted.
6. Latin script only for words the lexicon maps there after testing (e.g. swing). Untested
   Latin words may be read letter by letter or with an English accent.
7. Keep display text free of vowel marks. They belong only in the speech text.

## 4. Probing a word (method)

```bash
python3 scripts/probe_pronunciation.py --out probe/ "frame=فریم|فْریم|frame|فَریم"
```

Order the variants: plain spelling, candidate fixes (jazm on the first letter, Latin), and
last a control with the vowel forced in (zabar after the first letter). Each variant is
spoken in the same carrier sentence (default "یہ {} ہے۔"; change it with `--carrier` when the
word needs context) and the voice's own word timings are read back.

Read the result like this:

- Forced-vowel control 50 to 120 ms longer than plain, jazm about the same as plain:
  plain is already fine. No lexicon entry.
- Jazm clearly shorter than plain (40 ms or more) and the control longer than plain: plain
  had an inserted vowel. Add `plain<TAB>jazm<TAB>evidence` to the lexicon.
- Jazm longer than plain or the numbers disagree between voices: leave it, or try Latin,
  and put the word on the human listening sheet.

For homographs, put the word in a real phrase (`--carrier "اب {} کریں۔"`) and compare the
plain spelling with each marked reading. The plain spelling usually times like the reading
the voice chose.

The probe also writes `listening-sheet.mp3` (each variant announced by number) unless you
pass `--no-sheet`. Send that to a native speaker for anything timing cannot settle.

## 5. Results so far

Carrier "یہ {} ہے۔". Milliseconds relative to the plain spelling, Asad / Uzma.

| Word | Jazm on first letter | Latin | Forced vowel | Verdict |
|---|---|---|---|---|
| کلاسک classic | -63 / -50 | -50 / -87 | +63 / +63 | use کْلاسک (listener heard "calassic") |
| فریم frame | -100 / -87 | -37 / -12 | +88 / +50 | use فْریم |
| پلیٹ plate | -63 / -50 | -13 / +13 | +50 / +50 | use پْلیٹ |
| بریکر breaker | -38 / -26 | -26 | +87 / +87 | use بْریکر |
| سوئنگ swing | +138 (with zer) | -62 / -37 | +162 / +213 | use Latin "swing" |
| سوئچ switch | +37 / +87 (with zer) | -76 / -63 | +37 / +112 (pesh) | use Latin "switch"; sw- clusters do best in Latin |
| بریک brake | -13 | -26 | +100 | plain is fine |
| بریکٹ bracket | -13 | -13 | +100 | plain is fine |
| کلیمپ clamp | +37 | +37 | +124 | plain is fine |
| کریک crack | -26 / 0 | -50 / -37 | +74 / +76 | plain is fine |

Homographs, carrier "اب {} کریں۔", Asad:

| Phrase | Plain | Marked readings | Verdict |
|---|---|---|---|
| پون انچ اونچا | 838 ms | پَون 875, پَوَن 1038 | plain already reads "paun" |
| بولٹ کس | 488 ms | کِس 525, کَس 612 | plain leans to "kis": write کَس |
| کٹر بند | 562 ms | کَٹّر 562, کَٹَر 600 | plain reads "kattar": write کَٹَر |
| سوا انچ نیچا | 938 ms | سِوا 975, سَوا 1025 | inconclusive: write سَوا, listener check |
| گدی الگ | 575 ms | گَدّی 550, گُدّی 550 | inconclusive: say سیٹ instead |
| پتی تیار | 675 ms | پَتّی 675, پَتی 688 | inconclusive: write پَتّی |

## 6. What timing cannot tell you

Timing shows whether a vowel was added or removed. It cannot tell "a" from "i", stress, or
whether the overall voice sounds like it is from Lahore or from somewhere else. You cannot
listen. So every delivery of Urdu audio comes with a short listening sheet and a plain
request: "I couldn't listen to this myself; which number sounds right?" Record the answer in
the lexicon's evidence column (e.g. "listener chose 2, 2026-10").
