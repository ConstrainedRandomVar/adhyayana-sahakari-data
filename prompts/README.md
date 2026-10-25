# Prompts

The prompts behind the machine-made layers in this repository and on adhyayana-sahakārī. Most were run on Google Gemini
(Vertex AI or the Gemini web app); one rubric (pramāṇa) was followed by Claude agents and is included for completeness.

- **Verbatim.** Template files are copied as they are. Prompts that our scripts build in code are extracted as the
  exact source lines, in a code block: `${…}`, `+ v.x +` and joined arrays mark where the input (verse, words, notes)
  is inserted at run time.
- **One template, many calls.** Per-batch prompt files (e.g. `prompt-shard-NN.txt`, `atmabodha-1-15.md`) are the
  template plus that batch's input; they are not copied — the template is.
- **Model** is given where our run notes record it; "not recorded" otherwise. Every output was then checked by
  rule-based gates (text must not change, splits must rejoin, …) and, for text corrections, against the printed page.
- **Redactions:** local file paths and personal names only (listed at the end). Nothing else was edited.

| Prompt | What it produced | Model | Source in our pipeline | Notes |
|---|---|---|---|---|
| **Grammar and kāraka** | | | | |
| [`grammar-karaka/gemini-morph-prompt.md`](grammar-karaka/gemini-morph-prompt.md) | per-word morphology + samāsa peel of the mūla (10 Upaniṣads, VC): analyses/corpus | gemini-3.7 (2026-08-20 batch); VC re-run 3.7 | `searchtool/khan/gemini-morph-prompt.md` | stage 1 of the clause-cluster model; batch.js / run.js send it per verse |
| [`grammar-karaka/gemini-karaka-tree-prompt.md`](grammar-karaka/gemini-karaka-tree-prompt.md) | kāraka roles + governors + clauses of the mūla (10 Upaniṣads, VC): analyses/corpus | gemini-3.7 (2026-08-20 batch) | `searchtool/khan/gemini-karaka-tree-prompt.md` | stage 2, fed the stage-1 morph |
| [`grammar-karaka/gemini-karaka-vibhakti-prompt-lean.md`](grammar-karaka/gemini-karaka-vibhakti-prompt-lean.md) | two-layer kāraka + vibhakti-sūtra overlay (vibhaktiSutra / vibhaktiType fields): analyses/corpus | gemini-3.8-flash (runner default); earlier overlays not recorded | `searchtool/khan/gemini-karaka-vibhakti-prompt-lean.md` | the version actually sent (build_karaka_vibhakti_shards.js packs it with verses into prompt-shard-NN.txt) |
| [`grammar-karaka/gemini-karaka-vibhakti-prompt.md`](grammar-karaka/gemini-karaka-vibhakti-prompt.md) | design document for the lean prompt above | — | `searchtool/khan/gemini-karaka-vibhakti-prompt.md` | full rationale; the lean version is what was run |
| [`grammar-karaka/combined-prompt-prakarana.md`](grammar-karaka/combined-prompt-prakarana.md) | everything for the prakaraṇa mūla in one call — words, morph, meaning, samāsa, clauses, kāraka tree, sandhi (Ātmabodha, Saddarśanam, Upadeśa Sāram): analyses/corpus | gemini-3.7 (AB, run by hand); SD/US not recorded | `searchtool/khan/karaka-prompt-variants/atmabodha-1-15.md (text before "## Verses")` | "combined prompt"; run_saddarshanam.js / run_upadesha_saram.js / make_ups_prompt.js append the numbered verses. Per-batch files (atmabodha-*.md) = this text + verses, not copied |
| [`grammar-karaka/gemini-protocol-prompt.md`](grammar-karaka/gemini-protocol-prompt.md) | the śābdabodha protocol used in the Gemini "Gem" for single-sentence analysis (hand use); protocol_run.js | Gemini Gem (web) | `searchtool/khan/gemini-protocol-prompt.md` | a styled HTML/PDF twin of the same ruleset is what the Gem reads |
| [`grammar-karaka/gemini-extract-json-prompt.md`](grammar-karaka/gemini-extract-json-prompt.md) | second step after the protocol: turns the prose analysis into JSON (protocol_run.js) | not recorded | `searchtool/khan/gemini-extract-json-prompt.md` |  |
| [`grammar-karaka/gemini-pada-analysis-prompt.md`](grammar-karaka/gemini-pada-analysis-prompt.md) | single-word derivation (prakriyā) protocol, companion to the Gem protocol (hand use) | Gemini Gem (web) | `searchtool/khan/gemini-pada-analysis-prompt.md` | no bulk data was produced with it |
| [`grammar-karaka/dhatu-resolution.md`](grammar-karaka/dhatu-resolution.md) | dhātu (gaṇa · upadeśa · artha) for verbs/kṛdantas the lookup could not resolve: analyses/corpus dhatu field | not recorded | `searchtool/khan/vc-karaka/run_dhatu_gemini.js lines 20–30` |  |
| [`grammar-karaka/json-output-rules.md`](grammar-karaka/json-output-rules.md) | a block pasted into the JSON-producing prompts to prevent malformed output | — | `searchtool/khan/vc-karaka/gemini_json.js lines 90–97 (exported as JSON_PROMPT_RULES)` |  |
| **Samāsa** | | | | |
| [`samasa/bhasya-samasa-vigraha.md`](samasa/bhasya-samasa-vigraha.md) | recursive samāsa peel (vigraha) of compounds in Śaṅkara's bhāṣya and the Gītā mūla: analyses/corpus/peel.json.gz, bhāṣya hover cards | not recorded | `searchtool/khan/vc-karaka/run_bhasya_samasa.js lines 44–60` | batches of numbered terms with their split; an optional context sentence rule |
| [`samasa/samasa-middle-member-peel.md`](samasa/samasa-middle-member-peel.md) | classification (कृत्/तद्धित/समास/मूल) of middle compound members the left-spine peel skipped: analyses/corpus/peel.json.gz | not recorded (pasted by hand) | `searchtool/khan/build_samasa_middle_prompt.js lines 30–76` | the script writes the prompt file(s); members are listed with counts and examples |
| [`samasa/samasa-leaves-classify.md`](samasa/samasa-leaves-classify.md) | derivation type of the terminal leaves of samāsa decompositions (samasa-leaves-classified.json) | not recorded (pasted by hand) | `searchtool/khan/karaka-prompt-variants/samasa-leaves-classify.md` |  |
| **Word meanings** | | | | |
| [`gloss-meaning/compound-gloss.md`](gloss-meaning/compound-gloss.md) | English meanings for mūla compounds missing from the deposit: analyses/corpus meaning (source tag gemini) | gemini-3.7-flash | `searchtool/khan/vc-karaka/run_compound_gloss.js lines 32–50` |  |
| [`gloss-meaning/simple-word-gloss.md`](gloss-meaning/simple-word-gloss.md) | English meanings for inflected mūla words missing from the deposit: analyses/corpus meaning | gemini-3.7-flash | `searchtool/khan/vc-karaka/run_simple_gloss.js lines 32–48` |  |
| [`gloss-meaning/vc-sandhi-meaning.md`](gloss-meaning/vc-sandhi-meaning.md) | sandhi + per-word meaning for the Vivekacūḍāmaṇi mūla (VC sandhi/meaning batches) | not recorded | `searchtool/khan/karaka-prompt-variants/gemini-sandhi-meaning-prompt.md` | run_vc_uvaca_sandhi_meaning.js uses the text between >>> PROMPT START/END |
| [`gloss-meaning/padartha-equals-pass.md`](gloss-meaning/padartha-equals-pass.md) | 577 padārtha "=" connectors added to the bhāṣya annotation: annotations/bhashya-roles | gemini-3.8-flash | `work/gemini-eq-pilot/run_full.js lines 29–48` |  |
| **Commentary annotation (roles)** | | | | |
| [`commentary-annotation/bhasya-annotation-upanishads.md`](commentary-annotation/bhasya-annotation-upanishads.md) | role colours, =/→ connectors, saṅgraha, citations on Śaṅkara's bhāṣya (Upaniṣads, Gītā, BS): annotations/bhashya-roles | not recorded | `searchtool/khan/gemini-bhasya-annotation-prompt.md` | the copy read by annotate_text.js / rerun_refs.js / annotate_brihad_3928.js (text between >>> PROMPT START/END) |
| [`commentary-annotation/bhasya-annotation-canonical.md`](commentary-annotation/bhasya-annotation-canonical.md) | role annotation of the Vivekacūḍāmaṇi vyākhyā and later commentary runs (loosened tātparya standard): annotations/bhashya-roles (VC) | not recorded (pasted by hand in shards ≤ ~30k chars) | `searchtool/khan/vc-karaka/gemini-bhasya-annotation-prompt.md` | the canonical successor; both copies were used for shipped data |
| **Commentary word analysis** | | | | |
| [`commentary-word-analysis/vc-vyakhya-gloss.md`](commentary-word-analysis/vc-vyakhya-gloss.md) | per-sentence word analysis, translation and roles of the VC vyākhyā (Candraśekhara Bhāratī): analyses/tika-word-analysis/vc, annotations/tika-roles | not recorded | `searchtool/khan/vc-karaka/vc_bhashya_gloss_pilot.js lines 35–86` | exported to vc_bhashya_gloss_chunk.js, which ran the verses in chunks; vc_bhashya_gloss.js holds an earlier one-verse variant |
| [`commentary-word-analysis/vc-vyakhya-regloss-sentences.md`](commentary-word-analysis/vc-vyakhya-regloss-sentences.md) | re-analysis of VC vyākhyā sentences after the print/advaitaśārada text pass | not recorded | `searchtool/khan/vc-karaka/vc_bhashya_regloss_sentences.js lines 33–58` |  |
| [`commentary-word-analysis/saddarshanam-tika-gloss.txt`](commentary-word-analysis/saddarshanam-tika-gloss.txt) | word analysis, translation, roles and OCR suspects for Kapāli Śāstrī's bhāṣya: analyses/tika-word-analysis, annotations/tika-roles | not recorded | `searchtool/khan/vc-karaka/sad-tika-PROMPT.txt` | run_sad_tika_gloss.js |
| [`commentary-word-analysis/upadesasaram-tika-gloss.txt`](commentary-word-analysis/upadesasaram-tika-gloss.txt) | same, for Gaṇapati Muni's Upadeśasārabhāṣya | not recorded | `searchtool/khan/vc-karaka/ups-tika-PROMPT.txt` | run_ups_tika_gloss.js |
| [`commentary-word-analysis/atmabodha-tika-gloss.txt`](commentary-word-analysis/atmabodha-tika-gloss.txt) | same, for Padmapāda's Vedāntasāra ṭīkā on the Ātmabodha | not recorded | `searchtool/khan/vc-karaka/ab-tika-PROMPT.txt` | run_ab_tika_gloss.js |
| [`commentary-word-analysis/vicharasagara-gloss.md`](commentary-word-analysis/vicharasagara-gloss.md) | per-word analysis, translation and roles of the Vicārasāgara: analyses/vicharasagara | not recorded | `searchtool/khan/vc-karaka/vs_run.js lines 27–89` |  |
| **Translation** | | | | |
| [`translation/anandagiri-english-and-pada.md`](translation/anandagiri-english-and-pada.md) | English translation and padaccheda of Ānandagiri's ṭīkā (Māṇḍūkya, Bṛhadāraṇyaka): analyses/translations | gemini-3.8-flash | `work/anandagiri-en/run.js lines 67–118` | three prompts: translation, पद split (two variants) |
| **Text checking (OCR / print)** | | | | |
| [`text-checking-ocr/atmabodha-tika-ocr-check.md`](text-checking-ocr/atmabodha-tika-ocr-check.md) | OCR correction suggestions for the Ātmabodha ṭīkā scan (each checked against the page): etexts/atmabodha-padmapada | not recorded | `searchtool/khan/vc-karaka/run_ab_tika_ocrfix.js lines 21–44` | sent with the page image |
| [`text-checking-ocr/shankaranandi-crop-check.md`](text-checking-ocr/shankaranandi-crop-check.md) | blind re-reading of doubtful OCR words from crops of the Nirṇayasāgara 1916 print: etexts/shankaranandi | not recorded | `work/shankaranandi/run_crop_check.js lines 27–54` | two prompts (batch read; check) |
| [`text-checking-ocr/vartika-tika-adjudicate.md`](text-checking-ocr/vartika-tika-adjudicate.md) | choice between the two OCR readings (MRI vs Ānandāśrama) of the Śāstraprakāśikā: the vārttika ṭīkā text on the site | gemini-3.8-flash | `out-of-repo pipeline: mri-work/vartika/run_tika_adjudicate.js lines 21–38` | text-only |
| [`text-checking-ocr/vartikasara-proof.md`](text-checking-ocr/vartikasara-proof.md) | text-only proofreading suggestions for the Vārttikasāra OCR (then scan-adjudicated): etexts/vartikasara | gemini-3.8-flash | `out-of-repo pipeline: vartika/brihadaranyaka-vartika-sara/work/proof_prompt.py (prompt builder; run_proof.js sends the files)` |  |
| [`text-checking-ocr/brahmatattvaprakashika-page-check.md`](text-checking-ocr/brahmatattvaprakashika-page-check.md) | page-by-page transcription check of the Trivandrum print (flags then scan-adjudicated): etexts/brahmatattvaprakashika | gemini-3.8-flash | `out-of-repo pipeline: brahmatattvaprakashika/work/gemini_check.js lines 13–24` | sent with the page image |
| [`text-checking-ocr/vrk-monograph-ocr.md`](text-checking-ocr/vrk-monograph-ocr.md) | OCR corrections + reading structure of the English monograph (V. R. Kalyanasundara Sastri) on the site | not recorded | `out-of-repo pipeline: monograph/vrk-gita-upanishads/gemini_correct.py lines 19–71` |  |
| **Corpus chat** | | | | |
| [`corpus-chat/corpus-chat-system-prompt.md`](corpus-chat/corpus-chat-system-prompt.md) | system prompt of the "ask the corpus" chat (answers via tool calls over analyses/corpus) | not recorded | `searchtool/khan/corpus/GEMINI-SYSTEM-PROMPT.md (generated from corpus/corpus-chat.js)` |  |
| **Pramāṇa classification (Claude, not Gemini)** | | | | |
| [`classification-claude/pramana-rubric.md`](classification-claude/pramana-rubric.md) | śruti/yukti/anubhava grade of each argument segment: annotations/pramana.json | Claude agents (not Gemini) | `searchtool/khan/pramana-rubric.md` | included for completeness — this layer was classified by Claude agents following the rubric |

## Not included

- **Pañcadaśī** prompts (the combined mūla prompt `karaka-prompt-variants/pd-*.md`, the Padadīpikā gloss prompt
  `pd-full-paste-PROMPT.txt`, the PD pratīka prompt) are held back together with the Pañcadaśī data, which is not in
  this release.
- **Experiments that produced no shipped data:** `karaka-prompt-variants/adversarial-*`, `bg-*`, `morph-test-v4.md`,
  `ab-A-presplit.md` / `ab-B-raw.md` (prompt comparisons); `vc-karaka/mulam-eval/atomic-prompt*.md` (evaluation of the
  annotation prompt against a hand-annotated gold passage); `verify/self-consistency.js`; the Ānandagiri English pilot.
- **The Śrīrāmodantam** analysis on our sister site used the same combined prakaraṇa prompt (`grammar-karaka/combined-prompt-prakarana.md`).
- **Sri Tamal Maharaj's deposit** (bhāṣya padaccheda, grammar, meanings) was produced by his own pipeline, not by these prompts.
- **The Vivekacūḍāmaṇi vyākhyā print check** (167 corrections in `corrections/`) was adjudicated by Claude agents against the
  1952 print; that instruction file is not in the repository.

## Redactions

- `grammar-karaka/gemini-karaka-vibhakti-prompt.md`: a local path (replaced by `[redacted: local path]`)
- `grammar-karaka/gemini-extract-json-prompt.md`: a name (replaced by `[redacted: name]`)
- `gloss-meaning/vc-sandhi-meaning.md`: a name (replaced by `[redacted: name]`)
- `commentary-annotation/bhasya-annotation-canonical.md`: a name (replaced by `[redacted: name]`)
- `text-checking-ocr/vartikasara-proof.md`: a name (replaced by `[redacted: name]`)
- `text-checking-ocr/vartikasara-proof.md`: a name (replaced by `[redacted: name]`)
- `classification-claude/pramana-rubric.md`: a local path (replaced by `[redacted: local path]`)
