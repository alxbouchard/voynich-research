"""Fit on the upper sign ranks and reveal the lower ranks in a separate invocation."""
from collections import Counter, defaultdict
from functools import lru_cache
import argparse
import json
import math
from pathlib import Path
import random
import re

HERE = Path(__file__).resolve().parent
VIEWS = ("commun", "A", "B")
EDITIONS = ("accord", "ZL", "IT")
DESTINATIONS = ("prose", "mots")
METHODS = ("copie", "table")
UNIT = re.compile(r"@[0-9]{3};|ckh|cth|cph|cfh|ch|sh|[a-z]")


def read(name):
    return json.loads((HERE / name).read_text())


def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def graphemes(field):
    units = UNIT.findall(field)
    return units if units and "".join(units) == field else []


def parse_field(text, is_mark):
    text = re.sub(r"<![^>]*>|<[%$\-~]>|!", "", text).strip()
    parts = text.split(".")
    if is_mark and len(parts) != 1:
        return None
    units = graphemes(parts[0])
    if not units or (is_mark and len(units) != 1):
        return None
    return units[0]


def extract(path, allowed):
    result = {}
    for line in path.read_text().splitlines():
        header, _, payload = line.partition(">")
        if not header.startswith("<f66r."):
            continue
        index = int(header.split(",")[0].split(".")[1])
        if index not in allowed:
            continue
        assert index not in result
        result[index] = parse_field(payload, 16 <= index <= 49)
    assert set(result) == set(allowed)
    return result


def value(data, edition, index):
    key = str(index)
    if edition == "accord":
        a, b = (data[ed][key] for ed in ("ZL", "IT"))
        return a if a == b else None
    return data[edition][key]


def majority(values):
    counts = Counter(values)
    return min(counts, key=lambda k: (-counts[k], k)) if counts else None


def fit(rows):
    pairs = defaultdict(list)
    for sign, initial in rows:
        pairs[sign].append(initial)
    table = {m: values[0] for m, values in sorted(pairs.items())
             if len(values) >= 2 and len(set(values)) == 1}
    return table, majority([v for _, v in rows])


def possibilities(predicted, targets):
    n = len(targets)
    if not n:
        return {"n": 0, "couvertes": 0, "exactes": 0, "p": None, "rotations": []}
    observed = sum(p == t for p, t in zip(predicted, targets))
    rotations = [sum(p == targets[(i + step) % n] for i, p in enumerate(predicted))
                 for step in range(n)]
    @lru_cache(maxsize=None)
    def favorable(mask, need):
        left = n - mask.bit_count()
        if need < 1:
            return math.factorial(left)
        if left < need:
            return 0
        i = n - left
        return sum(favorable(mask | (1 << j), need - (predicted[i] == targets[j]))
                   for j in range(n) if not mask & (1 << j))
    num, den = favorable(0, observed), math.factorial(n)
    return {"n": n, "couvertes": sum(p is not None for p in predicted),
            "exactes": observed, "p": num / den, "permutations_au_moins": num,
            "permutations": den, "rotations": rotations,
            "p_rotation": sum(x >= observed for x in rotations) / n}


def one_fit(geometry, training, view, edition, dest, reserved):
    pairs = geometry[view][dest]
    train = []
    for row in pairs:
        rank, loc = row
        if rank <= 22 and loc not in reserved:
            sign = value(training, edition, rank+15)
            initial = value(training, edition, loc)
            if sign is not None and initial is not None:
                train.append((sign, initial))
    table, frequent = fit(train)
    guesses = []
    for rank, loc in pairs:
        if rank <= 22:
            continue
        sign = value(training, edition, rank+15)
        guesses.append({"rang_marque": rank, "locus_cible": loc, "marque": sign,
                        "copie": sign, "table": table.get(sign), "majorite": frequent})
    return {"apprentissage": train, "cle_apprise": table, "initiale_majoritaire": frequent,
            "annonces": guesses}


def split(geometry):
    reserved = {loc for view in VIEWS for dest in DESTINATIONS
                for rank, loc in geometry[view][dest] if rank >= 23}
    training = {loc for view in VIEWS for dest in DESTINATIONS
                for rank, loc in geometry[view][dest] if rank <= 22} - reserved
    return training | set(range(16,50)), reserved


def collect(allowed, source):
    return {ed: {str(k): v for k,v in extract(source/(ed+".txt"),allowed).items()}
            for ed in ("ZL", "IT")}


def predict(geometry, training, reserved):
    return {view: {ed: {dest: one_fit(geometry,training,view,ed,dest,reserved)
                        for dest in DESTINATIONS} for ed in EDITIONS} for view in VIEWS}


def permutation_by_locus(rows, method):
    """Shuffle physical initials once per distinct target, preserving reused lines."""
    group = defaultdict(list)
    actual = {}
    for row in rows:
        loc = row["locus_cible"]
        group[loc].append(row[method])
        actual[loc] = row["initiale_observee"]
    keys = sorted(group)
    n = len(keys)
    if not n:
        return None
    score = [[group[loc].count(actual[target]) for target in keys] for loc in keys]
    observed = sum(score[i][i] for i in range(n))
    @lru_cache(maxsize=None)
    def favorable(mask, need):
        i = mask.bit_count()
        if need <= 0:
            return math.factorial(n-i)
        if i == n:
            return 0
        return sum(favorable(mask | (1 << j), need-score[i][j])
                   for j in range(n) if not mask & (1 << j))
    num = favorable(0,observed)
    return {"loci_distincts": n, "permutations_au_moins": num,
            "permutations": math.factorial(n), "p": num / math.factorial(n)}


def one_score(model, data, ed):
    truth, rejected = [], []
    for guess in model["annonces"]:
        actual = value(data, ed, guess["locus_cible"])
        row = dict(guess, initiale_observee=actual)
        if actual is None or row["marque"] is None:
            rejected.append(row)
        else:
            truth.append(row)
    targets = [row["initiale_observee"] for row in truth]
    scored = {}
    for method in ("copie", "table", "majorite"):
        guesses = [row[method] for row in truth]
        scored[method] = possibilities(guesses, targets)
        scored[method]["controle_par_locus_unique"] = permutation_by_locus(truth,method)
        scored[method]["marques_distinctes_exactes"] = sorted({
            row["marque"] for row in truth if row[method] == row["initiale_observee"]})
    training_counts = Counter(sign for sign, _ in model["apprentissage"])
    eligible = [row["rang_marque"] for row in truth if training_counts[row["marque"]] >= 2]
    return {"lignes": truth, "ecartees_lecture": rejected, "scores": scored,
            "rangs_avec_deux_exemples_ou_plus_en_apprentissage": eligible}


def adjust(models):
    family = [(dest,m) for dest in DESTINATIONS for m in METHODS]
    def p(pair):
        dest,m = pair
        val = models[dest]["scores"][m]["p"]
        return 1.0 if val is None else val
    floor = 0.0
    for index, pair in enumerate(sorted(family, key=p)):
        dest,m = pair
        score = models[dest]["scores"][m]
        floor = max(floor, min(1.0,(len(family)-index)*p(pair)))
        score["p_holm"] = floor if score["n"] else None
        score["regle_retenue"] = bool(score["n"] and floor <= .05 and score["exactes"] >= 3
                                     and len(score["marques_distinctes_exactes"]) >= 2
                                     and score["exactes"] > models[dest]["scores"]["majorite"]["exactes"])


def calibration():
    signs = list("abcd")*8 + list("ab")
    shuffled = signs.copy()
    random.Random(661117).shuffle(shuffled)
    result = {}
    for case, initials in [("copie",signs),("table",[dict(zip("abcd","mnop"))[s] for s in signs]),
                           ("melange",shuffled)]:
        table, common = fit(list(zip(signs[:22],initials[:22])))
        held = signs[22:]
        result[case] = {method:possibilities(pred,initials[22:])
                        for method,pred in [("copie",held),("table",[table.get(s) for s in held]),
                                            ("majorite",[common]*len(held))]}
    assert result["copie"]["copie"]["exactes"]==result["table"]["table"]["exactes"]==12
    assert result["table"]["copie"]["exactes"]==0 and result["melange"]["table"]["couvertes"]==0
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("etape", choices=["apprendre","devoiler","rejouer","calibrer"])
    parser.add_argument("--sources",type=Path,default=HERE/"../../voynich_phase46/sources")
    args=parser.parse_args()
    if args.etape=="calibrer":
        save("CALIBRATION.json",calibration())
        return
    geometry=read("ALIGNEMENTS.json")
    train, reserved=split(geometry)
    if args.etape=="apprendre":
        data=collect(train,args.sources)
        save("APPRENTISSAGE.json",data)
        save("PREDICTIONS.json",predict(geometry,data,reserved))
        return
    if args.etape=="devoiler":
        save("RESERVE.json",collect(reserved,args.sources))
    prediction=read("PREDICTIONS.json")
    assert prediction==json.loads(json.dumps(predict(geometry,read("APPRENTISSAGE.json"),reserved)))
    data=read("RESERVE.json")
    assert not train & reserved
    results={}
    for view, models in prediction.items():
        results[view]={}
        for ed,dests in models.items():
            results[view][ed]={dest:one_score(model,data,ed) for dest,model in dests.items()}
            adjust(results[view][ed])
    save("RESULTATS.json",results)


if __name__=="__main__":
    main()
