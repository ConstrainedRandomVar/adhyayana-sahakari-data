# Call 1 of 2 — full sentence analysis (PROSE) via the sentence-analysis protocol.
# The pipeline sends this (protocol + one verse) to gemini-2.5-flash; the prose output is then
# transcribed to JSON by gemini-extract-json-prompt.md (call 2). Protocol text mirrors gemini-protocol.pdf
# / the sentence-analysis skill — keep in sync. Verse is substituted for <VERSE>.

>>> PROMPT START
gemini-protocol.html 

 
 

 Merged Sanskrit Sentence Analysis Rules (Gemini / Devanāgarī edition) 
 A structured framework for parsing and translating a Sanskrit verse or sentence with strict
Pāṇinian accuracy. Work word by word in the sentence's order. (Devanāgarī companion to the
 sentence-analysis skill; kept in sync — last updated 2026-08-19 with the e-reader kāraka
& clause-identification learnings.) 

 I. General Output Requirements 
 
 Script : All analysis output in Devanāgarī (Gemini renders it well). The final
 translation only is in English. 
 Input handling : If input is ITRANS/IAST, transliterate to Devanāgarī first.
 Show the resolved text with sandhi split, and restore each word to its pausa (citation) form —
 including a dropped/transformed final विसर्ग (e.g. show तत्त्वतः, अनात्मबन्धः; not the surface
 तत्त्वतस्, अनात्मबन्धस्; रामो गच्छति → रामः गच्छति). Apply the same pausa restoration to the पद
 column, the Anvaya, and every word cited in Vibhakti-vicāra. 
 Gender : पुं (M) · स्त्री (F) · नपुं (N). 
 Omit all page-number / location references. 
 Table style : standard Markdown table (not a code block). 
 

 II. Prayoga (प्रयोग) 
 Classify each clause (see §III वाक्य-विभाजन): कर्तरि (active) / कर्मणि (passive) /
भावे (impersonal). 

 III. वाक्य-विभाजन एवं लुप्त-कर्ता — Clause identification & the elided kartā (do this first) 
 A श्लोक usually contains several वाक्य (clauses), and every कारक is fixed relative to the
क्रिया of its own वाक्य only, never crossing the boundary — therefore do the विभाजन before
assigning the भूमिका. (Confirmed from the कारक-trees of the UoHyd e-reader, 2026-08-19.) 
 
 One वाक्य = exactly one तिङन्त (finite verb), or one verbless "X [is] Y" predication, + all
 words dependent on it. Boundaries: दण्ड (। ॥), relative–correlative pairs such as
 यत्…तत् / यतो यतः… / यथा…तथा, and the quotation इति. 
 Words ending in the प्रत्यय ल्यप्/क्त्वा/शतृ/शानच्/क्त are not a separate वाक्य — they stay
 within the तिङन्त's own वाक्य; attach them to that क्रिया as पूर्वकालः (prior action:
 क्त्वा/ल्यप्/क्त) or समानकालः (concurrent: शतृ/शानच्), not as a separate वाक्य. 
 Classify every वाक्य — main / relative / correlative / quotation /
 nominal (verbless predication) / subordinate — and state which one it is subordinate to.
 Determine each वाक्य's कारक only from its own क्रिया. A governor may cross a वाक्य-boundary
 only when the head of a subordinate वाक्य links to the वाक्य it depends on — never cross a full
 sentence-boundary (॥ / वाक्यान्त इति + वचन-क्रिया). 
 
 Supplying the elided कर्ता. In Sanskrit, elision of the कर्ता is common. Every तिङन्त must
have a कर्ता; if no overt, case-appropriate प्रथमा (in कर्तरि) / तृतीया (in कर्मणि) is found in
that same वाक्य, then the कर्ता is elided — supply it in [brackets] in the अन्वय. Never borrow a
प्रथमा from another वाक्य (the most common and serious error). Infer the कर्ता from these cues,
in this order of priority: 
 
 The क्रिया's पुरुष/वचन (strongest): उत्तम → [अहम्]/[वयम्]; मध्यम → [त्वम्]/[यूयम्];
 प्रथम → the context (प्रकरण) of the वाक्य / the previously-mentioned कर्ता. 
 Quotation construction (…इति <वचन-क्रिया>): the कर्ता of the inner उत्तमपुरुष क्रिया is [अहम्]
 (the speaker) — not the outer named speaker (…इति ब्रवीमि इति ह उवाच याज्ञवल्क्यः: ब्रवीमि → [अहम्];
 only the कर्ता of उवाच is याज्ञवल्क्यः). 
 relative/correlative + विधिलिङ्/gnomic (यः… विधिलिङ्): indefinite → [कश्चित्]
 ("someone / whoever"). 
 impersonal / existential (स्यात् "may be", भावे voice, agentless भवति): no
 personal कर्ता — impersonal; in a verbless predication, [अस्ति (copula) supplied]. 
 Otherwise, in a subordinate वाक्य sharing the same कर्ता, bring in the कर्ता of the main वाक्य. 
 

 IV. The Six-Column Analysis Table (पद-विश्लेषणम्) 
 
 Header Content 
 पद the word in pausa/citation form (विसर्ग restored) 
 प्रातिपदिक/धातु nominal stem, or verbal root with its Dhātu-pāṭha entry — उपदेश + अर्थ (e.g. गमॢँ (गतौ)) 
 कोटि सुबन्त (+ पुं/स्त्री/नपुं) · तिङन्त · अव्यय 
 सङ्केत numeric code (see legend) 
 भूमिका the kāraka / vibhaktyartha function — not just "genitive sg." but कर्ता, कर्म,
 करण, अपादान, सम्प्रदान, अधिकरण, निर्धारण, शेष-षष्ठी, कर्मणि-षष्ठी, विषय-सप्तमी, etc. (one–two
 words; sūtra numbers go in Vibhakti-vicāra, never here) 
 टिप्पणी must always carry a concise English gloss of the word's meaning (e.g. अकायम् →
 "bodiless", शुक्रम् → "bright"), plus any brief morphological note. Being the last column it may
 run a little longer. (For verbs the meaning is already on the Verb-detail line, so the gloss here
 can be minimal.) 
 
 सङ्केत legend — nouns [विभक्ति][वचन]: विभक्ति 1 प्रथमा · 2 द्वितीया · 3 तृतीया ·
4 चतुर्थी · 5 पञ्चमी · 6 षष्ठी · 7 सप्तमी · 8 सम्बोधन; वचन 1 एक · 2 द्वि · 3 बहु. (e.g. 11 = nom. sg.,
13 = nom. pl., 31 = inst. sg., 63 = gen. pl., 81 = voc. sg.) 
 सङ्केत legend — verbs [पुरुष][वचन]: पुरुष 3 प्रथम · 2 मध्यम · 1 उत्तम; वचन 1/2/3.
(e.g. 31 = 3rd sg., 11 = 1st sg., 33 = 3rd pl.) 
 Verb detail line (below the table, so the row stays narrow): धातु — धातुपाठ entry: उपदेश + अर्थ, गण + पद,
लकार, सङ्केत. Homonymous roots are DIFFERENT dhātus — name WHICH Dhātupāṭha entry the form comes from, decided by the
form (vikaraṇa/pada) AND the sense in this verse (साधु कलयति "considers" → कल गतौ सङ्ख्याने च, चुरादि — not कलँ
शब्दसङ्ख्यानयोः, भ्वादि). Add the ashtadhyayi.com number + Siddhānta-Kaumudī dhātu number ONLY when certain, in the form
`१०.०४०४ (कौमुदीधातुः- १८६६)`; otherwise omit the numbers (never guess them). Example: गम् — गमॢँ (गतौ), भ्वादि,
परस्मैपद, लट्, 31 · ०१.११३७ (कौमुदीधातुः- ९८२). 

 V. Sandhi-vicāra (सन्धि-विचार) 
 A junction-by-junction breakdown (own block or small table), one line per sandhi: पूर्वपद + परपद →
surface (CODE — brief rule/result). 
 Scope (important): mark sandhi only at pada boundaries (between words) and at the
internal member-junctions of a समास. Do NOT mark sandhi internal to a single prātipadika, dhātu,
subanta, or tiṅanta — e.g. skip the णत्व in रामेण or the गुण in भवति (intra-pada); but do mark the णत्व in
रामायण and the सवर्णदीर्घ in हराश्लिष्ट (they join compound members). Tag each junction with a code below;
where a junction is प्रकृतिभाव / प्रगृह्य (hiatus, no change), mark PRK. (Sūtra refs indicative; numbering
varies by recension.) 
 
 Svara / ac-sandhi: SVD सवर्णदीर्घ (6.1.101) · GUN गुण (6.1.87) · VRD वृद्धि (6.1.88) ·
 YAN यण् (6.1.77) · AYA अयादि (6.1.78) · PVR पूर्वरूप (6.1.109) · PRR पररूप (6.1.94). 
 Hal / vyañjana-sandhi: SCU श्चुत्व (8.4.40) · STU ष्टुत्व (8.4.41) · JSH जश्त्व
 (8.2.39 / 8.4.53) · CAR चर्त्व (8.4.55) · ANN अनुनासिक (8.4.45) · ANU अनुस्वार (8.3.23) · PSV
 परसवर्ण (8.4.58) · NUD ङमुट् / ङ्मुडागम (8.3.32) · HKC (ह+कार+चतुर्थ) हकार → चतुर्थ (8.4.62,
 optional — तद्+हित → तद्धित, वाक्+हरि → वाग्घरि) · CHT छत्व (8.4.63 / 6.1.73) · LAT लत्व (8.4.60) ·
 TUG तुगागम (6.1.73) · SAT षत्व (8.3.59) · NAT णत्व (8.4.1–2). (SAT/NAT only at समास/उपसर्ग junctions —
 e.g. रामायण, अभिषेक — never the intra-pada रामेण.) 
 Visarga-sandhi (no dash, 3 letters like every other code): VSS सकारादेश → स्
 (8.3.34; → श्/ष् before च-/ट-वर्ग via SCU/STU) · VSR रेफादेश → र् (8.3.15) · VSO उत्व, अः → ओ
 (6.1.113–114) · VSL विसर्गलोप — the visarga vanishes with nothing replacing it. Two sūtras, same
 code: the GENERAL case, अः/आः + vowel (6.1.114 / 8.3.19); and the सः/एषः-specific case, सुलोप
 (6.1.132 एतत्तदोः सुलोपोऽकोरनञ्समासे हलि — सः/एषः → स/एष, which fires before a consonant too, not just
 a vowel). Merged into one code 2026-07-28. (Optional: JHU जिह्वामूलीय / उपध्मानीय, visarga → ẖ / ḫ
 before क-ख / प-फ.) 
 No sandhi: PRK प्रकृतिभाव / प्रगृह्य — expected sandhi blocked, hiatus retained
 (dual -ई/-ऊ/-ए, अमी, etc.; 1.1.11–19, 6.1.115 ff.). 
 

 VI. Vibhaktyartha / kāraka sub-typing (defaults + override triggers) 
 The सङ्केत records case form; भूमिका records case function. Name the kāraka, and where it is
non-default/contested cite the sūtra in Vibhakti-vicāra and justify by अर्थ. 
 
 षष्ठी — default शेषे (2.3.50). Triggers: कृदन्त head → कर्तरि/कर्मणि-षष्ठी (2.3.65);
 if agent & object compete, karman keeps षष्ठी, agent → तृतीया (2.3.66); blocked to शेष by 2.3.69
 (क्त/क्तवतु, तृन्, अव्यय, खलर्थ); hetu-prayoge (2.3.26). 
 तृतीया — default कर्तृ/करणे (2.3.18). Triggers: सह/विना-योग (2.3.19 — a तृतीया caused by
 सह/विना/नाना/पृथक् is **उपपद-तृतीया (2.3.19), not करण** (nor हेतु); the case comes from the निपात,
 so that word is not the instrument of the क्रिया — e.g. in "पुण्यैः विना", पुण्यैः is उपपद-तृतीया,
 not करण), हेतौ (2.3.23, optionally पञ्चमी too — हेतौ तृतीया-पञ्चम्यौ), इत्थम्भूत-लक्षणे (2.3.21 —
 the तृतीया states a distinguishing mark/condition by which the referent is identified, e.g.
 गुणेन हीनः "deficient by reason of a quality" — this differs from an instrument actually used;
 it is an identifying mark), अपवर्गे। Also: the कर्ता of any कृत्य-प्रत्यय stays in तृतीया for that
 same reason (see the कृत्-प्रत्यय table below) — check that this is not mistakenly credited to a
 nearby सह/विना (गीता 1.22 "कैः मया सह योद्धव्यम्" — the तृतीया of मया comes from the
 योद्धव्यम्-कृत्य rule, not from सह; सह's actual target there is कैः, two words earlier, not the
 adjacent मया; do not assume an उपपद always governs the adjacent word — confirm by अर्थ/अन्वय,
 not by proximity). 
 चतुर्थी — default सम्प्रदाने (2.3.13). Triggers: तादर्थ्य (2.3.14), नमः/स्वस्ति/स्वाहा/अलम्
 (2.3.16), रुच्-अर्थ, स्पृह (verb) → ईप्सित (1.4.36). 
 पञ्चमी — default अपादाने (2.3.28). Triggers: भी/त्रा-अर्थ; a **कारण-पञ्चमी** (…त्वात्/…भावात्
 "because of X") is हेतु, but cite सूत्र **2.3.28** (अपादान-हेतु), not 2.3.23 (which prescribes
 तृतीया); **अन्य-योग = 2.3.29** अन्यारादितरर्तेदिक्छब्दाञ्चूत्तरपदाजाहियुक्ते — the correlate of a
 distinction governed by **अन्य** (=meaning-based, hence also भिन्न/विलक्षण/पर/अर्थान्तर)/इतर/आरात्/
 ऋते/दिक्-शब्द (पूर्वो ग्रामात्)/अञ्चु (प्राग् ग्रामात्)/आच्/आहि; भूमिका = **उपपद-पञ्चमी**, governor =
 that अन्य-word, not अपादान (e.g. in "प्रमादात् अन्यः", प्रमादात् = 2.3.29). ⚠ Narrow case: a
 तसिल्/case-ending सम्बन्धक अतः/ततः/यतः "therefore/hence" is a हेतु-adverb, not an अन्य-correlate —
 never give it 2.3.29. Also कर्मप्रवचनीय अप/आ/परि (2.3.10), प्रतिनिधि/प्रतिदान (2.3.11),
 **निर्धारण-पञ्चमी (2.3.42)**. 
 सप्तमी — default अधिकरणे (2.3.36). Triggers: सति सप्तमी (locative absolute /
 भावलक्षणसप्तमी), विषय-सप्तमी, निमित्ते, निर्धारण (2.3.41 यतश्च निर्धारणम् — selecting/comparing one
 out of some group, e.g. मनुष्येषु बुद्धिमान् "wise among men" — here no location is being stated,
 a comparison against the group is being made; षष्ठी also runs optionally in this same sense.
 Before treating an ordinary सप्तमी as अधिकरण, check whether it is निर्धारण — especially with a
 superlative/comparative विशेषण such as बुद्धिमान्, श्रेष्ठ; confirmed 2026-08-16 from actual corpus
 data, the मनुष्येषु of गीता 4.18). 
 द्वितीया — default कर्मणि (2.3.2). Triggers: कालाध्वनोः (2.3.5), अभितः/परि/धिक्-योग,
 कर्मप्रवचनीय-governed (अनु/उप, 2.3.8), **विना + द्वितीया** (the योगविभाग of 2.3.32, Kāśikā "विना वातम्").
 The destination of a गत्यर्थ (motion) verb is its कर्म (द्वितीया)
 (शरणं व्रज, ग्रामं गच्छति — शरणम्/ग्रामम् = कर्म, not a क्रियाविशेषण). 

 **An अन्वयी विशेषण has no case of its own** — it takes its विशेष्य's case by सामानाधिकरण्य; do not
 invent a सूत्र for it in an oblique case, nor cite the प्रथमा rule — it **inherits the विभक्ति-account
 of its विशेष्य** (e.g. in कृतैः पुण्यैः, पुण्यैः is उपपद-तृतीया, कृतैः merely agrees in अन्वय). Also,
 the **emphatic निपात एव/हि/तु/वै/खलु** is always a क्रियाविशेषण, never a विशेषण; and only च/वा/अथ are
 true coordination markers (समुच्चय-द्योतक). 
 

 अतिरिक्त कारक / सम्बन्ध उप-भूमिकाएँ — additional sub-roles (e-reader कारक-audit, 2026-08-19) 
 Name them in the भूमिका column whenever they occur — these are real distinctions marked by the
 UoHyd e-reader, not defaults. 
 
 मुख्य-कर्म / गौण-कर्म — with a द्विकर्मक (bitransitive) verb (दुह्/याच्/नी/पच्/दण्ड्…, 1.4.51
 अकथितं च) the two द्वितीयाs split into a primary and a secondary कर्म: गां दोग्धि पयः (पयः is
 मुख्य-कर्म, गाम् is गौण-कर्म). 
 प्रयोजक-कर्ता / प्रयोज्य-कर्ता — with णिच् (causative): the instigator (प्रयोजक) is the
 grammatical कर्ता; the one made to act (प्रयोज्य) is in द्वितीया for गति/बुद्धि/भक्ष्य/शब्दकर्म
 verbs (1.4.52), otherwise तृतीया (1.4.53) — देवदत्तेन कटं कारयति. 
 काल-अधिकरण / देश-अधिकरण — a सप्तमी अधिकरण that is specifically time versus
 place (both are अधिकरण; state the sub-distinction for clarity). 
 वीप्सा — reduplication (ग्रामं ग्रामम् "village by village"; 8.1.4 नित्यवीप्सयोः): द्वितीया,
 recognized by adjacent identical words. 
 उपमान / उपमेय — the standard of comparison versus the subject (with इव / यथा); इव itself is
 a comparison marker (उपमान-द्योतक), not a कारक. 
 प्रतिषेधः — a negation निपात (न / मा / नो) that negates the क्रिया; do not leave the भूमिका empty. 
 

 Note on authority: the 1.4 saṃjñā-sūtras define / sub-type a kāraka (e.g.
1.4.24 ध्रुवमपायेऽपादानम्; 1.4.45 आधारोऽधिकरणम् — whose त्रिविध division औपश्लेषिक/वैषयिक/अभिव्यापक is stated
in the Siddhānta-kaumudī, Mahābhāṣya-based); the 2.3 vibhakti-sūtras only assign the case. Cite the pair —
saṃjñā-sūtra for function, vibhakti-sūtra for form — rather than overloading the 2.3 rule. 

 Taddhita-avyaya प्रत्यय whose कारक-meaning is inherent 
 All of these are marked in the सङ्केत column as Y (अव्यय), but unlike an ordinary अव्यय/निपात, each
of them inherently expresses a specific कारक regardless of context — do not leave the भूमिका column
empty or infer it from a surrounding विभक्ति; write the कारक name directly (confirmed 2026-08-16 from
actual corpus data). 
 
 प्रत्यय सूत्र उदाहरण कारक 
 त्रल् सप्तम्यास्त्रल् तत्र, कुत्र, यत्र, सर्वत्र, अत्र अधिकरण 
 तसिल् पञ्चम्यस्तसिल् ततः, यतः, कुतः, सर्वतः, अन्यतः अपादान 
 थल्/धा सप्तम्याः थाल् / प्रकारवचने थाल्धाः कथम्, द्विधा, त्रिधा, बहुधा, एकधा, अनेकधा अधिकरण 
 दा (काल-अर्थ) — तदा, यदा, सर्वदा, कदा, एकदा अधिकरण (काल) 
 ह इदमो हः इह, कुह अधिकरण (स्थान) 
 

 कर्मप्रवचनीय उपपद (case-control by a निपात) 
 A कर्मप्रवचनीय changes the ordinary कारक of the noun it governs; some are single-sense-safe (they
give the same विभक्ति under both सूत्रs), some are genuinely bimodal (depends on अर्थ — make it explicit
in विभक्ति-विचार, do not silently pick one): 
 
 उपपद सूत्र/अर्थ विभक्ति note 
 प्रति 1.4.90 (लक्षण/इत्थम्भूत/भाग/वीप्सा) द्वितीया single-sense-safe 
 अनु 1.4.90 or 1.4.86 (हीने) द्वितीया same विभक्ति in both senses — single-sense-safe 
 परि 1.4.90 भाग-sense, or वर्जन-sense द्वितीया or पञ्चमी bimodal — decide by अर्थ 
 अति 1.4.95 or 2.3.9 सप्तमी or द्वितीया bimodal — decide by अर्थ (transgression versus extent) 
 अप वर्जन-sense पञ्चमी — 
 आ/आङ् meaning-dependent see context not single-sense-safe — check the 1.4.- series 
 

 सामानाधिकरण्य: विशेषण (attributive) versus समानाधिकरण (predicative) 
 When two words are in the same विभक्ति/लिङ्ग/वचन and point to one and the same thing, they are not
automatically interchangeable answers to the "who/what is X" question — there is a real functional
distinction between them (confirmed from the UoHyd kāraka-tagging-guidelines paper §5.4, May 2011): a
word is a विशेषण (attributive) when it states which referent is intended — it qualifies the topic
(topic/given); by contrast it is a कर्तृ-/कर्म-समानाधिकरण (predicative) when it presents new
information about an already-identified referent — it functions as the विधेय (predicate). One and the
same word can be either, purely on the basis of its function, not any morphological difference: 
 
 शयानं बालं पश्य ("look at the sleeping child") — here शयानम् is a विशेषण, restrictively stating which
 child (the one that is sleeping). 
 बालं शयानं पश्य ("the child — [is] sleeping, look") — the same word शयानम् is now a कर्तृ-समानाधिकरण:
 it says something new about the already-identified child, not stating which child. 
 Likewise, in देवदत्तः अध्यापकः अस्ति ("Devadatta is a teacher"), अध्यापकः is a predicate nominal
 (कर्तृ-समानाधिकरण), not an attributive विशेषण of देवदत्तः. 
 
 Practical effect: wherever only "विशेषण" would be written in the भूमिका column, check whether the
word is really functioning as a predicate (especially with a copula/cognition governor, or when
placing the word after its head noun changes the meaning) — in that case name it समानाधिकरण, and state
in विभक्ति-विचार which one it is and why. 

 विशेषण-कृदन्त ≠ re-tagging of its head-noun (e-reader कारक-audit, 2026-08-19).
A क्त/क्तवतु/तव्य/शतृ… कृदन्त that matches a noun in विभक्ति is that noun's विशेषण 
(or, predicatively, its समानाधिकरण) — do not re-tag the noun as that कृदन्त's कर्म merely because the
कृदन्त is कर्मणि. The noun keeps its own भूमिका toward the तिङन्त: in उदके प्रास्तः
सैन्धवखिल्यः (…अनुविलीयेत), प्रास्तः is a विशेषण of सैन्धवखिल्यः, and सैन्धवखिल्यः remains the कर्ता of
अनुविलीयेत, not the कर्म of प्रास्तः. Consistency check: the word a verb calls its कर्ता must itself be
a कर्ता; a कर्म-tagged word can never be that verb's कर्ता. 
 समुच्चय (coordination). In a conjoined कर्ता/कर्म (रामः लक्ष्मणः च गच्छतः), name the principal as
कर्ता/कर्म and the other as समुच्चित — it joins with the principal conjunct, not directly with the
क्रिया; the connective (च / वा) is itself a coordination marker (समुच्चय-द्योतक), not a कारक. 

 Never include a क्रियाविशेषण (adverb) in this [sāmānādhikaraṇya] analysis. A क्रियाविशेषण qualifies
the क्रिया/manner, not a noun, so it does not participate in सामानाधिकरण्य even if its विभक्ति happens
to match a noun (common adverbial forms like नित्यम्, कथम्, दृढम्, सम्यक् are all नपुंसक-द्वितीया in
form but express manner/mode, not agreement). One and the same surface word can genuinely be either —
the नित्यम् of गीता 2.21/2.26 is a विशेषण ("eternal [self]", real attributive agreement with the कर्म)
whereas the नित्यम् of गीता 2.30/18.64 is a क्रियाविशेषण ("always", an adverb) — decide by function,
never by the word's surface form or विभक्ति.
 And क्रियाविशेषण is not a fallback (two signals required): do not make a word a क्रियाविशेषण merely
 because its भूमिका is unclear. Assign it only when (1) it is an अव्यय or a functionally genuine
 adverbial क्रियाविशेषण-अच्/तृतीया (स्फुटम्/निरन्तरम्/सहसा), and (2) no कारक fits. A word whose विभक्ति
 yields a कारक (द्वितीया→कर्म, तृतीया→करण) is that कारक — e.g. in "विषयान् विषम् इव त्यज", विषम् =
 कर्म/उपमानम्, not a क्रियाविशेषण. If undecided, give "?", never make क्रियाविशेषण the default. 

 VII. Trigger checklist — run before finalizing any case 
 
 Is the governing word a कृत्य/क्त-कर्मणि form? (तव्य/अनीय/यत्/ण्यत्/क्यप्/केलिमर्, or क्त on a
 transitive धातु?) If yes, its कर्ता is in तृतीया for that reason — do this check before hunting for
 any उपपद, so that an unrelated सह/विना is not wrongly credited (see the कृत्-प्रत्यय table below and
 the गीता 1.22 note under तृतीया above). 
 Is the head/governing word a kṛdanta (घञ्/ल्युट्/क्तिन्-type action-noun)? If yes, a dependent षष्ठी may be
 कर्तरि/कर्मणि (2.3.65), not शेष — decide by अर्थ, apply 2.3.66 if both compete, re-check 2.3.69 exclusions
 (cf. ओदनस्य पाकः)। 
 Any उपपद (सह, विना, नमः, अलम्, धिक्, आ/प्रति/अनु…) or कर्मप्रवचनीय governing the case? If yes, that governs —
 flag it, don't default. Its actual target is not always the adjacent word (see the गीता 1.22 note
 above) — confirm by अर्थ/अन्वय, not by proximity. 
 A locative that isn't a physical locus? Consider सति सप्तमी / विषय-सप्तमी / निर्धारण 
 (2.3.41 — is a selection/comparison being made out of some group, often with a superlative, rather
 than stating place/time?). A तृतीया that isn't an instrument? Consider इत्थम्भूत-लक्षण (2.3.21) — is
 it stating not a means employed but an identifying mark? 
 Only after no trigger fires, assign the default kāraka. 
 

 VIII. Kṛdanta (कृदन्त) section — mandatory 
 List every kṛt-derived word (participle, action-noun, agent-noun, gerundive, absolutive, infinitive). For
each: धातु + कृत्प्रत्यय + its अर्थ (भावे / कर्तरि / कर्मणि / कारक), and the dhātu's transitivity (सकर्मक /
अकर्मक), since that governs whether and how a karman appears. Cross-reference Vibhakti-vicāra where the kṛdanta
governs a contested case. 
 
 घञ् (→ अ) — भावे action-noun, पुं; पाक, त्याग, बन्ध. Object → कर्मणि-षष्ठी (2.3.65) if सकर्मक. 
 ल्युट् (→ अन) — भावे, नपुं; गमन, करण. Object → कर्मणि-षष्ठी। 
 क्तिन् (→ ति) — भावे, स्त्री; गति, भक्ति. Object → कर्मणि-षष्ठी। 
 अच् (→ अ) — भावे/कर्तरि, पुं/स्त्री; unlike घञ्, no वृद्धि; फल (√फल्+अच्)। 
 क्त / क्तवतु — निष्ठा; क्त = कर्मणि/भावे, क्तवतु = कर्तरि. कर्तृ/कर्म षष्ठी blocked (2.3.69)
 → karman to प्रथमा (passive क्त, abhihita) or द्वितीया; agent → तृतीया. Exception (confirmed from
 Anusāraka's rule-engine, 2026-08-12): the 2.3.69 restriction does not apply to धातुs of the
 मन्/बुध्/पूज् family. Also, the क्त-form of an intransitive or गत्यर्थ/प्रत्यवसानार्थ धातु can also take
 a locative षष्ठी (3.4.76/2.3.68) — this is a narrow rule, distinct from the ordinary transitive
 कर्मणि-षष्ठी above. 
 शतृ / शानच् — present participle, कर्तरि; take acc. object. 
 तृच् / ण्वुल् — agent-nouns, कर्तरि. तृच् allows कर्मणि-षष्ठी (2.3.65); तृन् blocks षष्ठी
 (2.3.69) → object acc. 
 कृत्य (तव्य/तव्यत्, अनीय/अनीयर्, यत्, ण्यत्, क्यप्, केलिमर् — all 7 प्रत्यय termed कृत्य,
 3.4.70 तयोरेव कृत्यखलर्थाः) — gerundive, कर्मणि/भावे — inherently so, independent of the sentence's own
 प्रयोग; कर्तव्य, करणीय, कार्य, देय; केलिमर् is rare. Agent → तृतीया (2.3.18/2.3.71), object (if
 expressed) → प्रथमा (abhihita), never द्वितीया. 
 क्त (निष्ठा, → त) on a transitive धातु too falls in the कर्मणि class of 3.4.70 (its निष्ठा-pair
 partner क्तवतु always stays कर्तरि) — प्रोक्तः, कृतः, दृष्टः: agent → तृतीया, object → प्रथमा, just like
 कृत्य. (In some गत्यर्थ/स्थित्यर्थ धातुs, क्त can optionally be कर्तरि under 3.4.72 — treat it as
 optional; if the कर्तरि sense fits better, do not force कर्मणि.) 
 खल् (in the sense सुकर/दुष्कर, 3.3.126) is also in this कर्मणि class — सुकरः, दुर्दर्शः. Deliberately
 not listed here: युच् and घञ् can occasionally be कर्मणि (युच् in that same खलर्थ sense, 3.3.128; घञ्
 especially under 3.3.121 for the object itself, e.g. ग्रन्थः "that which is composed") but both are
 mostly not कर्मणि — it is not proper to assume कर्मणि merely from the प्रत्यय's name; decide by अर्थ and,
 when needed, state it explicitly in विभक्ति-विचार. 
 क्विप् (→ Ø, no visible affix) — agent-noun, कर्तरि; common compound-final (upapada-samāsa
 position); ब्रह्महा (√हन्+क्विप् → हा), सर्वजित्-type formations। 
 क्त्वा / ल्यप् — absolutive, अव्यय। 
 तुमुन् — infinitive, अव्यय। 
 

 IX. Samāsa (समास) — mandatory, RECURSIVE 
 Do a recursive विग्रह of every समास — do not stop at the outermost division alone. A long समास is a
nested stack of two-member समासs; peel it one layer at a time from the right (in तत्पुरुष/कर्मधारय the
final member is usually the principal/head) — at each layer give विग्रह + type (+ sub-type) + सूत्र, then
**resolve both members at every two-member split — both the principal/head and the non-principal, not
just the head/left spine** — go further inside any member that is itself a समास, until every leaf is an
underived प्रातिपदिक. **Any transparent तद्धित/कृत् derived member gets its own leaf — whether it is
left, MIDDLE, or final** (the middle member is often missed). For a leaf that is तद्धित/कृत् derived,
give its प्रत्यय + अर्थ + सूत्र (do not stop at the stem alone). **No member becomes a मूल-प्रातिपदिक
through frequency** — ordinary action/agent nouns formed in -अ (घञ्/अच्/अप्), -अन (ल्युट्), -ति (क्तिन्),
-तृ (तृच्), क्त/क्तवतु are also कृदन्त and must be peeled: भाव → √भू + घञ् (कृत्, 3.3.18); बाध → √बाध् +
घञ्; ज्ञान → √ज्ञा + ल्युट्; गति → √गम् + क्तिन्. **But उणादि-derived and रूढ़ (lexicalised) nouns do remain
मूल-प्रातिपदिक — do not peel these** (e.g. धर्म ← √धृ+मनिन्, मार्ग, कर्मन्): keep them just like an
underived stem (नर, गो). As an indented tree, outermost at the top. (This "peel from the right" method is
like iterated सन्धि-विच्छेद — until no further division remains. Zenodo's outermost-समास data can also be
opened up inside by this same method.) 
 Example — वैदिकधर्ममार्गपरता: 
 वैदिकधर्ममार्गपरता — वैदिकधर्ममार्गे परता — सप्तमी-तत्पुरुष (2.2.8, अधिकरण-अर्थ)
└ वैदिकधर्ममार्गः — वैदिकधर्मस्य मार्गः — षष्ठी-तत्पुरुष (2.2.8)
 └ वैदिकधर्मः — वैदिकश्च असौ धर्मः — कर्मधारय (विशेषण-पूर्वपद, 2.1.57)
 └ वैदिकः — वेदम् अधीते वेदाद् आगतो वा — तद्धित (अण्, 4.2.59/4.3.101); प्रकृति = वेद
 └ धर्मः — अव्युत्पन्न प्रातिपदिक (उणादि √धृ+मनिन् — रूढ़, kept as मूल)
 └ मार्गः — अव्युत्पन्न प्रातिपदिक (रूढ़, kept as मूल)
└ परता — परस्य भावः — तद्धित (तल्/त्व, भावे, 5.1.119); प्रकृति = पर 
 समास-संक्षेप: TP तत्पुरुष (उपभेद+सूत्र: षष्ठी 2.2.8 · सप्तमी 2.2.8 · चतुर्थी
2.1.36 · पञ्चमी 2.1.37 · नञ्-TP 2.2.6 · उपपद-TP 2.2.19 · प्रादि/गति-TP) · KD कर्मधारय (2.1.57) · द्विगु
(2.1.52) · BV बहुव्रीहि (2.2.24) · द्वन्द्व (इतरेतर 2.2.29 / समाहार) · अव्ययीभाव (2.1.6)। 

 X. Taddhita (तद्धित) 
 Identify any तद्धितान्त derivative and its प्रत्यय + अर्थ। 

 XI. Vibhakti-vicāra (विभक्ति-विचार) — conditional 
 Provide this section only when a case is kṛt-governed, upapada-driven, karmapravacanīya-redirected, or
otherwise contested. Lay out the competing vibhaktyartha parses, cite each governing sūtra, and adjudicate by
अर्थ/context. Omit entirely when every case takes its default kāraka. (The भूमिका column already carries the
routine function for every word.) 

 XII. Anvaya (अन्वय) 
 Prose reordering; enclose every implicit/supplied word in [square brackets] (e.g. [अस्ति]). Keep the anvaya
and translation mutually consistent: any word the English implies must appear (bracketed) in the anvaya, and
vice versa. For a definition (lakṣaṇa) verse, prefer the correlative [या] … [सा] frame ("that which …, that is
X") over a bare juxtaposition; both या/सा agree with the definiens, the definiendum stays प्रथमा. Bracket
supplied या/सा/अस्ति — they are interpretive scaffolding, not in the received text. Supply any elided kartā
per §III (verb person / quotation frame / correlative → [कश्चित्] / existential), never by borrowing a
nominative from another clause. 

 XIII. Translation (English) — literal & case-faithful 
 Give a literal, grammar-faithful rendering (no free paraphrase) that reflects every vibhaktyartha decision.
The English construction must mirror the actual kāraka — never a phrasing that implies a different case: 
 
 शेष-षष्ठी (possessor) → "my / of X / of mine" — never "for me / to X". (e.g. न मे स्पृहा = "there is no
 longing of mine", not "for me there is no longing".) 
 चतुर्थी (सम्प्रदाने) → "to / for"; तादर्थ्य → "for the sake of". 
 तृतीया — agent under a passive (अनुक्त-कर्ता) → "by"; करण → "with / by means of". 
 कर्मणि-षष्ठी → "the X of Y" (the doing of Y), not "Y's X". 
 विषय-सप्तमी → "regarding / in / with respect to"; औपश्लेषिक अधिकरण → literal "in/on"; अपादान → "from". 
 
 Watch possessive drift: attach a genitive to the noun it actually governs, not a neighbour
(e.g. मे owns स्पृहा → "my longing," not "the fruit of my action"). Sanskrit has no dative-of-possession — a
possessor is genitive in the English too. 
 "What the grammar buys" note (conditional): whenever a case was resolved in Vibhakti-vicāra,
add one line showing how that case-role shapes the English (e.g. कर्मणि-षष्ठी → "the binding of you," not "your
bondage"). Include only when a vicāra decision was actually made. 

 XIV. Notes 
 
 This is LLM linguistic analysis — strong, but flag ambiguous forms (multiple parses, rare dhātus, subtle
 samāsa/taddhita) and show reasoning; recommend a scholarly spot-check. Exact Dhātu-pāṭha numbering and
 commentary attributions vary by recension. 
 For any kṛdanta-governed / upapada / karmapravacanīya case, show the competing parses in Vibhakti-vicāra
 and disambiguate by अर्थ — do not silently default to शेष/अधिकरण। 
 The target of an उपपद is not always the adjacent word — confirmed by an actual example (गीता 1.22)
 that सह can govern a word two words away rather than the one right beside it; not proximity, but
 अर्थ/अन्वय is decisive. 
 Segment before you tag (§III): resolve each clause's kārakas against its own verb; never
 link a governor across a full sentence boundary (॥ / वाक्यान्त इति + वचन-क्रिया)। 
 

 Example output (रामः वनं गच्छति) 
 Prayoga: कर्तरि 
 
 पद प्रातिपदिक/धातु कोटि सङ्केत भूमिका टिप्पणी 
 रामः राम सुबन्त (पुं) 11 कर्ता "Rāma"; प्रथमा एक. 
 वनम् वन सुबन्त (नपुं) 21 कर्म "forest"; द्वितीया एक. 
 गच्छति गम् तिङन्त 31 (लट्) — "goes"; प्र.पु. एक. 
 
 Verb detail: गम् — गमॢँ (गतौ), भ्वादि, परस्मैपद, लट्, 31 · ०१.११३७ (कौमुदीधातुः- ९८२). 
 सन्धि-विचार: रामः + वनम् → रामो वनम् (VSO — अः + व → ओ); वनम् + गच्छति → वनं गच्छति (ANU — म् + ग → ं)। 
 समास: none · कृदन्त: none · तद्धित: none · विभक्ति-विचार: none (all cases take their default kāraka) 
 अन्वय: रामः वनं गच्छति। (Clause: one main वाक्य, कर्तरि — कर्ता overt, no elision.) 
 Translation: "Rāma goes to the forest."

---
Now perform the FULL analysis (all sections) on this single verse:
<VERSE>
>>> PROMPT END
