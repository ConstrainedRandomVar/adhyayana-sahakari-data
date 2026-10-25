<!-- Extracted verbatim from work/anandagiri-en/run.js lines 67–118. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
// ---- prompts ----
const KINDS = `Kinds: "avataranika" = Ānandagiri's lead-in saying what the next bhāṣya passage does; "prateeka" = Ānandagiri quoting the opening words of a bhāṣya passage (the full bhāṣya phrase is given as LEMMA); "vyakhya" = his explanation; "mangala" = a benedictory verse.`;
function tPrompt(text, c) {
  return `You are translating Ānandagiri's ṭīkā (sub-commentary) on Śaṅkara's bhāṣya on the ${TEXTS[text].name} into English, for students reading the Sanskrit alongside.

Context — the text being commented on (ref ${c.ref.replace(/::.*/, '')}):
${c.ctx.mula || '(none)'}

Śaṅkara's bhāṣya on it:
${c.ctx.bhashya || '(none)'}

The ṭīkā is given as numbered notes. ${KINDS}

Rules:
- Translate each note faithfully and completely; do not add commentary of your own. Use brief bracketed glosses [like this] only where the English would otherwise be unintelligible; keep them minimal.
- For a "prateeka", render it as a quotation of the bhāṣya: translate the quoted words (use the LEMMA to understand them), in double quotes, followed by "— (bhāṣya)".
- Keep technical terms recognisable: give the Sanskrit in IAST in parentheses at first use within a note where it matters (e.g. purport (tātparya)).
- Scriptural quotations: translate them and keep the citation.
- Output ONLY JSON: {"<id>": "<English>", ...} with every id exactly once.

Notes:
${c.notes.map(n => `[${n.id}] (${n.kind})${n.lemma ? ` LEMMA: ${n.lemma}` : ''}\n${n.text}`).join('\n\n')}`;
}
const PADA_RULES = `- Undo sandhi between words: separate padas with " + " (मयोक्तमिति → "मया + उक्तम् + इति"; सृष्टिर्या → "सृष्टिः + या").
- Inside a compound, join members with "-" and undo internal sandhi (उत्पत्त्यादिश्रुतीनाम् → "उत्पत्ति-आदि-श्रुतीनाम्").
- Restore the pausal final form of every pada (visarga, म्, त् …): write पुनः, not पुनर्; सः, not स; उच्यते for उच्यत before इति. A compound member ends in its pausal stem form too: यत्-शब्दस्य, तत्-कार्य (not यद्-, तद्-).
- Indeclinables are separate padas, never compound members: पुनः, अपि, तु, च, इति, इव, एव, न, हि, वा, अतः, ततः are joined with " + ", never "-" (पुनरुपन्यासः → "पुनः + उपन्यासः"; रज्ज्वामिवेति → "रज्ज्वाम् + इव + इति"). Only इत्यादि / इत्याद्य may stay inside a compound (इति-आदि-).
- Keep the spelling inside a word exactly as printed — including an anusvāra before a consonant (मंगलाचरणं → "मंगल-आचरणम्", NOT "मङ्गल-"); only a word-final ं becomes म्.
- Keep an upasarga attached to its verb or kṛdanta (प्रेत्य, उपसंहरति stay whole). Keep indefinites and -वत् words whole (केचित्, कश्चित्, किञ्चन, आत्मवत्, तद्वत्).
- A word with no sandhi and no compound is returned unchanged.
- Keep the printed spelling EXACTLY, even where it looks like a misprint — never correct it in the split. If you think a word is misprinted, still split it as printed, and list it under "misprints" with your suggested reading.
- A "prateeka" note quotes the bhāṣya in abbreviated form: X + इति, where X is just the first word(s) of the bhāṣya passage (its full LEMMA is given). Split ONLY the printed X — never expand it to the lemma: प्रज्ञानेति (lemma प्रज्ञानांशुप्रतानैः) → "प्रज्ञान + इति". Use the lemma only to get X's stem right: मृल्लोहेति (lemma मृल्लोहविस्फुलिङ्गाद्यैः) → "मृद्-लोह + इति", NOT "मृद्-लोहा"; कल्पेति (lemma कल्पसर्ग…) → "कल्प + इति".
- Output only the pada forms — no punctuation.
- Never translate; never drop, add or merge words.`;
function paPrompt(c) {
  return `Give the padaccheda (sandhi-split word division) of each word of this Sanskrit commentary (Ānandagiri's ṭīkā).
For each note you get a numbered list of surface words. For EACH word return its पद form:
${PADA_RULES}
Output ONLY JSON: {"splits": {"<id>": ["<pada form of word 1>", ...], ...}, "misprints": [{"id": "<id>", "word": "<as printed>", "suggested": "<reading>"}]} — each array's length must equal the number of words listed for that id.

${c.notes.filter(n => n.words.length).map(n => `[${n.id}]${n.kind === 'prateeka' && n.lemma ? ` (prateeka; LEMMA: ${n.lemma})` : ''} ${n.words.length} words:\n${n.words.map((w, k) => `${k + 1}. ${w.core}`).join('\n')}`).join('\n\n')}`;
}
function pbPrompt(c) {
  return `You are preparing a padapāṭha (word-by-word division) of Ānandagiri's Sanskrit commentary. Read each passage as a sentence, then for every word, in order, write its division into padas.
${PADA_RULES}
Each passage is followed by its words, numbered. Output ONLY JSON: {"splits": {"<id>": ["<division of word 1>", "<division of word 2>", ...], ...}, "misprints": []} — one entry per numbered word, in order.

${c.notes.filter(n => n.words.length).map(n => `[${n.id}]${n.kind === 'prateeka' && n.lemma ? ` (prateeka; LEMMA: ${n.lemma})` : ''} ${n.text}\nwords: ${n.words.map((w, k) => `${k + 1}=${w.core}`).join(' | ')}`).join('\n\n')}`;
}

// ---- calls (cached) ----
let spent = 0, calls = 0, failed = 0;
```
