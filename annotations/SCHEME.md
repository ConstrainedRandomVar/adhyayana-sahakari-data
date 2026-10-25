# Bhāṣya reading annotation: the scheme

This layer marks what each stretch of a commentary is doing in the argument (an objection, the reply, a gloss of a
root word and so on). It is a reading aid, not part of the text. It was made by adhyayana-sahakārī, mostly by machine,
and it may contain errors. It is not a traditional sub-commentator's reading of any passage.

## Where the scheme comes from

The categories and colours are taken from a teacher's class annotation of the Bṛhadāraṇyaka-bhāṣya (chapter 1 and
2.1–2.3), colour-marked by hand on the advaitaśārada text. The teacher prefers not to be named.

Applying the scheme to every text:

1. A language model (Google Gemini) read each passage of the bhāṣya and returned the passage with the classes below
   marked as spans.
2. A deterministic step (re-anchoring) laid those spans back onto the original digital text, character by
   character: a global alignment of the two Devanāgarī character streams, then each class boundary snapped to a word
   boundary. Every character in our files comes from the source text, never from the model, so the text is unchanged
   by construction. A model mistake can only move a class boundary.
3. If fewer than 60% of a passage's words appear in the model's output, the passage is left unannotated (flag
   `unannotated`). One passage is affected (Gītā `7.25::pre`).
4. Hand corrections on top:
   - 6 objections the model had left as plain exposition were marked pūrvapakṣa after checking against A. K. Aruna's
     upasanayoga.org editions: Gītā 4, Bṛhadāraṇyaka 1, Taittirīya 1.
   - Per-passage fixes to the model's markup, applied exactly as on our site.
5. Root-word quotations (`mula`) also include the marks we projected from three sources: the printed pratīka marks of
   the Mahesh Research Institute (Dakshinamurti Math) Upaniṣadbhāṣyam, A. K. Aruna's editions, and pratīkas we
   adjudicated by hand. Exactly which ṭīkā/bhāṣya/verse word each quotation points to is in `alignments/`, not here.

**Check against the teacher's annotation.** The teacher's marking of the Bṛ 2.1.15 debate (seven objection → reply
pairs) served as the answer key. In the exported data, all 7 objection heads carry `purvapaksha`, and all 7 reply heads
(the terse "न, …-त्वात्" sentences) carry `siddhanta` + `sangraha`. **Caveat:** that passage was used to calibrate
the prompt, so the result is in-sample. It is a sanity check, not a measured accuracy. We have no out-of-sample
agreement figure.

**Dropped classes.** Two classes from the teacher's annotation were tried and dropped because the model agreed too
rarely with the human marking: `key` (yellow, the general maxim or conclusion of a passage) and `avataranika`
(cyan, the introductory lead-in). Neither appears in these files.

## Classes, inline layer (`bhashya-roles/*.json`)

A character can carry several classes at once: one discourse role, plus any of the word and compression classes.

| class | meaning | how it is recognised | colour on our site (light / dark) |
|---|---|---|---|
| `purvapaksha` | objection (pūrvapakṣa) | `ननु`, `…इति चेत्`, `कथम्`, `स्यादेतत्` and the stretch that elaborates the objection | red `#b91c1c` / `#f79a9a` |
| `ekadeshi` | a partial or intermediate view (ekadeśin), e.g. `अपरे तु`, `अन्ये` | named other view that is neither the opponent's nor the siddhānta | orange `#c2410c` / `#fb923c` |
| `siddhanta` | Śaṅkara's reply / settled view, incl. a bare `न` / `नैष दोषः` with its reasons | answer to an objection | green `#15803d` / `#83e0a0` |
| `sangraha` | the short thesis-head of a move, which the following text then elaborates. At reply scale this is usually `न` + an ablative reason (`…त्वात्`, `…अनुपपत्तेः`). Reading the underlined heads in sequence gives the skeleton of the argument | compressed head before its elaboration | underline (any colour) |
| `mula` | a word of the root text quoted inside the commentary (pratīka) | quotation of the verse / sūtra | blue bold `#1a56db` / `#7ab0ff` |
| `gloss` | synonym gloss of the preceding root word (paryāya, vācyārtha); follows a `=` connector | `X = Y` | default ink `#3f4653` |
| `import` | intended sense (tātparya, lakṣyārtha), only where Śaṅkara signals it (`…इत्यर्थः`, `…इत्यभिप्रायः`); follows a `→` connector | `X → Y` | violet italic `#6d28d9` / `#c9b6f7` |
| `vyakarana` | Śaṅkara's own grammatical remark: a nirvacana (`X इति Y`), or a statement about case, particle or compound (`षष्ठी निर्धारणार्था`, `अवधारणार्थ एवकारः`) | grammar statement, not a synonym | slate italic `#6b6255` / `#b8b2a8` |
| `quote` | a quotation from scripture or smṛti marked by the model | `‘…’` + `इति श्रुतेः/स्मृतेः` | citation teal `#0e7490` / `#67d3e8` |

**Connectors** (`connectors: [[offset, glyph]]`): these are not part of the text. On our site the glyph is shown
before the character at `offset`:
- `=` marks a synonym gloss
- `→` marks the intended sense

A connector is kept only when the words on both sides of it are found in the source, and only at a word boundary.

**Citations** (`citations: [{start, end, label, target}]`): parenthesised references such as `(बृ. उ. ४ । ४ । २०)`.
- `target` = the verse of a text we host (work + ref), resolved deterministically.
- Where the edition's number is wrong (the quoted words are not at the printed reference but are at exactly one other
  verse of the same text), `target` is the corrected verse and `note` gives the printed number.
- `correctedLabel` gives the right work where the edition names the wrong one (hand-checked; 2 in these files).
- 375 citations in the Upaniṣad, Gītā and Brahma-sūtra bhāṣyas, all resolved to a hosted verse. Citations in the
  Vivekacūḍāmaṇi vyākhyā and the ṭīkās are linked on our site by a later pass and are not included here.
- The list of edition errors is in `corrections/`.

**Refs**:
- verse refs as in the Zenodo deposit
- `intro:<chapter>:<n>`: introductory bhāṣya before a chapter
- `<ref>::pre`: bhāṣya printed before that verse, as a lead-in

**Text**: the passage text is the advaitaśārada digital text as carried by the Zenodo deposit (prose without
daṇḍas; our site re-inserts the daṇḍas from the reader copy), with the corrections in `corrections/` applied.
`segments` concatenate to `text` exactly. The `.standoff.json` files carry the same information as `[start, end, class]`
spans over `text` (offsets in UTF-16 code units, as in JavaScript).

**Not included:** the role pills, the concession marker (अभ्यु॰) and other cue-word marks shown on the site. They are
derived from the classes above or from trigger words, not separate judgments.

## Sentence-level roles (`tika-roles/*.json`)

The prakaraṇa commentaries were analysed word by word, and the same model pass gave each sentence's discourse role(s)
as word ranges (`roles[].fromWord … toWord`, 1-based over `words[]`):
- the Vivekacūḍāmaṇi vyākhyā
- the Saddarśanam, Upadeśa Sāram and Ātmabodha ṭīkās

| role | meaning | colour on our site |
|---|---|---|
| `exposition` | plain exposition | none |
| `purvapaksha` | objection | red |
| `siddhanta` | reply / settled view | green |
| `ekadeshi` | partial view | orange |
| `drishtanta` | example, illustration | amber `#a16207` / `#fcd34d` |
| `lakshana` | definition | olive `#4d7c0f` / `#a3d65c` |
| `phalita` | upshot, what follows | rose `#be123c` / `#fb7185` |
| `anuvada` | restatement of what was said | default ink |
| `tarka`, `shruti` | rare labels the model used (10 sentences in all) | shown uncoloured on our site |

For the Vivekacūḍāmaṇi vyākhyā, our site colours the text from the inline layer (`bhashya-roles/vc.json`, same scheme
as the Śaṅkara-bhāṣya). It falls back to these sentence roles only where the inline layer does not reach a word.

## Pramāṇa grading (`pramana.json`)

Each discourse segment (objection / reply / partial view) of the Upaniṣad and Gītā bhāṣyas, the Saddarśanam ṭīkā and
the Vivekacūḍāmaṇi vyākhyā is graded by the means of knowledge it rests on:
- `shruti`: scriptural testimony, including smṛti
- `yukti`: reasoning (tarka, anumāna, upapatti)
- `anubhava`: direct experience (the three states, the witness, self-evidence)
- `none`: a bare question or exposition

The grading was done by language-model agents (Anthropic Claude) following a written rubric. On our site the grade
is shown as a small pill at the start of the segment (one magenta hue, `#ad24b2` / `#e67bea`, three lightness steps).

## Mahāvākya catalogue (`mahavakya.json`)

Verses of the root texts that state the identity of the Self and Brahman.
- Candidates came from a detector for co-reference (sāmānādhikaraṇya) over our kāraka analysis.
- Every candidate was judged by hand: a genuine identity statement, or a structural false positive.
- Subtypes: `mukhya` (direct jīva–brahman identity) and `badhayam` (sublation: the world / the witness is brahman).
- Text keys are our short ids: Brha, Chandogya, Kathaka, Taitiriya, Mandukya, Mundaka, Isha, Kena, Aitareya, Gita, VC,
  AB = Ātmabodha, UPS = Upadeśa Sāram, SAD = Saddarśanam, VS = Vicārasāgara.

## Counts

Per text and class: `COUNTS.json` (characters and spans per class, connectors, citations, passages).
