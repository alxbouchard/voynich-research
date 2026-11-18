"""Comparer les graphies inédites à des réattributions qui conservent les mots observés."""
from collections import Counter, defaultdict
from itertools import combinations
from random import Random
import json
from combiner import HERE, combine, segment, write


def main():
    ann = json.loads((HERE/"ANNONCES.json").read_bytes())
    res = json.loads((HERE/"RESULTATS.json").read_bytes())
    train = ann["apprentissage"]
    sites = [r for _,r in sorted(train.items()) if r["mot"]]
    target = Counter(r["mot"] for r in res["releve"].values() if r["lot"]=="zodiaque" and r["mot"])
    labels = {s['mot'] for s in sites}

    def score(stars):
        a, b = [], []
        for idx, row in enumerate(sites):
            (a if idx in stars else b).append(row["mot"])
        trial = combine(a,b,2,labels)["5_inedits"]
        return sum(w in target for w in trial), sum(target[w] for w in trial)

    actual = {i for i,row in enumerate(sites) if row["lot"]=="etoiles"}
    obs = score(actual)
    panel_scores, length_scores = Counter(), Counter()
    faces = sorted({row["face"] for row in sites})
    for pair in combinations(faces,2):
        sample = {i for i,row in enumerate(sites) if row["face"] in pair}
        panel_scores[score(sample)] += 1
    rng = Random(73023)
    lengths = defaultdict(list)
    for i,r in enumerate(sites):
        lengths[len(segment(r["mot"]))].append(i)
    for _ in range(2000):
        sample = set()
        for key in sorted(lengths):
            group = lengths[key]
            sample.update(rng.sample(group,sum(i in actual for i in group)))
        length_scores[score(sample)] += 1

    def describe(pairs):
        n = sum(pairs.values())
        return {"n":n, "distribution":[[a,b,f] for (a,b),f in sorted(pairs.items())],
                "au_moins_autant_formes":sum(f for (a,b),f in pairs.items() if a>=obs[0]),
                "strictement_plus_formes":sum(f for (a,b),f in pairs.items() if a>obs[0]),
                "au_moins_autant_lieux":sum(f for (a,b),f in pairs.items() if b>=obs[1])}
    write("CONTROLES.json",{"observe":obs,"panneaux":faces,"melanges_longueur":describe(length_scores),
                            "permutations_panneaux":describe(panel_scores)})


if __name__=="__main__":
    main()
