"""Forecast the last EVA unit of the short words on f66r from pairs of signs."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import math
import random
import re

HERE = Path(__file__).resolve().parent
UNIT = re.compile(r"@[0-9]{3};|ckh|cth|cph|cfh|ch|sh|[a-z]")
EDITIONS = ("accord", "ZL", "IT")
ALL_OMISSIONS = list(combinations(range(1,18),2))
RESERVE = range(11,16)


def write(name, obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")


def read(name):
    return json.loads((HERE/name).read_text())


def ingest(folder, allowed):
    result = {}
    for ed in ("ZL","IT"):
        rows = {}
        for line in (folder/(ed+".txt")).read_text().splitlines():
            header,_,text = line.partition(">")
            m = re.fullmatch(r"<f66r\.(\d+),.[A-Z][a-zA-Z0-9]",header)
            if not m or int(m[1]) not in allowed:
                continue
            idx = int(m[1])
            field = re.sub(r"<![^>]*>|<[%$\-~]>|!", "", text).strip()
            units = UNIT.findall(field)
            valid = bool(units and "".join(units)==field and (idx<16 or len(units)==1))
            rows[str(idx)] = {"champ":field,"unites":units if valid else None}
        assert set(map(int,rows))==set(allowed)
        result[ed] = rows
    return result


def edge(rows, edition, locus, pos):
    if locus is None:
        return None
    if edition=="accord":
        a,b = (edge(rows,ed,locus,pos) for ed in ("ZL","IT"))
        return a if a==b else None
    group = rows[edition][str(locus)]["unites"]
    return group[pos] if group else None


def mapping(omissions):
    return [j for j in range(1,18) if j not in omissions]


def geometric_views():
    geom = read("geometrie/COUTS.json")["releves"]
    views = {}
    options = []
    for name, info in geom.items():
        ranks = info["classement"]
        candidates = [mapping((a,b)) for _,a,b,cost in ranks if cost==ranks[0][3]]
        options.extend(candidates)
        views[name] = candidates[0]
        views[name+"_second"] = info["deux_premiers"][1]["paires_par_mot"]
    views["commun"] = [choices[0] if len(set(choices))==1 else None for choices in zip(*options)]
    return views


def fit(examples):
    observed = defaultdict(list)
    for sign, end in examples:
        if sign is not None and end is not None:
            observed[sign].append(end)
    table = {k:v[0] for k,v in observed.items() if len(v)>=2 and len(set(v))==1}
    counts = Counter(y for group in observed.values() for y in group)
    common = min(counts, key=lambda y:(-counts[y],y)) if counts else None
    return table,common


def frozen(rows, edition, pairs):
    def sign(pair):
        return edge(rows,edition,15+pair*2,-1) if pair else None
    examples = [(sign(pair),edge(rows,edition,word,-1)) for word,pair in enumerate(pairs[:10],1)]
    key,base = fit(examples)
    guesses = {}
    for i in RESERVE:
        pair = pairs[i-1]
        s = sign(pair)
        guesses[str(i)] = {"paire":pair,"copie":s,"table":key.get(s),"majorite":base}
    return {"apprentissage":examples,"cle":key,"annonces":guesses}


def predictions(rows):
    return {view:{ed:frozen(rows,ed,pairs) for ed in EDITIONS} for view,pairs in geometric_views().items()}


def score_holdout(model, data, ed):
    rows = []
    for k, item in model["annonces"].items():
        t = edge(data,ed,int(k),-1)
        rows.append(dict(mot=int(k),**item,finale=t))
    good = [r for r in rows if r["finale"] is not None and r["copie"] is not None]
    targets = [r["finale"] for r in good]
    scores = {}
    for method in ("copie","table","majorite"):
        guesses = [r[method] for r in good]
        success = sum(x==y for x,y in zip(guesses,targets))
        extreme = sum(sum(x==y for x,y in zip(guesses,t))>=success for t in permutations(targets)) if good else 0
        total = math.factorial(len(targets)) if good else 0
        scores[method] = {"n":len(good),"emises":sum(x is not None for x in guesses),
                          "exactes":success,"p":extreme/total if total else None,
                          "extremes":extreme,"permutations":total,
                          "marques_exactes":sorted({r["copie"] for r in good if r[method]==r['finale']})}
    smallest = 0.0
    for i,m in enumerate(sorted(("copie","table"),key=lambda k:scores[k]["p"] if good else 1)):
        s = scores[m]
        if good:
            smallest=max(smallest,min(1,(2-i)*s["p"]))
        s["p_holm"] = smallest if good else None
        s["retenue"] = bool(good and s["p_holm"]<=.05 and s["exactes"]>=3 and
                            len(s["marques_exactes"])>=2 and s["exactes"]>scores["majorite"]["exactes"])
    return {"mots":rows,"scores":scores}


def equal(x,y):
    return x is not None and y is not None and x==y


def could_equal(x,y):
    return x is None or y is None or x==y


def exhaustive(data,ed):
    first = [edge(data,ed,i,0) for i in range(1,16)]
    last = [edge(data,ed,i,-1) for i in range(1,16)]
    odd = [edge(data,ed,15+i,0) for i in range(1,35,2)]
    even = [edge(data,ed,15+i,0) for i in range(2,35,2)]
    detail = []
    for omissions in ALL_OMISSIONS:
        full = primary = possible = possible_full = coverage = 0
        seen=defaultdict(set)
        for i,j in enumerate(mapping(omissions)):
            a,b,c,d = odd[j-1],even[j-1],first[i],last[i]
            primary += equal(b,d)
            full += equal(a,c) and equal(b,d)
            possible += could_equal(b,d)
            possible_full += could_equal(a,c) and could_equal(b,d)
            if b is not None and d is not None:
                coverage+=1
                seen[b].add(d)
        conflicts = sorted(k for k,v in seen.items() if len(v)>1)
        detail.append(dict(omises=omissions,couverture=coverage,finales=primary,deux_bords=full,
                           max_avec_inconnues=possible,max_bords_avec_inconnues=possible_full,
                           table_possible=not conflicts,conflits=conflicts))
    def span(field):
        seq=[r[field] for r in detail]
        return [min(seq),max(seq)]
    summary={k:span(k) for k in ("finales","deux_bords","couverture","max_avec_inconnues","max_bords_avec_inconnues")}
    summary["tables_compatibles"]=sum(r["table_possible"] for r in detail)
    summary["geometrie"] = next(r for r in detail if list(r["omises"])==read("geometrie/COUTS.json")["releves"]["A"]["deux_premiers"][0]["omissions"])
    return {"finales":last,"seconds":even,"bilan":summary,"details":detail}


def best(targets, signs):
    # State k skips k of the first signs. At each next word the skip count can only increase.
    a=b=c=0
    for i,t in enumerate(targets):
        a,b,c=a+equal(t,signs[i]),max(a,b)+equal(t,signs[i+1]),max(a,b,c)+equal(t,signs[i+2])
    return max(a,b,c)


def null_test(data):
    ends = data["finales"]
    signs = data["seconds"]
    obs = best(ends,signs)
    assert obs==data["bilan"]["finales"][1]
    indices = [k for k,e in enumerate(ends) if e is not None]
    letters = [ends[k] for k in indices]
    def statistic(values):
        sample=list(ends)
        for i,e in zip(indices,values):
            sample[i]=e
        return best(sample,signs)
    rotations=[statistic(letters[i:]+letters[:i]) for i in range(len(letters))]
    rng=random.Random(6618)
    n=99999
    hist=Counter()
    for _ in range(n):
        shuffled=list(letters)
        rng.shuffle(shuffled)
        hist[statistic(shuffled)] += 1
    k=sum(count for value,count in hist.items() if value>=obs)
    return {"observe":obs,"nb_permutations":n,"au_moins":k,"p_mc":(1+k)/(1+n),
            "histogramme":dict(sorted(hist.items())),"rotations":rotations,
            "p_rotations":sum(x>=obs for x in rotations)/len(rotations) if rotations else None}


def calibrate():
    rng=random.Random(6618)
    for _ in range(300):
        letters=rng.choices([None,'a','b','c','d'],k=15)
        signs=rng.choices([None,'a','b','c','d'],k=17)
        brute=max(sum(equal(x,signs[i-1]) for x,i in zip(letters,mapping(o))) for o in ALL_OMISSIONS)
        assert best(letters,signs)==brute
    letters=list("abcdeabcdeabcde")
    signs=list("abcdeXabcdeYabcde")
    assert best(letters,signs)==15
    assert fit(list(zip("abab","xyxy")))[0]=={"a":"x","b":"y"}
    assert not fit(list(zip("abab","xyyx")))[0]
    return {"accord_dynamique_enumeration":300,"cas_positif_avec_deux_intrus":15,"cas_positif_total":15,
            "table_artificielle_retrouvee":{"a":"x","b":"y"},"table_conflictuelle":{}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("etape",choices=["predire","ouvrir","rejouer","calibrer"])
    parser.add_argument("--sources",type=Path, default=HERE/"../../voynich_phase46/sources")
    args=parser.parse_args()
    if args.etape=="calibrer":
        write("CALIBRATION.json",calibrate())
        return
    if args.etape=="predire":
        write("APPRENTISSAGE.json",ingest(args.sources,set(range(1,11)) | set(range(16,50))))
        write("PREDICTIONS.json",predictions(read("APPRENTISSAGE.json")))
        return
    if args.etape=="ouvrir":
        write("RESERVE.json",ingest(args.sources,set(RESERVE)))
    training,truth=read("APPRENTISSAGE.json"),read("RESERVE.json")
    forecasts=read("PREDICTIONS.json")
    assert json.loads(json.dumps(predictions(training)))==forecasts
    assert all(not set(training[e]) & set(truth[e]) for e in ("ZL","IT"))
    allrows={ed:training[ed] | truth[ed] for ed in training}
    output={k:{ed:score_holdout(model,truth,ed) for ed,model in v.items()} for k,v in forecasts.items()}
    write("RESULTATS.json",output)
    trials={ed:exhaustive(allrows,ed) for ed in EDITIONS}
    trials["permutations"]=null_test(trials["accord"])
    write("OMISSIONS.json",trials)


if __name__=="__main__":
    main()
