<!-- Extracted verbatim from searchtool/khan/vc-karaka/run_ab_tika_ocrfix.js lines 21–44. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const PROMPT = `You are proofreading Google Vision OCR of ONE page of a printed Sanskrit book: Śaṅkara's Ātmabodha with
Padmapāda's commentary (ṭīkā) "Vedāntasāra". The page SCAN is attached. Below are the OCR'd COMMENTARY lines of this
page (the mūla verses at the top of the page are NOT listed — ignore them), numbered R0, R1, … in reading order.

Compare every listed line against the PRINTED text in the image and report every place the OCR differs from the print.
Typical OCR failures here: dropped/half conjuncts (ञ्च read as श्च/श्व, द्ध, द्व, ष्ट), wrong mātrā (ि/ी, ु/ू, े/ै),
dropped repha or anusvāra, ह read for इ (हवेति for इवेति), त्त for त, spurious spaces splitting one word, a missing
space joining two words, stray marks/Latin letters, quote marks read as " or 66, daṇḍa read as | or 1.

Return STRICT JSON only: {"edits": [ {"row": <N of Rn>, "span": "<exact substring of that OCR line, verbatim>",
"text": "<what is PRINTED there>", "kind": "char|space|punct|noise", "confidence": "high|medium|low",
"reason": "<short English>"} ], "unreadable": [ {"row": N, "note": "..."} ]}

RULES (fidelity is paramount):
- Transcribe EXACTLY what is printed — the edition's own spelling, sandhi, anusvāra/conjunct choice and punctuation.
  Do NOT modernise, standardise, "correct" the author's Sanskrit, or fix grammar: if the PRINT itself has an unusual
  form, keep it (you may add it to "unreadable" with a note if you think the print itself is a misprint).
- "span" must be copied verbatim from the given line (long enough to be unique in that line, keep it short otherwise).
- The em-dash before a quoted pratīka is printed "—"; an OCR "-" or "--" there is fine, do not report it.
- A word broken at a line end with a hyphen is fine (it is re-joined later) — do not report it.
- Only report real differences; if a line is correct, report nothing for it. Write all prose in English.

OCR LINES:
`;
```
