"""Reporter une suite EVA observée dans le premier cahier sur une cible du second."""
from collections import Counter
from pathlib import Path
import re
import sys
from appellation import HERE, inventory, neighbor, site_id, write
import json

def position(s):
    p=s["face"]
    n=re.match(r"f(\d+)([rv])(\d*)",p)
    return int(n[1]),n[2],int(n[3] or 0),int(s["lieu"].split(".")[1]),s["positions"][0]

def main(mode):
    rows,raw,_=inventory(); rows=sorted(rows,key=position)
    if mode=="predire":
        known={}
        for s in rows:
            if not(s["cahier"]=="O" and s["locale"]):continue
            x=neighbor(s,raw,1); y=neighbor(s,raw,2)
            if x and y and x not in known:known[x]={"source":site_id(s),"successeur":y}
        calls=[]
        for s in rows:
            if s["cahier"]!="S":continue
            x=neighbor(s,raw,1)
            if x in known:calls.append(dict(id=site_id(s),locale=s["locale"],premier=x,**known[x]))
        write("COPIE-PREDICTIONS.json",dict(sources=known,appels=calls))
    else:
        plan=json.loads((HERE/"COPIE-PREDICTIONS.json").read_text()); index={site_id(s):s for s in rows}
        details=[]; counts=Counter()
        for c in plan["appels"]:
            act=neighbor(index[c["id"]],raw,2)
            details.append(dict(**c,observe=act,juste=(act==c["successeur"] if act else None)))
            counts["annonces"]+=1
            if act:counts["verifiables"]+=1;counts["justes"]+=int(act==c["successeur"])
        write("COPIE-RESULTATS.json",dict(comptes=counts,lieux=details))
if __name__=="__main__":main(sys.argv[1])
