# adhyayana-sahakārī — data

Data behind the reading site **adhyayana-sahakārī** (https://constrainedrandomvar.github.io/adhyayana-sahakari/): our
corrections to digital Vedānta texts, pratīka alignments, reading annotations, grammatical analyses and translations,
and our own transcriptions of older printed commentaries.

Much of the site rests on the word-level digital reader of the Prasthānatrayī with Śaṅkara's bhāṣya by Sri Tamal Maharaj
(RKMVERI; Zenodo [10.5281/zenodo.21279193](https://doi.org/10.5281/zenodo.21279193), CC BY 4.0; arXiv:2607.07282) and on
the digital texts of advaitaśārada (Dakshinamnaya Sri Sharada Peetham, Sringeri). See the site's *Sources & attribution* page.

## Licence

Our own work in this repository is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)** — see
`LICENSE`. Please attribute it to **adhyayana-sahakārī**, with a link to the site or this repository.

Our own work means: the corrections and errata lists, the pratīka alignments, the annotation layers (roles, pramāṇa,
mahāvākya), the grammatical analyses (machine-made, see below), the translations, and our transcriptions of the printed
editions in `etexts/` (the underlying works and prints are, as far as we know, in the public domain; see `etexts/README.md`).

**Not covered by our licence** — third-party material that keeps its owners' terms:

- **advaitaśārada digital texts** (© Dakshinamnaya Sri Sharada Peetham, Sringeri): the Śaṅkara-bhāṣyas, Ānandagiri's ṭīkās,
  Sureśvara's vārttikas, the Nyāyanirṇaya and the Vivekacūḍāmaṇi vyākhyā. Some annotation and analysis files reproduce this
  text so that the annotation can be read in place; our licence covers the annotation only.
- **Sri Tamal Maharaj's data** — his Zenodo deposit (CC BY 4.0) and the data of his Vedānta and Śaṅkara readers, which are
  the source of several fields and alignments here (marked per field / per file).
- **Gita Supersite (IIT Kanpur)** texts (Nīlakaṇṭha, Dhanapati), the **Dakshinamurti Math** Bhāṣyārkaprakāśa, the
  **sanskritdocuments.org** text of Gaṇapati Muni's Upadeśasārabhāṣya, the **UoHyd** e-reader kāraka data (Gītā), and the
  1964 Vicārasāgara edition. We list corrections to these texts, not the texts themselves, except where an annotation file
  carries the passage it annotates (stated in that folder's README).

## Contents

| Folder | What | README |
|---|---|---|
| `corrections/` | Corrections to digital texts (advaitaśārada, Zenodo deposit, Gita Supersite, his e-texts …), each with location, original reading, corrected reading and printed witness. The advaitaśārada sets correct the **digital text**; the Mahesh Research Institute print is the witness. | `corrections/README.md` |
| `alignments/` | Pratīka alignments: which base-text word each commentary pratīka explains (124,316 pratīkas; 109,004 linked to exactly one word). Method in `METHOD.md`. | `alignments/METHOD.md` |
| `annotations/` | Reading annotations of the bhāṣyas and ṭīkās: argument roles (pūrvapakṣa, ekadeśī, siddhānta, gloss, tātparya, saṅgraha …), resolved citations, pramāṇa grades, mahāvākya verses. **Machine-applied** under the scheme in `SCHEME.md`. | `annotations/README.md` |
| `analyses/` | The grammatical corpus (morphology, kāraka, samāsa, meanings), every field tagged with its source (ours/machine, Tamal Maharaj's deposit, UoHyd), plus ṭīkā word analyses and English translations. | `analyses/README.md` |
| `etexts/` | Our transcriptions of printed commentaries: Brahmatattvaprakāśikā, Śaṅkarānandī, Bṛhadāraṇyaka-vārttikasāra with Laghusaṅgrahā, Ātmabodha with Padmapāda's ṭīkā, Saddarśanam with Kapāli Śāstrī's bhāṣya. | `etexts/README.md` |

## Caveats

Machine-made layers (annotations, analyses, translations) were produced with Google Gemini models and checked by rule-based
gates and partial human review; they contain errors. Corrections are listed only where a printed edition confirms them.
Disagreements and errors are welcome — please use "report an issue" on any page of the site, or open an issue here.
