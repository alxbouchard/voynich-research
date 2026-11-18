"""Soumettre les deux mots à des noms botaniques fléchis puis vérifier leurs voisins."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/"cle"))
from chercher import LATIN, celsus, extend, segment
sys.path.insert(0,str(HERE.parents[1]))
from suites import adjacent, aligned, corpus

def forms():
    first={"bac"+extra+tail for extra in ("","c") for tail in ("a","ae","am","arum","is","as")}
    return {"baie":first, "racine":{"radix","radices",*("radic"+t for t in ("is","i","em","e","um","ibus"))},
      "feuille":{"folium","folii","folio","folia","foliorum","foliis"},
      "fleur":{"flos","flores",*("flor"+t for t in ("is","i","em","e","um","ibus"))},
      "baie_paradigme":first}


def from_latin(word,key):
    if not word:
        yield ""
        return
    for g,value in key.items():
        if word.startswith(value):
            for suffix in from_latin(word[len(value):],key):
                yield g+suffix


def predict(body):
    positions=defaultdict(Counter)
    counts=Counter()
    for words in body.values():
        counts.update(words)
        for a,b in zip(words,words[1:]):
            positions[a][b]+=1
    out={}
    for cat,variants in forms().items():
        attested=sorted(w for w in variants if counts[w])
        options=sorted(variants) if cat=="baie_paradigme" else attested
        keys=[]
        for a in options:
            for left in extend(segment("ctheor"),a,2,{}):
                for b in options:
                    if a==b:continue
                    for key in extend(segment("ctheol"),b,2,left):
                        keys.append({"formes":[a,b],"table":key})
        final_forms={k["formes"][1] for k in keys}
        totals=sum((positions[w] for w in sorted(final_forms)),Counter())
        lead=min(totals,key=lambda w:(-totals[w],w)) if totals else None
        for k in keys:
            k["suivants"]=dict(positions[k["formes"][1]])
            k["principal_encodable"]=sorted(set(from_latin(lead,k["table"]))) if lead else []
        out[cat]=dict(attestations={w:counts[w] for w in attested},tables=keys,
                      suivants=totals,principal=lead,formules_attestees={a+" "+b:positions[a][b]
                       for a in options for b in options if a!=b and positions[a][b]})
    return out

def targets():
    ed,sec=corpus()
    out={}
    for loc in ("f99r.29","f100r.25"):
        page=loc.split('.')[0]
        rows=list(aligned(ed,loc,page,sec[page],page,Counter()))
        anchors=[(i,r) for i,r in enumerate(rows) if r["mot"]=="ctheol" and r["rang_troncon_IT"]==5]
        assert len(anchors)==1
        i,anchor=anchors[0]
        n=rows[i+1] if i+1<len(rows) and adjacent(anchor,rows[i+1]) else None
        out[loc]={"mot":n["mot"] if n else None,"rangs":n["rangs_quatre"] if n else None,
                  "IT":ed["H"][loc][3],"ZL":ed["ZL"][loc][3]}
    return out

def open_words(pred):
    obs=targets()
    targets_read=[r["mot"] for r in obs.values() if r["mot"]]
    results={}
    for cat,case in pred.items():
        by_site=[set() for _ in targets_read]
        hits=[set() for _ in targets_read]
        fully=[set() for _ in targets_read]
        common=set()
        for t in case["tables"]:
            options=t["suivants"]
            key=t["table"]
            front=[([],key)]
            for i,w in enumerate(targets_read):
                s=segment(w)
                if all(g in key for g in s):
                    fully[i].add("".join(key[g] for g in s))
                possible={v for v in options if next(extend(s,v,2,key),None) is not None}
                by_site[i].update(possible)
                if w in t["principal_encodable"]:hits[i].add(w)
                front=[(chosen+[v],new) for chosen,k in front for v in possible for new in extend(s,v,2,k)]
            common.update((tuple(t["formes"]),tuple(chosen)) for chosen,k in front if targets_read)
        results[cat]={"lecture_complete_sans_ajout":[sorted(x) for x in fully],"possible_par_lieu":[sorted(x) for x in by_site],
                      "prediction_entiere_correcte":[sorted(x) for x in hits],
                      "extensions_communes":[[list(forms),list(v)] for forms,v in sorted(common)]}
    return {"lieux":obs,"ordre_des_lieux_evalues":[loc for loc,row in obs.items() if row["mot"]],"resultats":results}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=["annoncer","ouvrir"]);parser.add_argument("xml",type=Path)
    args=parser.parse_args()
    f=HERE/"ANNONCES.json"
    if args.mode=="annoncer":
        latin=json.loads(LATIN.read_bytes())
        body={**{"M/"+k:v for k,v in latin.items()},**celsus(args.xml,r"[.;:!?]")}
        out=predict(body)
    else:
        out=open_words(json.loads(f.read_bytes()));f=HERE/"OUVERTURE.json"
    f.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=1)+"\n")
