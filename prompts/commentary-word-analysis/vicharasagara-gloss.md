<!-- Extracted verbatim from searchtool/khan/vc-karaka/vs_run.js lines 27–89. The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
function promptFor(avs, shardIdx, shardTotal) {
  const rng = avs.length > 1 ? (avs[0].n + '–' + avs[avs.length - 1].n) : ('' + avs[0].n);
  const H = [
'# विचारसागर — taraṅga ' + CHAP + ' analysis (shard ' + shardIdx + '/' + shardTotal + ': āvartas ' + rng + ')',
'',
'You are an expert in Pāṇinian vyākaraṇa, Sanskrit lexicon, and Advaita Vedānta. The text below (after "## INPUT") is ALREADY split per āvarta into a [MULA] block and zero or more [TIPPANI n] blocks. Return a SINGLE JSON ARRAY, one object per āvarta, IN ORDER, and NOTHING else (no fences, no prose). Must parse with JSON.parse.',
'',
'## ABSOLUTE RULES',
'- Devanāgarī for ALL Sanskrit; English ONLY in "meaning" and "translation".',
'- The [MULA]/[TIPPANI] blocks are ALREADY SEPARATED. Do NOT move content between blocks or āvartas. [MULA]→"mula"; each [TIPPANI n]→a "tippani" entry with that note number. Keep membership exactly.',
'- JSON VALIDITY: output NO double-quote (") anywhere inside a string value. In the Sanskrit fields render embedded quotations with guillemets ‹ ›; in the ENGLISH "translation"/"meaning" fields use SINGLE quotes \'…\' for any quoted phrase — NEVER a double-quote. (A raw " in translation is the #1 cause of invalid JSON — e.g. do NOT write "translation":""I am Brahman"…"; write "translation":"\'I am Brahman\'…".) PRESERVE parenthetical source tags verbatim (e.g. "(क. १.२.९)"). Balance every { } and [ ]. No trailing commas.',
'- QUOTATION EXTENT: when the text quotes a multi-line / multi-pāda śloka, mark the ENTIRE śloka (all pādas — both half-verses) as ONE quotation inside a single ‹ › — do NOT quote only its last line and leave the first line as ordinary prose. The source tag (…) follows the whole quotation.',
'',
'## PER-ĀVARTA SHAPE',
'{"ref":"<chap>.<n>","heading":"<given heading; empty if none>",',
' "mula":[{"s":1,"sanskrit":"<one sentence of [MULA]>","words":[{"n":1,"word":"<segmented pada, citation-restored>","morph":"<see MORPH>","meaning":"<1-6 word English gloss as used here>","samasa":[<recursive layers — compounds ONLY; omit otherwise>]}],"translation":"<faithful readable English of THIS sentence>","roleSpans":[<see ROLES>]}],',
' "tippani":[{"note":1,"sentences":[{"s":1,"sanskrit":"…","words":[…same…],"translation":"…","roleSpans":[…]}]}]}',
'(Sentence-split each block. No [TIPPANI] → "tippani":[]. Analyse quoted verses too.)',
'',
'## ROLES (span-level classification — by WORD INDEX, not copied text)',
'For EACH sentence add "roleSpans": an ORDERED list of {"role":"<one below>","from":<the n of the FIRST word of this span>} using the SAME words[].n you emitted. A span runs from its "from" up to the next span\'s "from" (or the sentence end). The FIRST span MUST have from:1. A single-role sentence is just [{"role":"exposition","from":1}]. Break a role ONLY at a words[] boundary — NEVER split one pada across two roles. Do NOT copy the text.',
'Roles (classify by DISCOURSE FUNCTION, not mere keywords):',
'- "purvapaksha" — an objection / doubt / opponent\'s view (ननु, स्यादेतत्, इति चेत्, इति शङ्का, अत्राह, a numbered आक्षेपः/प्रश्नः).',
'- "siddhanta" — the author\'s resolution / refutation (अत्रोच्यते, तन्न, तदसत्, नैष दोषः, इति चेन्न, किन्तु, वस्तुतस्तु, राद्धान्तः, the settled conclusion).',
'- "drishtanta" — a SUSTAINED analogy: the यथा…तथा/एवम् correlative, or a stock Advaita dṛṣṭānta (रज्जुसर्प, घटाकाश, शुक्तिरजत, मरीचिजल, स्वप्न, तरङ्ग). Do NOT tag every इव/वत् comparison.',
'- "lakshana" — a DEFINITION of a technical term (X इत्युच्यते / X नाम Y / X लक्षणम्). (नाम is also a mere particle — tag only when defining.)',
'- "phalita" — the takeaway / doctrinal implication drawn FROM the siddhānta (तेन…सिद्ध्यति, तस्मात्, अतः सिद्धम्, इति फलितम्, इति भावः). Distinct from siddhanta (the refutation itself) — this is its consequence.',
'- "ekadeshi" — a NAMED intermediate / semi-accepted view (अपरे तु, अन्ये, केचित्, मतान्तरम्) — partially accepted/refined (vs pūrvapakṣa = refuted).',
'- "anuvada" — a mere RESTATEMENT / framing of a known fact or a previously-settled point (not an active objection or new claim). Optional; use to distinguish summary from live debate.',
'- "exposition" — plain running exposition / narration / connective reasoning. This is the DEFAULT.',
'RULES: Default to "exposition"; assign another role ONLY where a marker or unambiguous function is present — do NOT invent a debate the text does not stage. On an ambiguous marker (न च, इव, नाम, अथ, तस्मात्) default to exposition (use phalita only for a genuine concluding implication, not every connective तस्मात्). If a written token straddles an objection→answer flip (…इति चेन्न), assign it to "siddhanta". Quotations get their own colour downstream — do not special-case them here (tag the quoted words by their clause\'s role).',
'',
'## SPEAKER',
'Do NOT emit any "speaker" field. Dialogue attribution is added DETERMINISTICALLY downstream from explicit in-text markers (गुरुराह / शिष्यः पृच्छति / …उवाच) — a model guess (e.g. treating every pūrvapakṣa as the śiṣya) MISATTRIBUTES the author\'s own rhetorical objections (…इत्याशङ्कायां उच्यते / इति चेत्, where the author raises AND answers the doubt), so it is not wanted. Classify such author-self-objections under the "purvapaksha"/"siddhanta" ROLES as usual, but assign NO speaker.',
'',
'## SEGMENTATION',
'Undo sandhi; each pada its own unit, citation-ending restored. Keep a samāsa as ONE hyphen-joined unit. Join across spurious intra-word spaces. Drop nothing (च/एव/हि/वै/तु/अपि/इति incl.); no daṇḍa/numbers. Lone न/मा = own निषेध unit. COVERAGE: EVERY syllable of the sentence must be accounted for in words[] — do NOT skip or summarise; never drop a connective particle (च/तु/वा/हि/एव/अपि).',
'',
'## MORPH (exact)',
'Nominal: "<stem> · <विभक्ति>·<वचन>·<लिङ्ग>" (+ (सर्वनाम) for pronouns, samāsa type for compounds). Finite: "<√धातु> · <कर्तरि|कर्मणि|भावे>·<लकारः>·<पुरुष>·<वचन>·<पद>" — SPELL THE लकार IN FULL (लट्/लिट्/लुट्/लृट्/लोट्/लङ्/विधिलिङ्/आशीर्लिङ्/लुङ्/लृङ्; NEVER bare "लिङ्" — write विधिलिङ् or आशीर्लिङ्) and give पद (परस्मैपद/आत्मनेपद). कृदन्त: प्रत्यय+function (क्त/ल्यप्/क्त्वा/शतृ/शानच्/तुमुन्). Indeclinable: "अव्यय (<sense>)". A तृतीया governed by विना/सह/नाना/पृथक् is upapada-tṛtīyā (not karaṇa) — gloss it as "with/without …", not an instrument.',
'',
'## RECURSIVE SAMĀSA (compounds only) — CONSERVATIVE',
'Peel one BINARY layer from the RIGHT at a time; at EVERY split resolve BOTH members; recurse to underived प्रातिपदिक. FLAT array, outermost first: {"c":"…","vigraha":"…","type":"e.g. षष्ठी-तत्पुरुष","sutra":"…"} + "pratyaya" & type कृत्/तद्धित for a derived leaf. PEEL kṛt/taddhita leaves (ज्ञान→√ज्ञा+ल्युट् 3.3.115; भाव→√भू+घञ्; निश्चय→निः-√चि+अच्). STOP (मूल, no leaf) at underived + उणादि/lexicalised nouns (धर्म, मार्ग, कर्मन्, देव, गुरु, नर, पुत्र, गो, देश, आकाश); when unsure → मूल. Do not decompose pronouns/particles/prefixes.',
'',
'## GLOSS CONNECTOR (=)',
'The author often glosses a term inline: "X = Y" (Y is the paryāya / vivaraṇa — the synonym or plain sense of X), or "X इत्यर्थः / इति यावत्". PRESERVE the "=" VERBATIM in the "sanskrit" field wherever the source has it — it is a gloss marker, NOT a word (do not put it in words[]). Keep X (the glossed term) and Y (the gloss) as normal words on either side. This lets the reader see the author\'s A = B glosses.',
'',
'## TRANSLATION',
'Per SENTENCE. Faithful, readable, natural English. Keep CORE technical terms UNTRANSLATED (transliterated, in *italics* via _underscores_): Brahman, jīva, ātman, avidyā, māyā, vṛtti, upādhi, adhyāsa, ānanda, sākṣin, cit, prakṛti, jīvanmukti, mokṣa — and be CONSISTENT (do not render avidyā as "ignorance" one sentence and "nescience" the next). Gloss other terms in plain English.',
'',
'Output ONLY the JSON ARRAY.',
'',
'## INPUT',
''].join('\n');
  let body = '';
  for (const a of avs) {
    body += '\n### आवर्त ' + a.n + '  (ref ' + a.ref + ')\n';
    if (a.heading) body += '[HEADING] ' + a.heading + '\n';
    if (a.mula) body += '[MULA]\n' + a.mula + '\n';   // continuation chunks of a split āvarta carry no mūla → emit "mula":[]
    a.tippani.forEach(t => { body += '[TIPPANI ' + t.note + ']\n' + t.text + '\n'; });
  }
  return H + body + '\n';
}
```
