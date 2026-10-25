<!-- Extracted verbatim from searchtool/khan/vc-karaka/run_dhatu_gemini.js lines 20–30. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const prompt = ts => [
  'You are a Pāṇinian grammarian. For each TARGET word (a finite verb or a kṛdanta) from the Sanskrit verse below, identify WHICH Dhātupāṭha entry it comes from.',
  'Homonymous roots are DIFFERENT dhātus (√कल् = कलँ शब्दसङ्ख्यानयोः भ्वादि / कलँ क्षेपे चुरादि / कल गतौ सङ्ख्याने च चुरादि). Decide by the FORM (gaṇa vikaraṇa, pada; णिच्/सन् forms → the BASE dhātu) AND the SENSE in this verse.',
  'Give the gaṇa (1–10), the upadeśa exactly as listed in the Dhātupāṭha (with anunāsika/it-markers: गमॢँ, कलँ, भू, डुकृञ्), and the Dhātupāṭha artha (गतौ, सत्तायाम्, …). Do NOT give serial numbers.',
  'For a kṛdanta also give the kṛt-pratyaya and the resulting prātipadika (masculine/base stem, e.g. भिन्न, गच्छत्, गन्तव्य; for क्त्वा/ल्यप्/तुमुन् the indeclinable itself).',
  'If CANDIDATES are listed for a word, they are ashtadhyayi.com entries whose tables produce the form — prefer one of them unless clearly wrong.',
  'If the word is not verbal at all (a noun mis-tagged), give {"word":…, "notVerbal":true}.',
  '', 'Verse: ' + (ts[0].ctx || ''), '', 'TARGETS:',
  ...ts.map((t, i) => `${i + 1}. ${t.w} | source morph: ${t.gram}${t.cands && t.cands.length ? ' | CANDIDATES: ' + t.cands.map(c => `${c} ${dp[c].aupadeshik} ${dp[c].artha} (gaṇa ${dp[c].gana})`).join('; ') : ''}`),
  '', 'Output STRICT JSON only: an array of {"word":"<copied verbatim>","gana":<int>,"upadesha":"…","artha":"…","pratyaya":"…(kṛdanta only)","stem":"…(kṛdanta only)"}.',
].join('\n');
```
