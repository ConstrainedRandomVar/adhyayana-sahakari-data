# Gemini morph/segmentation protocol (feeds the kāraka-tree protocol)

Produces the numbered word-list + morphology that `gemini-karaka-tree-prompt.md` consumes, for texts
that have NO Zenodo morphology (e.g. Vivekacūḍāmaṇi). Paste one verse's raw text after the marker.

>>> PROMPT START

You are an expert in Pāṇinian vyākaraṇa. I give you ONE Sanskrit verse (Devanāgarī, sandhi-joined).
**Segment it into its analysable word-units and give each unit's morphology.** Output ONLY a JSON array.

## Segmentation rules
- **Undo sandhi** and list each underlying *pada* (declinable word / finite verb / indeclinable) as its
  own unit, in reading order. Restore each word's citation-form ending (e.g. `उदकमेव` → `उदकम्`, `एव`;
  `तान्येव` → `तानि`, `एव`).
- **Keep a samāsa (compound) as ONE unit**, write its members hyphen-joined (e.g. `सर्ववेदान्त-
  सिद्धान्त-गोचरम्`), note the OUTERMOST compound type in the morph, AND give a full **recursive
  `samasa` decomposition** (see "Recursive samāsa" below). Non-compound units omit `samasa`.
- Drop nothing; every surface piece becomes a unit (particles च/एव/हि/वै/तु/इति… included). Do NOT
  include the verse-number `॥ N ॥` or daṇḍas as units.
- **Negation — do not lose it.** नो (= न + उ), नैव (= न + एव), नो चेत्, and a lone न/मा all contain the
  प्रतिषेध particle — segment the न/मा as its OWN unit `न — अव्यय (निषेध)`. NEVER read नो/नु as `नः`
  (अस्मद् षष्ठी). e.g. `मुक्तिर्नो लभ्यते` → …, `न` (निषेध), `लभ्यते` — the sentence means "is NOT
  obtained." (A genuine `नः` = अस्मद् षष्ठीबहु "our/us" only when the sense truly needs a genitive.)

## Output — JSON array, one object per unit, in order
```
{"n": <1-based int>, "word": "<the segmented pada, citation-restored, Devanāgarī>",
 "morph": "<morphology, see format>",
 "dhatu": {"gana": <1-10>, "upadesha": "<aupadeśika form>", "artha": "<Dhātupāṭha artha>"},   ← ONLY for units with a √धातु
 "samasa": [ <recursive decomposition layers — ONLY for compound words; omit the field otherwise> ]}
```
Return ONLY the JSON array — no prose.

## Morph format (match EXACTLY — this is what the kāraka step reads)
- **Nominal (noun/adjective/pronoun):** `<stem> · <vibhakti>·<वचन>·<लिङ्ग>` using
  प्रथमा/द्वितीया/…/सप्तमी/सम्बोधन · एक/द्वि/बहु · पुं/स्त्री/नपुं. Add `(सर्वनाम)` for pronouns and the
  samāsa type `(तत्पुरुष|कर्मधारय|बहुव्रीहि|द्वन्द्व|अव्ययीभाव)` for compounds. Neuter प्रथमा=द्वितीया —
  give both as `प्रथमा/द्वितीया` when ambiguous.
- **Finite verb (तिङन्त):** `<√धातु> · <कर्तरि|कर्मणि|भावे>·<लकार>·<प्रथम/मध्यम/उत्तम>पुरुष·<एक/द्वि/बहु>·<परस्मैपद|आत्मनेपद>`.
  Name the लकार with its FULL, unambiguous name — one of exactly: लट् लिट् लुट् लृट् लोट् लङ् विधिलिङ् आशीर्लिङ् लुङ् लृङ्.
  Write the optative/potential as **विधिलिङ्** and the benedictive as **आशीर्लिङ्** — never the bare abbreviation "लिङ्" (it collides with the gender word लिङ्ग and drops the mood).
- **कृदन्त (participle/gerund):** name the कृत्-प्रत्यय + how it functions, e.g.
  `<√धातु> · <कर्मणि|कर्तरि> भूतकृदन्त (क्त) · <case·वचन·लिङ्ग>`; `ल्यबन्त (पूर्वकालिक)` for ल्यप्;
  `क्त्वान्त (पूर्वकालिक)` for क्त्वा; `शत्रन्त/शानजन्त (वर्तमान)` for शतृ/शानच्; `<√धातु> तुमुन् (हेत्वर्थ)`.
- **Indeclinable:** `अव्यय (<short sense — निषेध / अवधारण / सम्बोधन / दृष्टान्त / etc.>)`.
- Prefer the citation धातु with the upasarga, e.g. `अनु-वि-√ली`, `प्र-√वच्`.

## Dhātupāṭha entry (`dhatu` field — every unit whose morph has a √धातु: finite verbs AND कृदन्त)
Homonymous roots are DIFFERENT dhātus — `√कल्` alone is not enough: कलँ शब्दसङ्ख्यानयोः (भ्वादि, आत्मनेपद),
कलँ क्षेपे (चुरादि) and कल गतौ सङ्ख्याने च (चुरादि) are three entries. Identify WHICH Dhātupāṭha entry this
form comes from, and give it as
`"dhatu": {"gana": <1-10>, "upadesha": "<the aupadeśika form as listed in the Dhātupāṭha>", "artha": "<the Dhātupāṭha artha>"}`.
- Decide by the FORM (the gaṇa's vikaraṇa — शप्/श्यन्/श्नु/श/श्नम्/उ/श्ना, चुरादि णिच् -अय-; the pada) AND by
  the SENSE the word has in this verse (साधु कलयति "regards/considers" = सङ्ख्याने → कल गतौ सङ्ख्याने च, gaṇa 10).
- A causative (णिजन्त) or desiderative (सन्नन्त) form: give the BASE dhātu's entry (भ्रमयति → the entry of भ्रमुँ that
  fits the sense) — the morph already records णिच्/सन्.
- Copy the upadeśa and artha as the Dhātupāṭha has them (with anunāsika/it-markers: गमॢँ, कलँ, भू; artha
  e.g. गतौ, सत्तायाम्, गतौ सङ्ख्याने च). Do NOT give serial numbers (01.1137 / कौमुदी 982) — the pipeline resolves
  the number from gaṇa + upadeśa + artha and cross-checks it against the conjugation tables.
- If two entries remain genuinely possible, give the more likely one and add `"alt": [{"gana":…,"upadesha":…,"artha":…}]`.
- Example: `{"n":4,"word":"कलयति","morph":"√कल् · कर्तरि·लट्·प्रथमपुरुष·एक·परस्मैपद","dhatu":{"gana":10,"upadesha":"कल","artha":"गतौ सङ्ख्याने च"}}`

## Recursive samāsa (`samasa` field — compound units only)
Do NOT stop at the outermost split. A long compound is a nested stack of BINARY samāsas — **peel one
layer at a time from the RIGHT** (for a तत्पुरुष/कर्मधारय the final member is the head): record that
layer, then recurse into whichever member is ITSELF still a compound, until every member is an
underived प्रातिपदिक. A member that is a तद्धित/कृत् derivative gets its प्रत्यय. Emit `samasa` as a FLAT
array, outermost layer first; the `c` (compound) field of each layer says which sub-compound it splits:
`{"c":"<compound>","vigraha":"<vigraha>","type":"<type+sub-type, e.g. षष्ठी-तत्पुरुष>","sutra":"<sūtra>"}`
— for a तद्धित/कृत् leaf add `"pratyaya":"<प्रत्यय>"` with `type` `तद्धित`/`कृत्`. Stop when nothing splits.
**Resolve BOTH members at EVERY binary split — including the MIDDLE / non-head member, not just the left
spine** (in वैदिकधर्ममार्गपरता, परता must be peeled, not left dangling). Leaf policy (conservative):
- **कृत्** = derivable from a √धातु by a productive kṛt affix — **FREQUENCY does NOT make it मूल**: action
  nouns in -अ (घञ्/अच्/अप्), -अन (ल्युट्), -ति (क्तिन्), agent nouns in -तृ (तृच्), and क्त/क्तवतु participles
  ARE कृत् (e.g. भाव = √भू + घञ्).
- **तद्धित** = productive taddhita affix (अण्, तल्/त्व, मतुप्, इनि, ठक्, …).
- **मूल** = genuinely underived प्रातिपदिक — **उṇādi-derived AND lexicalised nouns also count as मूल; do NOT
  peel them** (धर्म ← √धृ+manin, मार्ग, कर्मन्, देव, गो, नर). Pronouns/particles/prefixes are मूल. When in
  genuine doubt between a lexicalised उṇādi noun and a transparent kṛt derivative, choose **मूल**.
Deep example — वैदिकधर्ममार्गपरता:
```
[{"c":"वैदिकधर्ममार्गपरता","vigraha":"वैदिकधर्ममार्गे परता","type":"सप्तमी-तत्पुरुष","sutra":"2.2.8"},
 {"c":"वैदिकधर्ममार्ग","vigraha":"वैदिकधर्मस्य मार्गः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"},
 {"c":"वैदिकधर्म","vigraha":"वैदिकश्च असौ धर्मः","type":"कर्मधारय","sutra":"2.1.57"},
 {"c":"वैदिक","vigraha":"वेदम् अधीते वेदाद् आगतो वा","type":"तद्धित","pratyaya":"अण्","sutra":"4.2.59"},
 {"c":"परता","vigraha":"परस्य भावः","type":"तद्धित","pratyaya":"तल्/त्व","sutra":"5.1.119"}]
```

## Worked example
Input verse: `सर्ववेदान्तसिद्धान्तगोचरं तमगोचरम् । गोविन्दं परमानन्दं मद्गुरुं प्रणतोऽस्म्यहम् ॥ १ ॥`
Output:
```json
[
 {"n":1,"word":"सर्ववेदान्त-सिद्धान्त-गोचरम्","morph":"सर्ववेदान्तसिद्धान्तगोचर · द्वितीया·एक·पुं (तत्पुरुष)","samasa":[{"c":"सर्ववेदान्तसिद्धान्तगोचर","vigraha":"सर्ववेदान्तसिद्धान्तानां गोचरः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"},{"c":"सर्ववेदान्तसिद्धान्त","vigraha":"सर्ववेदान्तानां सिद्धान्तः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"},{"c":"सर्ववेदान्त","vigraha":"सर्वे वेदान्ताः","type":"कर्मधारय","sutra":"2.1.57"},{"c":"वेदान्त","vigraha":"वेदस्य अन्तः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"},{"c":"सिद्धान्त","vigraha":"सिद्धः अन्तः","type":"कर्मधारय","sutra":"2.1.57"},{"c":"गोचर","vigraha":"गोषु चरति","type":"उपपद-तत्पुरुष","pratyaya":"ट","sutra":"3.2.16"}]},
 {"n":2,"word":"तम्","morph":"तद् · द्वितीया·एक·पुं (सर्वनाम)"},
 {"n":3,"word":"अगोचरम्","morph":"अगोचर · द्वितीया·एक·पुं (नञ्-तत्पुरुष)","samasa":[{"c":"अगोचर","vigraha":"न गोचरः","type":"नञ्-तत्पुरुष","sutra":"2.2.6"},{"c":"गोचर","vigraha":"गोषु चरति","type":"उपपद-तत्पुरुष","pratyaya":"ट","sutra":"3.2.16"}]},
 {"n":4,"word":"गोविन्दम्","morph":"गोविन्द · द्वितीया·एक·पुं"},
 {"n":5,"word":"परम-आनन्दम्","morph":"परमानन्द · द्वितीया·एक·पुं (कर्मधारय)","samasa":[{"c":"परमानन्द","vigraha":"परमः आनन्दः","type":"कर्मधारय","sutra":"2.1.57"}]},
 {"n":6,"word":"मत्-गुरुम्","morph":"मद्गुरु · द्वितीया·एक·पुं (तत्पुरुष)","samasa":[{"c":"मद्गुरु","vigraha":"मम गुरुः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"}]},
 {"n":7,"word":"प्रणतः","morph":"प्र-√नम् · कर्तरि भूतकृदन्त (क्त) · प्रथमा·एक·पुं","dhatu":{"gana":1,"upadesha":"णमँ","artha":"प्रह्वत्वे शब्दे च"}},
 {"n":8,"word":"अस्मि","morph":"√अस् · कर्तरि·लट्·उत्तमपुरुष·एक·परस्मैपद","dhatu":{"gana":2,"upadesha":"असँ","artha":"भुवि"}},
 {"n":9,"word":"अहम्","morph":"अस्मद् · प्रथमा·एक (सर्वनाम)"}
]
```

## Now segment this verse
<VERSE>

>>> PROMPT END
