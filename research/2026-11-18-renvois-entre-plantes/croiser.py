"""D'une grande plante à la prose des panneaux, en localisant chaque groupe lisible."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
import gzip
import json
from math import factorial
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, metadata, segment

CAT = HERE / "catalogue/RENVOIS.json"


def save(path, data):
    raw=(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    path.write_bytes(gzip.compress(raw,mtime=0) if path.suffix==".gz" else raw)


def load(path):
    raw=path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix==".gz" else raw)


def leaf(page):
    return int(re.match(r"f(\d+)",page)[1])


def texts(kind):
    ed,sections=corpus()
    meta=metadata()
    panels=set(load(CAT)["panneaux"])
    eligible=panels if kind=="panneaux" else {p for p,m in meta.items() if m.get("I")=="H"}
    pages={p:[] for p in eligible}
    for loc,(page,typ,_,_) in ed["H"].items():
        if page not in pages or typ!="P0" or loc not in ed["ZL"] or ed["ZL"][loc][1]!="P0":continue
        for row in aligned(ed,loc,page,sections[page],leaf(page),Counter()):
            ranks=tuple(map(int,row["rangs_quatre"].split("/")))
            pages[page].append((row["mot"],loc,row["troncon"],ranks))
    return pages


def adjacent(a,b):
    return a[1:3]==b[1:3] and all(y==x+1 for x,y in zip(a[3],b[3]))


def loc(row):
    return [row[1],row[2],row[3][0]]


def family(word):
    u=segment(word)
    return word[:-1] if len(u)>=4 and u[-1] in ("r","l") else None


def announce():
    pages=texts("plantes")
    doc=defaultdict(set)
    fam=defaultdict(set)
    for page,rows in pages.items():
        for word,*_ in rows:
            doc[word].add(leaf(page))
            if family(word):fam[family(word)].add(leaf(page))
    out={}
    for page in sorted({r["plante"] for r in load(CAT)["liens"]}):
        rows=pages.get(page,[])
        words=Counter(w for w,*_ in rows if len(segment(w))>=4)
        first={}; nexts=defaultdict(Counter); ngrams=defaultdict(Counter); examples={}
        for i,a in enumerate(rows):
            w=a[0];first.setdefault(w,i)
            if i+1==len(rows) or not adjacent(a,rows[i+1]):continue
            b=rows[i+1];v=b[0]
            nexts[w][v]+=1
            if min(len(segment(w)),len(segment(v)))<2:continue
            pair=w+" "+v
            c=rows[i+2] if i+2<len(rows) and adjacent(b,rows[i+2]) else None
            ngrams[pair]
            if c:ngrams[pair][c[0]]+=1
            examples.setdefault(pair,[]).append(loc(a))
        other=lambda fs:len(fs-{leaf(page)})
        ranked=sorted((w for w in words if other(doc[w])),key=lambda w:(-Fraction(words[w],1+other(doc[w])),first[w]))
        basewords=sorted(words,key=lambda w:(-words[w],first[w]))
        families=Counter()
        for w,n in words.items():
            stem=family(w)
            if stem and doc.get(stem+"r") and doc.get(stem+"l") and other(fam[stem]):
                families[stem]+=n
        def first_base(s):
            return min(first.get(s+end,len(rows)) for end in ("r","l"))
        stems=sorted(families,key=lambda s:(-Fraction(families[s],1+other(fam[s])),first_base(s)))
        rforms=[]
        if stems:
            stem=stems[0];rforms=sorted([stem+"r",stem+"l"],key=lambda w:(-words[w],first.get(w,len(rows))))
        main=ranked[0] if ranked else None
        out[page]={"positions":len(rows),"mot":main,"deux_meilleurs":ranked[:2],"plus_frequent":basewords[:1],
                   "voisin":nexts[main].most_common(1)[0][0] if main and nexts[main] else None,
                   "famille":rforms,
                   "choix":{"rang_source":first[main]+1,"occurrences":words[main],"autres_feuillets":other(doc[main])} if main else {},
                   "paires":{p:{"source":sites,"suite":ngrams[p].most_common(1)[0][0] if ngrams[p] else None}
                             for p,sites in examples.items()}}
    return out


def panel(rows):
    words=defaultdict(list);pairs=defaultdict(list)
    for i,a in enumerate(rows):
        words[a[0]].append(loc(a))
        if i+1==len(rows) or not adjacent(a,rows[i+1]):continue
        b=rows[i+1];c=rows[i+2] if i+2<len(rows) and adjacent(b,rows[i+2]) else None
        pairs[a[0]+" "+b[0]].append({"lieu":loc(a),"suivant":c[0] if c else None})
    return words,pairs


def evaluate(pred,index):
    words,pairs=index; w=pred["mot"]; neighbor=pred["voisin"]
    phrase=(w+" "+neighbor) if w and neighbor else None
    matches={}
    for p in pred["paires"].keys() & pairs.keys():
        matches[p]={"annonce":pred["paires"][p],"panneau":pairs[p]}
    thirds=[(v["annonce"]["suite"],r["suivant"]) for v in matches.values() for r in v["panneau"]
            if v["annonce"]["suite"] and r["suivant"]]
    kinds={"mot":[w] if w else [],"deux_meilleurs":pred["deux_meilleurs"],"frequent":pred["plus_frequent"],
           "famille":pred["famille"],"forme_exacte_famille":pred["famille"][:1]}
    events={k:{g:words[g] for g in guesses if g in words} for k,guesses in kinds.items()}
    score={k:int(bool(v)) for k,v in events.items()}
    score.update(paire_annoncee=int(phrase in pairs),paires_partagees=len(matches),occurrences_tiers_lisibles=len(thirds),
                 tiers_exacts=sum(a==b for a,b in thirds))
    return {"scores":score,"mots":events,"paire_annoncee":pairs.get(phrase,[]),"formules":matches}


@lru_cache(maxsize=None)
def distribution(matrix):
    n=len(matrix)
    @lru_cache(maxsize=None)
    def fill(mask):
        i=mask.bit_count()
        if i==n:return {0:1}
        values=Counter()
        for j in range(n):
            if mask>>j&1:continue
            for tail,count in fill(mask|1<<j).items():
                values[matrix[i][j]+tail]+=count
        return values
    hist=fill(0);assert sum(hist.values())==factorial(n)
    return hist


def shuffled(links, group, details):
    metrics=next(iter(next(iter(details.values())).values()))["scores"]
    stats={}
    for metric in metrics:
        total=0;dist=Counter({0:1})
        for pool in group.values():
            bypage={p:[r["plante"] for r in links if r["panneau"]==p] for p in pool}
            matrix=tuple(tuple(sum(details[src][cand]["scores"][metric] for src in bypage[orig]) for cand in pool) for orig in pool)
            total+=sum(row[i] for i,row in enumerate(matrix))
            hist=distribution(matrix)
            acc=Counter()
            for a,p in dist.items():
                for b,q in hist.items():acc[a+b]+=p*q
            dist=acc
        n=sum(dist.values())
        stats[metric]={"observe":total,"moyenne_perm":float(Fraction(sum(k*v for k,v in dist.items()),n)),
                       "aussi_haut":sum(v for k,v in dist.items() if k>=total),"permutations":n}
    return stats


def opening(pred):
    cat=load(CAT);pages=texts("panneaux");links=cat["liens"]
    out={"positions":{p:len(rows) for p,rows in pages.items()},"lots":{}}
    for label in ("principal","catalogue_direct","avec_petersen","origine_baies"):
        leaf_ok=lambda p:(leaf(p) not in {99,100} if label=="principal" else True)
        group=defaultdict(list)
        for p,item in sorted(cat["panneaux"].items()):
            if leaf_ok(p):group[item["cahier"]].append(p)
        retained=[r for r in links if leaf_ok(r["panneau"]) and (label!="principal" or leaf(r["plante"]) not in {17,96})
                  and (label=="avec_petersen" or r["classe"]!="petersen")
                  and (label!="origine_baies" or r["fragment"] in {94,116})]
        schema=set();distinct=[]
        for r in retained:
            pair=(r["panneau"],r["plante"])
            if pair not in schema:distinct.append(r);schema.add(pair)
        out["lots"][label]={}
        for length in ("tous","egaux"):
            limits={p:min(len(pages[x]) for x in pool) if length=="egaux" else len(pages[p]) for pool in group.values() for p in pool}
            indices={p:panel(pages[p][:n]) for p,n in limits.items()}
            details={p:{dst:evaluate(pred[p],idx) for dst,idx in indices.items()} for p in {r["plante"] for r in retained}}
            cases=[{"fragment":r["fragment"],"plante":r["plante"],"panneau":r["panneau"],"classe":r["classe"],
                    "choix":{k:v for k,v in pred[r["plante"]].items() if k!="paires"},
                    **details[r["plante"]][r["panneau"]]} for r in retained]
            summary=shuffled(retained,group,details)
            dedup=summary if len(distinct)==len(retained) else shuffled(distinct,group,details)
            out["lots"][label][length]={"limites":limits,"cas":cases,"couples_distincts":len(distinct),
                                        "bilan":summary,"bilan_couples_distincts":dedup}
    return out


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("annoncer","ouvrir"))
    mode=parser.parse_args().mode
    path=HERE/"ANNONCES.json.gz"
    if mode=="annoncer":save(path,announce())
    else:
        pred=load(path)
        assert pred==announce()
        save(HERE/"OUVERTURE.json.gz",opening(pred))
