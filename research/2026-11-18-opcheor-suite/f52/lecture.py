"""Deux alternances sur f52v sous une seule table, puis transfert à un autre feuillet."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import gzip
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"cle"))
from chercher import A,B,THIRD_PAGE,candidates_for,corpora,decode,index,merged,segment,unite

def calculate(data):
    pool=index(data)
    candidates=lru_cache(maxsize=None)(lambda g,cap:candidates_for(g,cap,pool))
    pairs=set()
    for word in THIRD_PAGE:
        u=segment(word)
        pairs.update(zip(u,u[1:]))
    stats={}; announced={}; joint={}
    for n in range(3):
        for rule in combinations(sorted(pairs),n):
            shape=lambda words:tuple(merged(w,rule) for w in words)
            for cap in (1,2):
                here=candidates(shape(THIRD_PAGE),cap)
                label=json.dumps([rule,cap],separators=(",",":"))
                stats[label]=len(here)
                for loc,pos,words,key in here:
                    fourth=decode("cheol",rule,key)
                    known=[decode(w,rule,key) for w in A+B]
                    signature=(loc,pos,fourth)
                    if signature not in announced:
                        announced[signature]=dict(lieu=[loc,pos+1],mots=words,quatrieme=fourth,
                                                  fusions=rule,table=key,lus_aux_deux_autres=known)
                    for name,triple in (("f89",A),("f100",B)):
                        for loc2,pos2,ws2,key2 in candidates(shape(triple),cap):
                            if (loc,pos)==(loc2,pos2):
                                continue
                            fixed=unite(key,key2)
                            if fixed is None:
                                continue
                            dis=(loc,pos,loc2,pos2,name,fourth,tuple(sorted(fixed.items())),rule)
                            joint[dis]=dict(f52=[loc,pos+1,words],autre=[name,loc2,pos2+1,ws2],
                                            quatrieme=decode("cheol",rule,fixed),table=fixed,fusions=rule)
    return {"regles":stats,"predictions":list(announced.values()),"avec_autre":list(joint.values())}

def analyze(mode,xml):
    source=HERE/"LECTURES-ANNONCEES.json.gz"
    data=corpora(xml)
    if mode=="annoncer":
        out={name:calculate(body) for name,body in data.items()}
    else:
        original=json.loads(gzip.decompress(source.read_bytes()))
        out={}
        for name,body in data.items():
            decoded=[]
            for r in original[name]["predictions"]+original[name]["avec_autre"]:
                loc,pos=(r["lieu"] if "lieu" in r else r["f52"][:2])
                w=body[loc][pos+2] if pos+2<len(body[loc]) else None
                decoded.append({**r,"atteste":w,"succes":None if None in (w,r["quatrieme"]) else w==r["quatrieme"]})
            out[name]=decoded
        source=HERE/"LECTURES-OUVERTES.json.gz"
    source.write_bytes(gzip.compress((json.dumps(out,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode(),mtime=0))

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("annoncer","ouvrir"));p.add_argument("xml",type=Path)
    a=p.parse_args();analyze(a.mode,a.xml)
