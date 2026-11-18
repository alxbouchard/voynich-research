"""Comparer la ligne de chaque ctheol aux lignes pharmaceutiques de même longueur."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/"2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned,corpus,parse,segment

ed,sections=corpus()
types=defaultdict(set)
for loc,(face,typ,*_) in ed["H"].items():
    if loc in ed["ZL"] and ed["ZL"][loc][1]==typ:
        types[face].add(typ)
sheets={p for p,types_here in types.items() if {"P0","Lf"}<=types_here}
rows={}
for loc,(face,typ,_,raw) in ed["H"].items():
    if face not in sheets or typ!="P0" or loc not in ed["ZL"] or ed["ZL"][loc][1]!=typ:
        continue
    leaf=int(re.match(r"f(\d+)",face)[1])
    _,parts=parse(raw,"joints")
    size=sum(map(len,parts))
    if not size:continue
    words=[row["mot"] for row in aligned(ed,loc,face,sections[face],leaf,Counter())]
    others=sum(w!="ctheol" and segment(w)[-3:]==("e","o","l") for w in words)
    rows[loc]=dict(page=face,feuillet=leaf,taille=size,lisibles=len(words),ctheol=words.count("ctheol"),
                   ctheor=words.count("ctheor"),autres_eol=others,incertains=size-len(words))
result={}
for loc,row in rows.items():
    if not row["ctheol"] or row["feuillet"] in {99,100} and loc not in ("f99r.29","f100r.25"):
        continue
    base=[r for r in rows.values() if r["feuillet"] not in {99,100} and not(r["ctheol"] or r["ctheor"])]
    stats={}
    for name,eligible in (("toutes",base),("meme_taille",[r for r in base if r["taille"]==row["taille"]])):
        stats[name]=dict(total=len(eligible),certain_au_moins_deux=sum(r["autres_eol"]>=2 for r in eligible),
                         possible_au_moins_deux=sum(r["autres_eol"]+r["incertains"]>=2 for r in eligible))
    result[loc]=dict(ligne=row,temoins=stats)
(HERE/"FINALES.json").write_text(json.dumps(result,indent=1,sort_keys=True)+"\n")
