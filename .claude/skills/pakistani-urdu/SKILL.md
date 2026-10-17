---
name: pakistani-urdu
description: Write and voice Urdu that sounds like a Pakistani wrote it and a Pakistani is saying it, not Google-translated, not Indian or Bollywood Hindi, and not robotic text-to-speech. Use this skill whenever you produce Urdu for Pakistani readers or listeners, in Urdu script or Roman Urdu, including translations, guides, PDFs, slides, subtitles, WhatsApp messages, video voice-overs and any TTS audio. Also use it when someone says Urdu sounds translated, word-by-word, Hindi-mixed, Indian, stiff or unnatural, or that a voice mispronounces words (for example "Classic" coming out as "calassic").
---

# Pakistani Urdu: writing it and voicing it

Urdu written by a model or a translation tool usually fails in three ways that native
Pakistani readers notice within one sentence:

1. **Translationese.** The English sentence is converted word by word. Word order, noun
   stacks, passives and headings follow English, so the Urdu is grammatical but nobody
   talks like that ("انجن اسٹاک رہیں گے", "چار سخت اصول", "صاف پڑھے جانے چاہئیں").
2. **The wrong country.** Sanskritised Hindi words, Mumbai slang, Indian ways of saying
   numbers ("ون ٹوئنٹی فائیو"), or "bike" vocabulary that Pakistanis don't use, make it sound
   like dubbed Indian content.
3. **The voice.** Urdu script leaves short vowels unwritten, so a TTS voice guesses them. It
   inserts vowels into English loanwords that start with two consonants (کلاسک → "ka-lassic"),
   and it can pick the wrong reading of ambiguous words (کس "kas" vs "kis").

This skill fixes each one. Do the writing work first; good audio cannot rescue translated text.

## Workflow

### 1. Pin down the listener before writing a word

Who is it for (a mechanic in Lahore, a mother in Karachi, an office team in Islamabad)? Is it
read or heard? The register follows from that: a workshop guide uses the words mechanics use
on the shop floor, including English loanwords; a family message uses warmer, simpler Urdu;
an official notice uses more formal Urdu. Decide this, then write for that person.

### 2. Write from meaning, not from the English sentence

Read the English, close it, and say the point the way that person would hear it from a
knowledgeable Pakistani. This is transcreation, not translation. In practice:

- **Restructure.** Turn English noun stacks and passives into Urdu verb phrases.
  "Tyre-to-mudguard gap at full compression" becomes
  "شاک پورا دب جائے تو ٹائر اور مڈگارڈ کے بیچ کتنا فاصلہ رہتا ہے".
- **Use the light verbs Urdu speakers use for instructions:** ناپ لیں، لگا دیں، کس دیں،
  دیکھ لیں، کروا لیں. Mix polite imperatives (کریں) with "کرنا ہے" and "نہیں کرنا".
  A wall of "آپ کو ... کرنا چاہیے" reads as translated.
- **Connect ideas the Urdu way:** پھر، اور، تاکہ، ورنہ، اس لیے. Give the reason in a ورنہ
  clause ("ربڑ ضرور لگائیں، ورنہ جھٹکوں سے ٹینکی کریک ہو جائے گی") instead of a separate
  English-style "Why:" line.
- **Keep the English words Pakistanis actually say** (ہینڈل، بریک، فریم، سیٹ، چیک کریں) and
  use Urdu where Pakistanis use Urdu (تار not کیبل for bike cables, ٹینکی not ٹینک for a bike
  tank). Forcing pure Urdu ("دستہ" for handlebar) is as unnatural as leaving English in.
- **Say numbers the way people do.** Workshop sizes are spoken in inches and fractions
  (سوا، ڈیڑھ، پون، آدھا، ڈھائی). Give mm in brackets in written material when precision
  matters. Model names follow Pakistani habit: "سی جی ون ٹو فائیو", "ہنڈا سیونٹی".
- **Headings are things people say:** "پہلا کام: سیٹ", "یہ کام نہیں کرنے",
  "موٹر سائیکل واپس کرنے سے پہلے". Not "قدم 1" or "اہم نکات".
- **Open and close like a Pakistani would** when the format allows: "السلام علیکم استاد جی",
  "شکریہ، اللہ حافظ".

`references/style-guide.md` has the full list of Pakistani-vs-Indian markers, calque
patterns with fixes, and before/after examples. Read it the first time you use this skill
in a conversation, and whenever you are unsure about a word.

For technical or trade vocabulary, check the matching glossary in `references/`
(`glossary-workshop.md` covers motorcycles and workshops). Add to it when you learn a term.

### 3. Check the text

Run the lint script over every Urdu file or string you produce:

```bash
python3 scripts/urdu_lint.py draft.txt            # display text
python3 scripts/urdu_lint.py --speech speech.txt  # text that will be spoken
```

It flags Sanskritised Hindi words, Mumbai slang, Indian number habits, English-style
passives, Latin script inside Urdu, and (in `--speech` mode) digits, brackets, long
sentences, ambiguous words without vowel marks, and loanwords missing from the
pronunciation lexicon. Treat each flag as a question, not an order: fix it or be able to say
why it is right here.

Then do a read-aloud pass in your head: would this exact sentence come out of the mouth of
the person in step 1? If a phrase only makes sense once you think of the English behind it,
rewrite it.

### 4. Make a separate speech text for audio

What reads well and what a TTS voice says well are different. Keep the display text (for
PDFs, slides, subtitles) and write a speech text beside it:

- Numbers as words, in the spoken style: "سوا سے دو انچ", "پندرہ ملی میٹر".
- No brackets, slashes, colons or bullet fragments. Use "،" for a breath and "۔" to end.
- Sentences of at most about 20 words.
- Where a word is ambiguous without vowel marks, either use a word that is not ambiguous
  ("سیٹ" instead of گدی) or add the marks (کَس دیں، کَٹَر).
- English loanwords go through the lexicon (next step). Do not hand-edit spellings in the
  script without testing them; a mark in the wrong place makes things worse.

### 5. Synthesize with the lexicon

```bash
python3 scripts/urdu_tts.py --in speech.txt --out narration.mp3            # one file
python3 scripts/urdu_tts.py --json scenes.json --field narration_ur \
        --id-field id --outdir audio/ur                                    # many segments
python3 scripts/urdu_tts.py --in speech.txt --print-speech                 # dry run
```

`urdu_tts.py` applies `scripts/speech_lexicon.tsv` (display spelling → spelling the voice
says correctly), then calls the voice with retries. Default voice is `ur-PK-AsadNeural`
(male); `ur-PK-UzmaNeural` is the female Pakistani voice. Do not use `ur-IN-*` voices for
Pakistani listeners. Leave the rate at +0%; slowing it down makes Urdu sound robotic.

The voices are Microsoft's neural voices reached through the `edge-tts` package
(`pip install edge-tts`). That needs network access to `speech.platform.bing.com`; in a
sandbox, that host may have to be allowed first.

### 6. Test new loanwords instead of guessing

You cannot hear audio. Before trusting a new English loanword in speech, especially one
starting with two consonants (cl-, fr-, pl-, br-, gr-, tr-, sw-), probe it:

```bash
python3 scripts/probe_pronunciation.py --out probe/ \
  "frame=فریم|فْریم|frame|فَریم"
```

Give the plain spelling first, then candidates (jazm on the first letter, Latin script),
and last a control with the vowel forced in. The script prints each variant's duration from
the voice's own word timings. An inserted vowel costs roughly 40 to 100 ms, so if the jazm
variant is clearly shorter than plain and the forced-vowel control is clearly longer, the
plain spelling was getting an extra vowel and jazm fixes it. If plain is already about as
short as jazm, leave it alone. Add the result to `speech_lexicon.tsv` with the evidence.
`references/tts-pronunciation.md` explains the method and lists every measured result.

### 7. Hand the human a listening check

Timings catch inserted vowels, not wrong vowels or an accent that feels off. Whenever you
deliver Urdu audio, also deliver a short listening sheet for the words you could not verify
(the probe script writes one: each variant announced by number), and ask the person to say
which number sounds right. Say plainly that you could not listen yourself. Their answer goes
into the lexicon, so the next run is right.

## Files

- `references/style-guide.md`: register, Pakistani vs Indian markers, calques, examples.
- `references/glossary-workshop.md`: motorcycle and workshop vocabulary as said in Pakistan.
- `references/tts-pronunciation.md`: how the voices misread Urdu, the probing method, results.
- `scripts/urdu_lint.py`: flags Indian/Hindi markers, translationese and speech problems.
- `scripts/urdu_tts.py`: lexicon-aware TTS with retries; `--print-speech` for a dry run.
- `scripts/probe_pronunciation.py`: timing probe plus a numbered listening sheet.
- `scripts/speech_lexicon.tsv`: tested display → speech spellings, with evidence.
