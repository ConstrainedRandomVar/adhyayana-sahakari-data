# analyses/ — grammatical analysis, with the source of every field

The word-level and sentence-level analysis behind adhyayana-sahakārī's word cards, read-a-verse walks, वाक्य-विग्रह /
वाक्य-विभाग tutorials and corpus search. **Much of it is machine-made (Google Gemini) and has not been checked word
by word.** Some of it is *not ours* — it comes from your Zenodo deposit or from the University of Hyderabad e-reader. So
every field carries a source tag: compare only the fields tagged `gemini` (and the other "ours" codes) when looking for
our errors.

Licence: our analyses here are CC BY 4.0 (attribution: *adhyayana-sahakārī*). Fields tagged `zenodo*` are your own
deposit data (CC BY 4.0, yours). The Sanskrit texts these analyses sit on are the editions' — see the top-level README for
each edition and its copyright; we do not license them.

## Files

| file | size | what |
|---|--:|---|
| `corpus/<Text>.json.gz` (18 files) | 13 KB – 1.5 MB | the corpus, one file per text, with a `src` tag on every word field and verse field |
| `corpus/peel.json.gz` | 2.4 MB | the shared samāsa-peel dictionary (surface compound → layers), all `gemini` |
| `corpus/provenance-report.json` | 16 KB | counts of every (text, field, source) and the fields we could not attribute |
| `vicharasagara/words.json.gz` | 3.1 MB | Vicārasāgara (538 āvartas): per-sentence words with morph/meaning/samāsa, English translation, discourse roles |
| `tika-word-analysis/<x>.json.gz` | 59 KB – 2.0 MB | prakaraṇa commentaries, per sentence: words with morph/meaning/samāsa + English translation (AB Padmapāda 67 v; SD Kapāli Śāstrī 44; US Gaṇapati Muni 30; VC Candraśekhara Bhāratī 472 v) |
| `translations/anandagiri-en-{mandukya,brha}.json.gz` | 0.5 / 1.4 MB | Ānandagiri's ṭīkā on the Māṇḍūkya(-kārikā) and Bṛhadāraṇyaka bhāṣyas: English per note + पद split |

Text keys: `Gita`, `Isha`, `Kena`, `Kathaka`, `Prashna`, `Mundaka`, `Mandukya` (with kārikā), `Taitiriya`, `Aitareya`,
`Chandogya`, `Brha`, `BS`, `VC` (Vivekacūḍāmaṇi), `AB` (Ātmabodha), `UPS` (Upadeśa Sāram), `SAD`
(Saddarśanam), `VS` (Vicārasāgara).

**Not in this folder (and why):** the Śaṅkara-bhāṣya passages with their discourse-role spans (pūrvapakṣa / siddhānta /
gloss / tātparya …) are in `../annotations/`; the corpus's Vaiyāsika-nyāya-mālā adhikaraṇa table is advaitaśārada's text,
not ours, so it is left out. Nothing else was removed from the corpus.

## Corpus record shape

`corpus/<Text>.json.gz` = `{ text: {label, counts…}, generated, verses: [verse…] }`.

```jsonc
verse = {
  "text": "VC", "ref": "2.15", "rawRefs": {…}, "label": "2.15",
  "moola": "…verse text…",
  "words":    [ word… ],
  "sandhi":   [ { rule, sutra, before:[…], after, subtype } ],
  "clusters": [ { governorWord, clauseType, voice, transitivity, isFiniteVerb, subjectIsHead } ],
  "relations":[ { relation, word, governorWord, role?, targetWord?, … } ],   // kāraka web
  "clauses":  [ { id, type, subordinateTo, words, elided, headWord, gloss } ], // gloss = English of the clause
  "mahavakya": { subtype, label },            // where present
  "virodha":  [ … ],                          // where present (curated paradox units)
  "src": { "moola": …, "sandhi": …, "clusters": …, "relations": …, "clauses": …, "mahavakya": …, "virodha": … }
}
word = {
  "word": "आत्मैक्य-बोधेन", "wordIndex": 3,
  "morph": "…raw grammar string…",            // see below — the best field to compare first
  "lemma": "…", "vibhakti": "तृतीया", "vacana": "एकवचन", "linga": "पुंलिङ्ग",
  "karakaRoles": ["करणम्"], "meaning": "…",
  "dhatu": { root, lakara, purusha, vacana, pada, voice?, prayoga? }, "krt": { pratyaya, prayoga },   // where present
  "samasaCategory": "…", "compound": "<key into peel.json>", "samasaType": "…", "peelDepth": 4,
  "vibhaktiSutra": { num, text }, "vibhaktiType": "कारक|उपपद|…", "overlayRole": "…",
  "src": { "<field or dhatu.x / krt.x>": "<source code>", … }
}
```

- `morph` is the raw grammar string the word card shows as व्याकरणम्: for the Upaniṣads and the Gītā it is your
  deposit's `.g` (tag `zenodo`); for VC/AB/US/SD it is the Gemini morph string (tag `gemini`). Gītā: present for
  6,622 of 10,174 word records (the rest are compound members / sub-tokens with no deposit token of their own).
- **wordCode convention** (in our tutorial data, decoded here): a nominal's code is `[vibhakti][vacana]`, a finite
  verb's is `[puruṣa][vacana]` — so `31` on a verb is 3rd person singular, not तृतीया. In the corpus these are already
  decoded into `vibhakti`/`vacana` or `dhatu.purusha`/`dhatu.vacana`.
- `lemma` / `dhatu.root` for Upaniṣad and Gītā verbs read like `√कम् कमुँ कान्तौ 01ASS`: the root is parsed from your
  grammar string; the Dhātupāṭha entry after it (aupadeśika form, meaning, gaṇa·pada·karma·iṭ code) is our lookup in the
  ashtadhyayi.com Dhātupāṭha.
- Known corpus caveats: repeated identical forms in one verse are merged into one word record; `samasaCategory` (coarse)
  and `samasaType` (peel layer 0) are different vocabularies; BS has bhāṣya only (no mūla word analysis); VS has no
  kāraka (reading-only); Upaniṣad `sandhi` is empty (only Gītā and the prakaraṇas carry sandhi).

## Source codes (`src`)

| code | meaning |
|---|---|
| `zenodo` | your deposit's value, verbatim |
| `zenodo-parsed` | your deposit's split/grammar, sorted into this field by our deterministic code (no model) |
| `zenodo+fix` | your deposit's value with one of our hand corrections (listed in `../corrections/`) |
| `gemini` | **ours — machine analysis** (Google Gemini) |
| `dhatupatha-lookup` | **ours** — a finite verb your deposit has no entry for: root found by looking the form up in the ashtadhyayi.com conjugation tables (homonymous roots decided by Claude, else left open) |
| `uohyd` | University of Hyderabad e-reader data (Gītā kāraka), converted by our tutorial builder |
| `uohyd+heuristic` | Gītā word kāraka: e-reader roles, plus peripheral roles (adhikaraṇa / karaṇa / hetu / sambodhya) from **our** gloss-based heuristic where the e-reader has none; the two are not separable per word |
| `curated` | **ours, by hand**: mahāvākya catalogue (human-audited); virodha units (machine candidates, human-reviewed) |
| `edition` | the verse text as printed in the edition (VC/AB/US/SD/VS) |
| `unknown` | could not be attributed — 1 word (Chāndogya 4.17.9 एवंविदम्, `meaning`) |

## Provenance by text × field

| field | Gītā | 10 Upaniṣads | VC · AB · US · SD | VS | BS |
|---|---|---|---|---|---|
| verse text (`moola`) | zenodo | gemini padaccheda of your mūla, joined | edition | edition | zenodo |
| word split (`word`) | zenodo | gemini | gemini | gemini | — |
| `morph` | zenodo | zenodo (2 Chāndogya fixes) | gemini | in `vicharasagara/` | — |
| vibhakti · vacana · liṅga | zenodo-parsed | gemini | gemini | — | — |
| finite verb lakāra · puruṣa · vacana · pada | zenodo-parsed | gemini | gemini | — | — |
| lemma · dhātu root | zenodo-parsed (+ Dhātupāṭha entry) | zenodo-parsed; 406 verbs dhatupatha-lookup; 3 fixes | gemini | gemini | — |
| kṛt | zenodo-parsed | — | — | — | — |
| meaning (English) | zenodo | zenodo; **2,806 gemini** (words absent from your deposit) | gemini | gemini | — |
| kāraka role (`karakaRoles`) | uohyd+heuristic | gemini | gemini | — | — |
| clusters · relations · clauses (+ clause English) | uohyd | gemini | gemini | — | — |
| sandhi | zenodo-parsed | — | gemini | — | — |
| samāsa (peel, samasaType, samasaCategory) | gemini (samasaCategory: zenodo-parsed) | gemini | gemini | gemini | — |
| vibhakti sūtra · type · role overlay | gemini | gemini | gemini | — | — |
| mahāvākya · virodha | curated | curated | curated | curated | curated |

Exact counts per text and field: `corpus/provenance-report.json` (`counts`, keyed `Text|field|source`).

## Models and reliability

- **Gemini runs** (Google, Aug–Oct 2026): the kāraka / morph clause-cluster analysis of the Upaniṣads, VC and AB
  used gemini-3.7(-flash); the English meanings for words missing from your deposit used gemini-3.7-flash (verse given as
  context); the Ānandagiri English used gemini-3.8-flash, with review passes; the other layers (US/SD analysis, the
  commentary word analyses, the vibhakti-sūtra overlay, VS) used gemini-3.7-flash or 3.8-flash (the model is not recorded
  per run).
- **None of the Gemini output has been verified word by word.** Our build checks guard structure (no dropped or
  reordered verses, the split rejoins to the printed text, no corrupted characters). They cannot tell whether a role,
  case, root or samāsa analysis is right. A blind audit of 20 hard verses (clause decomposition) held up. Other than
  that, the analysis has been corrected only where readers or we noticed errors.
- **Gītā kāraka (UoHyd e-reader)** is about 57% reliable in our checks. Every claim whose implied case contradicts your
  deposit's case tag is dropped. The gloss heuristic that fills peripheral roles measured 69.3% precision against the
  e-reader (85.8% for adhikaraṇa).
- Your Heritage-verified morphology is exactly the check this data has not had.

## Sending disagreements back

Any format is welcome; most useful is one row per word: `text`, `ref`, `word`, `field`, our value, your value, and a
note. Send them by email, or use "report an issue" on the word card at
https://constrainedrandomvar.github.io/adhyayana-sahakari/ for single words. Corrections we accept go into our override
files and are credited to you.

## Regenerating

From the private build repo (needs your Zenodo deposit on disk):
`node work/share-tamal/export/export_analyses.js <bundle>` (corpus + provenance) and
`node work/share-tamal/export/export_analyses_extra.js <bundle>` (VS, commentary word analyses, translations).
Generated from `corpus.json.gz` of 2026-10-24.
