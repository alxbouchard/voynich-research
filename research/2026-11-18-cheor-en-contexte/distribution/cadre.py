"""Les voisins d'un cheor textuel correspondent-ils à une inscription de fragment ?"""

from collections import Counter, defaultdict
from fractions import Fraction
from math import factorial, prod
import json

from localite import HERE, MODES, agreed, blocks, common_words, corpus, folio, inventory
from comparer import eligible, permutation_distribution

MARK = "cheor"
SEED = "f102v2"


def occurrences(loci, selected, distance):
    rows = []
    markers = {}
    for locus, grams in loci.items():
        page = locus.partition(".")[0]
        n = grams[0][(MARK,)]
        if page not in selected or not n:
            continue
        markers[locus] = n
        for sequence, count in grams[distance].items():
            for anchor, side, neighbor in [(0, "droite", -1), (-1, "gauche", 0)]:
                if sequence[anchor] == MARK:
                    word = sequence[neighbor]
                    rows.append({"panneau": page, "lieu": locus, "cote": side,
                                 "sequence": list(sequence), "voisin": word, "n": count,
                                 "admissible": bool(eligible(word)) and word != MARK})
    # Une ligne à plusieurs cheor ne permettrait pas de rattacher automatiquement tous les côtés
    # à une mention individuelle. Toutes les lignes de ces 15 panneaux ont une mention au plus.
    assert all(n == 1 for n in markers.values())
    assert all(n == 1 for n in Counter((r["lieu"], r["cote"]) for r in rows).values())
    return markers, rows


def summarize(rows, markers, labels, groups):
    matrix = {p: {q: 0 for q in labels if groups[p] == groups[q]} for p in labels}
    results = []
    for row in rows:
        p, w = row["panneau"], row["voisin"]
        matches = {}
        if row["admissible"]:
            for source, words in labels.items():
                if groups[p] == groups[source] and w in words:
                    matches[source] = words[w]
                    matrix[p][source] += row["n"]
        results.append(dict(row, legendes_compatibles=matches, correspondance_locale=p in matches))

    actual = sum(matrix[p][p] for p in labels)
    distribution = Counter({0: 1})
    for group in blocks(labels, groups):
        partial = permutation_distribution(group, matrix)
        combined = Counter()
        for a, u in distribution.items():
            for b, v in partial.items():
                combined[a + b] += u * v
        distribution = combined
    total = sum(distribution.values())
    assert total == prod(factorial(len(g)) for g in blocks(labels, groups))
    favorable = sum(count for score, count in distribution.items() if score >= actual)
    by_side = {}
    for side in ("gauche", "droite"):
        subset = [r for r in results if r["cote"] == side]
        by_side[side] = {"lus": sum(r["n"] for r in subset),
                         "admissibles": sum(r["n"] for r in subset if r["admissible"]),
                         "reprises": sum(r["n"] for r in subset if r["correspondance_locale"])}
    return {"cheor": markers, "cheor_avec_voisin": len({r["lieu"] for r in results}),
            "cheor_avec_voisin_admissible": len({r["lieu"] for r in results if r["admissible"]}),
            "par_cote": by_side, "voisins": results, "reprises": actual,
            "feuillets_reprises": sorted({folio(r["panneau"]) for r in results if r["correspondance_locale"]}),
            "histogramme": dict(sorted(distribution.items())), "au_moins_observe": favorable,
            "permutations": total, "p": str(Fraction(favorable, total))}


def main():
    pages, groups, views = inventory()
    labels = {p: common_words([views[mode][0][p] for mode in MODES]) for p in pages if p != "f101r"}
    editions, _ = corpus()
    lines = agreed(editions)
    summary = {}
    for name, selected in [("depart", [SEED]), ("transfert", [p for p in labels if p != SEED]),
                           ("hors_feuillet_102", [p for p in labels if folio(p) != "f102"])]:
        pool = {p: labels[p] for p in selected}
        result = {"panneaux": sorted(pool)}
        for distance in [1, 2]:
            markers, rows = occurrences(lines, pool, distance)
            stats = summarize(rows, markers, pool, groups)
            result[distance] = stats
            print(name, distance, len(markers), stats["cheor_avec_voisin"], stats["par_cote"],
                  stats["reprises"], stats["p"], [(r["lieu"],r["voisin"],list(r["legendes_compatibles"]))
                                                 for r in stats["voisins"] if r["legendes_compatibles"]])
        summary[name] = result
    (HERE / "CADRE-RESULTATS.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
