#!/usr/bin/env python3
"""Export pratīka → target-word alignments from the DEPLOYED academy build (read-only).
Usage: .venv/bin/python work/share-tamal/export/export_alignments.py <academy_dir> <provenance_dir> <out_dir>
Reads reading-*.html + lane-*.json (the build-time exact targets written by searchtool/khan/jump_resolve.js) and
analysis-data/pratika-provenance/<text>.json (who marked each pratīka). Writes <out>/<text>-<lane>.tsv + counts.json."""
import sys, os, re, json, glob, collections
from lxml import html as LH

ACAD, PROV_DIR, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
UNIFIED = ['isha','kena','kathaka','prashna','mundaka','mandukya','taitiriya','aitareya','chandogya','brha','gita','bs']
PRAK = {'vc':'vivekacudamani','pd':'panchadashi','ab':'atmabodha','sad':'saddarshanam','ups':'upadesasaram'}
TEXTNAME = {'isha':'isha','kena':'kena','kathaka':'katha','prashna':'prashna','mundaka':'mundaka','mandukya':'mandukya',
  'taitiriya':'taittiriya','aitareya':'aitareya','chandogya':'chandogya','brha':'brihadaranyaka','gita':'gita','bs':'brahmasutra'}
def lane_name(fam, side):
    if side == 'tika': return 'nyayanirnaya' if fam == 'bs' else 'anandagiri'
    return {'shankaranandi':'shankaranandi','sridhara':'sridhari','madhusudana':'madhusudani','nilakantha':'nilakanthi',
            'dhanapati':'dhanapati','bhashyarka':'bhashyarka','vanamala':'vanamala','ratnaprabha':'ratnaprabha',
            'brahmatattva':'brahmatattvaprakashika','purnanandi':'purnanandi'}.get(side, side)
# where the pratīka MARKS come from (lanes without per-item provenance); per item: printed vs detected via data-pdet
LANE_MARKS = {
  'anandagiri': 'per item: as = advaitaśārada <prateeka> markup; mri = bold in the Mahesh Research Institute print',
  'nyayanirnaya': 'printed: advaitaśārada <span class="pratika"> markup',
  'bhashyarka': 'printed: bold in the Dakshinamurti Math print (PDF text layer)',
  'dhanapati': 'printed: Gita Supersite e-text marks / opening «…इति»',
  'sridhari': 'printed = bold in Sri Tamal Maharaj\'s e-text (+ restored opening «…इति»); detected = see METHOD',
  'madhusudani': 'no printed marks in the source; detected = see METHOD',
  'nilakanthi': 'printed = Gita Supersite <b>; detected = see METHOD',
  'shankaranandi': 'printed = marked in the Nirṇayasāgara 1916 print; detected = see METHOD',
  'brahmatattvaprakashika': 'detected (the TSS print marks none) = see METHOD',
  'vanamala': 'Sri Tamal Maharaj\'s marks (paragraph-opening pratīka) + bold in the Mahesh Research Institute print',
  'ratnaprabha': 'Sri Tamal Maharaj\'s marks (<span class="pk"> in his e-text)',
  'purnanandi': 'Sri Tamal Maharaj\'s marks; its alignment to the Ratnaprabhā word is also his (rw), checked exact-or-nothing',
}
DEV = re.compile(r'[ऀ-ॿ]')
MARK_CODE = {'nyayanirnaya': 'printed:as', 'bhashyarka': 'printed:print-bold', 'dhanapati': 'printed:supersite',
  'sridhari': 'printed:tamal-bold', 'nilakanthi': 'printed:supersite-bold', 'madhusudani': 'printed:opening-iti',
  'shankaranandi': 'printed:print', 'vanamala': 'marked:tamal-or-mri', 'ratnaprabha': 'marked:tamal', 'purnanandi': 'marked:tamal'}
NORM = lambda s: re.sub(r'[^ऀ-ॿ]|इति$|ति$', '', re.sub(r'[^ऀ-ॿ]', '', s or ''))
GLOB = {}

def text_of(el):
    """surface as printed: prefer the sandhi (bhsj) form, drop the पद copy (bhsp)."""
    parts = []
    def walk(e):
        cls = e.get('class') or ''
        if 'bhsp' in cls.split(): 
            if e.tail: parts.append(e.tail)
            return
        if e.text: parts.append(e.text)
        for c in e: walk(c)
        if e is not el and e.tail: parts.append(e.tail)
    walk(el)
    return re.sub(r'\s+', ' ', ''.join(parts)).strip()

def parse_key(k):
    """'<Slug>:<ref>[::zone]:<local>' → (ref, layer, ord) ; layer mula|bhashya|bhashya-intro|tika:<side>|…"""
    m2 = re.match(r'^([^:]+):([^:]+):(\d+):(\d+)$', k)   # Gītā/BS-style mūla key = deposit word i, pada j
    if m2: return (m2.group(2), 'mula', (int(m2.group(3)), int(m2.group(4))))
    m = re.match(r'^([^:]+):(.*):([^:]+)$', k)
    if not m: return (None, None, None)
    ref, loc = m.group(2), m.group(3)
    if re.fullmatch(r'\d+', loc): return (ref, 'mula', int(loc))
    mm = re.fullmatch(r'b(\d+)', loc)
    if mm: return (ref, 'bhashya', int(mm.group(1)))
    mm = re.fullmatch(r'ib(\d+)-(\d+)', loc)
    if mm: return (ref, 'bhashya', int(mm.group(2)))
    mm = re.fullmatch(r't([A-Za-z]+)_(\d+)_(?:s(\d+)_)?(\d+)', loc)
    if mm: return (ref, 'tika:' + mm.group(1) + (':sub' if mm.group(3) else ''), int(mm.group(4)))
    return (ref, 'other', loc)

def lane_frags(fam):
    out = []
    for f in sorted(glob.glob(f'{ACAD}/lane-{fam}-*.json')):
        if not re.match(rf'lane-{fam}(-\d+)?-[a-z]+\.json$', os.path.basename(f)): continue
        j = json.load(open(f)); out.extend(j.get('h') or [])
    return out

def pages(fam):
    fs = [f for f in glob.glob(f'{ACAD}/reading-{fam}*.html') if re.match(rf'reading-{fam}(-\d+)?\.html$', os.path.basename(f))]
    return sorted(fs, key=lambda f: int((re.search(r'-(\d+)\.html$', f) or [0, 0])[1]))


DEPOSIT = os.environ.get('DEPOSIT_DIR', 'prasthanatrayi-zenodo-deposit/data')   # the Zenodo deposit's data/ folder
DEP_STATS = {}
def dnorm(x): return re.sub(r'[^ऀ-ॿ]', '', re.sub(r'\([^)]*\)', '', x)).replace('ं', 'म्')
def deposit_map(W, slug):
    """our mūla word key → 'w<i>.p<j>': word i (0-based) of the verse in Sri Tamal Maharaj's deposit (prasthan-words-<slug>.json),
    pada j of its 'p' split. Only verses whose whole word sequence aligns are mapped."""
    cands = [slug] + ([slug + '_pada', slug + '_vakya'] if slug == 'Kena' else [])
    best = ({}, 0, 0, None, 0)
    for sl in cands:
        f = f'{DEPOSIT}/prasthan-words-{sl}.json'
        if not os.path.exists(f): continue
        d = json.load(open(f)); d = d[next(iter(d))]
        out = {}; ok = bad = 0
        uses_ij = any(o[1] >= 0 for (r_, l_), lst in W.groups.items() if l_ == 'mula' for o, k in lst)
        for (ref, layer), lst in W.groups.items():
            if layer != 'mula' or ref not in d: continue
            ours = [k for o, k in sorted(lst)]
            if uses_ij:   # keys carry the deposit word index (+ pada index for a split word): map directly
                for o, k in lst: out[k] = f'w{o[0]}.p{max(o[1], 0)}'
                ok += 1; continue
            seq = []
            for i, w in enumerate(d[ref]):
                for j, pd in enumerate([x for x in re.split(r'\s\+\s', re.sub(r'\([^)]*\)', '', w.get('p') or w.get('w') or '')) if dnorm(x)]):
                    seq.append((f'w{i}.p{j}', dnorm(pd)))
            # word-level alignment (difflib over normalized padas): equal runs → exact w<i>.p<j>; a differing block whose
            # deposit padas all belong to ONE deposit word i → w<i> (our split differs inside that word); otherwise unmapped
            import difflib
            A = [dnorm(W.w[k]) for k in ours]; B = [n for _, n in seq]
            sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
            got = 0
            for tag, a1, a2, b1, b2 in sm.get_opcodes():
                if tag == 'equal':
                    for x in range(a2 - a1): out[ours[a1 + x]] = seq[b1 + x][0]; got += 1
                elif tag == 'replace':
                    ws = {seq[y][0].split('.')[0] for y in range(b1, b2)}
                    if len(ws) == 1:
                        for x in range(a1, a2): out[ours[x]] = next(iter(ws)); got += 1
            if got == len(ours): ok += 1
            else:
                bad += 1
                if os.environ.get('DBG') == slug and bad <= 3:
                    print('  PARTIAL', sl, ref, [W.w[k] for k in ours][:12], [n for _, n in seq][:12])
        WORDS = sum(1 for (r_, l_), lst in W.groups.items() if l_ == 'mula' for _ in lst)
        if len(out) > len(best[0]): best = (out, ok, bad, sl, WORDS)
    DEP_STATS[slug] = {'deposit_file': best[3] and f'prasthan-words-{best[3]}.json', 'verses_fully_mapped': best[1], 'verses_partly_mapped': best[2],
                       'mula_words': best[4], 'mula_words_mapped': len(best[0])}
    return best[0]

COLS = ['text','lane','ref','unit','pratika','lemma','mark','target_layer','target_ref','target_ord','target_occ','target_word','target_deposit',
        'target2_layer','target2_ref','target2_ord','target2_occ','target2_word','target2_deposit','member','status','source_key']
COUNTS = {}
def write(textn, lane, rows):
    base = f'{OUT}/{textn}-{lane}'
    lines = ['\t'.join(COLS)] + ['\t'.join(str(r.get(c, '') if r.get(c, '') is not None else '').replace('\t',' ').replace('\n',' ') for c in COLS) for r in rows]
    data = '\n'.join(lines) + '\n'
    if len(data.encode()) < 45_000_000:
        open(base + '.tsv', 'w').write(data); files = [os.path.basename(base) + '.tsv']
    else:
        files = []; chunk = []; size = 0; part = 1; hdr = lines[0]
        for ln in lines[1:]:
            chunk.append(ln); size += len(ln.encode()) + 1
            if size > 40_000_000:
                open(f'{base}.part{part}.tsv', 'w').write(hdr + '\n' + '\n'.join(chunk) + '\n'); files.append(f'{os.path.basename(base)}.part{part}.tsv'); part += 1; chunk = []; size = 0
        if chunk: open(f'{base}.part{part}.tsv', 'w').write(hdr + '\n' + '\n'.join(chunk) + '\n'); files.append(f'{os.path.basename(base)}.part{part}.tsv')
    c = collections.Counter(r['status'] for r in rows)
    c['unlinked'] += c.get('forced-first-word', 0)
    c2 = collections.Counter(('mula' if r['target_layer'].startswith('mula') else r['target_layer']) for r in rows if r['status'].startswith('linked'))
    COUNTS[f'{textn}-{lane}'] = {'pratikas': len(rows), 'linked': len(rows) - c.get('unlinked', 0), 'unlinked': c.get('unlinked', 0),
        'to_bhashya': c2.get('bhashya', 0), 'to_mula': c2.get('mula', 0), 'to_tika': c2.get('ratnaprabha', 0) + c2.get('tika', 0),
        'forced_first_word': c.get('forced-first-word', 0), 'detected': sum(1 for r in rows if r.get('mark', '').startswith('detected')), 'files': files}

class WordIndex:
    def __init__(self): self.w = {}; self.groups = collections.defaultdict(list); self.dep = {}
    def add(self, k, txt):
        if k in self.w: return
        self.w[k] = txt
        ref, layer, o = parse_key(k)
        if isinstance(o, (int, tuple)): self.groups[(ref, layer)].append((o if isinstance(o, tuple) else (o, -1), k))
    def finish(self):
        self.occ = {}
        for g, lst in self.groups.items():
            seen = collections.Counter()
            for o, k in sorted(lst):
                t = self.w[k]; seen[t] += 1; self.occ[k] = seen[t]
    def target(self, k):
        if not k: return {}
        ref, layer, o = parse_key(k)
        lay = layer
        if layer and layer.startswith('tika:'): lay = layer.split(':')[1]
        od = f'{o[0]}.{o[1]}' if isinstance(o, tuple) else o
        return {'layer': lay, 'ref': ref, 'ord': od, 'occ': self.occ.get(k, ''), 'word': self.w.get(k, '?MISSING'), 'dep': self.dep.get(k, '') if lay == 'mula' else ''}

def put(r, n, t):
    p = 'target' if n == 1 else 'target2'
    if not t: return
    r[p + '_layer'], r[p + '_ref'], r[p + '_ord'], r[p + '_occ'], r[p + '_word'] = t['layer'], t['ref'], t['ord'], t['occ'], t['word']
    r[p + '_deposit'] = t.get('dep', '')

def do_unified(fam):
    textn = TEXTNAME[fam]
    trees = []
    for f in pages(fam): trees.append(LH.fromstring(open(f, encoding='utf-8').read()))
    fr = lane_frags(fam)
    if fr: trees.append(LH.fromstring('<div>' + ''.join(fr) + '</div>'))
    W = WordIndex(); ti = {}
    for t in trees:
        for e in t.iter('span'):
            k = e.get('data-k')
            if k and 'w' in (e.get('class') or '').split():
                W.add(k, text_of(e))
                if e.get('data-ti') is not None:
                    ref, layer, o = parse_key(k); ti.setdefault((ref, e.get('data-ti')), k)
    W.finish()
    slug = next(iter(W.w)).split(':')[0]
    W.dep = deposit_map(W, slug)
    prov = {}
    pf = f'{PROV_DIR}/{fam}.json'
    if os.path.exists(pf): prov = json.load(open(pf))
    global GLOB
    GLOB = collections.defaultdict(set)   # lemma → set of source-sets (used only when the ref-local match fails and it is unambiguous)
    for lst in prov.get('tika', {}).values():
        for it in lst: GLOB[NORM(it[0])].add(','.join(it[1]))
    # ---- bhāṣya → mūla quotes ----
    rows = []; seen = set(); pb = prov.get('bhashya', {}); pcur = collections.defaultdict(int)
    for t in trees:
        for e in t.iter('span'):
            if e.get('data-jm') is None: continue
            k = e.get('data-k')
            if not k or k in seen: continue
            seen.add(k)
            ref, layer, o = parse_key(k)
            raw = e.get('data-w') or W.w.get(k, '')
            src = ''
            lst = pb.get(ref, []); i = pcur[ref]
            for j in range(i, min(i + 40, len(lst))):
                if lst[j][0] == raw: src = ','.join(lst[j][2]); pcur[ref] = j + 1; break
            if e.get('data-jma') is not None: src = (src + ',' if src else '') + 'adjudicated'
            kind = []
            if e.get('data-msub'):
                ms = e.find_class('msub'); q = ms[0].text_content() if ms else ''
                kind.append('sub-word'); pr = q
            else: pr = raw
            if e.get('data-jmp'): kind.append('hand-pin')
            r = {'text': textn, 'lane': 'bhashya', 'ref': ref, 'unit': k.split(':')[-1], 'pratika': pr, 'lemma': raw if pr != raw else '',
                 'mark': ';'.join(filter(None, [src] + kind)), 'source_key': k}
            tk = e.get('data-jmt')
            if tk: put(r, 1, W.target(tk)); r['status'] = 'linked'; r['member'] = e.get('data-jmm') or ''
            elif e.get('data-jmq'): r['status'] = 'linked-cross-verse'; r['target_layer'] = 'mula'; r['target_word'] = '(the one verse of the text containing this quote; resolved in the reader)'
            else: r['status'] = 'unlinked'
            rows.append(r)
    if rows: write(textn, 'bhashya', rows)
    # ---- ṭīkā pratīkas ----
    by_lane = collections.defaultdict(list); seen = set(); pt = prov.get('tika', {}); tcur = collections.defaultdict(int)
    for t in trees:
        for e in t.iter('span'):
            cls = (e.get('class') or '').split()
            if 'tk-prat' not in cls and 'tk-sprat' not in cls: continue
            ws = [x for x in e.iter('span') if x.get('data-k') and 'w' in (x.get('class') or '').split()]
            if not ws: continue
            k0 = ws[0].get('data-k')
            if k0 in seen: continue
            seen.add(k0)
            ref, layer, o = parse_key(k0)
            m = re.search(r':t([A-Za-z]+)_(\d+)(?:_s(\d+))?_\d+$', k0)
            side = m.group(1) if m else '?'
            sub = 'tk-sprat' in cls
            lane = 'purnanandi' if sub else lane_name(fam, side)
            unit = f't{side}_{m.group(2)}' + (f'_s{m.group(3)}' if m and m.group(3) else '') if m else ''
            printed = ' '.join(W.w.get(x.get('data-k'), '') for x in ws if DEV.search(W.w.get(x.get('data-k'), '')))
            lemma = e.get('data-lemma') or ''
            mark = ''
            if lane == 'anandagiri':
                lst = pt.get(ref, []); i = tcur[ref]
                hit = None
                for j in list(range(i, len(lst))) + list(range(0, i)):
                    if NORM(lst[j][0]) in (NORM(lemma), NORM(printed)): hit = j; break
                if hit is not None: mark = ','.join(lst[hit][1]); tcur[ref] = hit + 1
                else:
                    g = GLOB.get(NORM(lemma)) or GLOB.get(NORM(printed))
                    if g and len(g) == 1: mark = next(iter(g))
            elif e.get('data-pdet') is not None: mark = 'detected'
            else: mark = MARK_CODE.get(lane, 'printed')
            r = {'text': textn, 'lane': lane, 'ref': ref, 'unit': unit, 'pratika': printed, 'lemma': lemma, 'mark': mark, 'source_key': k0}
            tg = []
            if sub:
                if e.get('data-jst'): tg.append(W.target(e.get('data-jst')))
            else:
                if e.get('data-jbt'): tg.append(W.target(e.get('data-jbt')))
                if e.get('data-jti') is not None:
                    kk = ti.get((ref.split('::')[0], e.get('data-jti')))
                    if kk: tg.append(W.target(kk))
                if e.get('data-jmt'): tg.append(W.target(e.get('data-jmt')))
            if sub and tg: tg[0]['layer'] = 'ratnaprabha'
            for n, x in enumerate(tg[:2], 1): put(r, n, x)
            r['member'] = e.get('data-jmm') or ''
            r['status'] = 'linked' if tg else 'unlinked'
            by_lane[lane].append(r)
    for lane, rows in by_lane.items(): write(textn, lane, rows)
    do_vartika_tika(fam, trees)


VKRUN = re.compile(r'[\u0900-\u0963\u0966-\u096F\u0971-\u097F]+')
def do_vartika_tika(fam, trees):
    """Śāstraprakāśikā (ṭīkā on Sureśvara's Bṛhad-vārttika) fold-outs: <template data-id=ID> holds the notes; each .vk-prat
    carries data-vw = the word number in the vārttika verse that precedes <details class="vk-tk" data-tk=ID> (the reader numbers
    the verse's Devanāgarī runs with the पद copies (bhsp) removed and daṇḍas excluded — reproduced here)."""
    verse = {}
    for t in trees:
        for d in t.iter('details'):
            if 'vk-tk' not in (d.get('class') or '').split(): continue
            v = d.getprevious()
            x = None if v is None else next((e for e in v.iter('span') if 'vk-x' in (e.get('class') or '').split()), None)
            if x is None: continue
            inner = (x.text or '') + ''.join(LH.tostring(c, encoding='unicode') for c in x)
            inner = re.sub(r'<span class="bhsp">[^<]*</span>', '', inner)
            toks = [w for w in VKRUN.findall(re.sub(r'<[^>]+>', ' ', inner)) if not re.fullmatch(r'[०-९]+', w)]   # verse numbers are not words (reader fix 2026-10-25)
            n = next((e.text_content() for e in v.iter('span') if 'vk-n' in (e.get('class') or '').split()), '')
            verse[d.get('data-tk')] = (x.get('data-k') or '', n, toks)
    rows = []; seen = set()
    for t in trees:
        for tp in t.iter('template'):
            tid = tp.get('data-id')
            if not tid or tid in seen: continue
            els = [e for e in tp.iter('span') if 'vk-prat' in (e.get('class') or '').split()]
            if not els: continue
            seen.add(tid)
            vk, vn, toks = verse.get(tid, ('', '', []))
            ref = parse_key(vk)[0] if vk else ''
            for e in els:
                vw = e.get('data-vw')
                r = {'text': TEXTNAME[fam], 'lane': 'shastraprakashika', 'ref': ref, 'unit': tid, 'pratika': text_of(e), 'lemma': '',
                     'mark': 'printed:print', 'source_key': vk}
                if vw is not None and vw.isdigit() and int(vw) < len(toks):
                    i = int(vw); occ = toks[:i + 1].count(toks[i])
                    r.update({'target_layer': 'vartika', 'target_ref': f'{ref} · vārttika {vn}'.strip(), 'target_ord': i, 'target_occ': occ,
                              'target_word': toks[i], 'status': 'linked'})
                    L = lambda w: re.sub(r'[^अ-ह]', '', w)[:2]
                    if not any(L(w) and L(w) == L(toks[i]) for w in re.sub(r'[।॥*]', ' ', r['pratika']).split()): r['mark'] += ';check'
                else: r['status'] = 'unlinked'
                rows.append(r)
    if rows: write(TEXTNAME[fam], 'shastraprakashika', rows)

def do_prak(fam):
    textn = PRAK[fam]
    lanes = {'vc': 'vyakhya-candrasekhara', 'pd': 'padadipika', 'ab': 'tika-padmapada', 'sad': 'tika-kapali', 'ups': 'bhashya-ganapati'}
    rows = []
    for f in pages(fam):
        t = LH.fromstring(open(f, encoding='utf-8').read())
        ids = {}; byverse = collections.defaultdict(list)
        for e in t.iter('span'):
            i = e.get('id')
            if i and re.match(r'mb?-', i):
                ids[i] = text_of(e)
                mm = re.match(r'(mb?-.+)-(\d+)$', i)
                if mm: byverse[mm.group(1)].append((int(mm.group(2)), i))
        occ = {}
        for v, lst in byverse.items():
            c = collections.Counter()
            for o, i in sorted(lst): c[ids[i]] += 1; occ[i] = c[ids[i]]
        for e in t.iter('span'):
            if 'pratika' not in (e.get('class') or '').split(): continue
            tgt = e.get('data-t') or ''
            sec = next((a.get('id') for a in e.iterancestors() if a.get('id')), '')
            mm = re.match(r'mb?-(.+)-(\d+)$', tgt)
            gw = 'gw' in (e.get('class') or '').split()
            r = {'text': textn, 'lane': lanes[fam], 'ref': sec, 'unit': '', 'pratika': text_of(e), 'lemma': '',
                 'mark': 'march:glossed-word' if gw else 'march:raw-commentary', 'source_key': ''}
            if mm and tgt in ids:
                r.update({'target_layer': 'mula' if tgt.startswith('m-') else 'mula-half-verse', 'target_ref': mm.group(1), 'target_ord': mm.group(2), 'target_occ': occ.get(tgt, ''), 'target_word': ids[tgt],
                          'status': 'linked' if gw else 'forced-first-word'})
            else: r['status'] = 'unlinked'
            rows.append(r)
    if rows: write(textn, lanes[fam], rows)

for fam in UNIFIED:
    print('…', fam, flush=True); do_unified(fam)
for fam in PRAK:
    print('…', fam, flush=True); do_prak(fam)
json.dump({'lanes': COUNTS, 'deposit_mula_mapping': DEP_STATS}, open(f'{OUT}/counts.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(DEP_STATS, ensure_ascii=False))
for k, v in COUNTS.items(): print(k, {x: y for x, y in v.items() if x != 'files'})
