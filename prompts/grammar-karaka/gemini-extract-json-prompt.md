# Call 2 of 2 — transcribe the prose analysis (from gemini-protocol-prompt.md) into the pipeline JSON.
# Pure formatting, NO re-analysis — this is what avoids the "forcing JSON while reasoning" quality loss
# ([redacted: name], 2026-08-20). The completed prose analysis is substituted for <ANALYSIS>. Sent to gemini-2.5-flash.

>>> PROMPT START
You are given a COMPLETED Sanskrit sentence analysis (prose + tables) for one verse. Transcribe it
EXACTLY into a single JSON object. Do NOT re-analyse, re-segment, add, or decompose anything not already
stated in the analysis. Output ONLY the JSON object — no prose, no markdown code fences, nothing else.

Number the padas 1..N in the order they appear in the verse. Use this EXACT schema:

{
  "words": [
    { "n": <int>, "word": "<surface pada; hyphen-join compound members>",
      "morph": "<the morphology string from the pada table>",
      "samasa": [ { "c": "<compound/sub-stem>", "vigraha": "<vigraha>", "type": "<samāsa/derivation type, e.g. षष्ठी-तत्पुरुष, कर्मधारय, बहुव्रीहि, इतरेतर-द्वन्द्व, नञ्-तत्पुरुष, अव्ययीभाव, कृत्, तद्धित, प्रातिपदिक>", "sutra": "<a.p.n or omit>", "pratyaya": "<only for कृत्/तद्धित>" } ]
    }
  ],
  "tree": [
    { "n": <int>, "word": "<surface>", "morph": "<same string>", "clause": <clause id>,
      "role": "<the भूमिका/kāraka from the table: कर्ता, अभिहितकर्ता, कर्म, करणम्, सम्प्रदानम्, अपादानम्, अधिकरणम्, विषयाधिकरणम्, षष्ठीसम्बन्धः, विशेषणम्, समानाधिकरणम्, क्रियाविशेषणम्, प्रतिषेधः, पूर्वकालः, हेतुः, सम्बोध्यः, …>",
      "governor": <the n of the word this depends on; 0 if none / clause head>,
      "transitivity": "<सकर्मकः|अकर्मकः — verbs only>", "voice": "<कर्तरि|कर्मणि|भावे — verbs only>",
      "clauseType": "<main|nominal|relative|correlative|subordinate|quotation — verbs/heads only>", "subordinateTo": "<clause id or 0 — verbs/heads only>"
    }
  ],
  "clauses": [
    { "id": <int>, "type": "main|nominal|relative|correlative|subordinate|quotation",
      "subordinateTo": <clause id, or 0>,
      "words": [<the INTEGER n of every word in this clause>],
      "elided": [ "<supplied/understood word(s), e.g. अस्ति, पुरुषः>" ],
      "anuktaKarta": "<unexpressed agent/antecedent named in the analysis; empty string if none>",
      "gloss": "<the English translation of this clause>" }
  ]
}

HARD RULES:
- Include "samasa" ONLY for words the analysis's Samāsa section actually decomposes. OMIT the "samasa"
  key entirely for simple/underived words (do NOT invent प्रातिपदिक-only entries for every word).
- "samasa" is a FLAT array, OUTERMOST layer first, exactly as the Samāsa section nests it.
- clauses[].words MUST be integers (the n values), NEVER surface strings.
- Preserve the analysis's clause count, grouping, types, and elided/implied words verbatim — do not "fix" them.

ANALYSIS TO TRANSCRIBE:
<ANALYSIS>
>>> PROMPT END
