<!-- Extracted verbatim from out-of-repo pipeline: brahmatattvaprakashika/work/gemini_check.js lines 13–24. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const PROMPT = (lines) => `You are proofreading a transcription of one printed page of a Sanskrit commentary (Devanagari, 1909 print).
The image is the scanned page. Below is our transcription of its text lines (running header, page number, library watermark and stamps are omitted; footnote lines at the bottom are included).

Task: list ONLY the places where the transcription does NOT match what is printed in the image: a wrong akshara or conjunct, a missing or extra vowel sign, anusvara, visarga, virama or avagraha, a missing or extra word or letters.
Rules:
- Report what the PRINT shows, even if the print itself is a misprint. Do NOT correct the Sanskrit toward a standard or "better" form; do not normalise sandhi or spelling.
- Ignore: spacing, spaces before punctuation, line-break hyphens, quotation-mark style, superscript footnote numerals printed above words.
- If you are unsure of a glyph, report it with confidence "low"; never invent.
- Output ONLY a JSON array (no prose), each element: {"line": <line number>, "transcribed": "<the word exactly as in our text>", "printed": "<the word as printed>", "confidence": "high"|"low"}. Output [] if everything matches.

Transcription:
${lines.map((t, i) => `${i + 1}: ${t}`).join('\n')}`;
```
