"""Retrouver les cercles isolés dans les paragraphes et leurs voisins immédiats."""
from collections import Counter
import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / "2026-11-18-opcheor-paralleles/variantes"))
from compter import corpus, runs


def folio(locus):
    m = re.fullmatch(r"f(\d+)([rv])(\d*)\.(\d+)", locus)
    return int(m[1]), m[2], int(m[3] or 0), int(m[4])


def circles(raw, mode):
    result = []
    for run in runs(raw, mode):
        for i, (rank, word) in enumerate(run):
            if word == "o":
                left = run[i-1][1] if i else None
                right = run[i+1][1] if i+1 < len(run) else None
                result.append({"rang":rank, "gauche":left, "droite":right})
    return result


def main():
    eds, _ = corpus()
    loci = sorted(set.intersection(*(set(ed) for ed in eds.values())), key=folio)
    codes = Counter()
    records = []
    for loc in loci:
        if folio(loc)[0] in (88, 99):
            continue
        if not all(ed[loc][1].startswith("P") for ed in eds.values()):
            continue
        codes[eds["ZL"][loc][1]] += 1
        matches = {name+"/"+m: circles(ed[loc][3], m)
                   for name, ed in eds.items() for m in ("joints","separes")}
        if not all(matches.values()):
            continue
        vote = [Counter((i["gauche"],i["droite"]) for i in obs if i["gauche"] and i["droite"])
                for obs in matches.values()]
        shared = vote[0].copy()
        for v in vote[1:]:
            shared &= v
        records.append({"lieu":loc, "codes":{k:ed[loc][1] for k,ed in eds.items()},
                        "lectures":{k:ed[loc][3] for k,ed in eds.items()},
                        "positions":matches, "contextes_communs":[list(t) for t in shared.elements()]})
    both = [r for r in records if r["contextes_communs"]]
    out = {"paragraphes_par_code_ZL":codes, "lignes_avec_o":len(records),
           "lignes_avec_voisins_confirmes":len(both), "premier_avec_voisins":both[0]["lieu"] if both else None,
           "lieux":records}
    (HERE / "releve.json").write_text(json.dumps(out, ensure_ascii=False, indent=1)+"\n")
    print(out["paragraphes_par_code_ZL"], len(records), len(both))
    for r in both:
        print(r["lieu"], r["contextes_communs"], r["positions"])


if __name__ == "__main__":
    main()
