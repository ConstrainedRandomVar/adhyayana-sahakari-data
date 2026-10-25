# Pramāṇa classification rubric — bhāṣya discourse segments

Canonical, in-repo copy of the grading rubric (the working copy `[redacted: local path]` is disposable).
Used by the Opus grader agents (see `project_pramana_classification` memory) and by any future re-grade /
blind-audit / prakaraṇa-grantha pass. Keep this and the agent prompt in sync.

INPUT: a JSONL file (ONE JSON object per line) — each line = {"id","ref","role","text"} (a bhāṣya segment).
Read it with a single Read; it is small (~30 lines). Do NOT loop re-reading — read once, then classify.

For each segment name the ONE dominant epistemic instrument (3-way + none):

- **shruti** — SCRIPTURAL TESTIMONY as the settled authority ("इति श्रुतेः/स्मृतेः", a cited Veda/Upaniṣad/
  Gītā/smṛti doing the decisive work). smṛti folds in here (śabda-pramāṇa); the śruti/smṛti fineness is left
  to the plain citing word, not a separate label.
- **yukti** — REASONING: inference (anumāna), reductio/dialectic (tarka — अन्यथानुपपत्ति, prasaṅga,
  "illogical otherwise", यदि…तर्हि…तस्मात्, न अयुक्तेः), or a logical maxim (nyāya). `upapatti = tarka`.
- **anubhava** — DIRECT / SELF-EVIDENT EXPERIENCE. The canonical Advaita forms (per the avasthā-traya
  analysis — Māṇḍūkya + Māṇḍūkya-rahasya-vivṛti; Kulkarni, *Guide-lines to Shankara-Vedanta*, "First
  Fundamental"):
    • **avasthā-traya** — appeal to the three states (jāgrat / svapna / suṣupti) and what persists across
      them (e.g. "in deep sleep there is no duality yet one exists / knows on waking");
    • **sākṣī / witness-consciousness** — the self-evidence of awareness itself: the seer is never the seen,
      awareness needs no further proof, "no one doubts that they are conscious";
    • **ordinary perception / recognition** as self-certifying (सोऽयं देवदत्तः; "no questioning what is
      directly experienced" — न हि दृष्टेऽनुपपन्नम् / प्रसिद्धम्).
  Reserve anubhava for these EXPERIENTIAL grounds — it is rare outside Māṇḍūkya / Bṛhad 4.3 (dream-sleep)
  and the avasthā-traya passages; do NOT award it to an analogy that is merely the vehicle of an argument.
- **none** — pure exposition / word-gloss / restatement, or a bare question / assertion.

RULES:
1. Pick the DOMINANT instrument. An analogy used AS EVIDENCE → anubhava; an analogy as the vehicle of a
   reductio → yukti.
2. CITATION vs REASON: if reasoning carries the argument and a quote merely concludes/supports it → yukti;
   only if the citation IS the settled authority (reasoning incidental) → shruti (a तस्मात्/न अयुक्तेः/
   उपपद्यते spine ⇒ yukti even with a quote).
3. A reductio whose premise is experiential is still yukti (the MOVE is reasoning). Conversely, a bare
   appeal to the three-states / self-evidence of awareness, with no inferential move, is anubhava.

OUTPUT: JSONL (one object per line) — each line {"id":<int>,"pramana":"shruti|yukti|anubhava|none",
"reason":"<one concise English clause naming the deciding cue>"}. Write INCREMENTALLY (append each line as
you classify) so partial progress is saved. One line per input id. Brief reasons, no long deliberation.
