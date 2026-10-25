<!-- Extracted verbatim from searchtool/khan/vc-karaka/run_simple_gloss.js lines 32–48. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const promptFor = b => {
  const lines = b.targets.map((c, i) =>
    (i + 1) + '. word: ' + c.word + '  |  morph: ' + (c.morph || '—') + (c.role ? '  |  role: ' + c.role : '')).join('\n');
  return [
    'You are glossing individual Sanskrit words (mūla padas) from a Vedāntic text (Upaniṣad / Gītā / Brahmasūtra / prakaraṇa) with concise English meanings.',
    'For each TARGET word below, give a short English gloss in the style of a Sanskrit-English dictionary entry:',
    'lowercase, comma-separated senses, concise (e.g. "eye, sight"; "from the two ears"; "(he) was unable").',
    'Reflect the INFLECTED sense of the exact form (its case/number or, for a finite verb, person/number/tense) using the provided morph + verse context, but keep it a lexical gloss, not a full sentence translation.',
    '',
    'Verse (पदच्छेद, for context): ' + b.verse,
    '',
    'TARGET words:',
    lines,
    '',
    'Output STRICT JSON only — an array of {"word":"<exact word, copied verbatim>","meaning":"<english gloss>"}. No prose, no markdown fences.',
  ].join('\n');
};
```
