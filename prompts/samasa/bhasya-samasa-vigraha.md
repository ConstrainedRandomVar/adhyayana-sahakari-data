<!-- Extracted verbatim from searchtool/khan/vc-karaka/run_bhasya_samasa.js lines 44–60. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const HEADER =
`You are a Pāṇinian samāsa analyst. For each numbered Sanskrit term, output its RECURSIVE samāsa peel.
Return ONLY a JSON array, one object per term IN ORDER, no markdown/prose:
{"n":<num>,"w":"<term>","samasa":[{"c":"<compound/member stem>","vigraha":"<vigraha>","type":"<समास type: षष्ठी-तत्पुरुष|कर्मधारय|बहुव्रीहि|द्वन्द्व|अव्ययीभाव|द्विगु|… OR कृत्|तद्धित for a derived member>","pratyaya":"<kṛt/taddhita pratyaya if type कृत्/तद्धित, else omit>","sutra":"<Pāṇini sūtra e.g. 2.2.8>"}]}
Rules:
- Layer 0 = the whole compound; then recurse depth-first into EACH multi-member or derived (kṛdanta/taddhita) member. e.g. अध्यात्मयोगाधिगम → अध्यात्मयोग → अध्यात्म(अव्ययीभाव) ; अधिगम(कृत्,घञ्).
- A विच्छेद hint (member split) is given; use it for the top split, correct only if clearly wrong.
- If a term is NOT a compound and NOT a kṛt/तद्धित derivative, output "samasa":[].
- Devanāgarī only. JSON array ONLY.
Terms:`;

// Optional sentence CONTEXT (targets with `ctx`, e.g. the 2026-10-01 regap run): the analysis must follow how the
// term is used there — notably where a नञ् attaches (अकर्मदर्शनम् in Gītā 4.18 = अकर्मणः दर्शनम्, not न कर्मदर्शनम्).
// Prompt is byte-identical to before when no target carries ctx.
const CTX_RULE = `- Some terms carry a context sentence from Śaṅkara's bhāṣya (after "context:"). Analyse the term AS USED in that sentence — in particular decide where a negation (नञ्) or other prefix attaches from the sentence's sense, not mechanically.`;
const buildPrompt = batch => (batch.some(([nw, v]) => v.ctx) ? HEADER.replace('\nTerms:', '\n' + CTX_RULE + '\nTerms:') : HEADER) + '\n'
  + batch.map(([nw, v], i) => `${i + 1}. ${v.word}  (विच्छेद: ${v.p})` + (v.ctx ? `  — context: «${v.ctx}»` : '')).join('\n');
```
