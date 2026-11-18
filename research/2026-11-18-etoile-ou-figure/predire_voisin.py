"""Restituer un voisin entier d'une légende reprise dans la prose de même main."""
from collections import Counter, defaultdict
import argparse
import json
import sys
from combiner import HERE, segment, write
sys.path.insert(0,str(HERE.parent/"2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, metadata, strict_rows


def sites(section):
    ed,_ = corpus()
    meta = metadata()
    for loc,(page,kind,_,_) in ed["H"].items():
        info = meta.get(page,{})
        if (kind,info.get("I"),info.get("H"),info.get("L"))!=("P0",section,"2","B"):
            continue
        if loc not in ed["ZL"] or ed["ZL"][loc][1]!="P0":
            continue
        rows=list(aligned(ed,loc,page,section,page,Counter()))
        for i,row in enumerate(rows):
            word,block = row['mot'],row['troncon']
            ranks = list(map(int,row['rangs_quatre'].split('/')))
            neighbours={}
            for shift,key in ((-1,"gauche"),(1,"droite")):
                if 0<=i+shift<len(rows):
                    adj=rows[i+shift]
                    ar=list(map(int,adj['rangs_quatre'].split('/')))
                    if adj['troncon']==block and all(a+shift==b for a,b in zip(ranks,ar)):
                        neighbours[key]=adj['mot']
            yield f"{loc}/{block}/{ranks[0]}",word,neighbours


def namespace():
    src=json.loads((HERE/'ANNONCES.json').read_bytes())['apprentissage']
    return sorted({r['mot'] for r in src.values() if r['lot']=='figures' and r['mot'] and r['mot'].endswith('edy')})


def rank(c):
    return sorted(c,key=lambda w:(-c[w],w))


def announce():
    words=namespace()
    tables={key:{d:Counter() for d in ['gauche','droite']} for key in [*words,'tout','edy']}
    for _,w,neighbours in sites('B'):
        labels=['tout']
        if tuple(segment(w))[-3:]==('e','d','y'):
            labels.append('edy')
        if w in words:
            labels.append(w)
        for k in labels:
            for d,v in neighbours.items():
                tables[k][d][v]+=1
    ans={k:{d:{'trois':rank(c)[:3],'effectifs':[c[x] for x in rank(c)[:3]],'n':sum(c.values())}
            for d,c in v.items()} for k,v in tables.items()}
    write('VOISINS-ANNONCES.json',ans)


def verify():
    ann=json.loads((HERE/'VOISINS-ANNONCES.json').read_bytes())
    out = {}
    for loc,w,neighbours in sites('H'):
        if w not in namespace():
            continue
        out[loc]={'ancre':w,'voisins':neighbours}
    score={}
    for chosen in (['dshedy'],namespace()):
        candidates=[x for x in out.values() if x['ancre'] in chosen]
        for method in ['ancre','edy','tout']:
            vals=Counter()
            for row in candidates:
                key=row['ancre'] if method=='ancre' else method
                for d,actual in row['voisins'].items():
                    preds=ann[key][d]['trois']
                    vals['lieux']+=1
                    vals['abstention']+=not preds
                    vals['premier']+=bool(preds and preds[0]==actual)
                    vals['trois']+=actual in preds
            score[('dshedy' if len(chosen)==1 else 'toutes')+'/'+method]=vals
    write('VOISINS-RESULTATS.json',{'etendue':score,'ouvertures':out})


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['annoncer','verifier'])
    announce() if p.parse_args().mode=='annoncer' else verify()
