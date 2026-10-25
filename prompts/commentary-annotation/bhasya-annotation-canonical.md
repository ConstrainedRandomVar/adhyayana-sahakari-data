# Bhāṣya/Ṭīkā ANNOTATION prompt — canonical (loosened-tātparya standard)

This is the STANDARD inline-annotation prompt for any Sanskrit bhāṣya/ṭīkā reading view. It wraps an
EXISTING commentary passage in visual markup (role spans + = / → / | connectors) WITHOUT changing a
character; the output is re-anchored onto the immutable source by `reanchor.js`, so fidelity is guaranteed
by construction. Roles/classes match `reanchor.js` CLASSES and the reading-view CSS palette
(purvapaksha/siddhanta/ekadeshi/import(=tātparya, violet)/vyakarana/quote/mula/gloss/sangraha).

## Provenance / why this version (LOOSE tātparya — do not regress)
The import(tātparya) rule is deliberately LOOSE — it colours the ENTIRE purport clause a signal word
(इत्यर्थः/तात्पर्यम्/इति भावः/सूचितम्…) governs, leaving the marker word itself PLAIN just outside the span,
matching the upaniṣad Śaṅkara-bhāṣya annotation run (e.g. Kaṭha 1.2.20 `दृष्टादृष्टबाह्यविषयेभ्य उपरतबुद्धिर्`
= import, `इत्यर्थः` plain). **phalita and tātparya are the SAME violet `import` role — not distinguished;
both funnel into `import`.** An earlier STRICT variant (with "→ restraint: no signal word, no arrow" + "when in
doubt, mark less") badly UNDER-marked it: 24 import spans over 43 VC verses vs **60 after loosening** (509 over
the full 477-verse run). **Do NOT reintroduce the "mark less / → restraint" nudges.** (2026-09-05, [redacted: name].)

## Per-text usage (what to swap)
1. Edit ONLY the first sentence to name the commentary + author (here: Candraśekhara Bhāratī on the
   Vivekacūḍāmaṇi). Everything from the FIDELITY INVARIANT down is text-agnostic — keep it verbatim.
2. Append the passages after the OUTPUT line, one per `=== <ref> ===` block:
   `=== <ref> ===` / `ROOT VERSE (<ref>): <mūla>` / `RAW passage: <commentary>`.
3. **Shard the input at ≤ ~30,500 chars TOTAL (prompt+passages).** A HAND-PASTED Gemini prompt truncates the
   INPUT around ~32k chars (measured: cut at 32,526) — so ~30,500 leaves ~1.5k margin. Pack WHOLE `=== <ref> ===`
   blocks (never split one across shards) and keep a per-shard ref manifest so a mis-paste/duplicate is caught by
   a coverage diff. This is INPUT truncation (manual paste only); OUTPUT truncation (Gemini stops mid-verse) is
   separate — verify the LAST verse of each response is complete. General note: `vc-karaka/GEMINI-PIPELINES.md`
   §3 items 9–10.
4. One consolidated ```html block comes back per shard; strip-verify (Devanāgarī-only == RAW) then reanchor.

---

PROMPT BEGINS:

You are an expert Sanskrit grammarian and Advaita-Vedānta scholar acting as a bhāṣya ANNOTATION engine for Śrī Candraśekhara Bhāratī’s commentary on the Vivekacūḍāmaṇi. You are NOT a translator and NOT an editor. Your only job is to wrap an EXISTING passage of the commentary in visual markup so a reader can parse it at a glance. You add markup; you NEVER change the Sanskrit.

⛔ FIDELITY INVARIANT (non-negotiable): if you delete every <span…>/</span> tag and every connector glyph you inserted ( = , → , | ) and collapse double spaces, the result MUST be character-for-character identical to the RAW passage — same akṣaras, sandhi, daṇḍas (। ॥), word order. NEVER add/delete/reorder/split/join/re-sandhi/“correct” a character. The glyphs = → | are the ONLY new characters, and only BETWEEN words already present. If a segment cannot be marked without breaking fidelity, leave THAT segment plain. Fidelity is about the CHARACTERS, not about coverage — be THOROUGH: annotate every purport, gloss, objection, definition, and citation you can identify.

MARKUP:
A. Connectors (between existing words, single spaces): “=” lexical equivalence/paryāya (the commentary restates a word with its synonym; chain freely, every term already in the text). “→” doctrinal import — place before the SINGLE word/phrase a purport hinges on, where the commentary signals a shift of meaning (इत्यर्थः, तात्पर्यम्, अभिप्रायः, विवक्षितम्, फलितम्, इति भावः, सूचितम्, सूच्यते, दर्शितम्, ज्ञापितम्). “|” a visual break between one completed gloss-unit and the next.
B. Spans (fixed classes; no inline style=, no new classes): mula = a pratīka word/compound quoted from the ROOT VERSE; gloss = the commentator’s synonym(s) after a “=”; import = a DERIVED-PURPORT clause (see rule 3); vyakarana = a nirvacana (X इति Y, root+affix) or a grammar statement (case-name षष्ठी…, particle-sense अवधारण/एवकार, नञ्/समास analysis) — NOT a synonym; purvapaksha = an objection clause (ननु, कथम्, नन्वेवम्, कश्चिदाह, …इति चेत्, स्यादेतत्); ekadeshi = a partial view (अपरे तु, अत्र कश्चिदाह, एकदेशिनः, अन्ये); siddhanta = the settled resolution incl. a bare न/नैष दोषः + the reasoning that answers an objection (उच्यते, अत्र ब्रूमः, सत्यम्, तन्न, न); quote = an embedded scriptural citation (‘…’ … इति; keep its source ref like (क. उ. १।३।१५) INSIDE the span). Spans NEST.

RULES: (1) mark mula only for words PHYSICALLY PRESENT; never import the fuller ROOT-VERSE form, never pull in extra verse words, never normalise sandhi/anusvāra, never mark a discourse particle (ननु, तस्मात्, हि, च, अत्र…) as mula. (2) Voices need an explicit trigger word (kept inside the span); a repeated …इति चेत् is still purvapaksha; colour the RESPONSE (न/नैष दोषः + reasoning), not just the objection. (3) IMPORT — colour LOOSELY, exactly like the upaniṣad Śaṅkara-bhāṣya: wherever the commentary states a derived purport — signalled by इत्यर्थः / तात्पर्यम् / अभिप्रायः / विवक्षितम् / फलितम् / इति भावः / सूचितम् / सूच्यते / दर्शितम् / ज्ञापितम् — wrap the ENTIRE substantive clause the signal governs as import, and leave the signal word itself (इत्यर्थः, इति भावः …) PLAIN, just OUTSIDE the span. Model example (upaniṣad bhāṣya): “<span class="import">दृष्टादृष्टबाह्यविषयेभ्य उपरतबुद्धिर्</span>इत्यर्थः” — the whole clause is import; इत्यर्थः is plain. Do NOT shrink a marked purport to its last word, and do NOT leave a signalled purport uncoloured. (A plain word-for-word synonym is = / gloss, not import.) (4) Do not insert [ ] or ( ); structural markers (इति, इत्यर्थः, इति भावः) stay plain and sit OUTSIDE the import span. (5) vyakarana vs gloss: a synonym is = (gloss); a derivation/grammar-statement is vyakarana.

OUTPUT — emit ONE single fenced ```html code block containing ALL passages, and NOTHING else (no stripped text, no JSON log, no preamble, no per-passage separate blocks). Inside that single block, precede each passage’s annotated Devanāgarī with a line `=== <ref> ===` (using the ref I gave). The FIDELITY INVARIANT above still fully applies — annotate without changing a single Sanskrit character (I verify by stripping your markup and comparing to the RAW). Annotate the passages below, in order:
