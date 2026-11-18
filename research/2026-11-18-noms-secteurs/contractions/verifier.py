"""Relecture indépendante des fenêtres et des probabilités des cinq fichiers résultats."""
import gzip
import itertools
import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
DATA=HERE.parents[2]/"voynich_20261028/data"


@lru_cache(None)
def raw(page,n,ed,spacing,variant):
    path=DATA/({"H":"IT2a-n.txt","ZL":"ZL3b-n.txt"}[ed])
    txt=next(x.split(">",1)[1].strip() for x in path.read_text().splitlines() if x.startswith(f"<{page}.{n},"))
    txt=re.sub(r"<[-~]>",".",txt)
    txt=re.sub(r"<[^>]+>","",txt)
    seq=txt.replace(",","." if spacing=="separe" else "").split(".")
    row=[]
    for i,part in enumerate((w for w in seq if w),1):
        choose=lambda m:"?" if variant=="strict" else m[1].split(":")[0 if variant=="first" else -1]
        w=re.sub(r"\[([^\]]+)\]",choose,part).replace("{","").replace("}","")
        row.append([f"{page}.{n}:{i}",w if re.fullmatch("[a-z]+",w) else None])
    return row


@lru_cache(None)
def products(a,b,collapse):
    def units(w):
        return re.findall(r"c[kptf]h|[cs]h|.",re.sub("ii+","i",w) if collapse else w)
    left,right=units(a),units(b)
    return {("".join(left[:l]),"".join(right[r:])) for l in range(2,len(left)) for r in range(1,len(right)-1)}


def derive(labels,panels,collapse,reverse):
    found=set()
    for d,lines in panels.items():
        for line in lines:
            for k in range(len(line)-1):
                segment=line[k:k+2]
                a,b=[w for _,w in (segment[::-1] if reverse else segment)]
                if not (a and b):
                    continue
                for left,right in products(a,b,collapse):
                    for q,query in labels.items():
                        for t,(loc,w) in enumerate(query):
                            expected=re.sub("ii+","i",w) if w and collapse else w
                            if expected!=left+right:
                                continue
                            copies=(t+1<len(query) and k+2<len(line) and bool(line[k+2][1])
                                    and query[t+1][1]==line[k+2][1])
                            complete=(t==0 and (len(query)==1 or (copies and len(query)==2)))
                            found.add((int(q),int(d),segment[0][0],loc,left,right,bool(copies),bool(complete)))
    return found


@lru_cache(None)
def exact(n,q,active_rows):
    """Seules les requêtes ayant une possibilité augmentent le score."""
    m=len(active_rows)
    outcomes=Counter(sum(j in allowed for j,allowed in zip(p,active_rows))
                     for p in itertools.permutations(range(n),m))
    return [outcomes[i]*math.perm(n-m,q-m) for i in range(q+1)]


def audit(path):
    r=json.loads(gzip.decompress(path.read_bytes()))
    page=r["page"]
    geo=r["geometrie"]
    n=len(geo["destinations"])
    checked=0
    for reading,v in r["lectures"].items():
        ed,space,var=reading.split("/")
        row=lambda locus:raw(page,locus,ed,space,var)
        qs={i:row(locus) for i,locus in geo["legendes"].items()}
        full={i:[row(locus) for locus in ls] for i,ls in geo["destinations"].items()}
        assert qs==v["cibles"] and full==v["textes"]
        for where,scoring in v["analyses"].items():
            panels={i:(ls[-1:] if where=="derniere_ligne" else ls) for i,ls in full.items()}
            for name,test in scoring["regles"].items():
                expected=derive(qs,panels,"i_reduit" in name,"inverse" in name)
                observed={(h["requete"],h["destination"],h["source"][0][0],h["cible"][0],l,rr,
                           bool(h["troisieme_copie"]),h["legende_complete"])
                          for h in test["accords"] for l,rr in h["coupes"]}
                assert expected==observed
                for subset,modes in test["scores"].items():
                    order=v["ordre_requetes"][subset]
                    dest=v["ordre_destinations"]
                    for mode,score in modes.items():
                        yes={(q,d) for q,d,_,_,_,_,copied,complete in expected if q in order and
                             (mode=="deux" or mode=="trois" and copied or mode=="complet" and complete)}
                        active=tuple(tuple(j for j,d in enumerate(dest) if (q,d) in yes) for q in order)
                        assert score["effectifs_injections"]==exact(n,len(order),tuple(x for x in active if x))
                        rotations=[sum((q,dest[(dest.index(q)+s)%n]) in yes for q in order) for s in range(n)]
                        assert score["rotations"]==rotations
                        assert score["succes"]==sum(q==d for q,d in yes)
                        checked+=1
    return checked


if __name__=="__main__":
    paths=sorted(HERE.glob("f*.json.gz"))
    assert len(paths)==5
    print(sum(audit(p) for p in paths),"scores vérifiés à partir des IVTFF et des fenêtres réénumérées.")
