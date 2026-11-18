"""Retrouver les mêmes cinq mots malgré un décalage de rang au début de la ligne."""
from collections import Counter, defaultdict
import json
import re
import sys
from aligner import HERE, EDGES, corpus, sequence, write, manuscript


def search(views):
    tables=[]
    for seq in views:
        candidates=defaultdict(list)
        for i in range(len(seq)-4):
            ws=tuple(w for _,w in seq[i:i+5])
            if seq[i][0]!=seq[i+4][0] or ws[1]!=ws[3] or ws[1]!="daiin":continue
            if len(set(ws))==4 and all(re.fullmatch("[a-z]+",w) for w in ws):
                candidates[ws].append(i)
        tables.append(candidates)
    for ws in sorted(set.intersection(*(set(t) for t in tables))):
        if all(len(t[ws])==1 for t in tables):
            yield ws,[t[ws][0] for t in tables]


def main(mode):
    ed,_=corpus(); gallery,_,_=manuscript()
    if mode=="predire":sites=[]
    else:sites=json.loads((HERE/"LOCAL-PREDICTIONS.json").read_text())
    idx=defaultdict(list)
    for r in sites:idx[r["lieu"]].append(r)
    for loc in sorted(set.intersection(*(set(v) for v in ed.values()))):
        page=loc.split(".")[0]
        rs=[b[loc] for b in ed.values()]
        if page.startswith("f99") or any(r[1]!="P0" for r in rs):continue
        vs=[sequence(r[3],cut) for r in rs for cut in ("joints","separes")]
        if mode=="predire":
            for ws,coords in search(vs):
                sites.append(dict(lieu=loc,dans_panneaux=page in gallery,mots=ws,
                                  positions=coords,prevision="daiin"))
        elif loc in idx:
            for r in idx[loc]:
                obs={}
                for k,d in EDGES.items():
                    values=[seq[i+d][1] if 0<=i+d<len(seq) and seq[i+d][0]==seq[i][0] else None
                            for seq,i in zip(vs,r["positions"])]
                    w=values[0]
                    obs[k]=w if w and len(set(values))==1 and re.fullmatch("[a-z]+",w) else None
                r["observes"]=obs
    write("LOCAL-PREDICTIONS.json" if mode=="predire" else "LOCAL-RESULTATS.json",sites)


if __name__=="__main__":main(sys.argv[1])
