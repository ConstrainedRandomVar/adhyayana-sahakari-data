# annotations/: reading layers on the commentaries

These are optional reading layers made by **adhyayana-sahakārī**: the discourse roles of the bhāṣya, the gloss and
tātparya connectors, citation targets, pramāṇa grading, and a mahāvākya catalogue. Most of the work is machine-made,
with hand corrections, so it may contain errors. What each class means, where the scheme came from and how it was
applied: **[SCHEME.md](SCHEME.md)**.

## Licence

**CC BY 4.0, covering the annotation only.** Attribute to "adhyayana-sahakārī".

The commentary text inside these files is included so that the markup can be read and checked. The licence does not
cover the text:
- **Śaṅkara-bhāṣya** (`bhashya-roles/` except `vc*`): the advaitaśārada digital text, which is the same text the Zenodo
  deposit 10.5281/zenodo.21279193 carries (© Dakshinamnaya Sri Sharada Peetham, Sringeri), with the corrections in
  `corrections/` applied.
- **Vivekacūḍāmaṇi vyākhyā** (`bhashya-roles/vc*`, `tika-roles/vc.json`): the advaitaśārada digital text, checked
  against the 1952 Śṛṅgeri printing.
- **Saddarśanam, Upadeśa Sāram and Ātmabodha ṭīkās** (`tika-roles/`): the text is as described in
  `etexts/` (source, edition and status for each).

## Files

| file | contents |
|---|---|
| `bhashya-roles/<text>.json` | per passage: `text`, `segments` [{`t`, `c`: classes}] that concatenate to `text` exactly, `connectors` [[offset, `=`/`→`]], `citations` [{start, end, label, target {work, ref}}] |
| `bhashya-roles/<text>.standoff.json` | the same, as `[start, end, class]` spans over the passage text (UTF-16 offsets) |
| `tika-roles/<text>.json` | sentence-level roles for the prakaraṇa commentaries: per sentence `text`, `words`, `roles` [{role, fromWord, toWord}] |
| `pramana.json` | text → ref → [{role, text, pramana}], one entry per discourse segment |
| `mahavakya.json` | text → verse ref → {subtype, label, anchor} |
| `COUNTS.json` | per text: passages, characters and spans per class, connectors, citations |

Texts in `bhashya-roles/`: isha, kena (pada-bhāṣya), kathaka, prashna, mundaka, mandukya (with the kārikā),
taitiriya, aitareya, chandogya, brha, gita, bs, vc.

## Counts

Inline layer, spans per class:

| text | passages | annotated | pūrvapakṣa | siddhānta | ekadeśī | saṅgraha | mūla | gloss | tātparya | vyākaraṇa | quote | `=` / `→` | citations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Īśāvāsya | 34 | 34 | 8 | 10 | 0 | 8 | 207 | 138 | 19 | 31 | 36 | 142 / 20 | 20 |
| Kena (pada-bhāṣya) | 31 | 31 | 16 | 18 | 1 | 5 | 339 | 102 | 10 | 21 | 66 | 155 / 9 | 9 |
| Kaṭha | 124 | 124 | 19 | 195 | 0 | 13 | 1217 | 680 | 39 | 87 | 30 | 733 / 37 | 4 |
| Praśna | 68 | 68 | 30 | 74 | 1 | 20 | 823 | 286 | 20 | 38 | 15 | 328 / 22 | 0 |
| Muṇḍaka | 70 | 70 | 12 | 60 | 1 | 16 | 829 | 558 | 19 | 62 | 37 | 553 / 19 | 7 |
| Māṇḍūkya + kārikā | 222 | 222 | 114 | 331 | 0 | 40 | 1334 | 424 | 58 | 85 | 127 | 403 / 54 | 4 |
| Taittirīya | 53 | 53 | 73 | 103 | 6 | 65 | 1080 | 374 | 23 | 76 | 99 | 361 / 24 | 3 |
| Aitareya | 43 | 43 | 32 | 78 | 1 | 22 | 391 | 117 | 2 | 11 | 80 | 170 / 2 | 48 |
| Chāndogya | 591 | 591 | 189 | 413 | 14 | 122 | 5117 | 1717 | 165 | 299 | 264 | 1829 / 146 | 12 |
| Bṛhadāraṇyaka | 449 | 449 | 335 | 973 | 50 | 254 | 6546 | 2151 | 144 | 332 | 645 | 2095 / 136 | 88 |
| Bhagavad-gītā | 1132 | 1131 | 172 | 283 | 13 | 154 | 5070 | 3133 | 163 | 551 | 427 | 3220 / 158 | 122 |
| Brahma-sūtra | 670 | 670 | 623 | 983 | 27 | 297 | 1151 | 176 | 12 | 121 | 2148 | 116 / 11 | 58 |
| Vivekacūḍāmaṇi vyākhyā | 477 | 477 | 38 | 37 | 1 | 0 | 3474 | 1534 | 464 | 341 | 583 | 1254 / 67 | — |

A "span" is a maximal run of text carrying the class, so one long objection counts once.

Sentence roles (`tika-roles/`), number of role ranges:

| text | passages | sentences | pūrvapakṣa | siddhānta | ekadeśī | dṛṣṭānta | lakṣaṇa | phalita |
|---|---|---|---|---|---|---|---|---|
| Vivekacūḍāmaṇi vyākhyā | 472 | 3514 | 65 | 96 | 0 | 276 | 171 | 363 |
| Saddarśanam ṭīkā | 44 | 576 | 12 | 65 | 1 | 18 | 11 | 60 |
| Upadeśa Sāram bhāṣya | 30 | 209 | 11 | 32 | 0 | 0 | 6 | 36 |
| Ātmabodha ṭīkā | 67 | 287 | 33 | 38 | 0 | 42 | 5 | 30 |

Pramāṇa grading, segments per grade (śruti / yukti / anubhava / none):
- Īśa 3/8/0/3
- Kena 3/20/1/9
- Kaṭha 0/15/2/32
- Praśna 4/55/0/5
- Muṇḍaka 1/13/0/14
- Māṇḍūkya 10/89/10/53
- Taittirīya 12/86/8/40
- Aitareya 8/44/3/13
- Chāndogya 32/158/3/115
- Bṛhadāraṇyaka 36/154/6/82
- Gītā 28/165/14/182
- Saddarśanam ṭīkā 4/24/3/46
- Vivekacūḍāmaṇi vyākhyā 4/22/1/60

The Brahma-sūtra bhāṣya is not graded.

Mahāvākya catalogue: 188 verses across 16 texts.

## Fidelity

Each passage's `segments` were checked to rejoin exactly to its `text`. The text is the one our reading views use,
after the adjudicated corrections; 0 mismatches. The Śaṅkara-bhāṣya text carries no daṇḍas (as in the deposit's prose);
our site re-inserts them from the reader copy.
