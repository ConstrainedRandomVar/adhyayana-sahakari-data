# Corrections

Text corrections collected while building the adhyayana-sahakārī reading site. Every file is a UTF-8 TSV with the same seven
columns:

| column | meaning |
|---|---|
| `text` | the work (and commentary) |
| `layer` | which layer, and **whose digital text or print** is being corrected |
| `location` | ref in our numbering, plus the source's own block/unit id or page where known (`AS …` = advaitaśārada block id) |
| `original` | the reading as it stands in that digital text or print (private-use glyphs shown as `[U+XXXX]`) |
| `corrected` | the corrected reading |
| `witness` | what establishes it (print + page, a second edition, internal evidence…) |
| `note` | reasoning, flags, context |

**Important — what the advaitaśārada sets are.** The files named `*_advaitasharada.tsv` correct the **digital text** on
advaitasharada.sringeri.net (which other readers, including Sri Tamal Maharaj's, also use). The Mahesh Research Institute (MRI,
Dakshinamurti Math) print of the Upaniṣadbhāṣyam and Bhāṣyavārttika is the **witness** — these are not errors in the MRI print.
Only readings a printed edition (or, where stated, clear internal evidence) confirms are listed.

## Files

| file | corrects | rows | how established |
|---|---|---|---|
| `anandagiri-tika_advaitasharada.tsv` | Ānandagiri's ṭīkā on the Māṇḍūkya(-kārikā) and Bṛhadāraṇyaka bhāṣyas — advaitaśārada digital text | 622 (Māṇḍūkya 217, Bṛhad 405) | candidates from a word-by-word reading (machine + review); each confirmed in the MRI print (volume/page given). 30 are located by note because the same note recurs; 2 are digitisation defects (Latin letters inside a word) |
| `vartika-brhadaranyaka_advaitasharada.tsv` | Sureśvara's Bṛhadāraṇyaka-bhāṣya-vārttika — advaitaśārada digital text | 970 = 12 verses restored + 958 words | verses: missing/broken verses restored from the MRI and Ānandāśrama prints. Words: (a) 229 स्र-for-स्त्र/स्न font-mapping errors, each located in the MRI and Ānandāśrama OCR; (b) 729 words that Sri Tamal Maharaj's word data marks as misprints, fixed where both prints read the same different word (tier A) or the MRI reading rejoins his own padaccheda (tier B) |
| `vartika-brhadaranyaka_flags-where-print-agrees.tsv` | (not a correction) | 188 | words his word data marks as misprints where **both prints read exactly as the digital text** — offered as information; the text is left as printed |
| `nyayanirnaya_advaitasharada.tsv` | Ānandagiri's Nyāyanirṇaya on the Brahmasūtra-bhāṣya — advaitaśārada digital text | 27 | 5 edition misprints (witness: Tamal Maharaj's word data, which reads the intended form); 17 akṣaras carrying two vowel signs; 4 decomposed-vowel encodings (summary rows with counts); 1 duplicated run of 21 units |
| `purnanandi_advaitasharada.tsv` | Pūrṇānandī on the Ratnaprabhā — advaitaśārada digital text | 1 | his word data marks it मुद्रणदोषः; the commentary's own wording a few lines earlier |
| `bhasya-text_advaitasharada.tsv` | Śaṅkara-bhāṣya text (Chāndogya; Brahmasūtra) — advaitaśārada digital text, as carried into the Zenodo deposit | 11 | Chāndogya 6.11.2 from the MRI print; 10 un-converted private-use font glyphs in the BS bhāṣya. **One reading (U+E479, BS 1.3.32 प्रसिद्ध्यन्नर्थो) is inferred from grammar, not yet print-checked** |
| `zenodo-deposit.tsv` | *A Word-Level Digital Reader of the Prasthānatrayī with Śaṅkara's Bhāṣya* (Zenodo) — word dictionary | 5 = 1 correction + 4 suggestions | the one correction: a reversed savarṇa-dīrgha split; the 4 suggestions are judgment calls (a samāsa type named for a non-compound) |
| `zenodo-deposit_samasa-type.tsv` | the same deposit's word dictionary — the samāsa type in field `g` | 274 suggestions | words whose single samāsa tag disagrees with our reading of the word in its context (e.g. a bahuvrīhi qualifying a noun, tagged ṣaṣṭhī-tatpuruṣa). Found while checking our grammar-practice answer keys against our word cards; each judged in context by a model, sūtras checked against the Kāśikā, sample-read by us. **Suggestions, not error claims; not print-verified.** Composite tags (बहुव्रीहि-तत्पुरुष, X-गर्भ, X/Y) are left out — they turned out to be consistent with our analyses |
| `citations_advaitasharada.tsv` | citation references in the advaitaśārada bhāṣyas (Upaniṣads, Gītā, BS), Ānandagiri ṭīkās, VC vyākhyā | 103 | the quoted words are absent at the printed reference and found, uniquely, at the corrected one. (Already sent to advaitaśārada.) The source list also notes that AS numbers Muṇḍaka 2.2 differently in its mūla and in its citations |
| `vivekacudamani-vyakhya_advaitasharada.tsv` | Candraśekhara Bhāratī's Vivekacūḍāmaṇi vyākhyā — advaitaśārada digital text | 167 | checked against a scan of the 1952 Śṛṅgeri printing; quotations also against their source texts. (Already sent to advaitaśārada.) |
| `bhashyarkaprakasha_dakshinamurti-math-pdf.tsv` | Bhāṣyārkaprakāśa — the text layer of the Dakshinamurti Math PDF | 1 | a legacy-font glyph mis-map, checked against the printed page (the print itself is right) |
| `gita-supersite.tsv` | Dhanapati's Bhāṣyotkarṣadīpikā and Nīlakaṇṭha's Bhāvadīpa — Gita Supersite (IIT Kanpur) e-text | 49 = 8 suspected misprints + 41 encodings | the 8 Dhanapati items are **suspected only — not yet checked against the print**; the 41 are ॄ written as ृ + nukta (Dhanapati 27, Nīlakaṇṭha 14; the same encoding occurs in other Supersite commentaries) |
| `brahmatattvaprakashika_tss-print.tsv` | Brahmatattvaprakāśikā — the Trivandrum Sanskrit Series no. 7 print (1909) | 86 (12 marked uncertain) | editorial corrections of printer's errors in our edition of this text; the printed form is kept in the note on our site |
| `vartikasara_publisher-errata.tsv` | Bṛhadāraṇyaka-vārttikasāra — Chowkhamba 1915 print | 36 | the publisher's own शुद्धिपत्रम्, transcribed, with whether each was applied in our text (29 applied, 2 already correct, 5 not located) |
| `taittiriya-bhasya_readings-vs-mri.tsv` | (not a correction) Taittirīya-bhāṣya — advaitaśārada digital text vs the reading the Vanamālā quotes | 16 | पाठभेद: the Vanamālā's pratīka (with the MRI print, where noted) quotes a reading the digital bhāṣya does not print. We keep the digital bhāṣya as it is |
| `slips-in-rkmvu-etexts.tsv` | Sri Tamal Maharaj's own e-texts (Pañcadaśī and its Padadīpikā; Vanamālā — the Pañcadaśī rows are kept although our Pañcadaśī data is left out of this release, because they correct his text) | 14 | offered with thanks — slips noticed while using his texts, each with our witness (the Moḍak edition of the Pañcadaśī; the MRI print) |

## Not included

- **Our own OCR corrections** (VC vyākhyā scan, Vārttikasāra, Brahmatattvaprakāśikā, Śaṅkarānandī, AB/SD/PD ṭīkās): these fix our
  transcription, not anyone else's text. (The VC items relevant to advaitaśārada are in the vyākhyā file above.)
- **Unconfirmed suspicions**: 181 in the two Ānandagiri ṭīkās (49 Māṇḍūkya, 132 Bṛhad) await a scan check; BS bhāṣya 2.2.41
  `परिच्छिद्येेतेत` awaits a print check.
- **Pañcadaśī**: our three-way comparison (our mūla · Tamal Maharaj's e-text · Moḍak OCR) is still under review (chapters 1–5 ruled).
  Only the slips already ruled are listed. The ṭīkā collation for chapters 12–15 is raw and unadjudicated. The same व/त confusion
  as in the slips file recurs elsewhere in the Padadīpikā e-text (e.g. व्याज्यत्व in ch. 4 and 6), but those were not print-checked.

## Regenerate

```
node work/share-tamal/export/gen_corrections.js [outDir]   # in our (private) pipeline repository
```

(reads the correction files of the adhyayana-sahakārī build; writes only into `outDir`).
