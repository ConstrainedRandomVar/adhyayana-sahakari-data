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
- Not included yet: vigrahas for the ~30,800 compounds that already had one on our site from earlier runs (mostly where his `g`
  names the type); they can follow in the same shape.
