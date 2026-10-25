# Gemini prompt — kāraka + vibhakti dependency analysis (e-reader-compatible)

Comprehensive successor to `gemini-karaka-tree-prompt.md`. It keeps the same output shape (so the
output still slots into the `karaka-data-*` / `karaka-governor-*` pipeline used for BG) but does
justice to **two distinct layers** that the older prompt conflated:

- **Layer A — कारक / relational role** (the *semantic* syntactic role: कर्ता, कर्म, अपादानम्, …).
- **Layer B — विभक्ति-विधान** (WHICH Pāṇinian sūtra *ordains the case ending*). The case is usually a
  consequence of the kāraka + the anabhihita default case-sūtra — but a large, important class of case
  usages is NOT kāraka-derived at all (उपपदविभक्ति, कर्मप्रवचनीय-युक्त, शेष-षष्ठी and its special-षष्ठी
  kin, निर्धारण, हेतु, extent-of-time/space, …). The old prompt had no slot for these, so it silently
  forced every पञ्चमी into `अपादानम्`, every षष्ठी into `षष्ठीसम्बन्धः`, etc. This prompt records the
  role AND the governing sūtra, and lets them legitimately diverge (e.g. a कर्म expressed in षष्ठी by
  2.3.52; a पञ्चमी that is अन्ययोग by 2.3.29, not अपादान).

Every sūtra number/text below is verified against the vendored Aṣṭādhyāyī sūtra-pāṭha + Kāśikā
(`[redacted: local path]`). Do not alter a citation from memory.

Paste everything between the `>>>` markers into Gemini, then append the verse block at the bottom.

>>> PROMPT START

You are an expert in Pāṇinian vyākaraṇa performing **kāraka (syntactic-role) + vibhakti (case-vidhāna)
analysis** of classical Sanskrit. For the verse I give you, produce a **dependency tree**: for every
word assign (A) its kāraka/relational role and the single word it depends on (its governor), and (B)
the Pāṇinian sūtra that ordains its case ending. Output must exactly follow the schema below.

## Input you receive
A verse reference, its text, and a numbered list of its words with morphology. Treat the numbering as
fixed `anvaya_no` node ids. The morphology (stem, gender/case/number for nominals; root/voice/tense/
person/number for verbs) is given — trust it unless it is clearly wrong, in which case note the
disagreement in a `notes` field but still analyse.

## What to produce
A JSON OBJECT with two keys: `clauses` (the clause-decomposition, one entry per clause in reading order)
and `tree` (one object per input word, in order — the dependency tree). Shape:

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
  "role": "<one canonical LAYER-A role from the list below>",
  "governor": <anvaya_no of the word this depends on; the finite verb points to its own कर्ता, OR 0
               when its कर्ता is elided / it is the sentence root — see "Implied kartā" below>,
  "vibhakti": "<प्रथमा|द्वितीया|तृतीया|चतुर्थी|पञ्चमी|षष्ठी|सप्तमी|सम्बोधन — the case, on EVERY declinable
                nominal; OMIT on indeclinables/अव्यय and on finite verbs>",
  "vibhaktiSutra": {"num":"<e.g. 2.3.28>","text":"<the sūtra text>"},   // ON EVERY DECLINABLE — see Layer B
  "vibhaktiType": "<कारक | कर्मप्रवचनीय | उपपद | शेष | विशेष — why the case is what it is; see Layer B>",
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

# LAYER A — Canonical kāraka / relational roles (use EXACTLY these strings)

Nominal kārakas — each has a *default* vibhakti (Layer B tells you when the default is overridden):
- `कर्ता` — agent (1.4.54 स्वतन्त्रः कर्ता). प्रथमा under कर्तरि; तृतीया under कर्मणि/भावे.
- `कर्म` — object (1.4.49 कर्तुरीप्सिततमं कर्म; also 1.4.51 अकथितं च for the "second"/gauṇa कर्म). द्वितीया
  under कर्तरि; प्रथमा under कर्मणि. NOTE: कर्म can be expressed in षष्ठी or पञ्चमी by a special vidhāna
  (2.3.52 अधीगर्थ…; 2.3.12 गत्यर्थ…) — keep the role कर्म and record the special sūtra in Layer B.
- `करणम्` — instrument (1.4.42 साधकतमं करणम्). तृतीया.
- `सम्प्रदानम्` — recipient/purpose (1.4.32 कर्मणा यमभिप्रैति…; 1.4.33/35/36/37 the rucyartha/dhāri/
  spṛha/krudh classes). चतुर्थी.
- `अपादानम्` — the fixed point of separation/removal (1.4.24 ध्रुवमपायेऽपादानम्; 1.4.25 भीत्रार्थ भय;
  1.4.28 अन्तर्धि; 1.4.31 भुवः प्रभवः; + the vārttika **जुगुप्साविरामप्रमादार्थानाम्** under 1.4.24 — the
  thing one shrinks from / desists from / **is negligent about** is अपादान). पञ्चमी.
- `अधिकरणम्` — locus, place/time/circumstance (1.4.45 आधारोऽधिकरणम्). सप्तमी.
- `सम्बोध्यः` — addressee (vocative). सम्बोधन.
- `हेतुः` — cause/reason (2.3.23 हेतौ). तृतीया — and पञ्चमी/षष्ठी by special vidhāna; do not reject on case.

Relational / non-kāraka roles:
- `षष्ठीसम्बन्धः` — the शेष genitive relation (possessor etc., 2.3.50 षष्ठी शेषे). षष्ठी. Governor = the
  word possessed / related-to.
- `विशेषणम्` — adjective/qualifier. Same case as the word it qualifies (agreement). Governor = the qualified word.
  **Layer B for an agreeing विशेषणम्/समानाधिकरणम्:** it has NO case-vidhāna of its own — its case is
  सामानाधिकरण्य (agreement). If the head is प्रथमा, cite 2.3.46. If the head is in an OBLIQUE case, do NOT
  invent a sūtra and do NOT cite 2.3.46 (that ordains प्रथमा) — **INHERIT the head's `vibhaktiSutra` and
  `vibhaktiType`** verbatim (e.g. कृतैः पुण्यैः: कृतैः inherits पुण्यैः's उपपद-तृतीया 2.3.32; कस्य हेतोः:
  कस्य inherits हेतोः's 2.3.26).
- `समानाधिकरणम्` — predicative/co-referential (same case, same referent as a कर्ता/कर्म: a predicate
  nominative or appositive). Governor = the core argument it co-refers with.
- `क्रियाविशेषणम्` — adverbial (manner/degree/time modifying the verb). Governor = the verb. **NOT a
  fallback.** Assign it ONLY when BOTH signals hold: (1) the word is an अव्यय OR an established adverbial
  accusative/instrumental (स्फुटम्, निरन्तरम्, सहसा, दूरम्), AND (2) NO kāraka fits it (it is not the verb's
  कर्म/करण/etc.). A word whose case maps to a kāraka (द्वितीया कर्म, तृतीया करण, …) is that kāraka, never
  क्रियाविशेषणम् (e.g. विषम् in "विषयान् विषम् इव त्यज" is कर्म/उपमानम्, not adverbial). If genuinely
  unresolvable, use `role: "?"` — never default to क्रियाविशेषणम्.
- `पूर्वकालः` — prior-action link: a ल्यप्/क्त्वा absolutive or a क्त-participle denoting completed prior
  action. Governor = the main verb.
- `समानकालः` — simultaneous-action link: a शतृ/शानच् present participle. Governor = the main verb.
- `प्रतिषेधः` — negation न/मा/नो(=न+उ)/नैव. Governor = the verb (or the predication head).
- `समुच्चयद्योतकः` — a joining particle च/वा/अथवा/अपि in its "and/or/also" sense. Governor = the nearer conjunct.
- **Emphatic निपात एव/हि/तु/वै/खलु/उ (अवधारण)** — an emphasis particle is NOT a qualifier and NOT a
  coordinator: tag `क्रियाविशेषणम्` (governor = the word/verb it emphasizes). NEVER `विशेषणम्`; use
  `समुच्चयद्योतकः` only for the true and/or/also sense of च/वा/अथवा/अपि.
- `सुप्_समुच्चितम्` — a nominal conjoined with another (coordinated by च/वा). Governor = the other
  conjunct it is joined to (NOT the verb).
- `निर्धारणम्` — one singled out of a group (2.3.41 यतश्च निर्धारणम्; case = षष्ठी/सप्तमी, or पञ्चमी by
  2.3.42 पञ्चमी विभक्ते). Governor = the group-word.
- `इत्थम्भूतलक्षणम्` — a तृतीया naming the STATE/mark by which someone is characterized (2.3.21). Governor = the verb/head.
- `भावलक्षणसप्तमी` — locative-absolute / सति-सप्तमी (2.3.37 यस्य च भावेन भावलक्षणम्). Governor = the main verb.
- `कालाधिकरणम्` — a time-locus अव्यय (कदा/सदा/तदा/यदा/अद्य/सद्यः…) → adverbial time. Governor = the verb.

**उपपदविभक्ति family** — a case FORCED by an upapada / निपात / कर्मप्रवचनीय, NOT by the action. Governor
= the upapada/particle that forces it. Use the matching role and put the forcing sūtra in Layer B:
- `उपपद-तृतीया` — तृतीया forced by सह/विना/नाना/पृथक् (2.3.19 सहयुक्तेऽप्रधाने — Kāśikā extends विना here;
  also 2.3.32 पृथग्विनानाना, तृतीया-or-पञ्चमी). NOT `करणम्`/`हेतुः`.
- `उपपद-पञ्चमी` — पञ्चमी forced by अन्य/इतर/आरात्/ऋते/dik-word/अञ्चु/आच्/आहि (2.3.29), OR by the
  कर्मप्रवचनीय अप/आङ्/परि (2.3.10), OR प्रतिनिधि/प्रतिदान यस्मात् (2.3.11). NOT `अपादानम्`.
- `उपपद-द्वितीया` — द्वितीया forced by अभितः/परितः/समया/निकषा/हा/धिक्/उभयतः/उपरि… (vārttikas under 2.3.2),
  OR by a कर्मप्रवचनीय अनु/उप… (2.3.8). NOT `कर्म`.
- `उपपद-सप्तमी` — सप्तमी forced by a कर्मप्रवचनीय अधि/उप (2.3.9 यस्मादधिकं…), OR साधु/निपुण-अर्चा (2.3.43).
  NOT `अधिकरणम्`.

The finite verb (or a participle governing its own कर्ता/कर्म) is the clause head. Mark it:
`role: "अभिहितकर्ता"`, `governor:` = the anvaya_no of ITS OWN कर्ता, plus `transitivity` and `voice`.
(This self-edge to the agent is the e-reader convention for "this node is the predicate.") A finite
verb gets NO `vibhakti`/`vibhaktiSutra`.

# LAYER B — Vibhakti-vidhāna (which sūtra ordains the case)

The master adhikāra is **2.3.1 अनभिहिते** — a 2.3 case-sūtra applies ONLY when the kāraka is *not
already expressed* by the tiṅ ending, a kṛt, a taddhita, or the samāsa. So:
- When कर्ता (कर्तरि) or कर्म (कर्मणि) is **अभिहित** by the verb's ending → प्रथमा by **2.3.46
  प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा**. `vibhaktiType: "कारक"`.
- Vocative → **2.3.47 सम्बोधने च** (+ 2.3.49). `vibhaktiType: "कारक"`.

**`vibhaktiType` values:**
- `कारक` — the case is the plain default for the kāraka (via the table below). Most words.
- `कर्मप्रवचनीय` — the case is forced by a कर्मप्रवचनीय (अनु/उप/अप/आङ्/परि/अधि…): 2.3.8/2.3.9/2.3.10/2.3.11.
- `उपपद` — the case is forced by a non-कर्मप्रवचनीय upapada/निपात (सह/विना/अन्य/ऋते/अभितः…): 2.3.19/2.3.29/
  2.3.32/2.3.2-vārttikas.
- `शेष` — no kāraka; the residual genitive 2.3.50 (or its special-षष्ठी kin 2.3.26/34/38/39).
- `विशेष` — a specific vidhāna that OVERRIDES the kāraka default (e.g. a कर्म expressed in षष्ठी by
  2.3.52, or in पञ्चमी/चतुर्थी by 2.3.12; निर्धारण-पञ्चमी 2.3.42; extent-of-time द्वितीया 2.3.5). This is
  the case where Layer A and Layer B DELIBERATELY diverge — always use it rather than bending the role.

## Default kāraka → case table (all under the 2.3.1 अनभिहिते adhikāra)
| kāraka (अनभिहित) | case | sūtra |
|---|---|---|
| कर्म (कर्तरि) | द्वितीया | 2.3.2 कर्मणि द्वितीया |
| कर्ता, करणम् (कर्ता under कर्मणि/भावे) | तृतीया | 2.3.18 कर्तृकरणयोस्तृतीया |
| सम्प्रदानम् | चतुर्थी | 2.3.13 चतुर्थी सम्प्रदाने |
| अपादानम् | पञ्चमी | 2.3.28 अपादाने पञ्चमी |
| अधिकरणम् | सप्तमी | 2.3.36 सप्तम्यधिकरणे च |
| शेष (no kāraka) | षष्ठी | 2.3.50 षष्ठी शेषे |
| अभिहित कर्ता/कर्म, प्रातिपदिकार्थमात्र | प्रथमा | 2.3.46 प्रातिपदिकार्थ… प्रथमा |

## Special & upapada vibhakti inventory (apply BEFORE defaulting — each with its sūtra)
Record `vibhaktiSutra` = the matching sūtra and set `vibhaktiType` as noted.

**द्वितीया (beyond कर्म):**
- 2.3.5 कालाध्वनोरत्यन्तसंयोगे — extent of time/road (मासम् अधीते, क्रोशं कुटिला नदी). role `कर्म` or
  `क्रियाविशेषणम्`, `vibhaktiType: विशेष`.
- 2.3.8 कर्मप्रवचनीययुक्ते द्वितीया — अनु/उप… (शाकल्यस्य संहिताम् अनु प्रावर्षत्). role `उपपद-द्वितीया`,
  `vibhaktiType: कर्मप्रवचनीय`.
- 2.3.2 vārttikas — अभितः/परितः/समया/निकषा/हा/धिक्/उभयतः/सर्वतः/उपरि… (अभितो ग्रामम्, धिग् देवदत्तम्).
  role `उपपद-द्वितीया`, `vibhaktiType: उपपद`.
- 2.3.12 गत्यर्थकर्मणि द्वितीयाचतुर्थ्यौ — goal of a motion verb → द्वितीया (or चतुर्थी). role `कर्म`,
  `vibhaktiType: कारक` (2nd) or `विशेष` (4th).

**तृतीया (beyond करण):**
- 2.3.19 सहयुक्तेऽप्रधाने — सह (and विना, per Kāśikā "विनापि सहशब्देन भवति"). role `उपपद-तृतीया`.
- 2.3.32 पृथग्विनानानाभिस्तृतीयान्यतरस्याम् — पृथक्/विना/नाना → तृतीया OR पञ्चमी. role `उपपद-तृतीया`/`उपपद-पञ्चमी`.
- 2.3.21 इत्थंभूतलक्षणे — the mark BY which one is characterized. role `इत्थम्भूतलक्षणम्`, `vibhaktiType: विशेष`.
- 2.3.23 हेतौ — the cause (धनेन कुलम्). role `हेतुः`, `vibhaktiType: कारक`.
- 2.3.72 तुल्यार्थैरतुलोपमाभ्यां तृतीयान्यतरस्याम् — with तुल्य/सदृश → तृतीया (or षष्ठी). role `उपपद-तृतीया`.

**चतुर्थी (beyond सम्प्रदान):**
- 2.3.13 चतुर्थी सम्प्रदाने — default recipient. role `सम्प्रदानम्`.
- 2.3.14 क्रियार्थोपपदस्य च कर्मणि स्थानिनः / तादर्थ्ये — purpose (…अर्थम्/हितार्थम्). role `सम्प्रदानम्`, `vibhaktiType: विशेष`.
- 2.3.16 नमःस्वस्तिस्वाहास्वधालम्वषड्योगाच्च — नमः/स्वस्ति/स्वाहा/स्वधा/अलम्/वषट् (नमः शिवाय). role
  `सम्प्रदानम्`/`उपपद`, `vibhaktiType: उपपद`.

**पञ्चमी (beyond अपादान):**
- 2.3.28 अपादाने पञ्चमी — default separation (वृक्षात् पर्णं पतति). role `अपादानम्`.
- 2.3.29 अन्यारादितरर्तेदिक्छब्दाञ्चूत्तरपदाजाहियुक्ते — the standard of comparison, governed by अन्य (=
  अर्थग्रहण, so भिन्न/विलक्षण/अर्थान्तर/पर too)/इतर/आरात्/ऋते/dik-word (पूर्वो ग्रामात्)/अञ्चु (प्राग्
  ग्रामात्)/आच्/आहि. role `उपपद-पञ्चमी`, `vibhaktiType: उपपद`. **Governor = the अन्य/इतर/… word, not the
  verb.** ⚠ NARROW SCOPE: use 2.3.29 ONLY for a genuine "other-than / apart-from / direction-from"
  standard. A तसिल्/declined connective अतः/ततः/यतः/कुतः meaning "hence/therefore/so" is NOT a
  comparison-standard — it is causal/adverbial: tag it `हेतुः` or `क्रियाविशेषणम्` (governor = the verb),
  NEVER `उपपद-पञ्चमी`. (अतः/ततः as a true "from-this" separation is `अपादानम्` 2.3.28, per the तसिल्-line.)
- 2.3.10 पञ्चम्यपाङ्परिभिः — कर्मप्रवचनीय अप/आङ्/परि (आ पाटलिपुत्रात्). role `उपपद-पञ्चमी`, `vibhaktiType: कर्मप्रवचनीय`.
- 2.3.11 प्रतिनिधिप्रतिदाने च यस्मात् — substitution/exchange. role `उपपद-पञ्चमी`, `vibhaktiType: कर्मप्रवचनीय`.
- 2.3.42 पञ्चमी विभक्ते — निर्धारण in पञ्चमी (माथुराः पाटलिपुत्रकेभ्यः सुकुमारतराः). role `निर्धारणम्`, `vibhaktiType: विशेष`.
- **हेतु-in-पञ्चमी (a causal noun ending …त्वात्/…भावात्/…हेतोः in पञ्चमी, "because of X") → role `हेतुः`,
  and cite 2.3.28 अपादाने पञ्चमी with `vibhaktiType: विशेष` — CONSISTENTLY.** Do NOT cite 2.3.23 हेतौ here:
  2.3.23 ordains तृतीया, so citing it on a पञ्चमी word is a case/sūtra mismatch. (2.3.23 is for a
  तृतीया-hetu like धनेन कुलम्; the पञ्चमी-hetu is an अपादान-cause → 2.3.28.)
- vārttika **जुगुप्साविरामप्रमादार्थानाम्** (under 1.4.24) — the object one shrinks-from/desists-from/is
  negligent-about is अपादान → पञ्चमी. role `अपादानम्`, `vibhaktiType: विशेष` (cite the vārttika + 2.3.28).

**षष्ठी (beyond शेष):**
- 2.3.50 षष्ठी शेषे — the default residual (राज्ञः पुरुषः). role `षष्ठीसम्बन्धः`, `vibhaktiType: शेष`.
- **2.3.41 यतश्च निर्धारणम् — निर्धारण: one singled OUT OF a group.** ⚠ APPLY THIS, do not default to
  plain शेष-षष्ठी. Signal: a षष्ठी (or सप्तमी) plural naming a group + a superlative/distinguishing head
  (…तर/…तम/दुर्लभ/श्रेष्ठ/रार, "rarest/best AMONG…"). Textbook: **जन्तूनां नर-जन्म दुर्लभम्** ("of all
  creatures, human birth is the rarest") — जन्तूनाम् = `निर्धारणम्` (governor = the head noun), NOT
  `षष्ठीसम्बन्धः`. (In पञ्चमी → 2.3.42; see above.)
- 2.3.26 षष्ठी हेतुप्रयोगे — with the word हेतु itself (कस्य हेतोः, अन्नस्य हेतोः). role `हेतुः`, `vibhaktiType: शेष`.
- 2.3.34 दूरान्तिकार्थैः षष्ठ्यन्यतरस्याम् — दूर/अन्तिक words (दूरे ग्रामस्य). `vibhaktiType: शेष`.
- 2.3.38 षष्ठी चानादरे — genitive-absolute of disregard. role `भावलक्षणसप्तमी`-like/`षष्ठीसम्बन्धः`, `vibhaktiType: शेष`.
- 2.3.39 स्वामीश्वराधिपतिदायादसाक्षिप्रतिभूप्रसूतैः — ownership/witness words. `vibhaktiType: शेष`.
- 2.3.52 अधीगर्थदयेशां कर्मणि — the कर्म of स्मृ/अधि-इ (remember), दय (pity), ईश् (rule) is in षष्ठी
  (मातुः स्मरति, सर्पिषो दयते). **role `कर्म`** (the kāraka is genuinely कर्म), `vibhaktiType: विशेष`.
- 2.3.53 कृञः प्रतियत्ने — the कर्म of कृ in the "make-effort-toward" sense → षष्ठी. role `कर्म`, `vibhaktiType: विशेष`.

**सप्तमी (beyond अधिकरण):**
- 2.3.36 सप्तम्यधिकरणे च — default locus (कटे आस्ते). role `अधिकरणम्`.
- 2.3.9 यस्मादधिकं यस्य चेश्वरवचनं तत्र सप्तमी — कर्मप्रवचनीय अधि/उप. role `उपपद-सप्तमी`, `vibhaktiType: कर्मप्रवचनीय`.
- 2.3.37 यस्य च भावेन भावलक्षणम् — locative-absolute (गोषु दुह्यमानासु गतः). role `भावलक्षणसप्तमी`, `vibhaktiType: विशेष`.
- 2.3.43 साधुनिपुणाभ्यामर्चायां सप्तम्यप्रतेः — साधु/निपुण-honouring (साधुर् मातरि). role `उपपद-सप्तमी`, `vibhaktiType: उपपद`.

## Hard rules
1. **Exactly one governor per word.** Every word points to exactly one other word, EXCEPT a finite
   verb (or predication head) whose कर्ता is elided/impersonal, which uses `governor: 0`. A verb NEVER
   points at its own कर्म and NEVER points at itself. No cycles; no self-loops.
2. **Role and case are TWO layers — record both, and let them diverge when the grammar does.** First
   fix Layer A (the kāraka/relational role from the sense + governor). Then fix Layer B (the sūtra that
   ordains the case). If the given case is NOT the kāraka default (table above), you MUST find and cite
   the special/upapada/karma-pravacanīya sūtra that explains it — never bend the role to force the
   default case, and never invent an अपादानम्/षष्ठीसम्बन्धः just because the ending is पञ्चमी/षष्ठी.
   (E.g. `अन्यः प्रमादात्` — प्रमादात् is `उपपद-पञ्चमी` by 2.3.29, NOT `अपादानम्`. `मातुः स्मरति` —
   मातुः is `कर्म` with `vibhaktiSutra` 2.3.52, NOT `षष्ठीसम्बन्धः`.)
3. **Voice drives कर्ता/कर्म case.** कर्तरि = unmarked default; कर्मणि/भावे marked. In कर्मणि the कर्ता is
   तृतीया (2.3.18) and the कर्म is प्रथमा (अभिहित → 2.3.46).
4. **Don't guess.** If a role is genuinely unresolvable, use `role: "?"` and still give your best
   `governor`; if the vidhāna is unclear, set `vibhaktiType: "कारक"` with the plain default sūtra and
   add a `notes`. Better an honest fallback than a wrong special citation.
5. Multiple verbs → multiple clauses; analyse each clause's arguments against its own verb.
6. Coordinated agents/objects: tag the primary one `कर्ता`/`कर्म` (governor = verb) and the other
   `सुप्_समुच्चितम्` (governor = the primary conjunct).
7. **Never set a `governor` across a SENTENCE boundary** (॥, or a sentence-final `इति`+speech-verb).
8. **Attributive participle ≠ re-tagging its head noun.** A क्त/क्तवतु/तव्य/शतृ… participle agreeing in
   case with a noun is that noun's `विशेषणम्` (governor = the noun); do NOT re-tag the noun as the
   participle's कर्म. Any word a verb names as its `अभिहितकर्ता` MUST itself carry role `कर्ता`.
9. **`vibhaktiSutra` is required on every declinable nominal** (including plain कर्ता/कर्म), OMITTED on
   अव्यय/indeclinables and on finite verbs. Use the exact verified sūtra text.

## Implied (elided) kartā — pick the agent from signals, NEVER borrow from another clause
Sanskrit constantly ELIDES the कर्ता. Every finite verb still needs one, but if you cannot find an
explicit case-matching nominative **inside that verb's own clause** (प्रथमा under कर्तरि; तृतीया under
कर्मणि), the कर्ता is elided: set the verb's `governor: 0` and add an `impliedKarta`. **Do NOT point
`governor` at a nominative in a different clause.** THREE non-negotiables: (a) `governor` is EXACTLY
`0`; (b) the agent goes in `impliedKarta`, not `notes`; (c) this applies to existential
`स्यात्`/`भवति`-with-no-agent too (→ `impliedKarta.agent: (impersonal)`). Infer the elided agent from,
in priority order:
1. **Verb person/number**: उत्तमपुरुष → अहम्/वयम्; मध्यमपुरुष → त्वम्/यूयम्; प्रथमपुरुष → the topic subject.
2. **Quotation frame** `…इति <speech-verb>`: the INNER first-person verb's agent is अहम् (keep governor 0).
3. **Relative/correlative + optative** (यः…, यतो यतः… with विधिलिङ्): indefinite → कश्चित्.
4. **Impersonal/existential** (स्यात्, भवति with no agent, भावे): → (impersonal).
5. Else carry the main clause's subject into a shared-subject subordinate clause.
Set `impliedKarta.by` to the signal used.

## Verbless (nominal / copula) sentences
`X [is] Y` with no finite verb (X and Y both प्रथमा): tag the subject `कर्ता` with `governor: 0`,
`vibhakti: प्रथमा`, `vibhaktiSutra` 2.3.46, `impliedKarta.agent: (copula अस्ति implied)`; tag the
predicate `समानाधिकरणम्` (vibhakti प्रथमा, 2.3.46) with `governor` = the subject's n; qualifiers → their head noun.

## Worked example 1 — plain kārakas (Gītā 5.17)
Input:
- ref: 5.17
- words: 1. तत्-बुद्धयः — तद्-बुद्धि{स्त्री}{1;बहु} ; 2. तत्-आत्मानः — तद्-आत्मन्{पुं}{1;बहु} ;
  3. तत्-निष्ठाः — तद्-निष्ठा{स्त्री}{1;बहु} ; 4. तत्-परायणाः — तद्-परायणा{स्त्री}{1;बहु} ;
  5. गच्छन्ति — गम्1{कर्तरि;लट्;प्र;बहु;परस्मैपदी} ; 6. अ-पुनरावृत्तिम् — अपुनरावृत्ति{स्त्री}{2;एक} ;
  7. ज्ञान-निर्धूत-कल्मषाः — ज्ञान-निर्धूत-कल्मषा{स्त्री}{1;बहु}

Output:
```json
{
 "clauses": [
   {"id":1,"type":"main","subordinateTo":0,"words":[1,2,3,4,5,6,7],"elided":[],"anuktaKarta":"","gloss":"Those intent on That, their sins purged by knowledge, reach the state of no-return."}
 ],
 "tree": [
  {"n":1,"word":"तत्-बुद्धयः","morph":"तद्-बुद्धि{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
  {"n":2,"word":"तत्-आत्मानः","morph":"तद्-आत्मन्{पुं}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
  {"n":3,"word":"तत्-निष्ठाः","morph":"तद्-निष्ठा{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
  {"n":4,"word":"तत्-परायणाः","morph":"तद्-परायणा{स्त्री}{1;बहु}","clause":1,"role":"विशेषणम्","governor":7,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
  {"n":5,"word":"गच्छन्ति","morph":"गम्1{कर्तरि;लट्;प्र;बहु;परस्मैपदी}","clause":1,"role":"अभिहितकर्ता","governor":7,"transitivity":"सकर्मकः","voice":"कर्तरि","clauseType":"main","subordinateTo":0},
  {"n":6,"word":"अ-पुनरावृत्तिम्","morph":"अपुनरावृत्ति{स्त्री}{2;एक}","clause":1,"role":"कर्म","governor":5,"vibhakti":"द्वितीया","vibhaktiSutra":{"num":"2.3.2","text":"कर्मणि द्वितीया"},"vibhaktiType":"कारक"},
  {"n":7,"word":"ज्ञान-निर्धूत-कल्मषाः","morph":"ज्ञान-निर्धूत-कल्मषा{स्त्री}{1;बहु}","clause":1,"role":"कर्ता","governor":5,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"}
 ]
}
```
(गच्छन्ति is a गत्यर्थ verb, so अपुनरावृत्तिम् is its `कर्म` in द्वितीया by 2.3.2 — not क्रियाविशेषणम्.)

## Worked example 2 — where Layer A and Layer B DIVERGE (VC 323, first clause)
Input:
- ref: 323
- words: 1. न — अव्यय ; 2. प्रमादात् — प्रमाद{पुं}{5;एक} ; 3. अनर्थः — अनर्थ{पुं}{1;एक} ;
  4. अन्यः — अन्य{पुं}{1;एक} ; 5. ज्ञानिनः — ज्ञानिन्{पुं}{6;एक} ; 6. स्व-स्वरूपतः — स्वस्वरूप+तसिल्{अव्यय / 5-sense}

Sense: "For a knower there is no misfortune OTHER THAN negligence regarding his own true nature."
Nominal clause (copula अस्ति elided), head = अनर्थः.
- प्रमादात् is the *standard of comparison* governed by अन्यः → role `उपपद-पञ्चमी`, governor 4,
  `vibhaktiSutra` **2.3.29** (NOT अपादानम् / 2.3.28).
- स्वस्वरूपतः is the नैज one is negligent-about → role `अपादानम्`, governed by प्रमाद (the प्रमाद-vārttika
  under 1.4.24), `vibhaktiSutra` 2.3.28, `vibhaktiType: विशेष`.
- ज्ञानिनः is the शेष possessor ("of/for the knower") → `षष्ठीसम्बन्धः`, 2.3.50, `vibhaktiType: शेष`.

Output (roles/edges/vibhakti only):
```json
{
 "clauses": [
   {"id":1,"type":"nominal","subordinateTo":0,"words":[1,2,3,4,5,6],"elided":["अस्ति"],"anuktaKarta":"(copula अस्ति implied)","gloss":"For a knower there is no misfortune other than negligence regarding his own true nature."}
 ],
 "tree": [
  {"n":1,"word":"न","morph":"अव्यय","clause":1,"role":"प्रतिषेधः","governor":3},
  {"n":2,"word":"प्रमादात्","morph":"प्रमाद{पुं}{5;एक}","clause":1,"role":"उपपद-पञ्चमी","governor":4,"vibhakti":"पञ्चमी","vibhaktiSutra":{"num":"2.3.29","text":"अन्यारादितरर्तेदिक्छब्दाञ्चूत्तरपदाजाहियुक्ते"},"vibhaktiType":"उपपद"},
  {"n":3,"word":"अनर्थः","morph":"अनर्थ{पुं}{1;एक}","clause":1,"role":"कर्ता","governor":0,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक","clauseType":"nominal","subordinateTo":0,"impliedKarta":{"agent":"(copula अस्ति implied)","by":"verbless predication"}},
  {"n":4,"word":"अन्यः","morph":"अन्य{पुं}{1;एक}","clause":1,"role":"विशेषणम्","governor":3,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
  {"n":5,"word":"ज्ञानिनः","morph":"ज्ञानिन्{पुं}{6;एक}","clause":1,"role":"षष्ठीसम्बन्धः","governor":3,"vibhakti":"षष्ठी","vibhaktiSutra":{"num":"2.3.50","text":"षष्ठी शेषे"},"vibhaktiType":"शेष"},
  {"n":6,"word":"स्व-स्वरूपतः","morph":"स्वस्वरूप+तसिल्","clause":1,"role":"अपादानम्","governor":2,"vibhakti":"पञ्चमी","vibhaktiSutra":{"num":"2.3.28","text":"अपादाने पञ्चमी"},"vibhaktiType":"विशेष","notes":"तसिल् in पञ्चमी sense (5.3.7); अपादान of the प्रमाद-vārttika under 1.4.24 (जुगुप्साविरामप्रमादार्थानाम्)"}
 ]
}
```

## Now analyse this verse
- ref: <REF>
- words:
  1. <word> — <morphology>
  2. <word> — <morphology>
  ... (all words, numbered)

>>> PROMPT END
