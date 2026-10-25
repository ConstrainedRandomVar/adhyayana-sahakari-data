# Pratīka alignments — method

For every commentary shown on adhyayana-sahakārī, these files list each **pratīka** (the words of the base text that a
commentary quotes before explaining them) and the **one word of the base text it is linked to**, or say that it is not linked.

- Exported from the published reading pages (academy build `f9962b0`, 2026-10-25) by `export_alignments.py`. The links were
  computed when those pages were built; the export reads them back out and does not recompute anything.
- One TSV per text and commentary: `<text>-<lane>.tsv`, UTF-8, one row per pratīka. Per-file counts are in `counts.json`.
- `<text>-bhashya.tsv` = Śaṅkara's bhāṣya quoting the mūla. All other files are ṭīkās/vyākhyās, on the bhāṣya, on the mūla,
  on the vārttika, or (Pūrṇānandī) on another ṭīkā.

## Columns

| column | meaning |
|---|---|
| `text`, `lane` | the work and the commentary |
| `ref` | the passage in our numbering (the deposit's numbering for the upaniṣads, Gītā and BS). `intro` = introduction; `X::pre` = the avatārikā before X; `X::post` = after it; prakaraṇas give the page section id (`v-12`) |
| `unit` | the note: `t<lane>_<n>` = n-th note of that commentary on this passage (`_s<k>` = a Pūrṇānandī note under it); bhāṣya rows give the word number `b<n>` |
| `pratika` | the pratīka as printed in our text (sandhi form, any following इति kept) |
| `lemma` | the part of the pratīka that was matched (इति, case-tails and similar stripped), where this differs from `pratika` |
| `mark` | who marked it as a pratīka (see "Marks" below). `;check` = a doubtful target, see "Known limits" |
| `target_layer` | `mula`, `bhashya`, `vartika`, `ratnaprabha` (for Pūrṇānandī), `mula-half-verse` (VC half-verse units) |
| `target_ref`, `target_ord` | where the target word is. Its ordinal is 0-based. **mūla:** the n-th word of the verse in our padaccheda; for the Gītā and BS it is `i.j` = word i, pada j of the deposit's split. **bhāṣya:** the n-th Devanāgarī word of the bhāṣya passage, counting space-separated words of the advaitaśārada text and leaving out punctuation. **ṭīkā/vārttika:** the n-th word of that note or verse |
| `target_occ` | the target word is the k-th occurrence of that same form in that verse/passage, so you can join by (ref, form, k) without relying on our tokenization |
| `target_word` | the target word as it appears in our text |
| `target_deposit` | **mūla targets only:** the word in Sri Tamal Maharaj's Zenodo deposit (`prasthan-words-<slug>.json`): `w<i>.p<j>` = word i of the verse (0-based), pada j of its `p` split (split on " + ", parentheses ignored); `w<i>` alone = our split differs inside that deposit word. Coverage below |
| `target2_*` | a second target, when one pratīka is linked both to a bhāṣya word and to a mūla word |
| `member` | `a` or `a-b`: the pratīka quotes member(s) a…b (0-based) of a compound in the verse, not the whole word |
| `status` | `linked` · `linked-cross-verse` (an introduction quoting a verse elsewhere in the text; none in this export) · `unlinked` |
| `source_key` | the word's id on our page (`data-k`), useful for checking a row against the live page |

For bhāṣya targets, the deposit's `bhasya-words-ALL.json` is keyed by surface form, so `target_word` together with
(`ref`, `target_occ`) is the join key. We did not build a positional mapping to the deposit's bhāṣya.

## What counts as a pratīka (column `mark`)

**Śaṅkara's bhāṣya → mūla** (`*-bhashya.tsv`). A bhāṣya word counts as quoting the verse if any of these sources marks it.
The sources are recorded per word:
- `upasanayoga`: A. K. Aruna's editions (upasanayoga.org).
- `mri`: printed in regular type inside the bold bhāṣya of the Mahesh Research Institute *Upaniṣadbhāṣyam* (the Kaṭha and
  Chāndogya bhāṣyas are not marked in that print).
- `gemini`: a language-model annotation pass over the bhāṣya.
- `matcher`: a deterministic left-to-right walk that matches the verse's padas in the bhāṣya.
- `adjudicated`: added by hand after reading each case in context. This covers 179 «X इति» quotes, plus short fused quotes
  that the MRI and upasanayoga prints mark but that are too short for automatic recovery.
- `sub-word`: only part of a printed word is the quote. `hand-pin`: the target was fixed by hand for a repeated word.
- An empty `mark` means the word is marked on the page but its source was not recorded (about 4% of bhāṣya rows).

**Ṭīkās.**
- `as` / `mri` (Ānandagiri on the upaniṣads and Gītā): `as` = the advaitaśārada text's own pratīka markup; `mri` = bold in the
  MRI print. Both are recorded where both mark the pratīka.
- `printed:as` (Nyāyanirṇaya): advaitaśārada's pratīka markup.
- `printed:print-bold` (Bhāṣyārkaprakāśa): bold in the Dakshinamurti Math print (read from the PDF's font layer).
- `printed:supersite` / `printed:supersite-bold` (Dhanapati, Nīlakaṇṭha): the Gita Supersite e-text's marks.
- `printed:tamal-bold` (Śrīdharī): bold in Sri Tamal Maharaj's e-text.
- `printed:opening-iti` (Madhusūdanī): the source marks nothing; the opening «…इति» of each note is restored as a pratīka.
- `printed:print` (Śaṅkarānandī; Śāstraprakāśikā): marked in the print (Nirṇayasāgara 1916; MRI vārttika volumes).
- `marked:tamal` (Ratnaprabhā, Pūrṇānandī): Sri Tamal Maharaj's marks.
- `marked:tamal-or-mri` (Vanamālā): his marks (the pratīka opening each paragraph) together with bold runs in the MRI print.
  The export does not record which of the two marked each item.
- `detected` (the verse commentaries on the Gītā; the Brahmatattvaprakāśikā, whose print marks none): a whole word of the note
  counts as a pratīka when it equals a verse word that occurs **once** in the verse and is not a particle or pronoun, or when
  it is an «X इति» whose X opens the verse. Detection was sampled in context; it is not certified item by item.

**Prakaraṇa ṭīkās** (VC, AB, SD, US): see "Prakaraṇa texts" below.

## How a pratīka is resolved (Upaniṣads, Gītā, Brahmasūtra)

The rule is exact-or-nothing, decided when the page is built. A pratīka gets a link only when exactly one word of the base
text fits it. Otherwise it is left unlinked; we never guess.

1. **Matching key.** Each word is reduced to its initial independent vowel plus its consonant skeleton, with ं = म. Bhāṣya ⇄
   mūla matching treats voiced and voiceless stops alike (तदेव ↔ तत्, sandhi voicing). For ṭīkā pratīkas, only a consonant
   with no vowel after it is treated that way (so दैवं ≠ त्वं).
2. **Match tiers:** equal; quote = target + a fused particle (वेदेति, तदेव); the quote lacks only the target's final
   consonant (only when the target really ends in one); the quote lost the target's initial vowel in sandhi. A pratīka may
   also match a run of up to six consecutive words (नैजति = न एजति), allowing visarga sandhi at the joins, the reversal of a
   two-word quote, and consonant assimilation at a junction (तत्+च → तच्च). Whole-word matches are tried first.
3. **Vowel check.** One-word ṭīkā lemmas must also agree in vowel quality, with the final vowel compared only within its
   sandhi class (योगो ≡ योगः ≠ योगी). This stops the consonant skeleton from accepting काम for किम्.
4. **Order.** A commentator walks the text in order. A pratīka with exactly one candidate is an anchor. Any other pratīka is
   linked only if every best in-order alignment places it on the same word, i.e. exactly one candidate lies between its
   neighbouring anchors. Where neither holds (typically a word repeated in the verse or passage), there is **no link**.
5. **Later, strictly additive passes.** Each was proved not to move or remove an existing link:
   - hand-adjudicated quotes;
   - repeated-word marks placed by order;
   - compound members (`member` column), linked only when the member is unique among all members in the verse and not
     also a whole verse word;
   - the 24 placements that used Sri Tamal Maharaj's multi-word pratīka runs as a hint;
   - a small number of hand pins.
6. **Untagged commentaries** (one block per verse, e.g. Bhāṣyārka, Nyāyanirṇaya) are aligned against the whole passage:
   avatārikā, bhāṣya and closing. If a pratīka is not found in the bhāṣya, its mūla match is used.

**Checks.**
- A build gate fails if any word shown as a quotation has no target.
- Every target exists on the page.
- Each new pass was compared with the previous build (links added, lost, moved), and the added links were read in context.
- Headless-browser click checks confirmed landings on the exact word.

These checks show that the links are internally consistent and conservative. They are not a scholar's certification of every
row.

## Prakaraṇa texts (VC, AB, SD, US) — a different, weaker method

The commentary words are those of our word-glossed text. A commentary word counts as a pratīka when it equals a verse word,
either in exact form or in consonant skeleton (only for skeletons of 5 or more consonants). It links to the **first verse
word not already used**, walking in reading order (`march:glossed-word`). Words the model annotation marked as voicing the
mūla link only if they match exactly one verse word.

This is not the positional exact-or-nothing method above, so a quote of a word that is repeated in the verse can land on an
earlier occurrence. Use these rows with that in mind.

## Śāstraprakāśikā (Ānandagiri on Sureśvara's Bṛhad-vārttika)

The target is the n-th word of the vārttika verse the note explains. Words are counted the way the reader counts them:
Devanāgarī runs, with daṇḍas, verse numbers (e.g. «२४८» inside a block) and the hidden पद copies excluded.

The pratīka-to-word number was assigned when the ṭīkā text was prepared (outside the reading-view resolver). All 6,733 were
checked against their verses: the reader had counted mid-block verse numbers as words (26 pratīkas landed a word early; fixed),
and two targets were wrong in the data (4.3/443, intro/201; corrected). 2 rows remain marked `;check` (1.4/558 «किं त्विति»
→ किंतु, 4.4/275 «यो वेदेति» → योऽकाम): the target is plausible but the quoted word and the target spell differently.

## Counts

*detected = pratīkas found by detection rather than printed marks (see above).*

| file (text-lane) | pratīkas | linked | → bhāṣya | → mūla | → other | not linked | detected* |
|---|---:|---:|---:|---:|---:|---:|---:|
| isha-bhashya | 310 | 294 (94.8%) | 0 | 294 | 0 | 16 | 0 |
| isha-anandagiri | 83 | 56 (67.5%) | 55 | 1 | 0 | 27 | 0 |
| kena-bhashya | 532 | 462 (86.8%) | 0 | 462 | 0 | 70 | 0 |
| kena-anandagiri | 123 | 116 (94.3%) | 116 | 0 | 0 | 7 | 0 |
| katha-bhashya | 1,877 | 1,789 (95.3%) | 0 | 1,789 | 0 | 88 | 0 |
| katha-anandagiri | 150 | 129 (86.0%) | 129 | 0 | 0 | 21 | 0 |
| prashna-bhashya | 1,503 | 1,413 (94.0%) | 0 | 1,413 | 0 | 90 | 0 |
| prashna-anandagiri | 685 | 630 (92.0%) | 628 | 2 | 0 | 55 | 0 |
| mundaka-bhashya | 1,162 | 1,102 (94.8%) | 0 | 1,102 | 0 | 60 | 0 |
| mundaka-anandagiri | 142 | 116 (81.7%) | 116 | 0 | 0 | 26 | 0 |
| mandukya-bhashya | 2,289 | 2,030 (88.7%) | 0 | 2,030 | 0 | 259 | 0 |
| mandukya-anandagiri | 2,259 | 2,037 (90.2%) | 1,944 | 93 | 0 | 222 | 0 |
| taittiriya-bhashya | 1,759 | 1,398 (79.5%) | 0 | 1,398 | 0 | 361 | 0 |
| taittiriya-anandagiri | 382 | 355 (92.9%) | 354 | 1 | 0 | 27 | 0 |
| taittiriya-vanamala | 2,487 | 2,012 (80.9%) | 1,976 | 36 | 0 | 475 | 0 |
| aitareya-bhashya | 618 | 564 (91.3%) | 0 | 564 | 0 | 54 | 0 |
| aitareya-anandagiri | 796 | 726 (91.2%) | 722 | 4 | 0 | 70 | 0 |
| chandogya-bhashya | 9,753 | 8,800 (90.2%) | 0 | 8,800 | 0 | 953 | 0 |
| chandogya-anandagiri | 3,932 | 3,360 (85.5%) | 3,331 | 29 | 0 | 572 | 0 |
| brihadaranyaka-bhashya | 12,611 | 11,186 (88.7%) | 0 | 11,186 | 0 | 1,425 | 0 |
| brihadaranyaka-anandagiri | 8,811 | 7,410 (84.1%) | 7,270 | 140 | 0 | 1,401 | 0 |
| brihadaranyaka-shastraprakashika | 6,733 | 6,733 (100.0%) | 0 | 0 | 6,733 | 0 | 0 |
| gita-bhashya | 9,273 | 8,890 (95.9%) | 0 | 8,890 | 0 | 383 | 0 |
| gita-bhashyarka | 10,593 | 6,604 (62.3%) | 6,532 | 72 | 0 | 3,989 | 0 |
| gita-dhanapati | 310 | 201 (64.8%) | 191 | 10 | 0 | 109 | 0 |
| gita-madhusudani | 3,715 | 3,502 (94.3%) | 0 | 3,502 | 0 | 213 | 3,566 |
| gita-nilakanthi | 3,113 | 2,911 (93.5%) | 0 | 2,911 | 0 | 202 | 2,526 |
| gita-shankaranandi | 4,015 | 3,712 (92.5%) | 0 | 3,712 | 0 | 303 | 3,408 |
| gita-sridhari | 3,038 | 2,854 (93.9%) | 0 | 2,854 | 0 | 184 | 2,341 |
| gita-anandagiri | 5,013 | 4,475 (89.3%) | 4,468 | 7 | 0 | 538 | 0 |
| brahmasutra-bhashya | 1,834 | 1,396 (76.1%) | 0 | 1,396 | 0 | 438 | 0 |
| brahmasutra-brahmatattvaprakashika | 661 | 606 (91.7%) | 0 | 606 | 0 | 55 | 661 |
| brahmasutra-ratnaprabha | 4,316 | 3,769 (87.3%) | 3,703 | 66 | 0 | 547 | 0 |
| brahmasutra-purnanandi | 1,498 | 835 (55.7%) | 0 | 0 | 835 | 663 | 0 |
| brahmasutra-nyayanirnaya | 11,659 | 10,250 (87.9%) | 10,088 | 162 | 0 | 1,409 | 0 |
| vivekacudamani-vyakhya-candrasekhara | 5,082 | 5,082 (100.0%) | 0 | 5,082 | 0 | 0 | 0 |
| atmabodha-tika-padmapada | 373 | 373 (100.0%) | 0 | 373 | 0 | 0 | 0 |
| saddarshanam-tika-kapali | 656 | 656 (100.0%) | 0 | 656 | 0 | 0 | 0 |
| upadesasaram-bhashya-ganapati | 170 | 170 (100.0%) | 0 | 170 | 0 | 0 | 0 |
| **total** | **124,316** | **109,004** (87.7%) | | | | **15,312** | |


The unlinked rows are mostly words that occur more than once in the verse or passage, so no unique target exists. Other
reasons:
- Gītā 1.1–2.10 has no Śaṅkara-bhāṣya, so most Bhāṣyārka pratīkas there have nothing to link to.
- Pratīkas that quote a different passage.
- Readings where our text and the commentary's edition differ.

**Mūla targets mapped to the deposit** (column `target_deposit`; Gītā and BS keys already carry the deposit word/pada; for
the other texts our padaccheda was aligned verse by verse with the deposit's `p` splits). Every `w<i>.p<j>` was checked
against the deposit's pada text.

| text | deposit file | our mūla words | mapped |
|---|---|---:|---:|
| Isha | `prasthan-words-Isha.json` | 285 | 285 |
| Kena | `prasthan-words-Kena_pada.json` | 598 | 596 |
| Kathaka | `prasthan-words-Kathaka.json` | 1,986 | 1,976 |
| Prashna | `prasthan-words-Prashna.json` | 1,521 | 1,518 |
| Mundaka | `prasthan-words-Mundaka.json` | 1,163 | 1,151 |
| Mandukya | `prasthan-words-Mandukya.json` | 2,956 | 2,948 |
| Taitiriya | `prasthan-words-Taitiriya.json` | 2,318 | 2,308 |
| Aitareya | `prasthan-words-Aitareya.json` | 833 | 832 |
| Chandogya | `prasthan-words-Chandogya.json` | 15,566 | 15,518 |
| Brha | `prasthan-words-Brha.json` | 18,409 | 18,280 |
| Gita | `prasthan-words-Gita.json` | 9,029 | 9,029 |
| BS | `prasthan-words-BS.json` | 2,069 | 2,069 |


## Known limits

- Unlinked does not mean "not a pratīka". It means no single target could be chosen.
- `marked:tamal-or-mri` (Vanamālā) does not say which source marked each item. Bhāṣya rows with an empty `mark` have no
  recorded source.
- VC: 6 notes consisting only of a remark such as «स्पष्टोऽर्थः» used to be linked to the verse's first word by our reader;
  that rule was removed (2026-10-25), so they have no rows here.
- Prakaraṇa rows use the weaker first-unused-match method described above.
- The vārttikas, the Vaiyāsika-nyāya-mālā and the Vārtikasāra are placed by section or position. They have no word-level
  pratīka links, so they do not appear here.

## Whose data this is

- The texts of the **Vanamālā**, **Ratnaprabhā** and **Pūrṇānandī**, the alignment of their notes to the bhāṣya, and their
  pratīka marks come from **Sri Tamal Maharaj's** Śaṅkara reader. Each Pūrṇānandī pratīka's pinned Ratnaprabhā word (835 of
  them) is his alignment, re-checked here exact-or-nothing.
- The Śrīdharī and Madhusūdanī texts and the Śrīdharī bold marks are from his Gītā readers.
- The Gītā/BS mūla padaccheda, against which several lanes are detected and resolved, is from his deposit.
- His multi-word pratīka runs were used as a placement hint for 24 links.
- Everything else here (marking, resolution, adjudication, the export) is adhyayana-sahakārī's.
