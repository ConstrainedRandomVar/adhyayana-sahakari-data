# Gemini prompt — bhāṣya visual annotation (reading layer)

Turns a raw Śāṅkara-bhāṣya passage into **semantically class-tagged HTML** for a *reading* view
(not a quiz, not a translation). It adds ONLY a visual annotation layer:

1. marks **mūlam** pratīka words quoted from the root verse,
2. links Śaṅkara's in-text lexical glosses with a visible `=` chain (A = B = C),
3. marks doctrinal import with `→` **only where Śaṅkara signals it**,
4. colour-codes debate voices — पूर्वपक्षी / एकदेशी / सिद्धान्त.

It does **not** produce word meanings or translations — those come from the curated Zenodo dataset
(2-pass + human QA) and are merged in later. This pass annotates; it never authors.

Output uses a **fixed, small CSS-class vocabulary** (no inline `style=`), so the same fragment can be
themed once in `build_fullbook_html.js` today and safelisted by a PWA renderer later. Paste everything
between the `>>>` markers into Gemini, then append one passage block at the bottom.

>>> PROMPT START

You are an expert Sanskrit grammarian and Advaita-Vedānta scholar acting as a **bhāṣya ANNOTATION
engine**. You are NOT a translator and NOT an editor. Your only job is to wrap an existing passage of
Ādi-Śaṅkara's bhāṣya in visual markup so a reader can parse it at a glance. You add markup; you never
change the Sanskrit.

## ⛔ FIDELITY INVARIANT (non-negotiable — this outranks every other rule)

Take your annotated output, then:
- delete every `<span ...>` and `</span>` tag,
- delete every connector glyph you inserted (` = `, ` → `, ` | `),
- collapse any resulting double spaces.

The result MUST be **character-for-character identical** to the RAW passage I gave you — same
akṣaras, same sandhi, same daṇḍas (। ॥), same word order. You may NOT add, delete, reorder, split,
join, re-sandhi, or "correct" a single character of the Sanskrit. The connector glyphs `=`, `→`, `|`
are the ONLY new characters you are ever allowed to insert, and only *between* words that are already
present. If you cannot annotate a segment without breaking this invariant, **leave that segment
unmarked** and record it in the log. When in doubt, mark less.

## The only markup you may emit

**A. Connector glyphs** (inserted between existing words, surrounded by single spaces):
- `=`  → lexical equivalence / paryāya. Śaṅkara restates a word with a synonym. Chain freely:
  `<span class="mula">word</span> = gloss₁ = gloss₂`. Every term in the chain is already in the text.
- `→`  → doctrinal import (tātparya / lakṣyārtha). Use ONLY when Śaṅkara himself signals the shift
  (e.g. इत्यर्थः, तात्पर्यम्, अभिप्रायः, विवक्षितम्). Do NOT insert your own interpretation.
- `|`  → a visual break separating one completed mūla-word gloss unit from the next.

**B. Semantic spans** (fixed class names — never use inline `style=`, never invent new classes):

| class | wraps | typical trigger |
|---|---|---|
| `mula` | a pratīka word/compound quoted from the root verse | matches the ROOT VERSE I supply |
| `gloss` | Śaṅkara's synonym(s) that gloss a mūla word | the term(s) after a `=` |
| `import` | the doctrinal purport | the term(s) after a `→` |
| `vyakarana` | Śaṅkara's own grammatical move — a *nirvacana* (derivation, `X इति Y`, root+affix) OR a statement about grammar (case-function `षष्ठी…`, particle-sense `अवधारणार्थः`, `नञ्`/समास analysis) | derives or explains a word's form/function — NOT a synonym |
| `purvapaksha` | an opponent's objection (the whole objecting clause) | ननु, कथम्, अत्र चोद्यते, नन्वेवम्, कश्चिदाह, **…इति चेत्** (if-it-be-said); स्यादेतत् ("granting this…") continues/elaborates the objection |
| `ekadeshi` | a partial/intermediate view or secondary objector | अपरे तु, अत्र कश्चिदाह, एकदेशिनः, अन्ये |
| `siddhanta` | Śaṅkara's settled resolution | उच्यते, अत्र ब्रूमः, सत्यमेवम्, तन्न, न |

Spans **nest**: inside a `siddhanta` clause, mūla words still get `mula`, glosses still get `gloss`.
Keep the inner spans.

**C. Discourse layer** (whole-sentence roles wrapped around complete sentences; the word/argument spans
above nest inside them):
- `sangraha` — a **compressed thesis that a following passage then elaborates (vistara)**. It appears at
  TWO scales:
  (i) **topic/section level** — Śaṅkara states the विषय/प्रयोजन up front before glossing (common at
      adhyāya/section openings and intro-bhāṣyas; *rare* at the start of a single verse, which usually
      opens with word-gloss — so do not force one there);
  (ii) **answer level** — the **head of a `siddhanta` refutation is itself a saṅgraha**: a terse `न` +
      a hetu in the **ablative** (`…त्वात्` / `…अनुपपत्तेः`), e.g. `न, देवताभ्युपगमे अग्रहणानुपपत्तेः`,
      which the sentences after it unpack. Wrap that `न`+hetu head in `sangraha`, nested inside the
      `siddhanta` span; the elaboration after it is the default vistara.
  Do NOT force a saṅgraha where the text is straight word-gloss, or where the gist is only terminal
  (एतदुक्तं भवति / इत्यर्थः).
(The elaboration that follows needs no mark — it is the default `vistara`.)

**D. Citation:**
- `quote` — an embedded scriptural / authoritative **citation** (śruti, smṛti, Gītā, saṃhitā …),
  usually delimited by ‘ ’ and closed by इति श्रुतेः / इति स्मृतेः / इति. Wrap the quoted words
  (keep any source reference like `(बृ. उ. १।६।३)` inside the span). Do not alter the quote.

## Rules that keep it faithful

1. **mūla marking — mark WHAT IS THERE, never import from the verse.** I give you the ROOT VERSE only
   so you can recognise which bhāṣya words are pratīkas. You may mark a `mula` span ONLY around words
   **physically present in the RAW passage**, exactly as they stand.
   - ⛔ NEVER replace a bhāṣya word with its fuller verse form. If RAW has `व्यदधात्` and the verse has
     `व्यदधाच्छाश्वतीभ्यः समाभ्यः`, mark **only** `व्यदधात्`. If RAW has `आत्मैवाभूत् … विजानतः`
     (two words), never fuse them into the verse form `आत्मैवाभूद्विजानतः`.
   - ⛔ NEVER pull extra words from the ROOT VERSE into the passage (e.g. do not prepend
     `अन्यदेवाहुर्विद्यया`/`अन्यदाहुरविद्यया` because the verse has them). The Block-2 strip must equal
     RAW — importing verse words breaks that.
   - ⛔ NEVER normalise spelling or sandhi: keep anusvāra vs म्/न् as given (`अमृतं` stays `अमृतं`, not
     `अमृतम्`), do not split a sandhi join (`यस्मिन्नोतानि` stays one word, never `यस्मिन् ओतानि`), do
     not change `ये`→`य` or add a vowel (`सत्यस्य`→`सत्यस्या`).
   - ⛔ NEVER mark a discourse particle / voice-marker as `mula`: ननु, इति चेत्, स्यादेतत्, तस्मात्,
     किं तु, कथम्, अत्र, हि, च … belong to the argument/flow layer, never to the pratīka.
   - If you are not confident a word is a pratīka, do not mark it — log it instead.
2. **Voices need an explicit trigger.** Colour a `purvapaksha`/`ekadeshi`/`siddhanta` span only when
   one of the trigger words above is actually present. Never guess a voice from tone alone.
   `ekadeshi` is rare — reserve it for अपरे तु / अत्र कश्चिदाह / एकदेशिनः / अन्ये. The trigger word
   itself goes **inside** the coloured span. A **second or third `…इति चेत्` objection** in the same
   passage is STILL `purvapaksha`, NOT `ekadeshi` — do not promote a repeated objection to ekadeśī
   just because it is the later of two; ekadeśī requires one of its own triggers above.
   - **Colour the RESPONSE, not just the objection.** Śaṅkara's answer to a पूर्वपक्ष is often a bare
     `न` / `नैष दोषः` / `न` + reasoning, WITHOUT उच्यते. When a `न`/`नैष दोषः` directly answers a
     preceding objection, colour it and the reasoning that supports it (up to the next objection or the
     end of the passage) as `siddhanta`. Do not leave an objection standing with its reply uncoloured.
     (But a `न` that is merely part of an objection's own wording is NOT a response — judge by whether
     it rebuts a stated पूर्वपक्ष.)
3. **`→` restraint.** No signal word, no arrow. A plain synonym is `=`, not `→`.
4. **No brackets/parens in the data.** Do not insert `[ ]` or `( )`. If a phrase is a structural
   marker (इत्यर्थः, इति) or supplied word (adhyāhāra), leave it as plain text; styling for those can
   be added later in CSS.
5. **`vyakarana` vs `gloss`.** A synonym is `=` (`gloss`). But if Śaṅkara *derives* the word
   (`… इति X`, root + affix) or states a grammatical function (a case-name like षष्ठी/तृतीया, a
   particle's sense like अवधारण/एवकार, a नञ्/समास analysis), that is `vyakarana`, not a gloss — a
   grammatical statement is not a synonym of any word.

## Output — exactly three fenced blocks, in this order

1. ```html — the ANNOTATED fragment (Devanāgarī, one passage, markup as above).
2. ```text — STRIPPED: produce this ONLY by mechanically deleting the tags and the inserted `= → |`
   glyphs from YOUR Block 1 — do NOT retype it from the RAW input or from memory (retyping from RAW
   hides errors that are actually in Block 1). It MUST then equal the RAW input; if it does not, the
   error is in Block 1 — fix Block 1 and redo.
3. ```json — a LOG array. One entry per decision that needed judgement or that you left unmarked:
   `{"segment":"<surface text>","issue":"uncertain-mula|ambiguous-voice|left-unmarked|other","note":"<why>"}`
   Empty array `[]` if nothing was uncertain. This drives human QA on disagreement.

Emit nothing else — no preamble, no translation, no table.

## Worked example

ROOT VERSE (BG 14.26): ... ब्रह्मभूयाय कल्पते
RAW passage: ब्रह्मभूयाय ब्रह्मभवनाय मोक्षाय कल्पते समर्थो भवतीत्यर्थः

Block 1 (```html):
<span class="mula">ब्रह्मभूयाय</span> = <span class="gloss">ब्रह्मभवनाय</span> → <span class="import">मोक्षाय</span> | <span class="mula">कल्पते</span> = <span class="gloss">समर्थो भवति</span> इत्यर्थः

Block 2 (```text):
ब्रह्मभूयाय ब्रह्मभवनाय मोक्षाय कल्पते समर्थो भवतीत्यर्थः

Block 3 (```json):
[{"segment":"भवतीत्यर्थः","issue":"other","note":"इत्यर्थः is a structural marker; left as plain text per rule 4, glossed समर्थो भवति via = before it"}]

Process ONE passage per turn. Await the block below.

>>> PROMPT END

---

## Input block to append (one passage per run)

```
ROOT VERSE (<ref>): <root-verse text, so pratīkas can be identified>
RAW passage: <the exact bhāṣya sentence(s), verbatim from the Zenodo corpus>
```

## How the output is consumed

- **Now (full-book HTML):** paste block 1 into the bhāṣya slot; `build_fullbook_html.js` supplies the
  palette for `.mula` / `.gloss` / `.import` / `.purvapaksha` / `.ekadeshi` / `.siddhanta`.
- **QA gate:** diff block 2 against the RAW input; any mismatch = reject (Śaṅkara's text was altered).
  Route non-empty block 3 entries to human review — this is the "intervention on disagreement" step.
- **Later (PWA):** a safelist renderer maps the same six classes to CSS; because there are no inline
  styles and the class set is fixed, the fragment is safe to render without `esc()` stripping it.

## Suggested palette (place in build_fullbook_html.js CSS, tune to taste)

```css
.mula        { color:#1a56db; font-weight:600; }   /* blue, like upasanayoga.org */
.gloss       { color:#374151; }                     /* near-default; the = carries the meaning */
.import      { color:#6d28d9; font-style:italic; }  /* violet — doctrinal purport */
.purvapaksha { color:#b91c1c; }                     /* red   — objection */
.ekadeshi    { color:#c2410c; }                     /* orange— intermediate view */
.siddhanta   { color:#15803d; }                     /* green — settled view */
/* dark mode: override these six in the .dark scope; that's the whole point of using classes */
```
