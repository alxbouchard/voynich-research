"""Choisir un mot commun sur les deux faces à baies, puis vérifier les quatre nouvelles faces."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'2026-11-18-dam-en-fin-de-ligne'))
from corpus_dam import aligned,corpus,metadata,MODES,parse,WORD

INITIAL=('ctheor','ctheol')
TRAIN=('f17v','f96v')
TEST=('f35v','f37r','f89r2','f101v')
LABELS=('f89r2.4','f101v.7')


def leaf(page):
    return int(re.match(r'f(\d+)',page)[1])


def lines(ed, pages, retain):
    for loc,(p,kind,_,raw) in ed['H'].items():
        if kind=='P0' and p in pages and loc in ed['ZL'] and ed['ZL'][loc][1]=='P0':
            if retain(p):
                yield p,loc


def select():
    ed,_=corpus();m=metadata();ref=defaultdict(list)
    herbal={p for p,item in m.items() if item.get('I')=='H'}
    for p,loc in lines(ed,herbal,lambda p:p in TRAIN or leaf(p) not in {17,35,37,96}):
        ref[p].extend(r['mot'] for r in aligned(ed,loc,p,'H',leaf(p),Counter()))
    shared=(set(ref[TRAIN[0]])&set(ref[TRAIN[1]]))-set(INITIAL)
    candidates=[]
    for w in shared:
        local=[ref[p].count(w) for p in TRAIN]
        count=len({leaf(p) for p,s in ref.items() if p not in TRAIN and w in s})
        first=[ref[p].index(w)+1 for p in TRAIN]
        candidates.append(dict(mot=w,occurrences=local,autres_feuillets=count,premieres_positions=first))
    candidates.sort(key=lambda r:(-min(r['occurrences']),r['autres_feuillets'],*r['premieres_positions'],r['mot']))
    return dict(mot_choisi=candidates[0]['mot'] if candidates else None,candidats=candidates,
                positions_apprentissage={p:len(ref[p]) for p in TRAIN},feuillets_reference=sorted({leaf(p) for p in ref if p not in TRAIN}))


def open_data(forecast):
    ed,_=corpus();meta=metadata()
    panels=set(json.loads((HERE.parent/'RENVOIS.json').read_bytes())['panneaux'])
    herb={p for p,item in meta.items() if item.get('I')=='H'}
    wanted=set(INITIAL)|{forecast['mot_choisi']}
    strict=Counter(); hits=defaultdict(list); views=defaultdict(lambda:defaultdict(Counter)); seen=defaultdict(lambda:defaultdict(list))
    for p,loc in lines(ed,herb|panels,lambda p:True):
        for r in aligned(ed,loc,p,meta[p].get('I'),leaf(p),Counter()):
            strict[p]+=1
            if r['mot'] in wanted:
                hits[p].append([loc,r['troncon'],r['rangs_quatre'],r['mot']])
    # Les éditions peuvent compter une ligne P0 dans une seule source ;
    # ici chaque fréquence à une seule lecture utilise toutes ses propres lignes P0.
    for e,mode in MODES:
        for loc,(p,kind,_,raw) in ed[e].items():
            if p not in herb|panels or kind!='P0':
                continue
            name=e+'/'+mode
            _,blocks=parse(raw,mode)
            for b,block in enumerate(blocks,1):
                for i,w in enumerate(block,1):
                    if WORD.fullmatch(w):
                        views[p][name][w]+=1
                    if w in wanted:
                        seen[p][name].append([loc,b,i,w])
    labels={}
    for loc in LABELS:
        labels[loc]={}
        for e,mode in MODES:
            p,k,_,raw=ed[e][loc]
            assert k=='Lf'
            _,blocks=parse(raw,mode)
            labels[loc][e+'/'+mode]=blocks
    output={}
    for p in TEST+TRAIN:
        output[p]=dict(positions_strictes=strict[p],resultats_stricts=hits[p],
                       lectures={n:dict(positions_lisibles=sum(c.values()),occurrences=seen[p][n]) for n,c in views[p].items()})
    controls={}
    for name,pages in [('autres_grandes',herb-{p for p in herb if leaf(p) in {17,35,37,96}}),('autres_panneaux',panels-set(TEST)-{'f99r','f100r'})]:
        controls[name]={}
        for mode in [e+'/'+cut for e,cut in MODES]+['strict']:
            sizes={p:strict[p] if mode=='strict' else sum(views[p][mode].values()) for p in pages}
            records={p:hits[p] if mode=='strict' else seen[p][mode] for p in pages}
            eligible={p for p in pages if sizes[p]>0}
            controls[name][mode]=dict(faces_avec_lecture=len(eligible),positions=sum(sizes.values()),
                par_mot={w:{"faces":sum(any(s[-1]==w for s in records[p]) for p in eligible),"occurrences":sum(sum(s[-1]==w for s in records[p]) for p in eligible)} for w in sorted(wanted)})
    return dict(faces=output,etiquettes=labels,temoins=controls)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=['annoncer','ouvrir']);mode=parser.parse_args().mode
    if mode=='annoncer':
        out=select();dest=HERE/'ANNONCE.json'
    else:
        out=open_data(json.loads((HERE/'ANNONCE.json').read_bytes()));dest=HERE/'OUVERTURE.json'
    dest.write_text(json.dumps(out,indent=1,ensure_ascii=False,sort_keys=True)+'\n')
