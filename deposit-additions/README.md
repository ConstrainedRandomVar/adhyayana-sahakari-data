# Additions to Sri Tamal Maharaj's bhāṣya-word data

Keyed by **his surface forms** (the keys of `data/bhasya-words-ALL.json` in his Zenodo deposit, CC BY 4.0), so each row can be
folded straight back into his dictionary. His `p` (padaccheda) and `g` (grammar) are quoted next to our addition, with credit.

## `bhasya-vigraha.json` — samāsa vigraha for compounds that have none

- **What was missing:** 20,153 surface forms whose padaccheda `p` marks a compound (a hyphen between members) carry no vigraha,
  and for 16,685 of them `g` does not name the samāsa type either (a terse entry such as `लोकबुद्धि-सिद्ध नपुं॰ १।१`; contrast
  `स्वाभाविक-कर्म-विज्ञान (तत्पुरुष/कर्मधारय) …`). A reader hovering such a compound gets its split but no analysis, and anything
  that keys on the samāsa type (e.g. a samāsa drill) silently skips it.
- **What we add:** a vigraha for each of the 20,153: `words[surface] = { p, g, vigraha: [{ part?, layers: [{c, vigraha, type,
  pratyaya?, sutra?}], stripped?, source }], occ: [{text, refs}] }`. `layers[0]` is the whole compound, then each multi-member or
  derived (kṛt/taddhita) member, depth-first. `part` is set when the surface is a fused multi-word token and the vigraha is for
  one compound inside it. `stripped` lists members the model returned that do not occur in the compound (removed by a
  consonant-skeleton check). `occ` gives where the form occurs.
- **Provenance:** machine-made — Gemini 3.8 Flash, samāsa-only prompt (`prompts/samasa/bhasya-samasa-vigraha.md`) with his `p`
  as the split hint, temperature 0, 2026-10-25 (20,067 rows), or reused from the same compound analysed elsewhere in our data
  (1,050). Sūtra numbers are the model's. Not individually reviewed by a scholar; a hand check of a sample found most sound.
  Five forms the model judged not to be compounds (होयि, कश्चित्, कस्मिंश्चित्, …) are left out.

## `bhasya-vigraha-earlier.json` — the vigrahas our site already showed before 2026-10-25

- **What:** 25,492 more of his surface forms (padaccheda marks a compound) for which our reading cards showed a vigraha from
  earlier runs, before the file above existed. Same row shape: `words[surface] = { p, g, vigraha: [{ part?, layers, source,
  shownIn? }], occ: [{text, refs}] }`, with his `p`/`g` quoted.
- **How it was mapped (exact, never guessed):** for every page of our reading site, the word card of each of his surface
  forms was read as the site shows it, and matched line for line against our stored samāsa peels to recover the full layers
  (with sūtra and pratyaya, which the card does not print) and the run that produced them. Every card matched exactly
  (0 unmapped). `part` is the stored key, set when a card joins several stored peels (a fused multi-word token, or a member
  peel). `shownIn` lists the texts, where the same form's card differs between texts (182 forms). Forms whose card is fully
  explained by the 2026-10-25 file above are left out (already delivered); 189 forms appear in both because some page shows
  an older or a mixed peel for them, and that is what is given here.
- **`source` — the producing run** (number of vigraha entries): 2026-08-27 samāsa-only backfill 12,378 · 2026-09-24 gap
  recovery (gemini-3.7-flash) 12,405 + 2 reused · 2026-08-20 batch (the samāsa field of the first Gemini 3.7 kāraka/morph
  run; the least trusted) 1,276 · mūla-quote reuse (the same compound's peel in the root text) 893 · 2026-10-01
  sentence-aware regap (gemini-3.7-flash, with the bhāṣya sentence as context) 195 · same-verse reuse from our shared samāsa
  dictionary 61 · 2026-10-25 split-gap 236 (parts inside fused tokens whose other parts are older).
- **Counts, reconciled:** our site's coverage report counts compound word-instances per page (a word on several pages counts
  each time): 51,010, of which 33 are deliberate blanks. Per page, the 2026-10-25 map supplies 21,414 and earlier runs the
  rest; over distinct surface forms that is the 20,153 of the first file and the 25,492 here. Not included: 6,644 forms that
  carry a derivation peel (kṛt/taddhita) but whose padaccheda shows no compound, and 3 forms not in the deposit.
- **Machine-made, not scholar-reviewed;** the 2026-08-20 rows especially deserve checking.

