"""Comparer les mots de part et d'autre des interruptions matérialisées dans les éditions."""
import argparse
from collections import Counter,defaultdict
from itertools import accumulate
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from croiser import MODES,corpus,leaf,load,save
from aligner import WORD,bords,parse

def tokens_and_marks(raw,mode):
    marks,parts=parse(raw,mode)
    offsets=list(accumulate(map(len,parts)))[:-1]
    cuts=defaultdict(list)
    for offset,mark in zip(offsets,marks):cuts[offset].append(mark)
    return tuple(w for part in parts for w in part),cuts,marks

def interruptions():
    ed,_=corpus()
    for loc,(page,k,*_) in ed["H"].items():
        if k!="P0" or not page[1:2].isdigit() or leaf(page) in (3,23) or loc not in ed["ZL"] or ed["ZL"][loc][1]!="P0":continue
        views=[tokens_and_marks(ed[e][loc][3],m) for e,m in MODES]
        for source in (0,2):
            ref,cuts,_=views[source]
            if not cuts:continue
            maps=[bords.forced(ref,v[0]) for v in views]
            for j,markers in cuts.items():
                if markers!=["<->"] or j==0 or j>=len(ref):continue
                if not all(j-1 in mapping for mapping in maps):continue
                next_ids=[mapping[j-1]+1 for mapping in maps]
                cross=[v[1].get(idx,[]) for idx,v in zip(next_ids,views)]
                if cross[:2]==cross[2:]==[["<->"],["<->"]]:
                    if source!=0:continue
                    kind="commun" if all(v[2]==views[0][2] for v in views) else "commun_local"
                elif cross[:2]==[["<->"],["<->"]] and cross[2:]==[[],[]] and source==0:kind="IT_seul"
                elif cross[:2]==[[],[]] and cross[2:]==[["<->"],["<->"]] and source==2:kind="ZL_seul"
                else:continue
                after=[v[0][idx] if idx<len(v[0]) else None for idx,v in zip(next_ids,views)]
                right=after[0] if len(set(after))==1 and after[0] and WORD.fullmatch(after[0]) else None
                before=[v[0][idx-2] if idx>=2 and idx-1 not in v[1] else None for idx,v in zip(next_ids,views)]
                previous=before[0] if len(set(before))==1 and before[0] and WORD.fullmatch(before[0]) else None
                key=f"{loc}/{MODES[source][0]}/{j}"
                yield key,loc,page,kind,previous,ref[j-1],right,after

def masks():
    return {key:dict(ligne=loc,page=p,classe=kind,avant=[prev,left],annonce="sol")
            for key,loc,p,kind,prev,left,_,_ in interruptions() if left=="daiin"}

def open_words(pred):
    result={};others=defaultdict(list); data=list(interruptions())
    for key,loc,p,kind,prev,left,w,variants in data:
        if key in pred:
            result[key]={**pred[key],"lu":w,"lectures":variants}
        elif w:others[p,kind].append((loc,w))
    stats={}
    for kinds in (["commun"],["commun_local","IT_seul","ZL_seul"]):
        for subset in ("tout","ol","qokol"):
            rows=[v for v in result.values() if v["classe"] in kinds]
            if subset=="ol":rows=[v for v in rows if (v["avant"][0] or "").endswith("ol")]
            if subset=="qokol":rows=[v for v in rows if v["avant"][0]=="qokol"]
            exposed=[v for v in rows if v["lu"]]
            out=dict(annonces=len(rows),lisibles=len(exposed),exacts=sum(v["lu"]=="sol" for v in exposed),
                     debuts_sol=sum(v["lu"].startswith("sol") for v in exposed))
            for within in ("ligne","face"):
                baselines=[]
                for r in exposed:
                    pool=[w for cl in kinds for l,w in others[r["page"],cl] if within=="face" or l==r["ligne"]]
                    if pool:baselines.append((sum(w=="sol" for w in pool)/len(pool),sum(w.startswith("sol") for w in pool)/len(pool)))
                out[within]=dict(cibles_avec_temoins=len(baselines),attendues_exact=sum(x for x,y in baselines),
                                 attendues_debut=sum(y for x,y in baselines))
            stats["+".join(kinds)+"/"+subset]=out
    return {"bilan":stats,"lieux":result,"coupures_avec_gauche_lisible":dict(Counter(v[3] for v in data))}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("mode",choices=("annoncer","ouvrir"));mode=p.parse_args().mode
    path=HERE/"PREDICTIONS.json";pred=masks()
    if mode=="annoncer":save(path,pred)
    else:
        assert pred==load(path);save(HERE/"VERIFICATION.json",open_words(pred))
