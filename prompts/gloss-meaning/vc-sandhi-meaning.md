# Gemini prompt — per-word MEANING + inter-word SANDHI (JSON)

Run this in the Gemini UI on one Sanskrit verse (mūla or bhāṣya line). It returns a single JSON object
that the read-a-verse pipeline consumes directly: per-word English **meaning** (for the "what does this
word mean?" question) and every inter-word **sandhi** junction (for the sandhi split/join question). The
Gemini kāraka/morph runs never captured these — this fills that gap ([redacted: name], 2026-08-21). See
`build_vc_walk.js` for how VC read-a-verse is assembled; a companion merge step will fold this JSON in.

Paste the verse in place of `<VERSE>` and its reference in place of `<REF>`, then run.

>>> PROMPT START

You are an expert in Sanskrit (saṃskṛta) grammar and lexicon. I give you ONE verse (or one bhāṣya line).
Return a SINGLE JSON object — and NOTHING else (no markdown fences, no commentary, no ``` ). It must parse
with JSON.parse. Use Devanāgarī for all Sanskrit; use English for meanings.

Schema:
{
  "ref": "<REF>",
  "words": [
    { "n": 1, "word": "<pada in padaccheda / citation form>", "meaning": "<concise English gloss, 1–6 words>" }
    // one entry per word of the verse, in reading order, AFTER resolving sandhi (i.e. the split words)
  ],
  "sandhi": [
    {
      "before": ["<pada1>", "<pada2>"],   // the two adjacent underlying words that fuse (exactly two)
      "after": "<the combined surface form EXACTLY as written in the verse>",
      "rule": "<Sanskrit sandhi rule name, e.g. सवर्णदीर्घ / गुण / यण् / विसर्ग-उत्व / अनुस्वार>",
      "sutra": "<Pāṇini sūtra number if known, e.g. 6.1.101; else \"\">"
    }
    // one entry per INTER-word junction where adjacent words combine in the written verse
  ]
}

Rules:
- words: list EVERY word of the verse in padaccheda (post-split) form, in reading order. For a compound,
  give the whole compound as one word with its overall meaning (do NOT split the compound here). Drop the
  daṇḍa (।/॥) and the verse number.
- meaning: a concise English gloss of that word AS USED HERE (case-appropriate — e.g. षष्ठी → "of X"). Keep
  it short (1–6 words). For particles (निपात) give the particle sense (e.g. एव → "only / indeed").
- sandhi: report ONLY inter-word junctions (two separate words fusing in the written text). Do NOT report
  sandhi that is internal to a compound (that is samāsa, handled elsewhere). For a run of three fused words
  (e.g. न+आशा+अस्ति → नाशास्ति), emit ONE entry per adjacent pair, in order. `after` must be the exact
  substring as written (including the visarga/anusvāra/vowel change). If the verse has NO inter-word sandhi,
  return "sandhi": [].
- Output ONLY the JSON object.

## Verse
- ref: <REF>
- verse: <VERSE>

>>> PROMPT END
