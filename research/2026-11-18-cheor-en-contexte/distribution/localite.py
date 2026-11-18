"""Compter les reprises de légendes en conservant les paquets et la prose de chaque panneau."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial, prod
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-phrase-et-doublets/noms"))
from reprendre import MODES, agreed, common_words, corpus, inventory
from comparer import permutation_distribution
from compter import runs


def count_pages(lines):
    result = defaultdict(Counter)
    for locus, (unigrams, _, _) in lines.items():
        page = locus.partition(".")[0]
        result[page].update({word: freq for (word,), freq in unigrams.items()})
    return result


def folio(page):
    return re.match(r"f\d+", page)[0]


@lru_cache(maxsize=None)
def tail(N, K, n, x):
    """Queue hypergéométrique exacte, utilisée pour ordonner les cellules."""
    if not x:
        return Fraction(1)
    below = sum(comb(K, i) * comb(N - K, n - i) for i in range(max(0, n - N + K), x))
    return 1 - Fraction(below, comb(N, n))


def blocks(pages, groups):
    grouped = defaultdict(list)
    for page in sorted(pages):
        grouped[groups[page]].append(page)
    return list(grouped.values())


def probability(allowed_groups, mask):
    total = prod(factorial(len(group)) for group in allowed_groups)
    none = prod(permutation_distribution(group, mask)[0] for group in allowed_groups)
    return {"favorable": total - none, "total": total, "p": (total - none) / total}


def cutoff(cells, text, by_quire, by_folio, *, count=None, rarity=None):
    """Réunir les mots atteignant le seuil, puis compter les bijections qui en gardent au moins un."""
    mask = defaultdict(dict)
    matches = []
    for source, targets in cells.items():
        for target, words in targets.items():
            passed = False
            for word, (observed, score) in words.items():
                meets_threshold = observed >= count if count is not None else score <= rarity
                if meets_threshold:
                    passed = True
                    detail = {"legendes": source, "prose": target, "mot": word, "longueur": text[target].total()}
                    if score is None:
                        detail["lignes_distinctes"] = observed
                    else:
                        detail.update({"occurrences": observed, "queue": str(score)})
                    matches.append(detail)
            mask[source][target] = int(passed)
    return {"seuil": count if count is not None else str(rarity),
            "cahier": probability(by_quire, mask), "feuillet": probability(by_folio, mask),
            "attributions": matches}


def scan(labels, text, quires, seed=None):
    pages = sorted(labels)
    by_quire = blocks(pages, quires)
    by_folio = blocks(pages, {page: folio(page) for page in pages})
    totals = {}
    cells = defaultdict(dict)
    for group in by_quire:
        total = sum((text[target] for target in group), Counter())
        totals[quires[group[0]]] = total
        for source in group:
            for target in group:
                n = text[target].total()
                cells[source][target] = {
                    word: (text[target][word], tail(total.total(), total[word], n, text[target][word]))
                    for word in sorted(labels[source]) if text[target][word]
                }

    actual = [{"panneau": p, "mot": word, "x": x, "queue": str(score)}
              for p in pages for word, (x, score) in cells[p][p].items()]
    scores = [Fraction(row["queue"]) for row in actual]
    counts = [row["x"] for row in actual]
    assert actual, "Les deux ensembles étudiés contiennent au moins une reprise réelle."
    args = (cells, text, by_quire, by_folio)
    result = {
        "pages": {p: {"tokens": text[p].total(), "graphies_etiquettes": len(labels[p]),
                      "legendes_lisibles": len({loc for locs in labels[p].values() for loc in locs}),
                      "cheor": text[p]["cheor"]} for p in pages},
        "cahiers": by_quire, "feuillets": by_folio, "vrais_recouvrements": actual,
        "seuil_trois": cutoff(*args, count=3), "max_repetitions": cutoff(*args, count=max(counts)),
        "min_queue": cutoff(*args, rarity=min(scores))
    }
    if seed:
        p, word = seed
        q = quires[p]
        x, threshold = cells[p][p][word]
        result["reference_cheor"] = cutoff(*args, rarity=threshold)
        total = totals[q]
        stats = {}
        for target in pages:
            if quires[target] == q:
                n = text[target].total()
                observed = text[target][word]
                stats[target] = {"n": n, "x": observed, "queue": str(tail(total.total(), total[word], n, observed))}
        result["mot_fixe"] = {
            "cahier": q, "N": total.total(), "K": total[word], "panneaux": stats,
            "comparaison_compte": [p for p, v in stats.items() if v["x"] >= x],
            "comparaison_queue": [p for p, v in stats.items() if Fraction(v["queue"]) <= threshold]
        }
    return result


def figure_labels(editions, page):
    views = []
    for edition, cut in MODES:
        labels = {}
        for locus, (p, kind, _, raw) in editions[edition].items():
            if p == page and kind == "Ln":
                spans = runs(re.sub(r"\{[^}]*\}", "?", raw), cut)
                labels[locus] = [word for span in spans for _, word in span]
        views.append(labels)
    return common_words(views)


def main():
    pages, quires, views = inventory()
    captions = {
        p: common_words([views[mode][0][p] for mode in MODES]) for p in pages if p != "f101r"
    }
    editions, sections = corpus()
    agreed_rows = agreed(editions)
    texts = count_pages(agreed_rows)
    result = {"plantes": scan(captions, texts, quires, ("f102v2", "cheor"))}

    blocks_f102v2 = {}
    for first, last in [(17, 23), (30, 39)]:
        loci = [f"f102v2.{line}" for line in range(first, last + 1)]
        aligned = sum((agreed_rows[loc][0] for loc in loci), Counter())
        group = {"accord": {"n": aligned.total(), "cheor": aligned[("cheor",)]}}
        for edition, cut in MODES:
            words = Counter()
            for loc in loci:
                page, kind, _, raw = editions[edition][loc]
                assert page == "f102v2" and kind == "P0"
                spans = runs(re.sub(r"\{[^}]*\}", "?", raw), cut)
                words.update(word for span in spans for _, word in span)
            group[f"{edition}/{cut}"] = {"n": words.total(), "cheor": words["cheor"]}
        blocks_f102v2[f"{first}-{last}"] = group
    result["blocs_f102v2"] = blocks_f102v2

    by_section = defaultdict(Counter)
    faces = {}
    bath = {}
    for page, counts in sorted(texts.items()):
        section = sections[page]
        if counts["cheor"]:
            faces[page] = {"n": counts.total(), "x": counts["cheor"], "section": section}
        by_section[section].update({"n": counts.total(), "x": counts["cheor"], "panneaux": 1,
                                    "panneaux_avec_cheor": int(bool(counts["cheor"]))})
        if section == "B" and 75 <= int(folio(page)[1:]) <= 84:
            labels = figure_labels(editions, page)
            if labels:
                bath[page] = labels

    result["cheor_prose"] = {
        "sections": by_section, "faces_avec_cheor": faces,
        "loci": {locus: row[0][("cheor",)] for locus, row in agreed_rows.items() if ("cheor",) in row[0]}
    }
    bath_quires = dict.fromkeys(bath, "M")
    result["bains"] = scan(bath, texts, bath_quires)
    # Sensibilité enregistrée après le résultat principal. Chaque ligne ne vote qu’une fois par mot.
    line_counts = defaultdict(Counter)
    for locus, (unigrams, _, _) in agreed_rows.items():
        line_counts[locus.partition(".")[0]].update(word for (word,) in unigrams)
    for name, labels, groups in [("plantes", captions, quires), ("bains", bath, bath_quires)]:
        sample = sorted(labels)
        cells = {p: {
            target: {word: (line_counts[target][word], None) for word in sorted(labels[p])
                     if line_counts[target][word]} for target in sample if groups[target] == groups[p]
        } for p in sample}
        args = (cells, texts, blocks(sample, groups), blocks(sample, {p: folio(p) for p in sample}))
        highest = max(x for p in sample for x, _ in cells[p][p].values())
        result[name]["lignes_distinctes"] = {
            "seuil_trois": cutoff(*args, count=3), "maximum": cutoff(*args, count=highest)
        }
    (HERE / "RESULTATS.json").write_text(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n")
    for name in ("plantes", "bains"):
        sample = result[name]
        for key in ("max_repetitions", "min_queue"):
            print(name, key, sample[key]["seuil"], sample[key]["cahier"], sample[key]["feuillet"])


if __name__ == "__main__":
    main()
