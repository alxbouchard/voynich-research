"""Sensibilité : le premier mot du verso est-il annoncé par le recto ?"""
from collections import Counter
import json
import sys
from transitions import HERE, LOTS, FIELDS, metadata, views, distribution, write


def within(meta,lot):
    pairs = []
    for face,a in meta.items():
        if face[-1]!="r" or a["Q"] not in lot or a.get("I")!="H":
            continue
        other = face[:-1]+"v"
        b = meta.get(other,{})
        if a["I"]==b.get("I") and all(a.get(k) and a[k]==b.get(k) for k in ("H","L")):
            pairs.append((face,other))
    return pairs


def predict(meta):
    features = views({f for f in meta if f.endswith("r")})
    return {name:[{"source":a,"destination":b,"cahier":meta[a]["Q"],
                  "gauche":features[a]} for a,b in within(meta,qs)] for name,qs in LOTS.items()}


def main():
    meta = metadata()
    if sys.argv[1]=="predire":
        write("PREDICTIONS-RV.json",predict(meta))
        return
    expected = json.loads((HERE/"PREDICTIONS-RV.json").read_text())
    assert expected == predict(meta)
    readings=views(meta)
    values={f:{k:v["signe"] for k,v in fields.items()} for f,fields in readings.items()}
    result={}
    for name,qs in LOTS.items():
        pairs=within(meta,qs)
        checks=[{"source":a,"destination":b,"droite":readings[b]} for a,b in pairs]
        observed={f:distribution(meta,qs,values,f,pair_rule=within,fixed_left=True) for f in FIELDS}
        joint=tuple(FIELDS)[:3]
        comparison={f:distribution(meta,qs,values,f,joint,within,True) for f in joint}
        freq=Counter(values[b]["debut"] for a,b in pairs if values[b]["debut"] and values[a]["debut"])
        result[name]=dict(tous_les_couples=len(pairs),appels=sum(bool(values[a]["debut"]) for a,b in pairs),
                          frequences_droite=freq,mesures=observed,joint=comparison,cibles=checks)
    write("RECTO-VERSO.json",result)


if __name__=="__main__":
    main()
