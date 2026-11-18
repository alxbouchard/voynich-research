"""Les voisins de baccis dans deux versions du même vers sur le poivre."""
from lire_baies import HERE,corpus,aligned,adjacent,Counter,segment,extend
import json

tables=json.loads((HERE/"ANNONCES.json").read_bytes())["baie"]["tables"]
tables=[r["table"] for r in tables if r["formes"][1]=="baccis"]
ed,sections=corpus()
out={}
for loc in ["f99r.29","f100r.25","f88r.7"]:
    page=loc.split('.')[0]
    rows=list(aligned(ed,loc,page,sections[page],page,Counter()))
    i=next(i for i,r in enumerate(rows) if r["mot"]=="ctheol")
    left=rows[i-1]["mot"] if i and adjacent(rows[i-1],rows[i]) else None
    right=rows[i+1]["mot"] if i+1<len(rows) and adjacent(rows[i],rows[i+1]) else None
    detail={}
    for a,b in [("cum","lauri"),("lauri","vel")]:
        ld=[v for k in tables for v in extend(segment(left),a,2,k)] if left else []
        rd=[v for k in tables for v in extend(segment(right),b,2,k)] if right else []
        both=[v for k in ld for v in extend(segment(right),b,2,k)] if left and right else []
        detail[a+" baccis "+b]=dict(gauche=len(ld) if left else None,droite=len(rd) if right else None,
                                   tables_communes=both if left and right else None)
    out[loc]=dict(gauche=left,droite=right,tables_depart=len(tables),lectures=detail,
                  IT=ed["H"][loc][3],ZL=ed["ZL"][loc][3])
(HERE/"COPIE.json").write_text(json.dumps(out,indent=1,ensure_ascii=False,sort_keys=True)+"\n")
