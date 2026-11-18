"""Contrôle de récupération ouverte de noms botaniques par une clé partielle."""
import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import random
from string import ascii_lowercase

HERE = Path(__file__).resolve().parent
MODES = ("premier_mot", "nom_complet")


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def prepare(records, mode, merge_v):
    alphabet = list(range(80, 106))
    random.Random(14850328).shuffle(alphabet)
    code = dict(zip(ascii_lowercase, alphabet))
    names = {}
    for item in records:
        word = item["nom_latin"].lower()
        if mode == "premier_mot":
            word = word.split()[0]
        if merge_v:
            word = word.replace("v", "u")
        names[str(item["chapitre"])] = word
    cipher = {k: [code[c] if c != " " else 0 for c in w] for k, w in names.items()}
    return names, cipher


def fit(cipher, names, ids):
    key, reverse = {0: " "}, {" ": 0}
    for item in ids:
        if len(cipher[item]) != len(names[item]):
            return {}, "longueur"
    for item in ids:
        for sym, ch in zip(cipher[item], names[item]):
            if (sym in key and key[sym] != ch) or (ch in reverse and reverse[ch] != sym):
                return {}, "contradiction"
            key[sym] = ch
            reverse[ch] = sym
    return key, "coherent"


def predict(cipher, known, targets):
    key, status = fit(cipher, known, known)
    if status != "coherent":
        raise ValueError(status)
    return {k: "".join(key.get(sym, "?") for sym in cipher[k]) for k in targets}


def evaluate(readings, answers, skip=()):
    counts = Counter(dict(noms=0, exacts=0, partiels=0, inconnus=0,
                          lettres=0, justes=0, erronees=0, non_lues=0))
    individual = {}
    for k, result in readings.items():
        if k in skip:
            continue
        answer = answers[k]
        assert len(answer) == len(result)
        pairs = [(a,b) for a,b in zip(answer,result) if a != " "]
        correct = sum(a == b for a,b in pairs)
        blanks = sum(b == "?" for a,b in pairs)
        incorrect = len(pairs) - correct - blanks
        counts.update(noms=1, lettres=len(pairs), justes=correct, non_lues=blanks, erronees=incorrect)
        if len(pairs) == correct:
            counts["exacts"] += 1
        elif len(pairs) == blanks:
            counts["inconnus"] += 1
        elif incorrect==0:
            counts["partiels"] += 1
        individual[k] = {"attendu": answer, "lu": result}
    return {"comptes": dict(counts), "lecture_par_chapitre": individual}


def permute(cipher, known):
    hist = Counter()
    valid = []
    for ids in permutations(known):
        shuffled = {k: known[v] for k,v in zip(known,ids)}
        _, status = fit(cipher, shuffled, shuffled)
        hist[status] += 1
        if status == "coherent":
            valid.append(ids)
    return {"comptes": dict(hist), "appariements_coherents": valid}


def score(probe, truth, predicted):
    known = probe["paires_connues"]
    unseen = set(truth).difference(known)
    repeats = [k for k in unseen if truth[k] in known.values()]
    top_letter = Counter(w[0] for w in known.values()).most_common(1)[0][0]
    const = {k: top_letter + "".join(" " if c == " " else "?" for c in truth[k][1:]) for k in unseen}
    jackknife = {k: predict(probe["formes_opaques"], {i:v for i,v in truth.items() if i!=k}, [k])[k]
                 for k in truth}
    return {"reserve": evaluate(predicted, truth), "noms_repris_entrainement":sorted(repeats),
            "reserve_formes_nouvelles": evaluate(predicted, truth, repeats),
            "temoin_initiale": evaluate(const, truth),
            "permutations":permute(probe["formes_opaques"],known),
            "laisser_un_nom":evaluate(jackknife,truth)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["preparer", "predire", "verifier"])
    parser.add_argument("--sortie",type=Path,default=HERE)
    parser.add_argument("--titres",type=Path,default=HERE/"TITRES.json")
    args = parser.parse_args()
    out=args.sortie
    out.mkdir(exist_ok=True,parents=True)
    fixtures, guesses, results = {}, {}, {}
    if args.action != "preparer":
        fixtures = load(out/"DEFI.json")
    if args.action == "verifier":
        guesses = load(out/"PREDICTIONS.json")
    records = load(args.titres) if args.action != "predire" else []
    for mode in MODES:
        for merge in (False,True):
            condition = mode + ("_u_v_reunis" if merge else "_principal")
            if args.action == "preparer":
                truth, cipher = prepare(records,mode,merge)
                fixtures[condition] = {"formes_opaques":cipher,
                                       "paires_connues":{k:v for k,v in truth.items() if int(k)<=6}}
            else:
                probe=fixtures[condition]
                known=probe["paires_connues"]
                target=[k for k in probe["formes_opaques"] if k not in known]
                reading=predict(probe["formes_opaques"],known,target)
                if args.action == "predire":
                    guesses[condition]=reading
                else:
                    assert reading==guesses[condition]
                    truth,cipher=prepare(records,mode,merge)
                    assert cipher==probe["formes_opaques"]
                    results[condition]=score(probe,truth,reading)
    if args.action=="preparer":
        save(out/"DEFI.json",fixtures)
    elif args.action=="predire":
        save(out/"PREDICTIONS.json",guesses)
    else:
        save(out/"RESULTATS.json",results)


if __name__=="__main__":
    main()
