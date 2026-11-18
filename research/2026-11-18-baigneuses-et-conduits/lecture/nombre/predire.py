"""Déposer les six clés et les voisins attendus avant d'ouvrir les loci du Voynich."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import confronter as ref

FORMS = ("aqua","aquas")
EXCLUDED = {("adibis","aquas"),("aquas","alias"),("aquas","aqua")}
TARGET = {"otol":"aqua","otoly":"aquas"}


def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=1)+"\n")


def line_words(folder):
    path = folder/"vers.json"
    assert sha256(path.read_bytes()).hexdigest()==ref.read(HERE.parent/"SOURCE.json")["sha256"]
    return [[ref.words(v) for v in ch["vers"]] for ch in ref.read(path)]


def entries(chapters):
    out=[]
    for i,chapter in enumerate(chapters):
        for j,line in enumerate(chapter,1):
            for k,form in enumerate(line):
                if form not in FORMS: continue
                for d in (-1,1):
                    if not 0<=k+d<len(line): continue
                    w=line[k+d]
                    pair=(w,form) if d==-1 else (form,w)
                    out.append(dict(notice=i,vers=j,rang_cible=k+1,forme=form,cote=d,
                                    voisin=w,annonce=pair not in EXCLUDED))
    return out


def expected():
    keys=[]
    for record in ref.read(HERE.parent/"PREDICTIONS.json.gz"):
        if record["mode"]!="o" or record["largeur"]!=2:continue
        for t in record["lectures"]:
            if tuple(t["expression"]) not in EXCLUDED or not t["sens"]: continue
            key=t["cle"]
            if all(ref.decode(ref.transformed(w,"o"),key)==v for w,v in TARGET.items()):
                keys.append(dict(expression=t["expression"],ordre=record["ordre"],table=key))
    assert len(keys)==6
    return keys


if __name__=="__main__":
    neighbors=entries(line_words(Path(sys.argv[1])))
    write("ATTENTES.json",dict(cles=expected(),formes=TARGET,
          exclusions=sorted(EXCLUDED),voisins=neighbors))
    for f in FORMS:
        for d in (-1,1):
            print(f,d,[v['voisin'] for v in neighbors if v['forme']==f and v['cote']==d and v['annonce']])
