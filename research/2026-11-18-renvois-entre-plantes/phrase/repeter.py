"""L'élément qui précède daiin est-il prévisible à sa droite ?"""
import argparse
from collections import Counter,defaultdict
from pathlib import Path
import random
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from croiser import CAT,MODES,adjacent,corpus,leaf,load,metadata,save,segment,texts
from corpus_dam import parse

def events():
    all_pages=texts("tout",True);ed,_=corpus();meta=metadata();panels=load(CAT)["panneaux"]
    for p,rows in sorted(all_pages.items()):
        if not rows or not p[1:2].isdigit() or leaf(p) in {18,102}:continue
        sec="plantes" if meta[p].get("I")=="H" else "fragments" if p in panels else "autres"
        for i,(a,b) in enumerate(zip(rows,rows[1:])):
            if b[0]!="daiin" or not adjacent(a,b):continue
            nxt=rows[i+2] if i+2<len(rows) and adjacent(b,rows[i+2]) else None
            variants=[]
            for j,(e,m) in enumerate(MODES):
                _,parts=parse(ed[e][b[1]][3],m)
                simple=[w for block in parts for w in block]
                rank=b[3][j]
                variants.append(simple[rank] if rank<len(simple) else None)
            edge=None
            if nxt:
                _,parts=parse(ed["H"][b[1]][3],"joints")
                last=sum(map(len,parts))
                edge="fin" if nxt[3][0]==last else "interieur"
            key=f"{a[1]}/{a[3][0]}"
            yield key,p,sec,a[0],nxt[0] if nxt else None,edge,variants

def announce():
    out={}
    for key,p,sec,w,_,_,_ in events():
        if len(segment(w))<4 or w=="daiin":continue
        out[key]={"ancre":w,"page":p,"section":sec,"annonce_repetition":w,
                  "annonce_du_passage":(["qokol"] if sec=="plantes" else ["oky"] if sec=="fragments" else ["qokol","oky"]) if w=="qokol" else []}
    return out

def verify(pred):
    cases={}; strata=defaultdict(list); bases=defaultdict(Counter)
    for key,p,sec,w,n,edge,variants in events():
        if w!="qokol" and n:bases[sec][n]+=1
        if key not in pred:continue
        cases[key]={**pred[key],"lu":n,"lectures_du_rang_suivant":variants}
        if n:strata[p,edge].append((w,n))
    rng=random.Random(188102);dist=Counter();expected=0;hits=0
    for group in strata.values():
        a,b=map(Counter,zip(*group));expected+=sum(a[w]*b[w] for w in a)/len(group);hits+=sum(x==y for x,y in group)
    varying=0;fixed=0;shuffle_groups=[]
    for group in strata.values():
        left,right=map(list,zip(*group))
        if len(set(left))>1 and len(set(right))>1 and set(left)&set(right):
            shuffle_groups.append((left,right));varying+=len(group)
        else:fixed+=sum(a==b for a,b in group)
    for _ in range(9999):
        total=fixed
        for a,b in shuffle_groups:
            rng.shuffle(b);total+=sum(x==y for x,y in zip(a,b))
        dist[total]+=1
    return {"lieux":cases,"repetition":{"annonces":len(pred),"evaluables":sum(map(len,strata.values())),
             "exact":hits,"esperance":expected,"essais_variables":varying,"histogramme":dist,
             "aussi_haut":sum(v for k,v in dist.items() if k>=hits),"tirages":sum(dist.values())},
             "qokol_daiin":{k:r for k,r in cases.items() if r["ancre"]=="qokol"},
             "apres_daiin_sans_qokol":{sec:{"total":sum(cnt.values()),"qokol":cnt["qokol"],"oky":cnt["oky"]} for sec,cnt in bases.items()}}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=('annoncer','ouvrir'))
    f=HERE/'REPETITIONS-ANNONCEES.json.gz'
    if parser.parse_args().mode=='annoncer':save(f,announce())
    else:
        pred=load(f);assert pred==announce();save(HERE/'REPETITIONS-OUVERTES.json.gz',verify(pred))
