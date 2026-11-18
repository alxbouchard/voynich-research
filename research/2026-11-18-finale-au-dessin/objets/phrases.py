"""Appliquer les dix tables de « femme » hors des cinq feuillets de départ."""
from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
import json
import re

from comparer import MACER, folio
from personnages import corpus, runs

HERE = Path(__file__).resolve().parent
EXCLUDED = {"f73", "f75", "f77", "f82", "f84"}
SIGNS = tuple("otedy")
ALPHABET = set(SIGNS)


def windows(words, n):
    return zip(*(words[i:] for i in range(n)))


def concordance(editions, n):
    rows = {}
    for edition, lines in editions.items():
        for spacing in ("joints", "separes"):
            seen = {}
            for locus, (page, code, _, raw) in lines.items():
                if code != "P0" or folio(page) in EXCLUDED:
                    continue
                count = Counter()
                for span in runs(re.sub(r"\{[^}]*\}", "?", raw), spacing):
                    words = [w for _, w in span]
                    for group in windows(words, n):
                        if all(set(w) <= ALPHABET for w in group):
                            count[group] += 1
                seen[locus] = count
            rows[edition, spacing] = seen
    by_group = defaultdict(dict)
    for loc in set.intersection(*(set(v) for v in rows.values())):
        first, *others = [v[loc] for v in rows.values()]
        shared = first.copy()
        for other in others:
            shared &= other
        for group, count in shared.items():
            by_group[group][loc] = count
    return dict(sorted(by_group.items()))


def outcomes(table, groups, known, vocabulary):
    decoded = {w: "".join(table[s] for s in w) for g in groups for w in g}
    readings = []
    for group, loci in groups.items():
        words = tuple(decoded[w] for w in group)
        readings.append({"eva": group, "lecture": words, "total": sum(loci.values()),
                         "mots_attestes": all(w in vocabulary for w in words), "suite_attestee": words in known})
    return readings


def main():
    model = json.loads((HERE / "OTOLY.json").read_text())["latin"]["attestations"]
    editions, _ = corpus()
    chapters = json.loads(MACER.read_text())
    words = {w for c in chapters.values() for w in c}
    groups = concordance(editions, 2)
    pairs = {w for c in chapters.values() for w in windows(c, 2)}
    results = []
    for word, record in model.items():
        for key in record["tables"]["otedy"]:
            observed = outcomes(key, groups, pairs, words)
            hits = sum(r["total"] for r in observed if r["suite_attestee"])
            controls = Counter()
            for assignment in permutations(SIGNS):
                if assignment != SIGNS:
                    scrambled = {s: key[new] for s, new in zip(SIGNS, assignment)}
                    rows = outcomes(scrambled, groups, pairs, words)
                    controls[sum(r["total"] for r in rows if r["suite_attestee"])] += 1
            result = {"cible": word, "table": key, "sorties": observed, "occurrences_attestees": hits,
                      "histogramme_temoins": dict(sorted(controls.items()))}
            if hits:
                triples = concordance(editions, 3)
                matched = {tuple(r["eva"]) for r in observed if r["suite_attestee"]}
                triples = {g: v for g, v in triples.items() if g[:2] in matched or g[1:] in matched}
                known = {w for c in chapters.values() for w in windows(c, 3)}
                result["triplets"] = outcomes(key, triples, known, words)
                result["lieux_triplets"] = {" ".join(g): dict(sorted(v.items())) for g,v in triples.items()}
            results.append(result)
    summary = {"feuillets_exclus": sorted(EXCLUDED),
               "paires_lisibles": {" ".join(pair): dict(sorted(v.items())) for pair, v in groups.items()},
               "tables": results}
    (HERE / "PHRASES.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(len(groups), sum(sum(v.values()) for v in groups.values()),len({loc for v in groups.values() for loc in v}))
    for r in results:
        print(r["cible"], r["table"], sum(x["total"] for x in r["sorties"] if x["mots_attestes"]),
              r["occurrences_attestees"],r["histogramme_temoins"])


if __name__ == "__main__":
    main()
