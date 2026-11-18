"""Test the existence of a fixed key even with a choice of neighboring lines."""
import csv
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import sys

from tester import HERE, EDITIONS, collect, read, save, value


def candidates():
    a = read("geometrie/A.json")
    with (HERE / "geometrie/B.csv").open() as f:
        b = list(csv.DictReader(f))
    choices = {dest:{r:set() for r in range(1,35)} for dest in ("mots","prose")}
    for row in a["signes_milieu"]:
        choices["prose"][row["locus"]-15].update(row["corps"]["candidats"])
    for row in a["mots_gauche"]:
        for sign in row["signe"]["candidats"]:
            choices["mots"][sign-15].add(row["locus"])
    for row in b:
        opts = {int(row["nearest"]),int(row["runner_up"])}
        opts.update(int(x) for x in row["nearest_across_models"].split("|"))
        rank = int(row["from_rank"])
        if row["from_column"] == "S" and row["to_column"] == "P":
            choices["prose"][rank].update(x+49 for x in opts)
        if row["from_column"] == "W" and row["to_column"] == "S":
            for sign in opts:
                choices["mots"][sign].add(rank)
    return choices


def compact_witness(rows):
    for size in range(2,len(rows)+1):
        for subset in combinations(rows,size):
            if not set.intersection(*(letters for _,letters in subset)):
                return [{"rang":rank,"initiales":sorted(letters)} for rank,letters in subset]
    return []


def assess(choices, data, ed):
    ledger = {}
    for dest, entries in choices.items():
        rows = []
        constraints = defaultdict(list)
        for rank, options in entries.items():
            sign = value(data,ed,rank+15)
            targets = {loc:value(data,ed,loc) for loc in sorted(options)}
            initials = set(targets.values())
            if sign is None:
                status = "marque indéterminée"
            elif not options:
                status = "sans voisin"
            elif sign in initials:
                status = "copie possible"
            elif None in initials:
                status = "lecture indéterminée"
            else:
                status = "copie incompatible"
            rows.append({"rang":rank,"marque":sign,"initiales_par_locus":targets,"copie":status})
            if options and sign is not None and None not in initials:
                constraints[sign].append((rank,initials))
        counts = defaultdict(int)
        for row in rows:
            if row["rang"]>=23:
                counts[row["copie"]] += 1
        result = {"lignes":rows,"reserve":dict(counts)}
        if dest=="prose":
            keys = {}
            for sign,observations in constraints.items():
                allowed = set.intersection(*(letters for _,letters in observations))
                keys[sign] = {"rangs": [rank for rank,_ in observations],
                              "valeurs_compatibles": sorted(allowed),
                              "temoin_contradiction": compact_witness(observations) if not allowed else []}
            result["contraintes"] = keys
            result["conflits"] = sorted(sign for sign,item in keys.items() if item["temoin_contradiction"])
        ledger[dest] = result
    return ledger


if __name__ == "__main__":
    if len(sys.argv)>1:
        save("INITIALES_ET_MARQUES.json",collect(set(range(1,82)),Path(sys.argv[1])))
    data=read("INITIALES_ET_MARQUES.json")
    sets=candidates()
    save("VOISINS.json",{ed:assess(sets,data,ed) for ed in EDITIONS})
