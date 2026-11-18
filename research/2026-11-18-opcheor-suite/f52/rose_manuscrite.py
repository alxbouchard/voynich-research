"""Rejouer les tables après la lecture diplomatique de la rose dans le manuscrit de 1478."""
from itertools import combinations
from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"cle"))
from chercher import THIRD_PAGE,candidates_for,decode,index,merged,segment

units=[segment(w) for w in THIRD_PAGE]
pairs=sorted({pair for seq in units for pair in zip(seq,seq[1:])})
out={}
for name,phrase in {"edition":["flos","florum","nobis","rosa"],
                    "copie_1478":["flos","florum","rosa","nobis"]}.items():
    hits=[]
    for n in range(3):
        for rule in combinations(pairs,n):
            cipher=tuple(merged(w,rule) for w in THIRD_PAGE)
            for cap in (1,2):
                for _,_,_,k in candidates_for(cipher,cap,index({"rose":phrase[:3]})):
                    hits.append(dict(fusions=rule,cap=cap,table=k,quatrieme=decode("cheol",rule,k)))
    out[name]={"passage":phrase,"ajustements":hits,"quatriemes":sorted({r["quatrieme"] for r in hits if r["quatrieme"] is not None}),
               "justes":sum(r["quatrieme"]==phrase[3] for r in hits)}
(HERE/"ROSE-DEUX-VERSIONS.json").write_text(json.dumps(out,indent=1,ensure_ascii=False,sort_keys=True)+"\n")
