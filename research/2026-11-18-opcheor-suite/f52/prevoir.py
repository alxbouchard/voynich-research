"""Prévoir le voisin d'un groupe en eeor sans voir le mot suivant."""
from collections import Counter, defaultdict
import argparse
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from suites import EXCLUDED, adjacent, aligned, corpus, edge, segment

def read_windows():
    ed,sections=corpus()
    for loc,(face,kind,*_) in ed["H"].items():
        if kind!="P0" or loc not in ed["ZL"] or ed["ZL"][loc][1]!=kind:
            continue
        leaf=int(re.match(r"f(\d+)",face)[1])
        if leaf in EXCLUDED | {52}:
            continue
        rows=list(aligned(ed,loc,face,sections[face],leaf,Counter()))
        for i,row in enumerate(rows):
            key=f"{loc}/{row['troncon']}/{row['rang_troncon_IT']}"
            next_row=rows[i+1] if i+1<len(rows) and adjacent(row,rows[i+1]) else None
            prior=False
            if i>=2 and adjacent(rows[i-2],rows[i-1]) and adjacent(rows[i-1],row):
                a,b=[segment(x["mot"]) for x in rows[i-2:i]]
                prior=len(a)>=3 and a[:-1]==b[:-1] and (a[-1],b[-1])==("r","l")
            yield key,face,row["mot"],prior,next_row

def forecasts():
    announced={}
    for key,face,word,prior,_ in read_windows():
        signs=segment(word)
        if signs[-4:]!=("e","e","o","r"):
            continue
        base="".join(signs[:-4])
        announced[key]=dict(face=face,ancre=word,paire_avant=prior,retirer=base+"eol",garder=base+"eeol")
    return announced

def verify(pred):
    obs={}; byface=defaultdict(Counter); byword=defaultdict(Counter)
    for key,face,w,_,nxt in read_windows():
        if not nxt:
            continue
        if w.endswith("r"):
            tag=(face,edge(nxt))
            byface[tag][nxt["mot"]]+=1
            byword[tag,w][nxt["mot"]]+=1
        if key in pred:
            obs[key]=nxt
    rows={}
    for k,p in pred.items():
        n=obs.get(k)
        rec={**p,"lu":n["mot"] if n else None}
        if n:
            tag=p["face"],edge(n)
            matches=byface[tag]-byword[tag,p["ancre"]]
            rec["temoins"]=sum(matches.values())
            for rule in ("retirer","garder"):
                rec[rule+"_temoins"]=matches[p[rule]]
        rows[k]=rec
    out={}
    for group,include in [("cheeor",lambda r:r["ancre"]=="cheeor"),("autres",lambda r:r["ancre"]!="cheeor"),("apres_paire",lambda r:r["paire_avant"])]:
        part=[r for r in rows.values() if include(r)]
        known=[r for r in part if r["lu"] is not None]
        supported=[r for r in known if r["temoins"]]
        out[group]={"occasions":len(part),"lisibles":len(known),"lieux_avec_temoins":len(supported),
                    **{rule:{"exact":sum(r[rule]==r["lu"] for r in known),
                             "attendues_lieux_avec_temoins":sum(r[rule+"_temoins"]/r["temoins"] for r in supported)}
                       for rule in ("retirer","garder")}}
    return {"lieux":rows,"bilan":out}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=["annoncer","ouvrir"])
    mode=parser.parse_args().mode
    output=HERE/"ANNONCES.json"
    data=forecasts()
    if mode=="ouvrir":
        assert data==json.loads(output.read_bytes())
        data=verify(data)
        output=HERE/"OUVERTURE.json"
    output.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=1)+"\n")
