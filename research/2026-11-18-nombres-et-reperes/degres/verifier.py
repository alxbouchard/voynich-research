"""Recompter les paires exportées et leur espérance exacte par strate, sans NumPy."""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_20261028/data/ZL3b-n.txt"


def main():
    ring, groups, boundary = 0, {}, re.compile(r"^<([^.]+\.\d+),([@&])Lz>")
    for line in DATA.read_text().splitlines():
        match = boundary.match(line)
        if not match:
            continue
        loc, start = match.groups()
        ring += start == "@"
        groups[loc] = ring
    groups["f72r2.19+figure_sans_nom"] = groups["f72r2.19"]
    with (HERE / "PAIRES-10.tsv").open() as f:
        records = list(csv.DictReader(f, delimiter="\t"))
    results = json.loads((HERE / "RESULTATS.json").read_text())
    out = []
    for book in results["editions"]:
        for edge in ("initial", "final"):
            sample = [r for r in records if (r["edition"], r["bord"]) == (book, edge)]
            values = {}
            for r in sample:
                for letter in "AB":
                    loc, value = r["locus_" + letter], r["unite_" + letter]
                    assert values.setdefault(loc, value) == value
            assert len(values) == 300
            populations = defaultdict(Counter)
            for loc, value in values.items():
                if value:
                    populations[groups[loc]][value] += 1
            for method in sorted({r["parcours"] for r in sample}):
                pairs = [r for r in sample if r["parcours"] == method]
                known = [r for r in pairs if r["unite_A"] and r["unite_B"]]
                observed = sum(r["unite_A"] == r["unite_B"] for r in known)
                expected = 0.
                for r in known:
                    a, b = groups[r["locus_A"]], groups[r["locus_B"]]
                    ca, cb = populations[a], populations[b]
                    ma, mb = sum(ca.values()), sum(cb.values())
                    overlap = sum(n * (cb[v] - (a == b)) for v,n in ca.items())
                    expected += overlap / (ma * (mb - (a == b)))
                stat = results["editions"][book][edge]["resultats"][method]["ensemble"]
                assert (observed, len(known), len(pairs)) == (stat["accords"], stat["lisibles"], stat["paires"])
                assert abs(expected-stat["attendu"]) < .15
                out.append(dict(edition=book, bord=edge, parcours=method, accords=observed,
                                paires_lisibles=len(known), paires=len(pairs), esperance_exacte=round(expected,6)))
    (HERE / "VERIFICATION.json").write_text(json.dumps(out, ensure_ascii=False, indent=1)+"\n")


if __name__ == "__main__":
    main()
