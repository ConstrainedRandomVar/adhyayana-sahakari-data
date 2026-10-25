<!-- Extracted verbatim from work/shankaranandi/run_crop_check.js lines 27–54. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const BPROMPT = items => `You are reading a printed Sanskrit book (Śaṅkarānanda's commentary on the Bhagavadgītā, Nirṇayasāgara Press,
1916). Each attached image is a crop of ONE page. A previous owner wrote on the pages in RED ink — IGNORE everything red; read
only the black printed type. For each item, transcribe EXACTLY what is PRINTED inside the BLUE box(es), in Devanāgarī, in
reading order (if there is a blue vertical BAR instead, transcribe what is printed at the bar, or "" if nothing is).
- A word split across two lines with a hyphen is one word: join the pieces, drop the hyphen.
- Keep the print's own spelling exactly (anusvāra vs nasal, ृ vs ॄ, conjuncts, sandhi, ऽ, punctuation ।, ॥, ', —). Never
  modernise or correct; if the print looks wrong, transcribe it anyway and say so in "note".
${items.map((it, n) => `Item ${n + 1} (id ${it.id}) — image ${n + 1}.`).join('\n')}
Return STRICT JSON only: {"items": [{"id": "<id>", "printed": "<exact print>", "sure": "high|low", "note": "<optional>"}]}`;
const PROMPT = items => `You are checking OCR of a printed Sanskrit book (Śaṅkarānanda's commentary on the Bhagavadgītā,
Nirṇayasāgara Press, 1916). Each attached image is a crop of ONE page of this print. A previous owner wrote on the pages in
RED ink (underlines, strikes, added daṇḍas, marginal words) — IGNORE everything red; read only the black printed type.

For each item, look at what is inside the BLUE box (or, if there is a blue vertical BAR instead of a box, at the place
marked by the bar) and transcribe EXACTLY what is PRINTED there, in Devanāgarī.
- A word split across two lines with a hyphen counts as one word: join the pieces and drop the hyphen.
- Keep the print's own spelling: anusvāra vs nasal consonant, conjunct forms, sandhi, punctuation (।, ॥, ', —) as printed.
  Never modernise or correct the Sanskrit. If the print itself looks wrong, still transcribe it and say so in "note".
- For a BAR item: if nothing is printed at the bar (the two neighbouring words just follow each other), printed = "".
Then say which given reading matches the print exactly: "A", "B", "both" (they differ only in a way the print cannot show,
e.g. spacing), or "neither".

${items.map((it, n) => `Item ${n + 1} (id ${it.id}) — image ${n + 1}. ${it.kind === 'wit-only'
    ? `BAR item. A = "" (nothing printed there); B = "${it.wit}".`
    : `A = "${it.base}"; B = "${it.wit}".`}`).join('\n')}

Return STRICT JSON only: {"items": [{"id": "<id>", "printed": "<exact print>", "match": "A|B|both|neither",
"sure": "high|low", "note": "<optional short English>"}]}`;
```
