"""Compare the prespecified label and spoke maps on f69r and f67v1."""

import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

from secteurs import ALG, DATA, RULES, assess, contiguous, data, null_hist, slots

HERE = Path(__file__).resolve().parent
MAPS = {
    "f69r": ("strict", "possible"),
    "f67v1": ("axis_inside_visible_frame", "possible_including_edge"),
}


def digest(source):
    return hashlib.sha256(source.read_bytes()).hexdigest()


def check_null():
    # Direct enumeration independent of the rook-polynomial calculation.
    for n, masks in [(4, (0, 3, 9, 5)), (5, (2, 0, 6)), (5, (0, 0, 0, 0, 0))]:
        counts = Counter(
            sum((mask >> dest) & 1 for mask, dest in zip(masks, targets))
            for targets in itertools.permutations(range(n), len(masks))
        )
        assert [counts[j] for j in range(len(masks) + 1)] == null_hist(n, masks)


def score(queries, bodies, actual_ids, alphabet, rule):
    trial = assess(queries, bodies, alphabet, rule)
    masks = trial["masques_compatibles"]
    scores = trial["rotations"]
    n = len(bodies)
    hits = trial["succes"]
    def eligible(words):
        return any(w and (rule != "debut3" or len(ALG[alphabet].findall(w)) >= 3) for _,w in words)

    support = [i for i in queries if eligible(queries[i]) and eligible(bodies[i])]
    whole = {}
    for i, words in queries.items():
        for locus, group in itertools.groupby(bodies[i], key=lambda slot: slot[0].split(":")[0]):
            if contiguous(words, list(group)):
                whole.setdefault(actual_ids[i-1], []).append(locus)
    restricted_masks = tuple(
        sum(bool(masks[i-1] & (1 << (j-1))) << k for k, j in enumerate(support))
        for i in support
    )
    restricted = null_hist(len(support), restricted_masks)
    assert sum(restricted) == math.factorial(len(support))
    assert hits == sum((m >> i) & 1 for i, m in enumerate(restricted_masks))
    # Over all cyclic shifts, each label visits each destination exactly once.
    assert sum(scores) == sum(m.bit_count() for m in masks)
    assert sum(trial["distribution_permutations"]) == math.factorial(n)
    assert Fraction(sum(i*v for i, v in enumerate(trial["distribution_permutations"])), math.factorial(n)) == Fraction(sum(scores), n)
    return {
        "n_secteurs": n,
        "secteurs_comparables": [actual_ids[i-1] for i in support],
        "succes": hits,
        "succes_destination_unique": trial["succes_destination_unique"],
        "rencontres_locales": {actual_ids[i-1]: v for i,v in trial["rencontres_locales"].items()},
        "legendes_entieres_sur_un_seul_rayon": whole,
        "masques_ligne_par_legende": masks,
        "cellules_positives_matrice": sum(m.bit_count() for m in masks),
        "rotations": scores,
        "rotations_au_moins_aussi_bonnes": str(Fraction(sum(v >= hits for v in scores), n)),
        "esperance_permutations": trial["esperance_succes"],
        "permutations_au_moins_aussi_bonnes": trial["permutations_au_moins_aussi_bonnes"],
        "distribution_permutations": trial["distribution_permutations"],
        "permutations_secteurs_comparables": {
            "distribution": restricted,
            "au_moins_aussi_bonnes": str(Fraction(sum(restricted[hits:]), sum(restricted))),
        },
    }


def main():
    check_null()
    geo_path = HERE / "geometrie/GEOMETRIE.json"
    geo = json.loads(geo_path.read_text())
    results = {}
    out = {"geometrie_sha256": digest(geo_path), "sources_sha256": {},
           "ordre_loci": {}, "essais": {}, "resultats": results}
    for edition in ("ZL3b-n", "IT2a-n"):
        path = DATA / (edition + ".txt")
        table = data(path)
        out["sources_sha256"][edition] = digest(path)
        for page, maps in MAPS.items():
            for key in maps:
                ray_map = {int(i): rays for i, rays in geo[page][key].items()}
                ids = sorted(ray_map)
                out["ordre_loci"][page] = ids
                for split, variant in itertools.product((False, True), ("strict", "first", "last")):
                    queries = {i: slots(table, page, [locus], split, variant)
                               for i, locus in enumerate(ids, 1)}
                    text = {i: slots(table, page, ray_map[locus], split, variant)
                            for i, locus in enumerate(ids, 1)}
                    for limit, alphabet, rule in itertools.product((8, None), ALG, RULES):
                        bodies = {i: words[:limit] for i,words in text.items()}
                        result = score(queries, bodies, ids, alphabet, rule)
                        code = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()[:16]
                        if code in results:
                            assert results[code] == result
                        else:
                            results[code] = result
                        scenario = "/".join((edition, page, key, "separe" if split else "joint", variant,
                                             str(limit) if limit else "tout", alphabet, rule))
                        out["essais"][scenario] = code
    (HERE/"transfert.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
