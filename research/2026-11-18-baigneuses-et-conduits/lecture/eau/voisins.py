"""Vérifie les deux voisins annoncés et cherche d'autres occurrences matérielles de la paire."""
from itertools import permutations
from collections import defaultdict
import re
from prose import HERE, co, corpus
from essai import tables

PAIR=("shedy","sheol")


def compare(word,target,key):
    if word is None or not re.fullmatch("[a-z]+",word):
        return None
    signs=co.transformed(word,"o")
    return dict(eva=word,lu=co.decode(signs,key),
                possible=next(tables(signs,target,2,key),None) is not None)


def instances():
    editions,_=corpus()
    views=defaultdict(dict)
    for ed,lines in editions.items():
        for cut in ("joints","separes"):
            for loc,(_,kind,_,raw) in lines.items():
                # Keep uncertain neighboring groups in order, without crossing interruptions.
                for piece in re.split(r"<[-~]>",raw):
                    seq=co.tokens(re.sub(r"\{[^}]*\}", "?",piece),cut)
                    for i in range(len(seq)-1):
                        if seq[i:i+2]==PAIR:
                            sides=[seq[i-1] if i else None,seq[i+2] if i+2<len(seq) else None]
                            views[loc].setdefault(ed+"-"+cut,[]).append(sides)
    return views


def main(folder):
    guesses=co.read(HERE/"TABLES.json.gz")
    results=co.read(HERE/"PROSE.json.gz")["resultats"]
    success=[v["id"] for v in results if v["succes"]]
    phrases=co.repertories(folder)["bains"]
    occurrences=instances()
    hypotheses=[]
    for idx in success:
        key=guesses[idx]["cle"]
        sides={}
        for loc,views in sorted(occurrences.items()):
            sides[loc]={}
            for ed,readings in views.items():
                outcomes=[]
                for left,right in readings:
                    if loc=="f76r.36" and left and "?" in left:
                        assert left=="qok?l"
                        lefts=["qokal","qokol"]
                    else:
                        lefts=[left]
                    outcomes.append(dict(refrenat=[compare(a,"refrenat",key) for a in lefts],
                       turgida=compare(right,"turgida",key),frigida=compare(right,"frigida",key)))
                sides[loc][ed]=outcomes
        mixed=[]
        for values in permutations(key[s] for s in ("sh","e","d")):
            new=key|dict(zip(("sh","e","d"),values))
            q=tuple(co.decode(co.transformed(w,"o"),new) for w in PAIR)
            mixed.append(dict(nouvelles=values,paire=q,attestee=q in phrases))
        hypotheses.append(dict(id=idx,voisins=sides,temoins=mixed))
    return dict(occurrences=occurrences,accord_quatre=[loc for loc,v in sorted(occurrences.items()) if len(v)==4],
                tables=hypotheses)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    co.save("eau/VOISINS.json",main(Path(sys.argv[1])))
