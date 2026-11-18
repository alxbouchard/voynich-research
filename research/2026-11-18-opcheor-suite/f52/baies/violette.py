"""Vérifier le prolongement de la seule paire latine compatible dans les deux lignes."""
from lire_baies import HERE,LATIN,corpus,aligned,adjacent,Counter,segment,extend
import json

forms=json.loads((HERE/"ANNONCES.json").read_bytes())["feuille"]["tables"]
ed,sections=corpus()
loc="f99r.29"; page="f99r"
rows=list(aligned(ed,loc,page,sections[page],page,Counter()))
i=next(i for i,r in enumerate(rows) if r["mot"]=="ctheol")
a,b,c=rows[i:i+3]; assert adjacent(a,b) and adjacent(b,c)
keys=[k for t in forms if t["formes"][1]=="foliis" for k in extend(segment(b["mot"]),"violae",2,t["table"])]
occ=[]
for name,words in json.loads(LATIN.read_bytes()).items():
    for j in range(len(words)-1):
        if words[j:j+2]==["foliis","violae"]:
            occ.append([name,j+1,words[j:j+4]])
detail=[{"table":k, "sortie":"".join(k[g] if g in k else "["+g+"]" for g in segment(c["mot"])),
         "extensions_pour_cum":list(extend(segment(c["mot"]),"cum",2,k))} for k in keys]
(HERE/"VIOLETTE.json").write_text(json.dumps(dict(lieu=loc,signes=[r["mot"] for r in (a,b,c)],macer=occ,tables=detail),ensure_ascii=False,indent=1,sort_keys=True)+"\n")
