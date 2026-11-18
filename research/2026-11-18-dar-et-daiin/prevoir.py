"""Prédire un voisin sur un feuillet qui n’a pas servi à choisir la règle."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import comb
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-renvois-entre-plantes"))
from croiser import adjacent, corpus, leaf, load, metadata, save, segment, texts
from corpus_dam import parse

ORIGINAL = {14, 18, 23, 102}
SEEN = {3, 22, 89, 104}
SHORT, LONG = "qokol", "qokchol"
BLUE, RED = "daiin", "dar"


def eligible_page(page):
    return page[1:2].isdigit() and leaf(page) not in ORIGINAL


def group(scope, term):
    return term in (SHORT, LONG) if scope == "initial" else term not in (SHORT, LONG)


def words(rows):
    return {r[0] for page, items in rows.items() if eligible_page(page) for r in items}


def families(vocab):
    pairs = []
    for term in sorted(vocab):
        units = segment(term)
        if len(units) < 4 or units[-2:] != ("o", "l"):
            continue
        other_units = units[:-2] + ("ch", "o", "l")
        other = "".join(other_units)
        if other in vocab and segment(other) == other_units:
            pairs.append((term, other))
    used = Counter(w for pair in pairs for w in pair)
    return [(a, b) for a,b in pairs if used[a] == used[b] == 1 and not {a,b} & {SHORT, LONG}]


def announced(pages):
    # Les familles du lot principal sont choisies sans aucun mot des feuillets déjà dépouillés.
    clean = {p: rows for p,rows in pages.items() if eligible_page(p) and leaf(p) not in SEEN}
    pairs = [(SHORT, LONG), *families(words(clean))]
    mapping = {w: (a, b, BLUE if w == a else RED) for a,b in pairs for w in (a,b)}
    predictions = {}
    for p, rows in sorted(pages.items()):
        if not eligible_page(p):
            continue
        for r in rows:
            w,l,_,ranks = r
            if w in mapping:
                a,b,expected = mapping[w]
                predictions[f"{l}/{ranks[0]}"] = dict(page=p, rangs=ranks, ancre=w, formes=[a,b], annonce=expected)
    return {"familles": pairs, "lieux": predictions}


def opened(pages):
    editions, _ = corpus()
    data = []
    for p, rows in sorted(pages.items()):
        if not eligible_page(p):
            continue
        for i,r in enumerate(rows):
            term,l,_,ranks = r
            units=segment(term)
            if len(units)<4 or units[-2:] != ("o","l"):
                continue
            nxt = rows[i+1] if i+1 < len(rows) and adjacent(r,rows[i+1]) else None
            if not nxt:
                continue
            _,parts = parse(editions["H"][l][3],"joints")
            edge = "fin" if nxt[3][0]==sum(map(len,parts)) else "interieur"
            data.append((f"{l}/{ranks[0]}", p, term, nxt[0], edge))
    return data


def combinations(n,k):
    return comb(n,k) if 0<=k<=n else 0


@lru_cache(maxsize=None)
def dist(red, blue, other, nred, nblue):
    # Placer sans remise les couleurs dans les deux ensembles de positions prédites.
    n = red+blue+other
    hist=Counter()
    for r in range(min(red,nred)+1):
        for b in range(min(blue,nred-r)+1):
            first = combinations(red,r)*combinations(blue,b)*combinations(other,nred-r-b)
            if not first:continue
            for hits in range(min(blue-b,nblue)+1):
                second = combinations(blue-b,hits)*combinations(n-nred-(blue-b),nblue-hits)
                if second:hist[r+hits] += first*second
    assert sum(hist.values()) == comb(n,nred)*comb(n-nred,nblue)
    return hist


def combine(x,y):
    hist=Counter()
    for a,p in x.items():
        for b,q in y.items():hist[a+b]+=p*q
    return hist


def run_model(pred,data,domains,scope):
    choices = {k:v for k,v in pred["lieux"].items() if v["page"] in domains and group(scope,v["ancre"])}
    records = {}
    strata=defaultdict(list)
    for k,p,a,b,edge in data:
        if p in domains:
            strata[p,edge].append((k,a,b))
            if k in choices:
                records[k]=dict(**choices[k],suivant=b,position=edge)
    total_hist=Counter({0:1})
    controls=Counter()
    for pool in strata.values():
        guesses = Counter(choices[k]["annonce"] for k,_,_ in pool if k in choices)
        if not guesses:continue
        neighbors = Counter(b for _,_,b in pool)
        for k,_,b in pool:
            if k not in choices:controls[b]+=1
        total_hist=combine(total_hist,dist(neighbors[RED],neighbors[BLUE],len(pool)-neighbors[RED]-neighbors[BLUE],
                                           guesses[RED],guesses[BLUE]))
    denominator=sum(total_hist.values())
    hits=sum(r["annonce"]==r["suivant"] for r in records.values())
    expected=Fraction(sum(h*n for h,n in total_hist.items()),denominator)
    def summary(subset):
        return dict(evaluables=len(subset),dar=sum(r["suivant"]==RED for r in subset),
                    daiin=sum(r["suivant"]==BLUE for r in subset),
                    exact=sum(r["annonce"]==r["suivant"] for r in subset))
    stems={s:summary([r for r in records.values() if r["formes"][0]==s]) for s in sorted({v["formes"][0] for v in choices.values()})}
    return dict(annonces=len(choices),lu=summary(list(records.values())),formes={a:summary([r for r in records.values() if r["annonce"]==a]) for a in (BLUE,RED)},
                familles=stems,regle_inverse=sum(r["suivant"] in (RED,BLUE) and r["suivant"]!=r["annonce"] for r in records.values()),
                esperance_exacte=str(expected),probabilite_au_moins_observe=float(Fraction(sum(v for k,v in total_hist.items() if k>=hits),denominator)),
                temoins=dict(total=sum(controls.values()),dar=controls[RED],daiin=controls[BLUE]),
                distribution={k:float(Fraction(v,denominator)) for k,v in sorted(total_hist.items())},lieux=records)


def verify(pred,pages):
    assert dist(1,1,0,1,1)=={0:1,2:1}
    data=opened(pages)
    meta=metadata()
    out={}
    for domain, test in [("autres",lambda p:leaf(p) not in SEEN),("deja_consultes",lambda p:leaf(p) in SEEN),
                         ("autres_botanique",lambda p:leaf(p) not in SEEN and meta[p].get("I")=="H")]:
        allowed={p for p in pages if eligible_page(p) and test(p)}
        out[domain]={s:run_model(pred,data,allowed,s) for s in ("initial","extension")}
    return out


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("annoncer","ouvrir"))
    action=parser.parse_args().action
    pages=texts("tout",True)
    path=HERE/"PREDICTIONS.json.gz"
    if action=="annoncer":save(path,announced(pages))
    else:
        pred=load(path);save(HERE/"VOISINS.json.gz",verify(pred,pages))
