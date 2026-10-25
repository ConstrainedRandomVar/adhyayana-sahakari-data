You are an expert in Pāṇinian vyākaraṇa and Sanskrit lexicon. I give you a NUMBERED LIST of Sanskrit verses (Devanāgarī, sandhi-joined). Produce a COMPLETE analysis of EACH and return a SINGLE JSON ARRAY — one object per verse, IN THE SAME ORDER as given — and NOTHING else (no markdown fences, no prose, no ``` ). It must parse with JSON.parse. Use Devanāgarī for all Sanskrit; use English only for the `meaning` fields. Output STRICTLY VALID JSON — NEVER put an unescaped double-quote (") inside any string value; in glosses/meanings use single quotes or none (no `"…"` inside a value).

Each element of the returned ARRAY is a JSON object with EXACTLY four keys — `words` (segmentation + morphology + per-word meaning + recursive samāsa), `clauses` (clause decomposition), `tree` (kāraka dependency tree, one node per word), and `sandhi` (inter-word junctions). Shape:

{
  "ref": "<verse ref, e.g. 1.1>",
  "words": [
    { "n": 1, "word": "<segmented pada, citation-restored, Devanāgarī>",
      "morph": "<morphology — see MORPH FORMAT>",
      "meaning": "<concise English gloss of this word AS USED HERE, 1-6 words>",
      "samasa": [ <recursive decomposition layers — ONLY for compound words; omit the field otherwise> ] }
  ],
  "clauses": [
    { "id": 1, "type": "main|nominal|relative|correlative|quotation|subordinate", "subordinateTo": <clause id | 0>,
      "words": [<every n in this clause>], "elided": ["<supplied word(s), e.g. अस्ति; [] if none>"],
      "anuktaKarta": "<elided agent, e.g. अहम् / कश्चित् / (impersonal) / (copula अस्ति implied); '' if none>",
      "gloss": "<one-line English of the clause>" }
  ],
  "tree": [
    { "n": 1, "word": "<surface word, same as words[].word>", "morph": "<same morph>", "clause": <clause id>,
      "role": "<one canonical role from the list below>",
      "governor": <n of the word this depends on; a finite verb points to ITS OWN कर्ता, or 0 when the कर्ता is elided / it is the root>,
      "transitivity": "<सकर्मकः|अकर्मकः — verbs/participles-as-verbs only; else omit>",
      "voice": "<कर्तरि|कर्मणि|भावे — verbs only; else omit>",
      "clauseType": "<main|relative|correlative|quotation|nominal|subordinate — ONLY on the clause HEAD>",
      "subordinateTo": <clause id this clause hangs under, or 0 — ONLY on the head>,
      "impliedKarta": {"agent":"<अहम्/त्वम्/कश्चित्/तत्/(impersonal)/(copula अस्ति implied)>","by":"<signal used>"} }
  ],
  "sandhi": [
    { "before": ["<pada1>", "<pada2>"], "after": "<the combined surface form EXACTLY as written in the verse>",
      "rule": "<Sanskrit sandhi rule name, e.g. सवर्णदीर्घ / गुण / यण् / विसर्ग-उत्व / अनुस्वार>",
      "sutra": "<Pāṇini sūtra number if known, e.g. 6.1.101; else \"\">" }
  ]
}

## Segmentation (for `words`)
- **Undo sandhi**; list each underlying pada (declinable / finite verb / indeclinable) as its own unit, in reading order, citation-form ending restored (e.g. `भानेऽपि` → `भाने`, `अपि`).
- **The source may contain SPURIOUS spaces inside a single word or compound** (OCR/formatting artifacts). Do NOT treat every space as a word boundary — segment by grammar and sandhi, JOINING across a spurious intra-compound space (e.g. `अध्येतृवर्गमध्यस्थ पुत्राध्ययन शब्दवत्` is ONE compound `अध्येतृवर्गमध्यस्थपुत्राध्ययनशब्दवत्`, not three words).
- **Keep a samāsa (compound) as ONE unit**, members hyphen-joined (e.g. `अध्येतृ-वर्ग-मध्यस्थ`); note the OUTERMOST compound type in `morph` AND give the full recursive `samasa` decomposition. Non-compound units omit `samasa`.
- Drop nothing (particles च/एव/हि/वै/तु/अपि/इति… included); do NOT include the daṇḍa (।/॥) or the verse number.
- **Negation**: नो(=न+उ), नैव(=न+एव), lone न/मा → segment the न/मा as its OWN unit `न — अव्यय (निषेध)`.

## MEANING (for `words[].meaning`)
- A concise English gloss of the word AS USED HERE (case-appropriate — e.g. षष्ठी → "of X"). Keep it short (1-6 words). For particles (निपात) give the particle sense (e.g. एव → "only / indeed"). For a compound give its overall meaning.

## MORPH FORMAT (match exactly)
- **Nominal:** `<stem> · <vibhakti>·<वचन>·<लिङ्ग>` (प्रथमा/…/सप्तमी/सम्बोधन · एक/द्वि/बहु · पुं/स्त्री/नपुं). Add `(सर्वनाम)` for pronouns and the samāsa type `(तत्पुरुष|कर्मधारय|बहुव्रीहि|द्वन्द्व|अव्ययीभाव)` for compounds. Neuter प्रथमा=द्वितीया → give both as `प्रथमा/द्वितीया` when ambiguous.
- **Finite verb (तिङन्त):** `<√धातु> · <कर्तरि|कर्मणि|भावे>·<लकार>·<प्रथम/मध्यम/उत्तम>पुरुष·<एक/द्वि/बहु>·<परस्मैपद|आत्मनेपद>`.
- **कृदन्त:** name the कृत्-प्रत्यय + function, e.g. `<√धातु> · <कर्मणि|कर्तरि> भूतकृदन्त (क्त) · <case·वचन·लिङ्ग>`; `ल्यबन्त (पूर्वकालिक)`; `क्त्वान्त (पूर्वकालिक)`; `शत्रन्त/शानजन्त (वर्तमान)`; `<√धातु> तुमुन् (हेत्वर्थ)`.
- **Indeclinable:** `अव्यय (<short sense — निषेध / अवधारण / दृष्टान्त / सम्बोधन / etc.>)`. Prefer the citation धातु with upasarga, e.g. `प्रति-√बन्ध्`, `अधि-√इ`.

## Recursive samāsa (`samasa` field — compound units only)
Do NOT stop at the outermost split. A long compound is a nested stack of BINARY samāsas — peel one layer at a time from the RIGHT (for तत्पुरुष/कर्मधारय the final member is the head): record that layer, then recurse into whichever member is ITSELF still a compound, until every member is an underived प्रातिपदिक. A member that is a तद्धित/कृत् derivative gets its प्रत्यय. Emit `samasa` as a FLAT array, outermost first; each layer's `c` says which sub-compound it splits:
`{"c":"<compound>","vigraha":"<vigraha>","type":"<type+subtype, e.g. षष्ठी-तत्पुरुष>","sutra":"<sūtra>"}` — for a तद्धित/कृत् leaf add `"pratyaya":"<प्रत्यय>"` with `type` `तद्धित`/`कृत्`. Stop when nothing splits. **Go all the way down to the प्रातिपदिक (कृदन्त/तद्धित).**
**PEEL THE KṚT/TADDHITA LEAF TOO — do NOT stop at a derived noun.** Before you TERMINATE any member, ask: is it derivable from a √धातु (then कृत्) or from a nominal base (then तद्धित)? If yes, it gets a FINAL layer decomposing it into `<√root / base>` + `प्रत्यय`, with the vigraha showing that derivation. **FREQUENCY does NOT make a member मूल** — common action-nouns in -अ (घञ्/अच्/अप्), -अन (ल्युट्), -ति (क्तिन्), agent nouns in -तृ (तृच्), and क्त/क्तवतु participles ARE कृदन्त and MUST be peeled. E.g. भाव → `{"c":"भाव","vigraha":"√भू + घञ्","type":"कृत्","pratyaya":"घञ्","sutra":"3.3.18"}`; बाध → `{"c":"बाध","vigraha":"√बाध् + घञ्","type":"कृत्","pratyaya":"घञ्"}`; ग्रास → `√ग्रस् + घञ्`; आभास → `आ-√भास् + घञ्`; आनन्द → `आ-√नन्द् + घञ्`; ज्ञान → `√ज्ञा + ल्युट्`; भान → `{"c":"भान","vigraha":"√भा + ल्युट्","type":"कृत्","pratyaya":"ल्युट्","sutra":"3.3.115"}`; अध्ययन → `अधि-√इ + ल्युट्`; अध्येतृ → `अधि-√इ + तृच्`. Only a genuinely underived मूल-प्रातिपदिक (e.g. नर, पुत्र, गो, देश, आकाश) terminates without such a layer; a pronoun/particle/prefix (तत्, अ (नञ्), सु) is not decomposed.
Deep example — वैदिकधर्ममार्गपरता:
[{"c":"वैदिकधर्ममार्गपरता","vigraha":"वैदिकधर्ममार्गे परता","type":"सप्तमी-तत्पुरुष","sutra":"2.2.8"},
 {"c":"वैदिकधर्ममार्ग","vigraha":"वैदिकधर्मस्य मार्गः","type":"षष्ठी-तत्पुरुष","sutra":"2.2.8"},
 {"c":"वैदिकधर्म","vigraha":"वैदिकश्च असौ धर्मः","type":"कर्मधारय","sutra":"2.1.57"},
 {"c":"वैदिक","vigraha":"वेदम् अधीते","type":"तद्धित","pratyaya":"अण्","sutra":"4.2.59"},
 {"c":"परता","vigraha":"परस्य भावः","type":"तद्धित","pratyaya":"तल्","sutra":"5.1.119"}]

## Clauses + kāraka tree (`clauses`, `tree`)
Tag every word with its `clause` (1,2,3… in reading order). A CLAUSE = one finite verb (or one verbless "X [is] Y" predication) + all words depending on it, bounded by daṇḍas, relative–correlative joints (यत्…तत्, यथा…तथा), and quotation इति. Gerunds/participles stay in their finite verb's clause. On each clause HEAD also give `clauseType` + `subordinateTo`.

Canonical roles (use EXACTLY these strings):
- `कर्ता` agent (प्रथमा कर्तरि / तृतीया कर्मणि) · `कर्म` object (द्वितीया कर्तरि / प्रथमा कर्मणि) · `करणम्` तृतीया · `सम्प्रदानम्` चतुर्थी · `अपादानम्` पञ्चमी · `अधिकरणम्` सप्तमी (`कालाधिकरणम्` for time) · `सम्बोध्यः` सम्बोधन · `हेतुः` cause.
- `षष्ठीसम्बन्धः` genitive (governor = word possessed) · `विशेषणम्` adjective (governor = qualified word, same case) · `समानाधिकरणम्` predicate/appositive (governor = the core arg it co-refers with) · `क्रियाविशेषणम्` adverb (governor = verb) · `पूर्वकालः` ल्यप्/क्त्वा/prior-क्त (governor = main verb) · `समानकालः` शतृ/शानच् (governor = main verb) · `सुप्_समुच्चितम्` conjunct (governor = the other conjunct) · `प्रतिषेधः` न/मा (governor = verb) · `समुच्चयद्योतकः` च/वा/अपि coordinator · `उपमानम्`/`उपमेयम्` इव/यथा · `भावलक्षणसप्तमी` locative-absolute · `निर्धारणम्` selecting one of a group · `इत्थम्भूतलक्षणे` तृतीया of characterizing state.
- The clause HEAD (finite verb, or the subject of a verbless predication) is marked `role: "अभिहितकर्ता"`, `governor` = the n of ITS OWN कर्ता (or 0 if elided), plus `transitivity`, `voice`, `clauseType`, `subordinateTo`.

Hard rules: exactly one governor per word; a finite verb never points to its own कर्म or itself (governor = its कर्ता's n, or 0); case must agree with role (neuter प्रथमा=द्वितीया allowed); voice drives कर्ता/कर्म case; no cycles/self-loops; never set a governor across a ॥ / sentence-final इति boundary. If a role is genuinely unresolvable use `role:"?"` with your best governor. For an elided कर्ता: `governor: 0` + fill `impliedKarta`; for a verbless "X [is] Y", subject = कर्ता governor 0 impliedKarta (copula अस्ति implied), predicate = समानाधिकरणम् governor = subject's n.
**सम्बोध्यः (vocative) ONLY for a genuine address** — a person/deity/hearer explicitly invoked in सम्बोधन (often with हे/भोः or clear apostrophe). A descriptive or qualifying compound, or a word inside a simile (दृष्टान्त — इव / वत् / यथा), is NOT a vocative even if its stem-final resembles सम्बोधन; tag it by its real function — विशेषणम् (qualifier), उपमानम्/उपमेयम् (simile), or समानाधिकरणम् (appositive). Reserve सम्बोध्यः for true direct address.

## Sandhi (`sandhi`)
- Report ONLY inter-word junctions (two separate words fusing in the written text). Do NOT report sandhi internal to a compound (that is samāsa, handled in `words`). For a run of three fused words (e.g. न + आशा + अस्ति → नाशास्ति), emit ONE entry per adjacent pair, in order. `after` must be the exact substring as written. If the verse has NO inter-word sandhi, use `"sandhi": []`.
- INCLUDE word-final म् → anusvāra (ं) before a following consonant (मोऽनुस्वारः, 8.3.23) — e.g. स्फुटम् यतः → स्फुटं. These are inter-word sandhi and must appear.

Output ONLY the JSON ARRAY — exactly one object per input verse, in order, each with its matching "ref".

## Verses
- ref: {REF}
- verse: {VERSE}
…
