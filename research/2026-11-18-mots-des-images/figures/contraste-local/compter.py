"""Comparer deux groupes déjà repérés, au sein des mêmes faces du cahier des bains."""
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / "2026-11-18-mots-et-dessins"))
from etiquettes import DATA, FILES, corpus

LEAVES = list(range(75, 85))
WORDS = ("otedy", "otoly")
KINDS = ("Ln", "Lt")


def local_distribution(faces, word):
    """Réattribuer les emplacements du mot sur chaque face en gardant les volumes fixes."""
    distribution = {0: Fraction(1)}
    for face in faces.values():
        people = len(face["Ln"]["lisibles"])
        other = len(face["Lt"]["lisibles"])
        hits = sum(len(face[kind]["mots"][word]) for kind in KINDS)
        possible = range(max(0, hits - other), min(hits, people) + 1)
        ways = comb(people + other, hits)
        revised = Counter()
        for j in possible:
            mass = Fraction(comb(people, j) * comb(other, hits - j), ways)
            for i, previous in distribution.items():
                revised[i + j] += previous * mass
        distribution = revised
    assert sum(distribution.values()) == 1
    return distribution


def compare(edition, split):
    table = corpus(edition, LEAVES, split)
    faces = defaultdict(lambda: {k: {"lisibles": [], "exclus": [], "mots": {w: [] for w in WORDS}} for k in KINDS})
    for locus, (face, _, kind, words) in sorted(table.items()):
        if kind not in KINDS:
            continue
        row = faces[face][kind]
        if words is None:
            row["exclus"].append(locus)
            continue
        row["lisibles"].append(locus)
        for word in WORDS:
            if word in words:
                row["mots"][word].append(locus)
    mixed = {name: face for name, face in faces.items() if all(face[k]["lisibles"] for k in KINDS)}
    results = {}
    for word in WORDS:
        counts = {k: sum(len(f[k]["mots"][word]) for f in mixed.values()) for k in KINDS}
        distribution = local_distribution(mixed, word)
        rate = sum(mass for n, mass in distribution.items() if n >= counts["Ln"])
        results[word] = {
            "observations": counts,
            "distribution_exacte_Ln": {n: str(mass) for n, mass in sorted(distribution.items())},
            "probabilite_conditionnelle_au_moins_autant_Ln": str(rate),
        }
    return {
        "faces_mixtes": list(mixed),
        "denominateurs": {k: sum(len(f[k]["lisibles"]) for f in mixed.values()) for k in KINDS},
        "par_mot": results,
        "toutes_les_faces_avec_locus_Ln_ou_Lt": faces,
    }


def main():
    report = {
        "editions_sha256": {name: hashlib.sha256((DATA / filename).read_bytes()).hexdigest()
                            for name, filename in FILES.items()},
        "feuillets": LEAVES,
        "lectures": {},
    }
    for edition in ("accord", *FILES):
        for split in (False, True):
            name = edition + ("_separe" if split else "_joint")
            report["lectures"][name] = compare(edition, split)
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    (HERE / "RESULTATS.json").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
