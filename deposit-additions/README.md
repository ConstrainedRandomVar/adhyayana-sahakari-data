# Additions to Sri Tamal Maharaj's bhāṣya-word data

Keyed by **his surface forms** (the keys of `data/bhasya-words-ALL.json` in his Zenodo deposit, CC BY 4.0), so each row can be
folded straight back into his dictionary. His `p` (padaccheda) and `g` (grammar) are quoted next to our addition, with credit.
Regenerated 2026-10-26 from the final samāsa peel of our reading site (after a review pass that dropped wrong layers and added
whole-compound vigrahas).

## The gap these files fill

The deposit's `bhasya-words-ALL.json` has no vigraha for any compound: every entry carries only `p`, `g`, `m` and `c`. Of its
95,585 entries, 46,101 are split as compounds (a hyphen between members, not counting upasarga + verb splits). 19,539 of those
name the samāsa type in `g`, 4,994 name a derivation (a kṛt or taddhita suffix), and 21,568 name neither — so for nearly half
the compounds there is no samāsa classification at all (a terse entry such as `लोकबुद्धि-सिद्ध नपुं॰ १।१`, where others read
`स्वाभाविक-कर्म-विज्ञान (तत्पुरुष/कर्मधारय) …`). A reader hovering such a compound gets its split but no analysis, and anything
that keys on the samāsa type silently skips it. **The two files below together give a vigraha — with the samāsa type, member
by member — for 45,466 of the 46,101.** Counts measured against the deposit with the same compound test (a split token with a
non-upasarga hyphen).

## What a row looks like (both files)

`words[surface] = { p, g, vigraha: [{ part?, layers: [{c, vigraha, type, pratyaya?, sutra?}], source, stripped?, shownIn? }],
occ: [{text, refs}], fixNote? }`

- Each vigraha entry is **exactly what our reading card shows** for that form, with the full layers (incl. sūtra and pratyaya,
  which the card does not print) recovered from our stored peel and the run that produced them (`source`). `layers[0]` is the
  whole compound, then each multi-member or derived (kṛt/taddhita) member, depth-first.
- **Excluded:** 148 layers we reviewed by hand and found wrong for a given word, and layers that describe another word (a card
  shows only layers about its own word); duplicate lines are folded. None of the excluded layers appears in either file.
- `part` = the stored key, set when a card joins several stored peels (a fused multi-word token, or a member peel).
  `shownIn` lists the texts, where the same form's card differs between texts. `stripped` lists members the 2026-10-25 run
  returned that do not occur in the compound (removed by a consonant-skeleton check). `occ` gives where the form occurs.
- Every card line was traced to a stored layer (0 untraced); nothing was guessed.

## Which file a form is in

- **`bhasya-vigraha.json` — 20,720 forms.** The first (whole-compound) layer of every card that shows the form comes from one of
  the two runs made for this gap: the 2026-10-25 split-gap run (compounds marked only by the padaccheda split) or the
  2026-10-26 whole-compound run (compounds whose card had no whole-compound vigraha). Lower layers may come from older runs.
- **`bhasya-vigraha-earlier.json` — 24,746 forms.** The first layer of at least one card comes from an earlier run
  (2026-08-20 … 2026-10-01).
- **`lost-all-layers.json` — 5 forms** that were in the previous version of these files but whose cards now show no vigraha (every
  layer was garbled or about another word, e.g. «हृदहालय» for हृदयालय). Listed so nothing is dropped silently.

## `uncertain`

A layer carrying `"uncertain": true` is one our own review judged low-confidence (2026-10-27): the reading card shows it with a mark
rather than hiding it. Treat these as the least reliable rows.

## `source` — the producing run (number of vigraha entries)

| Run | in `bhasya-vigraha.json` | in `bhasya-vigraha-earlier.json` |
|---|---|---|
| gemini-3.8-flash 2026-10-25 split-gap run | 19,468 | 428 |
| gemini-3.8-flash 2026-10-26 whole-compound run | 2,433 | 59 |
| 2026-09-24 gap recovery (gemini-3.7-flash; exact-surface map) | 1,655 | 11,664 |
| 2026-08-27 samāsa-only backfill | 896 | 12,206 |
| 2026-08-20 batch (samāsa field of the first Gemini 3.7 kāraka/morph run; least trusted) | 93 | 1,377 |
| mūla-quote reuse (the same compound's peel in the root text) | 234 | 1,447 |
| 2026-10-01 sentence-aware regap (gemini-3.7-flash, with the bhāṣya sentence as context) | 77 | 253 |
| same-verse reuse from our shared samāsa dictionary | 38 | 311 |

Prompts: `prompts/samasa/`. Sūtra numbers are the model's.

## Changes from the first version (2026-10-25/26)

`bhasya-vigraha.json` 20,153 → 20,720 forms; `bhasya-vigraha-earlier.json` 25,492 → 24,746. About 2,300 forms moved into the
first file and about 1,600 into the second under the cleaner rule above (by the source of the whole-compound layer); 899 and
892 forms changed layers (wrong or other-word layers removed, whole-compound vigrahas added); 5 forms lost all layers. Deposit
coverage 45,456 → 45,466.

Not included: 6,636 forms that carry a derivation peel (kṛt/taddhita) but whose padaccheda shows no compound, and 3 forms not
in the deposit.

**Machine-made, not scholar-reviewed;** the 2026-08-20 rows especially deserve checking.
