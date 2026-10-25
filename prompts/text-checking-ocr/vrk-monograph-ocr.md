<!-- Extracted verbatim from out-of-repo pipeline: monograph/vrk-gita-upanishads/gemini_correct.py lines 19–71. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```python
PROMPT = """You are proofreading Google Vision OCR of one page of a printed English monograph on Advaita
Vedānta: "Gita and Upanishads" by V. R. Kalyanasundara Sastri (Adi Sankara Advaita Research Centre, Madras).
It shows how teachings of the Bhagavad-gītā parallel the Upaniṣads. The page image is attached. The OCR is
given below as numbered lines of word tokens `wN=text`.

The page mixes three kinds of text: English prose; Sanskrit in ITALIC IAST romanisation (in the body and
in footnotes, e.g. "drṣṭvā tu Pāṇḍavānīkaṁ"); and Sanskrit in DEVANĀGARĪ (often in footnotes).
Known OCR failures: IAST diacritics dropped or replaced with look-alikes (ä/à for ā, ş for ṣ, ü for ū,
plain n/t/d/s for ṇ/ṭ/ḍ/ś/ṣ, missing ṁ/ḥ/ṛ dots); daṇḍas read as "|" or "||"; small Devanāgarī slips.

Return JSON with exactly these keys:
1. "edits": list of {"ids": [consecutive word ids ON ONE LINE], "text": "corrected text", "kind": one of
   "iast" | "devanagari" | "english" | "punct" | "noise", "note": short English reason}.
   - Replace the listed tokens with "text" exactly as PRINTED in the image. For IAST, reproduce the printed
     diacritics exactly (use the edition's own letters, e.g. ṁ vs ṃ, ṛ vs r̥, as they appear). For
     Devanāgarī, transcribe exactly as printed. In Devanāgarī lines write printed daṇḍas as । and ॥; in
     IAST lines keep the printed vertical bars as | and ||.
   - Vision is USUALLY CORRECT on Devanāgarī. Change a Devanāgarī token only when the glyphs in the image
     clearly differ from the OCR. This edition contains MANY MISPRINTS in its Sanskrit, and they must be
     preserved: e.g. a printed "यजुस्तास्मादजायत" stays (not यजुस्तस्मात्), printed "तेद्य" stays (no added
     ऽ), printed "भगन" stays (not भगव), printed "पार्थय" stays. You will recognise many quotations (Gītā,
     Upaniṣads, Bhāṣya): NEVER use your memory of the canonical text to change what is printed; compare
     only against the image, letter by letter. A misprint goes in "suspects" ("MISPRINT?: ..."), not edits.
   - Do NOT standardise spelling, fix grammar, correct reference numbers, or "improve" the Sanskrit or
     English toward a textbook form, even if you think the print is wrong. Fix only what the OCR misread
     versus the print. If you believe the PRINT itself has an error, leave the text and add a "suspects"
     entry starting "MISPRINT?:".
   - English words and names in roman type (Sankara, Gita, Upanisads in headings) keep exactly the
     printed form, with or without diacritics, as printed.
   - "noise": text not on the page (show-through, specks, gutter shadow); set "text" to "".
   - Only include tokens that are actually wrong. Never merge tokens across lines in an edit.
2. "joins": list of [last_id_of_line, first_id_of_next_line] where ONE printed word is broken across a line
   break (with or without a hyphen). Only true word breaks, not compounds hyphenated in print mid-line.
3. "blocks": the page in READING ORDER as a list of {"type": ..., "ids": [ranges like "w0-w12" or "w15"]}
   with type one of "pagenum" | "running_head" | "heading" | "para" | "verse" | "footnote" | "caption" |
   "signature". Every word id must appear in exactly one block (noise ids too). Use "verse" for Sanskrit
   set apart on its own lines in the body. Each footnote (a numbered note below the rule, including its
   (a)/(b)… sub-items, Sanskrit lines and English translation) is ONE "footnote" block; add "n": its printed
   number (a footnote continuing from the previous page with no number gets "n": "cont"). Some pages
   consist ENTIRELY of footnotes (numbers like 3, 4, 5 at the left margin, no body text) — still use
   "footnote" blocks with "n" for those. Right-aligned
   source citations such as "(Ka. Up. 2-2-9)" or "(गीता महात्म्य)" belong IMMEDIATELY AFTER the
   verse/sub-item they label, in the same block, even though OCR lists them elsewhere.
4. "italic": list of id ranges printed in italic type (typically IAST Sanskrit and book titles).
5. "footnote_refs": list of {"id": word id, "n": "9"} for each superscript footnote call-out in the body
   text (OCR usually glues it to the word, e.g. "samsara.9" — then also add an edit that removes the digit
   from the word, kind "punct", so the word reads as printed without the superscript).
6. "suspects": list of {"ids": [...], "note": "..."} for anything you could not read confidently.

Write all prose in English. Output JSON only.

OCR:
"""
```
