"""Recherche des couples et triplets par backreferences, indépendante de l'énumération des clés."""
import gzip
import json
import re
from comparer import HERE, permit, titles, units

def compile_words(words,width):
    parts=[]
    seen=set()
    for i,word in enumerate(words):
        if i: parts.append(" ")
        for s in units(word):
            if s in seen:
                parts.append(f"(?P={s})")
            else:
                seen.add(s)
                parts.append(f"(?P<{s}>[a-z]{{1,{width}}})")
    return re.compile("".join(parts))

def compatible(pattern,target,width):
    match=pattern.fullmatch(target)
    if not match:
        return False
    return width!=1 or len(set(match.groups()))==len(match.groups())

def audit(catalog,pred,verification):
    checks=0
    for p,v in zip(pred,verification,strict=True):
        if not all(p["given"]):
            continue
        for width in (1,2,3):
            seen=set()
            third_hits=set()
            double=compile_words(p["given"],width)
            triple=compile_words(p["given"]+[v["third"]],width) if v["third"] else None
            for book,entries in catalog.items():
                for i in entries:
                    if i+1 not in entries or i+2 not in entries: continue
                    a,b,c=[entries[j][1] for j in (i,i+1,i+2)]
                    if not permit(a) or not permit(b): continue
                    if compatible(double,a+" "+b,width):
                        seen.add((book,i))
                        if triple and permit(c) and compatible(triple," ".join((a,b,c)),width):
                            third_hits.add((book,i))
            wanted={(r["book"],r["index"]) for r in p["models"][str(width)]}
            actual={(r["book"],r["index"]) for r in v["models"][str(width)]["detail"] if r["possible"]}
            assert (seen,third_hits)==(wanted,actual),(p["page"],p["rank"],width)
            checks+=1
    return checks

if __name__=="__main__":
    load=lambda name:json.loads(gzip.decompress((HERE/name).read_bytes()))
    n=audit(titles(),load("PREDICTIONS.json.gz"),load("VERIFICATION.json.gz"))
    print(f"{n} comparaisons des couples et des triplets concordent.")
