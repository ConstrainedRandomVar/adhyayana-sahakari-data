<!-- Extracted verbatim from searchtool/khan/vc-karaka/run_compound_gloss.js lines 32–50. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const promptFor = b => {
  const lines = b.targets.map((c, i) =>
    (i + 1) + '. word: ' + c.word + '  |  morph: ' + (c.morph || '—') + '  |  समास: ' + c.sam +
    '  |  विग्रह: ' + (c.peel || []).join(' ; ')).join('\n');
  return [
    'You are glossing Sanskrit समास (compound) words from a Vedāntic text (Upaniṣad / Gītā / Brahmasūtra / prakaraṇa) with concise English meanings.',
    'For each TARGET compound below, give a short English gloss in the style of a Sanskrit-English dictionary entry:',
    'lowercase, comma-separated senses, concise (e.g. "all, everything"; "endowed with seven limbs"; "beyond the three times (past, present, future)").',
    'Use the provided समास-विग्रह (decomposition) and morph to get the sense right; reflect the contextual meaning but keep it a lexical gloss, not a full sentence translation.',
    'Give the gloss for the compound AS A WHOLE (not its members separately).',
    '',
    'Verse (पदच्छेद, for context): ' + b.verse,
    '',
    'TARGET compounds:',
    lines,
    '',
    'Output STRICT JSON only — an array of {"word":"<exact word, copied verbatim>","meaning":"<english gloss>"}. No prose, no markdown fences.',
  ].join('\n');
};
```
