"""Dépose les clés complétées à f77v puis vérifie leurs lectures en prose hors des deux bifeuillets."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import confronter as co
sys.path.insert(0,str(co.RESEARCH/"2026-11-18-opcheor-paralleles/variantes"))
from compter import runs


def prepare(library):
    seeds=[]
    for e in co.read(co.HERE/"PREDICTIONS.json.gz"):
        for r in e["lectures"]:
            pair=tuple(r["expression"])
            if (pair,e["ordre"]) in [(("adibis","aquas"),"haut-bas"),(("aquas","alias"),"bas-haut")]:
                seeds.append((pair,e["ordre"],r["cle"]))
    proof=("abibis","aquas")
    for key in co.assignments(tuple(co.transformed(w,"o") for w in co.SEED), proof,2):
        seeds.append((proof,"haut-bas",key))
    output=[]
    vocab={word for pair in library for word in pair}
    for reading,direction,key in seeds:
        for orientation in (["direct","inverse"] if direction=="bas-haut" else ["direct"]):
            second=("otol","shedy") if orientation=="direct" else ("shedy","otol")
            seg=tuple(co.transformed(w,"o") for w in second)
            for expr in library:
                for ext in co.assignments(seg,expr,2,key):
                    covered={word for word in vocab if co.encodable(word,ext)}
                    output.append(dict(source=reading,empilement=direction,horizontal=orientation,
                        ancien=key,expression=expr,cle=ext,
                        possibles=sorted(" ".join(p) for p in library if set(p)<=covered)))
    return output


def concordance(sizes):
    editions,_=co.corpus() if hasattr(co,"corpus") else get_corpus()
    four=[]
    allowed={f"f{i}{side}" for i in (76,78,79,80,81,83) for side in ("r","v")}
    for rows in editions.values():
        for cut in ("joints","separes"):
            data={}
            for loc,(page,kind,pos,raw) in rows.items():
                if page not in allowed or kind!="P0":continue
                stream=list(runs(re.sub(r"\{[^}]*\}", "?",raw),cut))
                data[loc]={n:Counter(tuple(w for j,w in chunk[i:i+n]) for chunk in stream
                    for i in range(len(chunk)-n+1)) for n in sizes}
            four.append(data)
    shared={n:{} for n in sizes}
    groups=sorted(set.intersection(*(set(view) for view in four)))
    for locus in groups:
        for n in sizes:
            counted=four[0][locus][n].copy()
            for view in four[1:]:counted &= view[locus][n]
            for phrase,qty in counted.items():
                shared[n].setdefault(phrase,{})[locus]=qty
    return shared, len(groups)


def get_corpus():
    from transfert import corpus
    return corpus()


def evaluate(key, pairs, triplets, targets, three):
    unique={w for p in pairs for w in p}
    names={w:co.decode(co.transformed(w,"o"),key) for w in unique}
    fixed={p:tuple(names[w] for w in p) for p in pairs if all(names[w] is not None for w in p)}
    hits=[]; inverse=0; known=0
    vocab={word for pair in targets for word in pair}
    for p,q in fixed.items():
        qty=sum(pairs[p].values())
        known += qty*int(all(w in vocab for w in q))
        inverse += qty*int(q[::-1] in targets)
        if q in targets:
            hits.append(dict(eva=p,lecture=q,lieux=pairs[p]))
    good={tuple(row["eva"]) for row in hits}
    continuations=[]
    for t, locs in triplets.items():
        if t[:2] not in good and t[1:] not in good:continue
        vals=tuple(names.get(w) for w in t)
        continuations.append(dict(eva=t,lecture=vals,passe=vals in three,lieux=locs))
    return dict(paires_distinctes=len(fixed),occurrences=sum(sum(pairs[p].values()) for p in fixed),
                paires_de_mots_connus=known,occurrences_inversees=inverse,succes=hits,suites=continuations)


def check(folder,records):
    targets=co.repertories(folder)["bains"]
    three={tuple(ws[i:i+3]) for ch in co.read(folder/"vers.json") for line in ch["vers"]
           for ws in [co.words(line)] for i in range(len(ws)-2)}
    shared,n=concordance([2,3])
    results=[]; controls=[]; seen=set()
    for i,r in enumerate(records):
        key=r["cle"]
        test=evaluate(key, shared[2],shared[3],targets,three)
        assert all(" ".join(h["lecture"]) in r["possibles"] for h in test["succes"])
        results.append(dict(id=i,**test))
        orientation=r["empilement"],r["horizontal"]
        if "fervens" not in r["expression"] or orientation in seen:continue
        seen.add(orientation)
        signs=("sh","e","d")
        for vals in sorted(set(permutations(key[s] for s in signs))):
            scrambled=key|dict(zip(signs,vals))
            c=evaluate(scrambled,shared[2],shared[3],targets,three)
            controls.append(dict(id=i,nouveau=dict(zip(signs,vals)),distinctes=c["paires_distinctes"],
                        occurrences=c["occurrences"],succes=c["succes"]))
    return dict(lignes=n,paires_distinctes=len(shared[2]),paires_total=sum(sum(v.values()) for v in shared[2].values()),
                resultats=results,permutations=controls)


if __name__=="__main__":
    mode,folder=sys.argv[1],Path(sys.argv[2])
    if mode=="predire":
        co.save("eau/TABLES.json.gz",prepare(co.repertories(folder)["bains"]))
    elif mode=="verifier":
        co.save("eau/PROSE.json.gz",check(folder,co.read(HERE/"TABLES.json.gz")))
    else:
        raise ValueError("predire ou verifier")
