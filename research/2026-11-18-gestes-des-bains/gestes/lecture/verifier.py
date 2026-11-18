"""Tester la même lecture auprès des autres dessins et aux occurrences de prose."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

from proposer import HERE, SEEDS, STUDY, VERBS, analyze, books, ref, save
sys.path.insert(0,str(STUDY/"formule"))
from epreuve import parse
from transfert import corpus


def materials():
    eds,_=corpus()
    markers={"f77r.49","f78r.2","f80r.2","f83v.34"}
    checks={}
    prose=[]
    coverage=defaultdict(Counter)
    for loc in sorted(set.union(*(set(x) for x in eds.values()))):
        face=loc.split(".")[0]
        rs=[b.get(loc) for b in eds.values()]
        vs=[parse(r[3],cut) if r else [] for r in rs for cut in ("joints","separes")]
        if loc in markers:
            checks[loc]={"codes":[r[1] if r else None for r in rs],
                         "sources":[r[3] if r else None for r in rs],"lectures":vs,
                         "accord_integral":all(v==vs[0] for v in vs)}
        if not all(r and r[1] in {"P0","P1","Pb","Pc","Pr","Pt"} for r in rs):continue
        if int(re.match(r"f(\d+)",face)[1]) in range(76,84):continue
        for eva in SEEDS:
            places=[[j for j,w in enumerate(line) if w==eva] for line in vs]
            if not any(places):continue
            coverage[eva]["loci_au_moins_une_lecture"]+=1
            if len({len(x) for x in places})!=1:
                coverage[eva]["loci_non_concordants"]+=1;continue
            for rank in range(len(places[0])):
                item={"lieu":loc,"occurrence":rank+1,"mot":eva,"voisins":{}}
                for side in (-1,1):
                    nbrs=[seq[pos[rank]+side] if 0<=pos[rank]+side<len(seq) else None
                          for seq,pos in zip(vs,places)]
                    w=nbrs[0]
                    if w and len(set(nbrs))==1 and re.fullmatch("[a-z]+",w):
                        item["voisins"][str(side)]=w;coverage[eva]["voisins"]+=1
                prose.append(item);coverage[eva]["occurrences"]+=1
    return checks,prose,coverage


def reference(rows):
    lib=defaultdict(set)
    for loc,words in rows:
        for i,w in enumerate(words):
            for d in (-1,1):
                if 0<=i+d<len(words):lib[w,d].add(words[i+d])
    return lib


def main(cache):
    plan=json.loads((HERE/"PREDICTIONS.json").read_text())
    docs,hashes=books(cache)
    assert hashes==plan["empreintes"]
    markers,samples,n=materials()
    result={}
    for lang,rows in docs.items():
        lib=reference(rows)
        for width in (1,2):
            tag=lang+"/"+str(width); test=plan["experiences"][tag]
            learned=[]; seen=set()
            for pair in test["previsions"]:
                for third in pair["troisieme"]:
                    desc=(pair["lemme"],tuple(sorted(third["table"].items())))
                    if desc in seen:continue
                    seen.add(desc)
                    learned.append((pair["lemme"],third["table"]))
            out=[]; cnt=Counter(); by_form=Counter(); decoded=[]
            for item in samples:
                for side,neighbor in item["voisins"].items():
                    d=int(side);found=set();trials=set()
                    for j,(lemma,k) in enumerate(learned):
                        w=ref.decode(ref.units(item["mot"]),k)
                        assert w in test["formes_attestees"][lemma]
                        nb=ref.decode(ref.units(neighbor),k)
                        if nb is None:continue
                        trials.add(nb)
                        if nb in test["formes_attestees"][lemma]:continue
                        for mode,which in (("direct",d),("cotes_echanges",-d)):
                            if nb in lib[w,which]:
                                found.add(mode)
                                out.append(dict(**item,cote=d,voisin=neighbor,verbe=w,lecture=nb,cle=j+1,mode=mode))
                    if trials:cnt["cotes_entierement_decodables"]+=1
                    if trials:decoded.append(dict(lieu=item["lieu"],eva=neighbor,cote=d,lectures=sorted(trials)))
                    cnt.update(found)
            for lemma,k in learned:by_form[ref.decode(ref.units(SEEDS[2]),k)]+=1
            result[tag]=dict(cles=len(learned),formes_de_la_troisieme_figure=by_form,voisins=cnt,
                             accords=out,decodages=decoded)
    latin_mod=[(loc,["lavare" if w=="lauare" else w for w in line]) for loc,line in docs["latin"]]
    family={lemma:["lavare" if w=="lauare" else w for w in terms] for lemma,terms in VERBS["latin"].items()}
    variant=analyze(latin_mod,family,2)
    sensitivity=dict(cles=len(variant["previsions"]),
                     couples_de_flexions_distinctes=sorted({(r["premier"],r["second"]) for r in variant["previsions"] if r["premier"]!=r["second"]}),
                     vocabulaire_admissible=variant["une_seule_forme"])
    save("RESULTATS.json",dict(sensibilite_lauare_lavare=sensitivity,sources=markers,couverture=n,occurrences_de_prose=samples,tests=result))
    print(markers,n)
    for k,v in result.items():print(k,v['cles'],v["voisins"])


if __name__=="__main__":main(Path(sys.argv[1]))
