<!-- Extracted verbatim from searchtool/khan/vc-karaka/vc_bhashya_regloss_sentences.js lines 33–58. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
function prompt(ref, items) {
  const v = byRef[ref] || {};
  return [
'# विवेकचूडामणि — भाष्यम् (श्रीचन्द्रशेखरभारती, 1952 मुद्रणम्): RE-ANALYSE ' + items.length + ' sentence(s) of verse-unit ' + ref,
'',
'You are an expert in Pāṇinian vyākaraṇa, Sanskrit lexicon, and Advaita Vedānta. The text of the sentences under [TARGETS] was just proof-corrected against the printed book. Analyse ONLY those sentences, word by word, in the SAME format as the rest of this commentary\'s gloss. [MULA] and [BHASYA CONTEXT] are context only. Return a SINGLE JSON OBJECT and NOTHING else (no fences, no prose). Must parse with JSON.parse.',
'',
'## ABSOLUTE RULES',
'- Devanāgarī for ALL Sanskrit; English ONLY in "meaning" and "translation".',
'- VERBATIM: "sanskrit" must reproduce the target sentence EXACTLY as given; every "word" is a segmented pada of THAT text, in order, covering all of it (the gloss connector "=" and punctuation are not words). Do NOT fix, normalise or improve the text.',
'- JSON VALIDITY: NO double-quote (") inside any string value. Sanskrit quotations use guillemets ‹ › exactly as in the input; English uses SINGLE quotes. Balance every { } [ ]. No trailing commas.',
'',
'## SHAPE',
'{"ref":"' + ref + '","sentences":[{"id":"<target id>","sanskrit":"<VERBATIM>","words":[{"n":1,"word":"<segmented pada>","morph":"<see MORPH>","meaning":"<1-6 word English gloss>","samasa":[<recursive layers — compounds ONLY; omit otherwise>]}],"translation":"<faithful English>","roleSpans":[<see ROLES>]}]}',
'',
RULES,
'',
'Output ONLY the JSON OBJECT.',
'',
'## INPUT',
'[MULA — CONTEXT ONLY]', v.mula || '',
'[BHASYA CONTEXT — the whole corrected commentary, CONTEXT ONLY]', ((v.prelude || '') + '\n' + (v.commentary || '')).trim(),
'[TARGETS]',
...items.map(p => JSON.stringify({ id: `${p.part}-${p.i}`, sanskrit: p.sanskrit })),
''].join('\n');
}
```
