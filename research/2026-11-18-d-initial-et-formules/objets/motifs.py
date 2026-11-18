"""Mesurer quelle part des légendes conserve un même motif sur chaque feuillet."""
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-legendes-repetitions/categories"))
from predire import SOURCE, inventory
sys.path.insert(0, str(RESEARCH / "2026-11-18-mois-automne/cle"))
from dechiffrer import segment

LOCAL = {"Ln": "Lt", "Lf": "Lc"}
KINDS = ("Ls", "Lf", "Ln", "Lz", "Lt", "Lc")


def profile(rows, width):
    counts = defaultdict(Counter)
    sizes = Counter()
    for leaf, locus, word, kind in rows:
        units = segment(word)
        assert "".join(units) == word, (locus, word, units)
        motifs = {units[i:i + width] for i in range(len(units) - width + 1)}
        counts[kind, leaf].update(motifs)
        sizes[kind, leaf] += 1
    return counts, sizes


def summary(rows, width, minimum):
    counts, sizes = profile(rows, width)
    answer = {}
    for kind in KINDS:
        leaves = sorted(leaf for (cat, leaf), total in sizes.items()
                        if cat == kind and total >= minimum)
        if not leaves:
            answer[kind] = {"feuillets": []}
            continue
        shared = set.intersection(*(set(counts[kind, leaf]) for leaf in leaves))
        floor = {motif: min(Fraction(counts[kind, leaf][motif], sizes[kind, leaf])
                            for leaf in leaves) for motif in shared}
        best = max(floor.values(), default=Fraction(0))
        winners = []
        for motif in sorted(m for m in shared if floor[m] == best):
            def by_category(category, eligible):
                return [sum(counts[category, leaf][motif] for leaf in eligible),
                        sum(sizes[category, leaf] for leaf in eligible)]
            baseline = LOCAL.get(kind)
            matched = [leaf for leaf in leaves if baseline and sizes[baseline, leaf] >= minimum]
            others = {cat: by_category(cat, [leaf for (c, leaf) in sizes if c == cat])
                      for cat in KINDS}
            winners.append({
                "unites": list(motif),
                "par_feuillet": {leaf: by_category(kind, [leaf]) for leaf in leaves},
                "tous_lieux_admis_par_categorie": others,
                "comparaison_sur_memes_feuillets": {
                    "feuillets": matched, "cible": by_category(kind, matched),
                    "temoin": by_category(baseline, matched), "type_temoin": baseline}
                    if baseline else None})
        answer[kind] = {"feuillets": leaves, "etiquettes": sum(sizes[kind, f] for f in leaves),
                        "meilleur_minimum": [best.numerator, best.denominator],
                        "motifs_communs": len(shared), "ex_aequo": winners}
    return answer


def macer():
    source = RESEARCH / "2026-11-18-legendes-repetitions/temoin/occurrences.tsv"
    by_lemma = defaultdict(list)
    with source.open() as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            by_lemma[row["lemme"]].append(row)
    out = {}
    for lemma, rows in by_lemma.items():
        forms = {r["forme"] for r in rows}
        pairs = set.intersection(*({w[i:i+2] for i in range(len(w) - 1)} for w in forms))
        out[lemma] = {"emplois": len(rows), "formes": sorted(forms),
                      "notices": len({r["notice"] for r in rows}),
                      "paires_dans_toutes_les_formes": sorted(pairs)}
    return {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "lemmes": out}


def main():
    rows = inventory(json.loads(SOURCE.read_text()))
    out = {"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
           "temoin_macer": macer(), "etiquettes": len(rows), "feuillets": len({row[0] for row in rows}),
           "essais": {f"{width}_signes_{threshold}_lieux": summary(rows, width, threshold)
                      for width, threshold in [(1, 4), (2, 4), (3, 4), (2, 1)]}}
    (HERE / "RESULTATS.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
