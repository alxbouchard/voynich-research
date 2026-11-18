"""Apprendre sur A, puis évaluer les formes figées sur des classements photographiques."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
import json

from annoncer import HERE, RULES, digest, features, units, write


def load(name):
    return json.loads((HERE / name).read_bytes())


def cases(lot):
    key = load("images/CLE.json")
    values = [load(f"votes/{lot}-{i}.json") for i in (1, 2)]
    assert all(set(v) == {k for k, item in key.items() if item["lot"] == lot} for v in values)
    grades = {}
    for code in values[0]:
        rows = key[code]["rangs"]
        for source in values:
            assert [len(x) for x in rows] == [len(x) for x in source[code]]
        for rank, row in enumerate(rows):
            for position, number in enumerate(row):
                grades[number] = [v[code][rank][position] for v in values]
                assert set(grades[number]) <= set("YSXM") and len(grades[number]) == 2
    records = [dict(row, votes=grades[row["fragment"]]) for row in load("ANNONCES.json")["annonces"] if row["lot"] == lot]
    assert len(records) == len(grades)
    return records


def sample(rows, reading="strict", allow_multi=False):
    keep = []
    for row in rows:
        g1, g2 = row["votes"]
        if g1 != g2 or g1 not in ("YSM" if allow_multi else "YS"):
            continue
        words = row["lectures"][0] if reading == "H" else row["commun"]
        if not words or (reading != "attaches" and row["attache"] != "ordre_documente"):
            continue
        keep.append((row, features(words), g1 == "Y"))
    return keep


def null_by_panel(rows, rule):
    counts = defaultdict(lambda:[0, 0, 0])
    for row, words, truth in rows:
        v = counts[row["page"]]
        v[0] += 1
        v[1] += truth
        v[2] += rule in words
    distribution = {0:Fraction(1)}
    for n, positives, selected in counts.values():
        probs = {hits:Fraction(comb(positives,hits)*comb(n-positives,selected-hits),comb(n,selected))
                 for hits in range(max(0,positives+selected-n),min(positives,selected)+1)}
        new = defaultdict(Fraction)
        for score, weight in distribution.items():
            for hits,prob in probs.items():
                new[score+hits] += prob*weight
        distribution = new
    assert sum(distribution.values()) == 1
    return distribution


def score(rows, rule):
    tp, fp, fn, tn = [], [], [], []
    for row, words, truth in rows:
        dest = (tp if truth else fp) if rule in words else (fn if truth else tn)
        dest.append(row["fragment"])
    dist = null_by_panel(rows,rule)
    return {"VP":tp, "FP":fp, "FN":fn, "VN":tn, "constante_majoritaire":max(len(tp)+len(fn),len(fp)+len(tn)),
            "VP_attendus":float(sum(k*v for k,v in dist.items())),
            "p_VP_au_moins":float(sum(v for k,v in dist.items() if k>=len(tp)))}


def learn():
    rows = sample(cases("A"))
    candidates = []
    positives = sum(pos for _,_,pos in rows)
    negatives = len(rows) - positives
    if positives and negatives:
        for rule in sorted(set().union(*(tokens for _,tokens,_ in rows))):
            panels = {row["page"] for row, toks, y in rows if y and rule in toks}
            if len(panels) < 2:
                continue
            tp = sum(y and rule in tokens for _,tokens,y in rows)
            fp = sum(not y and rule in tokens for _,tokens,y in rows)
            value = Fraction(tp,positives) - Fraction(fp,negatives)
            if value > 0:
                rank = (-value,-tp,rule[0] != "mot",-len(units(rule[1],False)),rule[1],rule[0])
                candidates.append((rank,rule))
    best = min(candidates)[1] if candidates else None
    reserve = {}
    for row in load("ANNONCES.json")["annonces"]:
        if row["lot"] == "B":
            reserve[row["fragment"]] = (best in features(row["commun"])) if best and row["commun"] else None
    write("APPRENTISSAGE.json",{"A_positifs":positives,"A_simples":negatives,
          "regles_admissibles":len(candidates),"regle":best,"annonces_B":reserve,
          "empreintes_A":[digest(HERE / f"votes/A-{i}.json") for i in (1,2)]})


def evaluate():
    fit = load("APPRENTISSAGE.json")
    by_lot = {lot:cases(lot) for lot in ("A","B")}
    all_cases = by_lot["A"]+by_lot["B"]
    tested = {}
    for reading in ("strict","attaches","H"):
        for multi in (False,True):
            for lot, records in (("A",by_lot["A"]),("B",by_lot["B"]),("ensemble",all_cases)):
                subset = sample(records,reading,multi)
                rules = list(RULES)
                if lot == "B" and fit["regle"]:
                    rules.append(tuple(fit["regle"]))
                tested[f"{reading}/{int(multi)}/{lot}"] = {
                    "Y":sum(y for _,_,y in subset),"autres":sum(not y for _,_,y in subset),
                    "regles":{"/".join(rule):score(subset,rule) for rule in rules}}
    write("RESULTATS.json",{"accords_et_desaccords":dict(Counter("".join(row["votes"]) for row in all_cases)),
        "fragments":all_cases, "mesures":tested})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action",choices=["apprendre","verifier"])
    if parser.parse_args().action == "apprendre":
        learn()
    else:
        evaluate()
