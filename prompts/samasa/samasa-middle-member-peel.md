<!-- Extracted verbatim from searchtool/khan/build_samasa_middle_prompt.js lines 30–76. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const POLICY = `## Policy (CONSERVATIVE — match it exactly)
For each member, ask: **is it a *transparent* derivative?**
1. **कृत्** — derivable from a √धातु by a productive kṛt affix. **Frequency does NOT make it मूल**: action-nouns
   in -अ (घञ्/अच्/अप्), -अन (ल्युट्), -ति (क्तिन्), agent-nouns in -तृ (तृच्), and क्त/क्तवतु participles ARE कृदन्त.
   e.g. भाव → √भू + घञ्; बोध → √बुध् + घञ्; आनन्द → आ-√नन्द् + घञ्; भव → √भू + अच्; बन्ध → √बन्ध् + घञ्; गति → √गम् + क्तिन्.
2. **तद्धित** — derivable from a nominal base by a productive taddhita affix (अण्, तल्/त्व, मतुप्, इनि, ठक्, …).
   e.g. परता → पर + तल्; वैदिक → वेद + अण्; बौद्ध → बुद्धि + अण्.
3. **समास** — the member is itself a further compound (give its layer(s), outermost first, same shape).
   e.g. सर्ववेदान्त → सर्वे वेदान्ताः (कर्मधारय), and वेदान्त → वेदस्य अन्तः (षष्ठी-तत्पुरुष).
4. **मूल** — a genuinely underived प्रातिपदिक. **उṇādi-derived and lexicalised nouns ALSO count as मूल — do
   NOT peel them** (e.g. धर्म ← √धृ+manin, मार्ग, कर्मन्, देव, गो, नर). Pronouns/particles/prefixes are मूल.
   When in genuine doubt between a lexicalised उṇādi noun and a transparent kṛt derivative, choose **मूल**.

## Output — ONE json array, nothing else
One object per member (echo the \`member\` string EXACTLY as given so it can be merged back):
\`\`\`json
[
  {"member":"आनन्द","decision":"कृत्","layers":[{"c":"आनन्द","vigraha":"आ-√नन्द् + घञ्","type":"कृत्","pratyaya":"घञ्","sutra":"3.3.18"}]},
  {"member":"परता","decision":"तद्धित","layers":[{"c":"परता","vigraha":"परस्य भावः","type":"तद्धित","pratyaya":"तल्","sutra":"5.1.119"}]},
  {"member":"सर्ववेदान्त","decision":"समास","layers":[{"c":"सर्ववेदान्त","vigraha":"सर्वे वेदान्ताः","type":"कर्मधारय","sutra":"2.1.57"},{"c":"वेदान्त","vigraha":"वेदस्य अन्तः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"}]},
  {"member":"धर्म","decision":"मूल"},
  {"member":"आत्म","decision":"मूल"}
]
\`\`\`
- For \`decision\` ∈ {कृत्, तद्धित}: exactly ONE leaf layer, whose \`c\` is the member stem, with \`pratyaya\` + \`sutra\`.
- For \`decision\` = समास: one or more compound layers (outermost first); तद्धित/कृत् leaf layers inside get \`pratyaya\`.
- For \`decision\` = मूल: omit \`layers\`.
- Emit ONLY the json, and include EVERY member in THIS list exactly once.`;

function termLine(g) {
  const egs = [...new Set(g.occurrences.map(o => o.word))].slice(0, 3).join(', ');
  return `- \`${g.member}\`  (×${g.count}; e.g. ${egs})`;
}

function makePrompt(slice, partLabel) {
  return `# समास मध्य-पद peel — gap fill${partLabel ? ' (' + partLabel + ')' : ''}

You are a Pāṇinian vyākaraṇa expert. Below are **${slice.length} prātipadika members** pulled from compounds
across our corpus. Each currently has **NO derivation analysis** in our data — they are the *middle /
non-head* members a left-spine peel tends to skip (e.g. in वैदिक-धर्म-मार्ग-परता we already peel वैदिक and
परता, but धर्म and मार्ग were never classified). For **each** member decide, per the policy, how it decomposes.
${partLabel ? '\n**This is ' + partLabel + ' — classify ONLY the members listed here; the other parts are separate pastes.**\n' : ''}
${POLICY}

## Members (${slice.length})
${slice.map(termLine).join('\n')}
`;
```
