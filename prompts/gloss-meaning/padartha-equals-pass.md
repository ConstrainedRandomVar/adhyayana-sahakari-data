<!-- Extracted verbatim from work/gemini-eq-pilot/run_full.js lines 29–48. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const PROMPT = (ref, verse, raw, pairs) => `You are annotating Śaṅkara's Sanskrit commentary (bhāṣya). Task: find PADĀRTHA GLOSSES that are not yet marked.

A padārtha gloss is: Śaṅkara repeats a word of the root verse — or ONE MEMBER of a compound in the root verse (members are separated by "-" below) — and immediately gives his synonym or definition of it. Example from Gītā 6.9 (verse compound सुहृत्-मित्र-अरि-उदासीन-…): "मित्रं स्नेहवान्, अरिः शत्रुः" → pairs मित्रं = स्नेहवान् and अरिः = शत्रुः.

A gloss of one compound member INSIDE Śaṅkara's analysis of a verse compound IS wanted — e.g. Kaṭha 2.2.2 "नृषु मनुष्येषु सीदतीति नृषत्" → नृषु = मनुष्येषु. But the derivation itself (vyutpatti, e.g. "वसुः वासयति सर्वानिति", "हंसः हन्ति गच्छतीति") is NOT a gloss.

Do NOT report: a subject followed by its predicate; etymologies (… इति, करोतीति …); a verse phrase that simply continues; questions; quotations of other texts; examples; Śaṅkara's own sentences that merely begin with a verse word (especially particles/pronouns like न, स, यदि, अथ, इति, तत्); and any pair already in ALREADY MARKED.

Copy X and Y EXACTLY as they appear in RAW (same spelling, sandhi, anusvāra) — Y is only the gloss itself (stop before the next comma/daṇḍa or the next pratīka). If X is fused with Y in one written word, skip it.

ROOT VERSE (${ref}), padas with compound members split by "-":
${verse}

ALREADY MARKED (do not repeat):
${pairs.join('\n') || '(none)'}

RAW (the bhāṣya, exact text):
${raw}

Answer with JSON only: [{"x": "...", "y": "...", "verse_word": "the verse word or member it quotes"}]  — or [] if none.`;
```
