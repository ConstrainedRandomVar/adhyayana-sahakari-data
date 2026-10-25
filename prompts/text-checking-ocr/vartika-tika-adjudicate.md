<!-- Extracted verbatim from out-of-repo pipeline: mri-work/vartika/run_tika_adjudicate.js lines 21–38. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const PROMPT = items => `You are proofreading OCR of a printed Sanskrit commentary: Ānandagiri's Śāstraprakāśikā on Sureśvara's
Bṛhadāraṇyaka-bhāṣya-vārttika. The text was OCR'd from TWO independent printed editions: M (Mahesh Research Institute — the
BASE edition, carefully edited) and A (Ānandāśrama). Below, each item is a place where the two OCR outputs disagree. "ctx"
shows the surrounding M text with ⟨…⟩ marking the disputed spot.

For each item decide what the PRINTED M edition most likely reads at that spot:
- "M"  — M's OCR reading is correct as is (valid Sanskrit in context).
- "A"  — M's OCR is a misreading and A's reading is what the print says (the editions share this text).
- "R"  — both OCR readings are garbled: give the minimal repair in "text" (change only what the OCR broke).
- For an item where one side is EMPTY: "M" or "A" for the side whose text genuinely belongs to the commentary
  ("X" in "text" if the non-empty side is page furniture, a footnote, or a header rather than commentary text).
Rules: M wins whenever M's reading is valid Sanskrit in context, even if A differs (that is an edition variant, not an
error). Do NOT standardise spelling, sandhi, or orthography (keep anusvāra/nasal, avagraha, spacing choices as printed);
fix ONLY OCR damage. Ignore differences of spacing, hyphenation, dashes vs daṇḍas. If you are not confident, set "unsure": true.
Return ONLY a JSON array: [{"id": <id>, "pick": "M"|"A"|"R", "text": "<repair, only for R or X>", "unsure": true|false}]
${G.JSON_PROMPT_RULES || ''}
ITEMS:
${items.map(s => JSON.stringify({ id: s.id, M: s.M, A: s.A, ctx: s.ctx })).join('\n')}`;
```
