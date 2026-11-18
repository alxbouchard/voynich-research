"""Independently enumerate literal occurrences of every frozen pair, in both texts."""
import itertools
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = {"H":"IT2a-n.txt","ZL":"ZL3b-n.txt"}
BASE = "accord/joint/strict"
FOCUS = BASE+"/proche/exact"


def parse(path):
    tables = {}
    for line in path.read_text().splitlines():
        m = re.fullmatch(r"<(f\w+\.\d+),.P\w>\s*(.*)",line)
        if not m:
            continue
        line = re.sub(r"<[-~]>",".",m[2])
        line = re.sub(r"<[^>]*>|[!,{}]","",line)
        ws = [w for w in line.strip().split(".") if w]
        tables[m[1]] = ws,"<%>" in m[2],"<$>" in m[2]
    return tables


def segments(loci,table):
    seq, result = [],[]
    for loc in loci:
        if loc not in table or table[loc][1]:
            if seq:
                result.append(seq)
            seq=[]
        if loc in table:
            seq.append(loc)
            if table[loc][2]:
                result.append(seq)
                seq=[]
    return result+([seq] if seq else [])


def indexed(loci,table):
    words=defaultdict(list)
    count=0
    for loc in loci:
        for pos,w in enumerate(table[loc][0],1):
            words[w].append((count,loc,pos))
            count+=1
    return words


def hits(pair,table):
    a,b=pair
    observed = set()
    for (i,li,_),(j,lj,_) in itertools.product(table[a],table[b]):
        if 0<abs(i-j)<=8:
            observed.add((a,b,li,lj) if i<j else (b,a,lj,li))
    return observed


def main():
    rows=json.loads((HERE/"predictions.json").read_text())["conditions"][BASE]
    markup=json.loads((HERE/"notices/paragraphes.json").read_text())["accord"]
    text={ed:parse(HERE.parents[1]/"voynich_20261028/data"/name) for ed,name in FILES.items()}
    pot=("okol","otoldy")
    all_pairs={tuple(pair) for row in rows.values() for pair in row["paires"]}
    n_tests, matches=0,0
    for scope in ("local","notices"):
        run=json.loads((HERE/(scope+".json")).read_text())["analyses"][FOCUS]
        for key, recorded in run["blocs"].items():
            if scope=="local":
                row=rows[key]
                ids=[row["page"]+"."+str(n) for n in row["prose"]]
                parts=[p for p in segments(ids,text["H"]) if p in segments(ids,text["ZL"])]
                pairs={tuple(pair) for pair in row["paires"]}
            else:
                parts=[[w.partition(",")[0] for w in group] for group in markup]
                pairs=all_pairs.copy()
            if recorded["pot_fragment"] is not None:
                pairs.add(pot)
            read=defaultdict(set)
            for part in parts:
                h,z=[indexed(part,text[ed]) for ed in ("H","ZL")]
                for pair in pairs:
                    n_tests+=1
                    common=hits(pair,h) & hits(pair,z)
                    read[pair].update((part[0],*occ) for occ in common)
            for pair in pairs:
                rec=recorded["rencontres"].get(" ".join(pair),[])
                if pair==pot and recorded["pot_fragment"] is not None:
                    rec=recorded["pot_fragment"]
                described={(v["notice"],*v["ordre"],*v["lignes"]) for v in rec}
                assert read[pair]==described,(scope,key,pair,read[pair],described)
                matches+=len(described)
    print(f"{n_tests} recherches de paires par paragraphe vérifiées, {matches} signatures concordantes.")

if __name__=="__main__":
    main()
