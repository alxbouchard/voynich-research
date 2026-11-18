"""Inventaire des légendes simples et des trois fenêtres des notices botaniques."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / '2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, labels, tokens

TARGETS = {'cpheor', 'cpheol'}
WINDOWS = ('ligne_1', 'ligne_2', 'positions_1_a_16')


def edition(rows, faces, split):
    inscriptions = labels(rows, split)
    single = {loc:seq[0] for loc,seq in inscriptions.items()
              if len(seq) == 1 and re.fullmatch('[a-z]+',seq[0])}
    within_labels = Counter(w for seq in inscriptions.values() for w in seq)
    retained = {loc:w for loc,w in single.items() if within_labels[w] == 1}
    pages, occurrences = defaultdict(list), defaultdict(list)
    global_counts, pairs = Counter(), []
    for loc,(face,kind,_,raw) in rows.items():
        seq = tokens(raw, split)
        global_counts.update(seq)
        for n,w in enumerate(seq,1):
            if w in TARGETS:
                occurrences[w].append([loc,kind,n])
            if n < len(seq) and (w,seq[n]) in {('cpheol','cpheor'),('cpheor','cpheol')}:
                pairs.append([loc,kind,n,w,seq[n]])
        if face in faces and kind == 'P0':
            pages[face].append((loc,seq))
    inventory = {}
    for name in WINDOWS:
        pos = Counter()
        hits = defaultdict(list)
        face_count = 0
        for face, lines in pages.items():
            if name == 'positions_1_a_16':
                window = [(loc,i,w) for loc,seq in lines for i,w in enumerate(seq,1)][:16]
            else:
                selected = lines[int(name[-1])-1:int(name[-1])]
                window = [(loc,i,w) for loc,seq in selected for i,w in enumerate(seq,1)]
            face_count += bool(window)
            for loc,i,w in window:
                pos['positions'] += 1
                pos['lisibles'] += bool(re.fullmatch('[a-z]+', w))
                if w in within_labels:
                    hits[w].append([face,loc,i])
        inventory[name] = {'faces':face_count, **pos, 'hits':dict(hits)}
    rare = {loc:w for loc,w in retained.items() if global_counts[w] == 2}
    return {'legendes':len(inscriptions),'simples_lisibles':len(single),'uniques':retained,
            'un_seul_autre':rare,'fenetres':inventory,'occurrences':occurrences,
            'paires':pairs,'faces_sans_P0':sorted(faces-pages.keys())}


def summarize(sources):
    domains = {}
    keys = list(sources)
    labs = sources[keys[0]]['uniques']
    for name in ('uniques','un_seul_autre'):
        common = {w:loc for loc,w in labs.items() if all(s[name].get(loc)==w for s in sources.values())}
        result = {}
        for window in WINDOWS:
            form_hits = {}
            for w,loc in common.items():
                # Rapprochement au même locus dans chaque édition ; un espace en amont peut varier.
                sets = [{(face,line) for face,line,_ in ed['fenetres'][window]['hits'].get(w,[])}
                        for ed in sources.values()]
                shared = set.intersection(*sets)
                if shared:
                    form_hits[w] = {'legende':loc,'lignes':sorted(shared)}
            result[window] = {'formes':len(form_hits),'couples_forme_face':sum(
                len({f for f,_ in v['lignes']}) for v in form_hits.values()), 'detail':form_hits}
        domains[name] = {'denominateur':len(common),'formes_et_legendes':common,'fenetres':result}
    return domains


if __name__ == '__main__':
    eds, sections = corpus()
    faces = {f for f,c in sections.items() if c=='H'}
    report = {'faces_herbier_IVTFF':len(faces),'conventions':{}}
    for split in ('joints','separes'):
        source = {ed:edition(rows, faces, split) for ed,rows in eds.items()}
        stats = {'accord':summarize(source), **{ed:summarize({ed:s}) for ed,s in source.items()}}
        for s in source.values():
            for stripe in s['fenetres'].values():
                del stripe['hits']
        report['conventions'][split] = {'comptes':stats,'entrees':source}
    (HERE/'resultats.json').write_text(json.dumps(report, ensure_ascii=False, indent=1)+'\n')
