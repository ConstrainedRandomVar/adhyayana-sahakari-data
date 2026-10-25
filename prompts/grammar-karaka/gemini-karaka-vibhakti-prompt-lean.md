# Gemini prompt — kāraka + vibhakti analysis (LEAN bulk edition)

Leaner twin of `gemini-karaka-vibhakti-prompt.md` for bulk runs: identical ruleset + full vibhakti
inventory + the one divergence example, prose compressed and the redundant plain worked-example dropped.
Every sūtra is verified against the vendored Aṣṭādhyāyī sūtra-pāṭha + Kāśikā — do not alter from memory.

>>> PROMPT START

You are an expert in Pāṇinian vyākaraṇa. For each verse, produce a dependency tree assigning every word
(A) its **kāraka/relational role** + the one word it depends on (governor), and (B) the **sūtra that
ordains its case**. The case usually follows from the kāraka via the anabhihita default — but a large
class of cases is NOT kāraka-derived (उपपदविभक्ति, कर्मप्रवचनीय, शेष-षष्ठी + kin, निर्धारण, हेतु, extent).
Record role AND governing sūtra, and let them DIVERGE when the grammar does (a कर्म in षष्ठी by 2.3.52;
a पञ्चमी that is anya-yoge 2.3.29, not अपादान).

## Input
A ref + numbered words with morphology (stem·case·number·gender for nominals; root·voice·लकार·person·
number·pada for verbs). Numbering = fixed `anvaya_no`. Trust the given morph unless clearly wrong (then
note it) — √? means the root lemma is unknown; infer it.

## Output — JSON only, one node per word, numbering kept
```
{"clauses":[{"id":<int>,"type":"main|nominal|relative|correlative|quotation|subordinate","subordinateTo":<id|0>,
   "words":[<anvaya_no…>],"elided":["<supplied word(s); [] if none>"],"anuktaKarta":"<elided agent or ''>",
   "gloss":"<one-line English>"}],
 "tree":[{"n":<int>,"word":"<surface>","morph":"<given/corrected>","clause":<id>,
   "role":"<one Layer-A role>","governor":<anvaya_no this depends on; finite verb → its own कर्ता, or 0 if कर्ता elided/root>",
   "vibhakti":"<प्रथमा|द्वितीया|…|सप्तमी|सम्बोधन — on EVERY declinable; OMIT on अव्यय & finite verbs>",
   "vibhaktiSutra":{"num":"<e.g. 2.3.28>","text":"<sūtra text>"},   // on EVERY declinable
   "vibhaktiType":"<कारक|कर्मप्रवचनीय|उपपद|शेष|विशेष>",
   "transitivity":"<सकर्मकः|अकर्मकः — finite verbs only>","voice":"<कर्तरि|कर्मणि|भावे — verbs only>",
   "clauseType":"<… — clause HEAD only>","subordinateTo":<id|0 — head only>,
   "impliedKarta":{"agent":"<अहम्/त्वम्/कश्चित्/तत्/(impersonal)/(copula अस्ति implied)>","by":"<signal>"},  // elided-कर्ता head only
   "notes":"<only if deviating/unsure>"}]}
```
Return ONLY the JSON. For multiple verses return a JSON ARRAY of `{"ref",...,"clauses","tree"}`.

## Clauses
Tag each word's `clause` (1,2,… in reading order). A clause = one finite verb (or one verbless "X[is]Y")
+ its dependents, bounded by daṇḍas ।/॥, relative–correlative joints (यत्…तत्, यथा…तथा), quotation इति.
Gerunds/participles (ल्यप्/क्त्वा/शतृ/क्त) are NOT own clauses. On the HEAD only give `clauseType` +
`subordinateTo`. A governor crosses a clause boundary ONLY for a subordinate HEAD → the clause it
modifies; ordinary कारक words attach within their clause; NEVER cross a SENTENCE boundary (॥ / final इति).

# LAYER A — roles (exact strings)
Kārakas (default case in parens): `कर्ता` agent (1.4.54; प्रथमा कर्तरि / तृतीया कर्मणि) · `कर्म` object
(1.4.49; द्वितीया कर्तरि / प्रथमा कर्मणि — but षष्ठी/पञ्चमी by special vidhāna, keep role कर्म) · `करणम्`
instrument (1.4.42; तृतीया) · `सम्प्रदानम्` recipient/purpose (1.4.32; चतुर्थी) · `अपादानम्` separation
point (1.4.24; पञ्चमी — incl. the vārttika जुगुप्साविरामप्रमादार्थानाम्: the thing one shrinks-from/
desists-from/is-negligent-about) · `अधिकरणम्` locus (1.4.45; सप्तमी) · `सम्बोध्यः` vocative · `हेतुः`
cause (2.3.23; तृतीया/पञ्चमी).
Relational: `षष्ठीसम्बन्धः` शेष genitive (2.3.50) · `विशेषणम्` qualifier (agrees; governor = qualified
word) · `समानाधिकरणम्` predicative co-referential · `क्रियाविशेषणम्` adverbial (gov = verb) — **NOT a
fallback: assign ONLY if (1) अव्यय or an established adverbial acc./instr. (स्फुटम्/निरन्तरम्/सहसा) AND
(2) no kāraka fits; a case that maps to a kāraka (द्वितीया→कर्म, तृतीया→करण) IS that kāraka; if unresolvable use `?`** · `पूर्वकालः`
ल्यप्/क्त्वा/क्त prior action (gov = main verb) · `समानकालः` शतृ/शानच् (gov = main verb) · `प्रतिषेधः`
न/मा/नो/नैव (gov = verb) · `समुच्चयद्योतकः` च/वा/अथवा joiner ("and/or/also") · **emphatic निपात एव/हि/तु/
वै/खलु/उ = अवधारण → `क्रियाविशेषणम्` (gov = the emphasized word/verb); NEVER `विशेषणम्`, and NOT
`समुच्चयद्योतकः`** · `सुप्_समुच्चितम्` conjoined nominal (gov =
other conjunct) · `निर्धारणम्` one singled out of a group (2.3.41) · `इत्थम्भूतलक्षणम्` (2.3.21) ·
`भावलक्षणसप्तमी` locative-absolute (2.3.37) · `कालाधिकरणम्` time-अव्यय.
**उपपदविभक्ति family** (case FORCED by an upapada/निपात/कर्मप्रवचनीय; governor = that word):
`उपपद-तृतीया` (सह/विना/नाना/पृथक्) · `उपपद-पञ्चमी` (अन्य/इतर/आरात्/ऋते/dik/अप-आङ्-परि) · `उपपद-द्वितीया`
(अभितः/परितः… / अनु-उप) · `उपपद-सप्तमी` (अधि-उप / साधु-निपुण).
Finite verb / predication head: `role:"अभिहितकर्ता"`, governor = its own कर्ता (or 0 if elided), +
`transitivity`+`voice`; no vibhakti.
**Agreeing विशेषणम्/समानाधिकरणम् — Layer B:** no case-vidhāna of its own. If head is प्रथमा cite 2.3.46;
if head is OBLIQUE, do NOT invent one / do NOT cite 2.3.46 — **INHERIT the head's `vibhaktiSutra`+`vibhaktiType`**.

# LAYER B — vibhakti-vidhāna (which sūtra ordains the case)
Master adhikāra **2.3.1 अनभिहिते**: a 2.3 case-sūtra applies only when the kāraka is NOT already expressed
by the tiṅ/kṛt/taddhita/samāsa. So an **अभिहित** कर्ता(कर्तरि)/कर्म(कर्मणि) → प्रथमा by **2.3.46
प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा**; vocative → **2.3.47 सम्बोधने च**.
`vibhaktiType`: `कारक` (plain default) · `कर्मप्रवचनीय` (2.3.8/9/10/11) · `उपपद` (सह/विना/अन्य/ऋते/अभितः…)
· `शेष` (2.3.50 + kin) · `विशेष` (a vidhāna OVERRIDING the default — use this when Layer A ≠ default case).

**Default kāraka→case (all under 2.3.1):** कर्म कर्तरि → द्वितीया **2.3.2** · कर्ता(कर्मणि)/करणम् → तृतीया
**2.3.18** · सम्प्रदानम् → चतुर्थी **2.3.13** · अपादानम् → पञ्चमी **2.3.28** · अधिकरणम् → सप्तमी **2.3.36**
· शेष → षष्ठी **2.3.50** · अभिहित/प्रातिपदिकार्थमात्र → प्रथमा **2.3.46**.

**Special & upapada inventory (apply BEFORE defaulting):**
- द्वितीया: 2.3.5 कालाध्वनोरत्यन्तसंयोगे (extent of time/road; role कर्म/क्रियाविशेषणम्, विशेष) · 2.3.8
  कर्मप्रवचनीययुक्ते द्वितीया (अनु/उप; उपपद-द्वितीया, कर्मप्रवचनीय) · 2.3.2-vārt अभितः/परितः/समया/निकषा/हा/
  धिक्/उभयतः/सर्वतः (उपपद-द्वितीया, उपपद) · 2.3.12 गत्यर्थकर्मणि द्वितीयाचतुर्थ्यौ (goal of motion; कर्म).
- तृतीया: 2.3.18 कर्तृकरणयोस्तृतीया · 2.3.19 सहयुक्तेऽप्रधाने (सह, and विना per Kāśikā; उपपद-तृतीया) ·
  2.3.32 पृथग्विनानानाभिस्तृतीयाऽन्यतरस्याम् (पृथक्/विना/नाना → तृतीया or पञ्चमी) · 2.3.21 इत्थंभूतलक्षणे
  (इत्थम्भूतलक्षणम्, विशेष) · 2.3.23 हेतौ (हेतुः) · 2.3.72 तुल्यार्थैः… (तुल्य/सदृश → तृतीया or षष्ठी).
- चतुर्थी: 2.3.13 चतुर्थी सम्प्रदाने · 2.3.14 क्रियार्थोपपदस्य…/तादर्थ्ये (purpose; विशेष) · 2.3.16
  नमःस्वस्तिस्वाहास्वधालम्वषड्योगाच्च (नमः/स्वस्ति…; उपपद).
- पञ्चमी: 2.3.28 अपादाने पञ्चमी · **2.3.29 अन्यारादितरर्तेदिक्छब्दाञ्चूत्तरपदाजाहियुक्ते** — comparison-
  standard with अन्य (=अर्थग्रहण, so भिन्न/विलक्षण/अर्थान्तर/पर)/इतर/आरात्/ऋते/dik (पूर्वो ग्रामात्)/अञ्चु
  (प्राग् ग्रामात्)/आच्/आहि; **governor = the अन्य/इतर/… word**; role उपपद-पञ्चमी, उपपद. ⚠ NARROW: a तसिल्/
  connective अतः/ततः/यतः/कुतः meaning "hence/therefore" is NOT a standard — tag हेतुः/क्रियाविशेषणम् (gov =
  verb), never उपपद-पञ्चमी. · 2.3.10 पञ्चम्यपाङ्परिभिः (अप/आङ्/परि; कर्मप्रवचनीय) · 2.3.11 प्रतिनिधिप्रतिदाने
  च यस्मात् (कर्मप्रवचनीय) · 2.3.42 पञ्चमी विभक्ते (निर्धारण; विशेष) · **हेतु-in-पञ्चमी** (causal …त्वात्/
  …भावात्/…हेतोः "because of X") → role हेतुः, cite **2.3.28** (विशेष), NEVER 2.3.23 (that ordains तृतीया).
- षष्ठी: 2.3.50 षष्ठी शेषे · **2.3.41 यतश्च निर्धारणम्** — one singled OUT OF a group (षष्ठी/सप्तमी plural
  + superlative/distinguishing head): **जन्तूनां नर-जन्म दुर्लभम्** → जन्तूनाम् = निर्धारणम् (gov = head),
  NOT षष्ठीसम्बन्धः. · 2.3.26 षष्ठी हेतुप्रयोगे (with the word हेतु; कस्य हेतोः) · 2.3.34 दूरान्तिकार्थैः ·
  2.3.38 षष्ठी चानादरे · 2.3.39 स्वामीश्वराधिपति… (ownership) · **2.3.52 अधीगर्थदयेशां कर्मणि** — the कर्म
  of स्मृ/अधि-इ/दय/ईश् is षष्ठी (मातुः स्मरति): **role कर्म**, विशेष · 2.3.53 कृञः प्रतियत्ने (कर्म, विशेष).
- सप्तमी: 2.3.36 सप्तम्यधिकरणे च · 2.3.9 यस्मादधिकं… (कर्मप्रवचनीय अधि/उप; उपपद-सप्तमी) · 2.3.37 यस्य च
  भावेन भावलक्षणम् (locative-absolute; भावलक्षणसप्तमी, विशेष) · 2.3.43 साधुनिपुणाभ्याम्… (उपपद-सप्तमी).

## Hard rules
1. Exactly one governor per word, EXCEPT a finite verb with elided कर्ता → `governor:0`. No cycles/self-loops.
2. **Role and case are two layers — record both, let them diverge.** Fix role from sense+governor; then
   fix the case-sūtra. If the case ≠ the kāraka default, FIND the special/upapada/कर्मप्रवचनीय sūtra —
   never bend the role to force the default, never invent अपादानम्/षष्ठीसम्बन्धः just because the ending
   is पञ्चमी/षष्ठी. (अन्यः प्रमादात् → उपपद-पञ्चमी 2.3.29; मातुः स्मरति → कर्म w/ 2.3.52.)
3. Voice drives कर्ता/कर्म case: in कर्मणि, कर्ता तृतीया (2.3.18), कर्म प्रथमा (अभिहित, 2.3.46).
4. Don't guess: unresolvable role → `"?"` w/ best governor; unclear vidhāna → `कारक` + the plain default + a note.
5. Multiple verbs → multiple clauses; analyse each against its own verb.
6. Coordinated: primary = कर्ता/कर्म (gov=verb), other = सुप्_समुच्चितम् (gov=primary conjunct).
7. An अभिहितकर्ता target MUST itself be role कर्ता. An attributive क्त/शतृ agreeing with a noun is that
   noun's विशेषणम् (gov=noun) — don't re-tag the noun as the participle's कर्म.
8. `vibhaktiSutra` required on every declinable (incl. plain कर्ता/कर्म); omit on अव्यय & finite verbs; use exact sūtra text.

## Implied (elided) kartā
If no case-matching nominative in the verb's OWN clause (प्रथमा कर्तरि / तृतीया कर्मणि), the कर्ता is
elided: `governor:0` + `impliedKarta`. Never point governor at a nominative in another clause. Signals
(priority): उत्तम→अहम्/वयम्, मध्यम→त्वम्/यूयम्, प्रथम→topic; quotation …इति → inner 1st-person = अहम्;
relative+optative (यः…, विधिलिङ्) → कश्चित्; existential स्यात्/भवति-no-agent/भावे → (impersonal); else
carry main-clause subject. Verbless X[is]Y: subject = कर्ता gov 0, प्रथमा 2.3.46, impliedKarta (copula
अस्ति implied); predicate = समानाधिकरणम् (प्रथमा 2.3.46) gov=subject.

## Worked example — Layer A ≠ Layer B (VC 323, first clause)
Input: 1.न—अव्यय 2.प्रमादात्—प्रमाद{पुं}{5;एक} 3.अनर्थः—अनर्थ{पुं}{1;एक} 4.अन्यः—अन्य{पुं}{1;एक}
5.ज्ञानिनः—ज्ञानिन्{पुं}{6;एक} 6.स्व-स्वरूपतः—स्वस्वरूप+तसिल्
Sense: "For a knower there is no misfortune OTHER THAN negligence regarding his own true nature." Nominal
clause (copula elided), head अनर्थः. प्रमादात् = comparison-standard governed by अन्यः → उपपद-पञ्चमी 2.3.29
(NOT अपादान). स्वस्वरूपतः = what one is negligent-about → अपादानम् (प्रमाद-vārttika) 2.3.28 विशेष.
```json
{"ref":"323","clauses":[{"id":1,"type":"nominal","subordinateTo":0,"words":[1,2,3,4,5,6],"elided":["अस्ति"],"anuktaKarta":"(copula अस्ति implied)","gloss":"For a knower there is no misfortune other than negligence regarding his own nature."}],
 "tree":[
 {"n":1,"word":"न","morph":"अव्यय","clause":1,"role":"प्रतिषेधः","governor":3},
 {"n":2,"word":"प्रमादात्","morph":"प्रमाद{पुं}{5;एक}","clause":1,"role":"उपपद-पञ्चमी","governor":4,"vibhakti":"पञ्चमी","vibhaktiSutra":{"num":"2.3.29","text":"अन्यारादितरर्तेदिक्छब्दाञ्चूत्तरपदाजाहियुक्ते"},"vibhaktiType":"उपपद"},
 {"n":3,"word":"अनर्थः","morph":"अनर्थ{पुं}{1;एक}","clause":1,"role":"कर्ता","governor":0,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक","clauseType":"nominal","subordinateTo":0,"impliedKarta":{"agent":"(copula अस्ति implied)","by":"verbless predication"}},
 {"n":4,"word":"अन्यः","morph":"अन्य{पुं}{1;एक}","clause":1,"role":"विशेषणम्","governor":3,"vibhakti":"प्रथमा","vibhaktiSutra":{"num":"2.3.46","text":"प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा"},"vibhaktiType":"कारक"},
 {"n":5,"word":"ज्ञानिनः","morph":"ज्ञानिन्{पुं}{6;एक}","clause":1,"role":"षष्ठीसम्बन्धः","governor":3,"vibhakti":"षष्ठी","vibhaktiSutra":{"num":"2.3.50","text":"षष्ठी शेषे"},"vibhaktiType":"शेष"},
 {"n":6,"word":"स्व-स्वरूपतः","morph":"स्वस्वरूप+तसिल्","clause":1,"role":"अपादानम्","governor":2,"vibhakti":"पञ्चमी","vibhaktiSutra":{"num":"2.3.28","text":"अपादाने पञ्चमी"},"vibhaktiType":"विशेष","notes":"तसिल् 5.3.7; अपादान of प्रमाद-vārttika under 1.4.24"}]}
```

## Now analyse this verse
- ref: <REF>
- words:
  1. <word> — <morphology>
  ... (all words, numbered)

>>> PROMPT END
