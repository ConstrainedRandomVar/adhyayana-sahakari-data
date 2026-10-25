<!-- Extracted verbatim from out-of-repo pipeline: vartika/brihadaranyaka-vartika-sara/work/proof_prompt.py (prompt builder; run_proof.js sends the files). The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```python
#!/usr/bin/env python3
"""Build the TEXT-ONLY Gemini proofing prompt for one page ([redacted: name] 2026-10-06: never send the page image).
Per line: the Vision OCR reading only (Tesseract dropped — [redacted: name] 2026-10-06), with the zone and Vision's own
low-confidence words marked ⟨…⟩ (word confidence < 0.70). Gemini SUGGESTS; Claude adjudicates each suggestion against the scan. Usage: proof_prompt.py <page> → stdout."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'pages.json')))
D = P
INSTR = """You are helping proof-read OCR of a printed Sanskrit book (Benares, 1915): Vidyāraṇya's Bṛhadāraṇyaka-vārtikasāra
(verses) with Maheśvaratīrtha's Laghusaṅgraha commentary, interleaved with Bṛhadāraṇyaka Upaniṣad mantras.
Each numbered line is the OCR reading of one printed line. Words the OCR engine itself was unsure of are marked ⟨…⟩
(but any word may be wrong). You do NOT see the page image.
Task: list ONLY the words that are probably a misreading of the print, with your best reading of what is printed.
Rules:
- Reconstruct what the 1915 PRINT says, not what you think the ideal text is. Keep the edition's orthography,
  sandhi, anusvāra/class-nasal choices, avagraha and punctuation exactly as printed. Do NOT normalise spelling.
- Base each suggestion on evidence: the verse metre (anuṣṭubh), an exact quotation (Upaniṣad mantra), grammar, or a
  typical OCR confusion of Devanāgarī print (e.g. ध/घ, भ/म, व/ब, ष/प, ङ्ग/ङ्ग, missing mātrā) — say which.
- If the word is plausible as printed, do not suggest anything. Never rewrite whole lines. Never add or drop words.
- Line-broken words (ending in "-") continue on the next line; judge them joined.
Output JSON only: [{"line": <n>, "w": "<OCR word>", "s": "<suggested word>", "why": "metre|quote|grammar|ocr|other", "conf": "high|med|low"}]
Return [] if nothing needs changing."""
def build(p):
    L = [x for x in D[str(p)]['lines'] if x['zone'] in ('mula', 'tika')]
    out = [INSTR, '', 'PAGE %s' % p]
    for i, x in enumerate(L):
        z = {'mula': 'VERSE/MANTRA', 'tika': 'COMMENTARY'}[x['zone']]
        t = ' '.join(('⟨%s⟩' % w[4]) if w[5] < 0.70 else w[4] for w in x['w'])
        out.append('%d [%s] %s' % (i + 1, z, t))
    return '\n'.join(out)
if __name__ == '__main__': print(build(int(sys.argv[1])))
```
