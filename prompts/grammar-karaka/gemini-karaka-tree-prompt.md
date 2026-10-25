# Gemini prompt — kāraka dependency tree (e-reader-compatible)

Produces the same shape as the UoHyd e-reader's `kaaraka_sambandha` edges, so the output can slot
into the same `karaka-data-*` / `karaka-governor-*` pipeline used for BG. Paste everything between the
`>>>` markers into Gemini, then append the verse block at the bottom.

>>> PROMPT START

You are an expert in Pāṇinian vyākaraṇa performing **kāraka (syntactic-role) dependency analysis** of
classical Sanskrit. For the verse I give you, produce a **dependency tree**: assign every word a
kāraka/relational role and the single word it depends on (its governor). Output must exactly follow
the schema below.

## Input you receive
A verse reference, its text, and a numbered list of its words with morphology. Treat the numbering as
fixed `anvaya_no` node ids. The morphology (stem, gender/case/number for nominals; root/voice/tense/
person/number for verbs) is given — trust it unless it is clearly wrong, in which case note the
disagreement in a `notes` field but still analyse.

## What to produce
A JSON OBJECT with two keys: `clauses` (the clause-decomposition, one entry per clause in reading order)
and `tree` (one object per input word, in order — the kāraka dependency tree). Shape:

```
{
 "clauses": [
   {"id": <int>, "type": "main|nominal|relative|correlative|quotation|subordinate", "subordinateTo": <clause id | 0>,
    "words": [<anvaya_no… every word in this clause>],
    "elided": ["<supplied/understood word(s), e.g. अस्ति / दुर्लभम् अस्ति; [] if none>"],
    "anuktaKarta": "<the elided agent, e.g. (जनैः) / अहम् / कश्चित् / (impersonal); '' if none>",
    "gloss": "<one-line English of the clause>"}
 ],
 "tree": [
{
  "n": <anvaya_no, integer>,
  "word": "<surface word, as given>",
  "morph": "<the morphology, as given or corrected>",
  "clause": <integer clause id this word belongs to — see "Clauses" below>,
  "role": "<one canonical role from the list below>",
  "governor": <anvaya_no of the word this depends on; the main verb points to its own कर्ता, OR 0
               when its कर्ता is elided / it is the sentence root — see "Implied kartā" below>,
  "transitivity": "<सकर्मकः | अकर्मकः — ONLY on finite verbs / participles acting as verbs; else omit>",
  "voice": "<कर्तरि | कर्मणि | भावे — ONLY on verbs; else omit>",
  "clauseType": "<main | relative | correlative | quotation | nominal | subordinate — ONLY on the
                  clause's HEAD (its finite verb, or the subject of a verbless predication)>",
  "subordinateTo": <clause id this clause hangs under, or 0 if it is a main clause — ONLY on the head>,
  "impliedKarta": {"agent": "<pronoun/word supplying the elided कर्ता, e.g. अहम् / त्वम् / कश्चित् / तत्,
                              or (impersonal) / (copula अस्ति implied)>",
                   "by": "<the signal used — see below>"},   // ONLY on a verb/predication whose कर्ता is elided
  "notes": "<optional: only when you deviate from the given morph or are genuinely unsure>"
}
 ]
}
```

Return ONLY the JSON OBJECT — no prose. The `tree` has EXACTLY one node per input pada, keeps the given
numbering, and NEVER merges two words into one node.

## Clauses
Tag every word with the `clause` it belongs to (`1, 2, 3 …` in the reading order the clauses start).
A CLAUSE = exactly one finite verb (or one verbless predication) + all words depending on it, bounded
by daṇḍas (।/॥), relative–correlative joints (यत्…तत्, यतो यतः…, यथा…तथा), and quotation इति.
- Every finite verb heads its own clause; a verbless "X [is] Y" is its own clause (headed by its
  subject). Gerunds/participles (ल्यप्/क्त्वा/शतृ/क्त…) are NOT separate clauses — they stay in the
  clause of the finite verb they modify.
- On each clause's HEAD only (its finite verb, or the predication subject) also give `clauseType`
  (main | relative | correlative | quotation | nominal | subordinate) and `subordinateTo` (the clause
  id it hangs under, or 0 for a main clause).
- A `governor` may cross a clause boundary ONLY for a subordinate clause's HEAD attaching to the clause
  it modifies (a पूर्वकालः/समानकालः gerund, or a relative clause, → the main verb). Every ordinary कारक
  word attaches WITHIN its own clause. Never link across a full SENTENCE boundary (॥ / sentence-final इति).

## Canonical roles (use EXACTLY these strings)
Nominal kārakas — each has a default vibhakti; use it to self-check your assignment:
- `कर्ता` — agent. प्रथमा under कर्तरि (active) voice; तृतीया under कर्मणि (passive).
- `कर्म` — object. द्वितीया under कर्तरि; प्रथमा under कर्मणि.
- `करणम्` — instrument. तृतीया.
- `सम्प्रदानम्` — recipient/purpose. चतुर्थी.
- `अपादानम्` — source/ablative point. पञ्चमी.
- `अधिकरणम्` — locus (place/time/circumstance). सप्तमी.
- `सम्बोध्यः` — addressee (vocative). सम्बोधन.
- `हेतुः` — cause/reason. तृतीया/पञ्चमी (free) — do not reject on case.

Relational / non-kāraka roles:
- `षष्ठीसम्बन्धः` — genitive relation (possessor, etc.). षष्ठी. Governor = the word possessed.
- `विशेषणम्` — adjective/qualifier. Same case as the word it qualifies (agreement). Governor = the qualified word.
- `समानाधिकरणम्` — predicative/co-referential (same case, same referent as a कर्ता/कर्म, e.g. a
  predicate nominative or an appositive). Governor = the core argument it co-refers with.
- `क्रियाविशेषणम्` — adverbial (manner/degree modifying the verb). Governor = the verb.
- `पूर्वकालः` — prior-action link: a ल्यप्/क्त्वा absolutive or a क्त-participle denoting completed
  prior action. Governor = the main verb.
- `समानकालः` — simultaneous-action link: a शतृ/शानच् present participle. Governor = the main verb.
- `सुप्_समुच्चितम्` — a nominal conjoined with another (coordinated by च/और). Governor = the other
  conjunct it is joined to (NOT the verb).
- `उपपद-तृतीया` — a तृतीया forced by an upapada निपात विना/सह/नाना/पृथक् (2.3.19), NOT the action's
  instrument. Governor = the upapada. Use this, never `करणम्`/`हेतुः`, for such a word (पुण्यैः विना →
  पुण्यैः is `उपपद-तृतीया`). See the upapada checklist below.

The finite verb (or a participle governing its own कर्ता/कर्म) is the clause head. Mark it:
`role: "अभिहितकर्ता"`, `governor:` = the anvaya_no of ITS OWN कर्ता, plus `transitivity` and `voice`.
(This self-edge to the agent is the e-reader convention for "this node is the predicate.")

## Hard rules
1. **Exactly one governor per word.** Every word points to exactly one other word, EXCEPT a finite
   verb (or predication head) whose कर्ता is elided/impersonal, which uses `governor: 0` (= root /
   points to nothing). A verb NEVER points at its own कर्म and NEVER points at itself — its governor is
   either its explicit in-clause कर्ता's `n`, or `0`. No cycles; no self-loops.
2. **Case must agree with the role.** Before finalising a nominal's role, confirm its given vibhakti
   matches the default above (accounting for the verb's voice for कर्ता/कर्म). If they contradict,
   the role is wrong — reconsider. Neuter प्रथमा=द्वितीया syncretism is allowed.
3. **Voice drives कर्ता/कर्म case.** Read the verb's voice from its morphology (कर्तरि = unmarked
   default; कर्मणि/भावे marked). In कर्मणि the कर्ता is तृतीया and the कर्म is प्रथमा.
4. **Don't guess.** If a word's role is genuinely unresolvable, use `role: "?"` and still give your
   best `governor` — never invent a role to force-fill. Better an honest `?` than a wrong tag.
5. Multiple verbs → multiple clauses; analyse each clause's arguments against its own verb. A
   subordinate clause's verb depends (पूर्वकालः/समानकालः/etc.) on the main verb.
6. Coordinated agents/objects (राम + लक्ष्मण both agents): tag the primary one `कर्ता`/`कर्म` (governor
   = verb) and the other `सुप्_समुच्चितम्` (governor = the primary conjunct).
7. **A clause = one finite verb + the words depending on it**, bounded by daṇḍas (।/॥), relative–
   correlative joints (यत्…तत्, यतो यतः…, यथा…तथा), and quotation `इति`. **Never set a `governor`
   across a SENTENCE boundary** (॥, or a sentence-final `इति`+speech-verb). Resolve each clause's
   कारकs against ITS OWN verb only.
8. **Attributive participle ≠ re-tagging its head noun.** A क्त/क्तवतु/तव्य/शतृ… participle that AGREES
   in case with a noun (e.g. `उदके प्रास्तः सैन्धवखिल्यः` — प्रास्तः प्रथमा agrees with सैन्धवखिल्यः प्रथमा)
   is that noun's `विशेषणम्` (governor = the noun). Do NOT then re-tag the noun as the participle's कर्म
   just because the participle is कर्मणि — the noun keeps the role it has toward the FINITE verb (here
   सैन्धवखिल्यः = कर्ता of अनुविलीयेत). **Consistency check:** any word a verb names as its `अभिहितकर्ता`
   (governor edge) MUST itself carry role `कर्ता`; a word tagged `कर्म` can never be a verb's कर्ता target.

## Implied (elided) kartā — pick the agent from signals, NEVER borrow from another clause
Sanskrit constantly ELIDES the कर्ता. Every finite verb still needs one, but if you cannot find an
explicit case-matching nominative **inside that verb's own clause** (प्रथमा under कर्तरि; तृतीया under
कर्मणि), the कर्ता is elided. In that case: set the verb's `governor: 0` and add an `impliedKarta`
object. **Do NOT point `governor` at a nominative that belongs to a different clause — that is the most
common and worst error.** THREE non-negotiables for an elided-कर्ता verb: (a) `governor` is EXACTLY `0`
— never the verb's own `n` (no self-loops), never its कर्म; (b) the agent goes in the `impliedKarta`
field, NOT in `notes`; (c) this applies to existential `स्यात्`/`भवति`-with-no-agent too (→
`impliedKarta.agent: (impersonal)`), which learners most often get wrong. Infer the elided agent from
these signals, in priority order:
1. **Verb person/number** (strongest): उत्तमपुरुष → `अहम्`/`वयम्`; मध्यमपुरुष → `त्वम्`/`यूयम्`;
   प्रथमपुरुष → the sentence's topic/previously-named subject.
2. **Quotation frame** `…इति <speech-verb>`: the INNER first-person verb's agent is `अहम्` (the
   speaker). Keep `governor: 0` + `impliedKarta.agent: अहम्` — do NOT link it to the outer speaker's
   named node (e.g. in `…इति ब्रवीमि इति ह उवाच याज्ञवल्क्यः`, ब्रवीमि → अहम् (governor 0); only उवाच
   takes याज्ञवल्क्यः as its explicit कर्ता).
3. **Relative/correlative + optative/gnomic** (यः…, यतो यतः… with विधिलिङ्): indefinite agent → `कश्चित्`
   ("one/whoever").
4. **Impersonal/existential** (स्यात् "there would be", भवति with no agent, भावे voice): no personal
   agent → `impliedKarta.agent: (impersonal)`.
5. Else **carry the main clause's subject** into a shared-subject subordinate clause.
Set `impliedKarta.by` to whichever signal you used (e.g. "उत्तमपुरुष verb", "quotation frame", "यतो-यतः
correlative + optative → indefinite", "existential स्यात्", "shared main-clause subject").

## Verbless (nominal / copula) sentences
`X [is] Y` with no finite verb (X and Y both प्रथमा, e.g. `इदं ब्रह्म`, `विज्ञानघन एव`): tag the subject
`कर्ता` with `governor: 0` and `impliedKarta.agent: (copula अस्ति implied)`; tag the predicate
`समानाधिकरणम्` with `governor` = the subject's n; qualifiers → their head noun. Do NOT hang any of these
on a finite verb in a neighbouring sentence.

### Mini-example (elided kartā + quotation + nominal predication)
Input: `1. ग्रामम् — ग्राम द्वि·एक·पुं ; 2. गच्छेत् — √गम् विधिलिङ्·प्र.पु.·एक ; 3. इति — अव्यय ;
4. ब्रवीमि — √ब्रू लट्·उ.पु.·एक ; 5. सः — तद् प्रथमा·एक·पुं ; 6. धार्मिकः — धार्मिक प्रथमा·एक·पुं`
Three clauses: **1** = the quoted "ग्रामं गच्छेत्" (headed by गच्छेत्, quotation, subordinateTo 2);
**2** = "इति ब्रवीमि" (headed by ब्रवीमि, main); **3** = the nominal "सः धार्मिकः" (headed by सः, nominal).
Output (roles/edges only): गच्छेत्(2) clause 1, `अभिहितकर्ता` governor 0, clauseType quotation,
subordinateTo 2, impliedKarta{agent:`कश्चित्`, by:"प्र.पु. optative, no in-clause nominative → indefinite"},
सकर्मकः, कर्तरि; ग्रामम्(1) clause 1, `कर्म` gov 2; इति(3) clause 2, `क्रियाविशेषणम्` gov 4; ब्रवीमि(4)
clause 2, `अभिहितकर्ता` governor 0, clauseType main, subordinateTo 0, impliedKarta{agent:`अहम्`,
by:"उत्तमपुरुष / quotation frame"}, सकर्मकः, कर्तरि; सः(5) clause 3, `कर्ता` governor 0, clauseType nominal,
subordinateTo 0, impliedKarta{agent:`(copula अस्ति implied)`}; धार्मिकः(6) clause 3, `समानाधिकरणम्` gov 5.

## Finer roles & trigger checklist (apply BEFORE defaulting a role)
- **निर्धारणम्** (2.3.41 यतश्च निर्धारणम्) — a षष्ठी/सप्तमी singling ONE out of a group (जन्तूनाम् … नरजन्म =
  "rarest AMONG creatures"): tag निर्धारणम्, not plain शेष-षष्ठीसम्बन्धः.
- **इत्थम्भूतलक्षणे तृतीया** (2.3.21) — a तृतीया naming a STATE/identity the referent is characterized BY
  (ब्रह्मात्मना संस्थितिः = "abiding AS the Brahman-Self"): tag इत्थम्भूतलक्षणे, not plain करणम्.
- **तसिल् + declined पञ्चमी सर्वनाम → अपादानम्** — अतः/ततः/यतः/कुतः (पञ्चम्यस्तसिल्, 5.3.7) AND तस्मात्/
  अस्मात्/यस्मात् (पञ्चमी सर्वनाम, 2.3.28) are ALL अपादानम् ("from X"), NOT हेतुः/क्रियाविशेषणम् — keep a
  सोपान ("from X → Y") ladder consistent.
- **Negation → `प्रतिषेधः`** (its own role, NOT क्रियाविशेषणम्) — न/मा/नो(=न+उ)/नैव, governor = the verb.
  NEVER read नो/नु as नः (अस्मद्).
- **Coordinator → `समुच्चयद्योतकः`** — a joining particle च/वा/अथवा/अपि (in its "and/or/also" sense) is
  `समुच्चयद्योतकः` (governor = the nearer conjunct), NOT क्रियाविशेषणम्. (The conjoined item itself is
  `सुप्_समुच्चितम्`.)
- **Temporal अव्यय → `कालाधिकरणम्`** — कदा/कदाचन/सदा/तदा/यदा/अद्य/सद्यः… name a time-locus →
  कालाधिकरणम्, not a generic क्रियाविशेषणम्.
- **गत्यर्थ verb's goal → `कर्म`** — a motion verb (गम्/या/व्रज्/इ/आगम्…) takes its destination in
  द्वितीया as its कर्म (शरणं व्रज → शरणम् = कर्म; ग्रामं गच्छति → ग्रामम् = कर्म), not क्रियाविशेषणम्.
- **सति-सप्तमी → `भावलक्षणसप्तमी`** — a locative-absolute (a सप्तमी noun + an agreeing शतृ/शानच्/क्त
  participle, naming the circumstance "when/while X…", e.g. गुरौ उपविष्टे) is `भावलक्षणसप्तमी`, NOT a
  plain place/time अधिकरणम्.
- **तादर्थ्य / purpose → `सम्प्रदानम्`** — a चतुर्थी (or an …अर्थम्/हितार्थम् purpose word) expressing the
  goal/purpose of the action (तादर्थ्ये चतुर्थी, 2.3.14) is `सम्प्रदानम्`.
- **upapada** — विना/सह/नाना/पृथक् force तृतीया on their object (2.3.19); ऋते → पञ्चमी; नमः/स्वस्ति → चतुर्थी.
  Tag the upapada `क्रियाविशेषणम्` pointing at ITS OBJECT (the case-word), NOT the verb. Tag the OBJECT itself
  `उपपद-तृतीया` (governor = the upapada), **NOT `करणम्` and NOT `हेतुः`** — its तृतीया is forced by the निपात
  (2.3.19), so it is an उपपदविभक्ति, not the action's instrument or cause (पुण्यैः विना → पुण्यैः is
  `उपपद-तृतीया`). सह/विना may govern a NON-adjacent word — resolve by अन्वय, not proximity.
- **मुख्य/गौण-कर्म** (1.4.51 अकथितं च), **प्रयोजक/प्रयोज्य-कर्ता** (णिच्, 1.4.52/53), **वीप्सा** (8.1.4),
  **उपमानम्/उपमेयम्** (इव/यथा) — use when they occur.
- **क्त voice** — क्त of a सकर्मक root is कर्मणि (agent तृतीया); of an अकर्मक/गत्यर्थ root is कर्तरि.

## Worked example
Input:
- ref: 5.17
- words:
  1. तत्-बुद्धयः — तद्-बुद्धि{स्त्री}{1;बहु}
  2. तत्-आत्मानः — तद्-आत्मन्{पुं}{1;बहु}
  3. तत्-निष्ठाः — तद्-निष्ठा{स्त्री}{1;बहु}
  4. तत्-परायणाः — तद्-परायणा{स्त्री}{1;बहु}
  5. गच्छन्ति — गम्1{कर्तरि;लट्;प्र;बहु;परस्मैपदी}
  6. अ-पुनरावृत्तिम् — अपुनरावृत्ति{स्त्री}{2;एक}
  7. ज्ञान-निर्धूत-कल्मषाः — ज्ञान-निर्धूत-कल्मषा{स्त्री}{1;बहु}

Output:
```json
{
 "clauses": [
   {"id":1,"type":"main","subordinateTo":0,"words":[1,2,3,4,5,6,7],"elided":[],"anuktaKarta":"","gloss":"Those intent on That, their sins purged by knowledge, reach the state of no-return."}
 ],
 "tree": [
  {"n":1,"word":"तत्-बुद्धयः","morph":"तद्-बुद्धि{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7},
  {"n":2,"word":"तत्-आत्मानः","morph":"तद्-आत्मन्{पुं}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7},
  {"n":3,"word":"तत्-निष्ठाः","morph":"तद्-निष्ठा{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7},
  {"n":4,"word":"तत्-परायणाः","morph":"तद्-परायणा{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7},
  {"n":5,"word":"गच्छन्ति","morph":"गम्1{कर्तरि;लट्;प्र;बहु;परस्मैपदी}","clause":1,"role":"अभिहितकर्ता","governor":7,"transitivity":"सकर्मकः","voice":"कर्तरि","clauseType":"main","subordinateTo":0},
  {"n":6,"word":"अ-पुनरावृत्तिम्","morph":"अपुनरावृत्ति{स्त्री}{2;एक}","clause":1,"role":"कर्म","governor":5},
  {"n":7,"word":"ज्ञान-निर्धूत-कल्मषाः","morph":"ज्ञान-निर्धूत-कल्मषा{स्त्री}{1;बहु}","clause":1,"role":"कर्ता","governor":5}
 ]
}
```
(The verb गच्छन्ति (5) is the head; its agent is word 7 (कर्ता, प्रथमा — matches कर्तरि voice); the
object is word 6 (कर्म, द्वितीया); words 1–4 are adjectives agreeing with and qualifying word 7.)

## Now analyse this verse
- ref: <REF>
- words:
  1. <word> — <morphology>
  2. <word> — <morphology>
  ... (all words, numbered)

>>> PROMPT END
