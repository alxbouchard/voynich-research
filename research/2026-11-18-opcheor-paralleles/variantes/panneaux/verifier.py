"""Croise les légendes entières et les paires r/l, à l'intérieur de chaque cahier."""
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from compter import SIMPLE, analyze, corpus, langage, runs, segment
from transfert import labels

MODES=[(ed,cut) for ed in ('H','ZL') for cut in ('joints','separes')]


def admissible_labels(versions, page):
    signature={}
    for loc in sorted(set.intersection(*(set(book) for book in versions))):
        if loc.partition('.')[0]!=page:
            continue
        vals=[book[loc] for book in versions]
        if len(vals[0])==1 and all(ws==vals[0] for ws in vals) and SIMPLE.fullmatch(vals[0][0]):
            signature[loc]=vals[0][0]
    return signature


def loci_pairs(rows, page, cut):
    data=defaultdict(list)
    for locus,(p,kind,_,raw) in rows.items():
        if p!=page or kind!='P0':
            continue
        for span in runs(raw,cut):
            words=[w for _,w in span]
            for i,a,b in analyze(words)[1]:
                if a.endswith('r'):
                    data[locus,a,b].append(span[i][0])
    return data


def compare(captions, pairs):
    encounters=[]
    for loc,word in captions.items():
        units=segment(word)
        shorter={units[:i]+units[i+1:] for i,u in enumerate(units) if u=='ch'}
        for row in pairs:
            start=segment(row['mots'][0])
            if units==start or start in shorter:
                method='exact' if units==start else 'effacer_ch'
                encounters.append({'legende':loc,'mot_legende':word,'regle':method,**row})
    return encounters


def main():
    eds,_=corpus()
    books=[labels(eds[ed],cut) for ed,cut in MODES]
    panel_sets=[]
    for ed in eds.values():
        with_labels={p for p,kind,_,_ in ed.values() if kind=='Lf'}
        with_prose={p for p,kind,_,_ in ed.values() if kind=='P0'}
        panel_sets.append(with_labels & with_prose)
    assert panel_sets[0]==panel_sets[1]
    pages=sorted(panel_sets[0])
    quires=dict(re.findall(r'^<(f\w+)>\s+<![^>]*\$Q=(\w)',(langage.DATA/'ZL3b-n.txt').read_text(),re.M))
    captions,pairs={},{}
    for page in pages:
        captions[page]=admissible_labels(books,page)
        versions=[loci_pairs(eds[ed],page,cut) for ed,cut in MODES]
        pairs[page]=[]
        for key in sorted(set.intersection(*(set(d) for d in versions))):
            loc,a,b=key
            pairs[page].append({'ligne':loc,'mots':[a,b],'multiplicite':min(len(d[key]) for d in versions),
                                'rangs':{'/'.join(mode):d[key] for mode,d in zip(MODES,versions)}})
    assert all(v['multiplicite']==1 for vs in pairs.values() for v in vs)
    rows={}
    totals=defaultdict(Counter)
    for p,q in product(pages,repeat=2):
        if quires[p]!=quires[q]:
            continue
        result=compare(captions[p],pairs[q])
        rows[p+'>'+q]=result
        kind='meme_panneau' if p==q else 'autre_panneau_du_cahier'
        group=totals[kind]
        group['cellules']+=1
        group['cellules_exploitables']+=int(bool(captions[p] and pairs[q]))
        group['comparaisons_legende_paire']+=len(captions[p])*len(pairs[q])
        group['cellules_positives']+=int(bool(result))
        group.update(v['regle'] for v in result)
    result={'cahiers':{p:quires[p] for p in pages},'legendes':captions,'paires':pairs,'cellules':rows,'totaux':totals}
    (HERE/'resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main()
