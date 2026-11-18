"""Comparer les clés par mots de Celse sur tout autre feuillet."""
from collections import Counter,defaultdict
from itertools import permutations
from pathlib import Path
import sys

from dictionnaire import HERE,EVA,load,read_books,save
from croiser import adjacent,leaf,metadata,texts
EXCLUDED={3,14,18,22,23,89,102,104}


def occurrences(body):
    counts=Counter()
    for ws in body.values():
        for n in (1,2,3,4):
            counts.update(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))
    return counts


def collect(pages):
    meta=metadata()
    result=defaultdict(Counter)
    places=defaultdict(list)
    for p,rows in sorted(pages.items()):
        if not p[1:2].isdigit() or leaf(p) in EXCLUDED:continue
        section=meta[p].get("I","?")
        for i,a in enumerate(rows):
            result[section][a[0]]+=1
            for size in (2,3):
                sub=rows[i:i+size]
                if len(sub)==size and all(adjacent(x,y) for x,y in zip(sub,sub[1:])):
                    places[tuple(x[0] for x in sub)].append([p,a[1],a[3][0]])
    return places,result


def counts_for(mapping,ng,n,hist):
    words=mapping.keys()
    results=[]
    rows=[(g,sites) for g,sites in ng.items() if len(g)==n and all(w in words for w in g)]
    for g,sites in rows:
        plain=tuple(mapping[w] for w in g)
        results.append({"eva":g,"latin":plain,"sites":sites,"dans_celse":hist[plain]})
    return results


def score(mapping,ng,hist):
    result={}
    for size in (2,3):
        cases=counts_for(mapping,ng,size,hist)
        forms={tuple(c["eva"]):len(c["sites"]) for c in cases}
        def stat(key):
            unique=sum(tuple(key[w] for w in g) in hist for g in forms)
            sites=sum(n for g,n in forms.items() if tuple(key[w] for w in g) in hist)
            return unique,sites
        true=stat(mapping)
        alt=Counter(stat(dict(zip(mapping,perm))) for perm in permutations(mapping.values()))
        result[size]={"formes":len(forms),"lieux":sum(forms.values()),"formes_attestees":true[0],"lieux_attestes":true[1],
                      "permutations":sum(alt.values()),"formes_aussi_bonnes":sum(n for (s,t),n in alt.items() if s>=true[0]),
                      "lieux_aussi_bons":sum(n for (s,t),n in alt.items() if t>=true[1]),
                      "distribution":[[s,t,n] for (s,t),n in sorted(alt.items())],"detail":cases}
    return result


def extend_choice(source_body,x,y,z):
    alternatives=[]
    for place,ws in source_body.items():
        for i in range(len(ws)-3):
            if ws[i:i+3]==[x,y,z]:
                alternatives.append((ws[i+3],place,i+1))
    counts=Counter(r[0] for r in alternatives)
    top=[w for w,n in counts.items() if n==max(counts.values())]
    return (top[0] if len(top)==1 else None), dict(counts),alternatives


def run(paths):
    books=read_books(*paths)
    latin=books["Celse"];hist=occurrences(latin)
    candidates=load(HERE/"OUVERTURE-sept.json.gz")["Celse"]["interne"]["paires_retenues"]
    meanings={tuple(r["mots"]) for r in candidates}
    assert len(meanings)==5
    guess,ct,examples=extend_choice(latin,"est","id","quod")
    maps={" / ".join(s):dict(zip(EVA,s)) for s in sorted(meanings)}
    seed=dict(zip(EVA,("et","linum","est","id")))
    assert guess and guess not in {*seed.values(),"quod"}
    for spelling in ("dala","dalo"):
        maps[spelling]={**seed,spelling:"quod","qotolo":guess}
    ng,sections=collect(texts("tout",True))
    vocabulary=sorted(set().union(*(m.keys() for m in maps.values())))
    all_counts=sum(sections.values(),Counter())
    full={w:all_counts[w] for w in vocabulary}
    historic={}
    for name,b in books.items():
        if name.lower() not in {"celse","macer"}:continue
        counter=Counter(w for ws in b.values() for w in ws)
        historic[name]={w:counter[w] for w in sorted({v for m in maps.values() for v in m.values()})}
        historic[name]["total"]=sum(counter.values())
    return {"mot_apres_est_id_quod":{"choisi":guess,"compte":ct,"passages":examples},
            "voynich":{"toutes_sections":full,"total":sum(all_counts.values()),
                       "sections":{s:{**{w:c[w] for w in vocabulary},"total":sum(c.values())} for s,c in sections.items()}},
            "latin":historic,"tables":{name:{"table":m,"n_grammes":score(m,ng,hist)} for name,m in maps.items()}}


if __name__=="__main__":
    save(HERE/"SUITE.json.gz",run(list(map(Path,sys.argv[1:]))))
