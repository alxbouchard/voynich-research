"""Freeze pairs from actual fragment inscriptions without processing any prose."""
import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-noms-secteurs"))
from secteurs import ALG, DATA, ROW, slots

EDITIONS = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}
GEOMETRY = HERE / "rangees/rangees.tsv"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def listed(value):
    return [int(n) for n in value.split(",") if n]


def load_labels(path):
    labels = {}
    for line in path.read_text().splitlines():
        header = line.partition(">")[0]
        if not header.endswith(("Lf", "Lc")):
            continue
        match = ROW.fullmatch(line)
        if match:
            labels[match[1], int(match[2])] = match[3]
    return labels


def forms(table, page, ids, split):
    if not all((page,n) in table for n in ids):
        return []
    words = [w for _,w in slots(table, page, ids, split, "strict")]
    return words if words and all(words) else []


def word_pairs(objects):
    return {tuple(sorted((a,b))) for left,right in itertools.combinations(objects,2)
            for a in left for b in right if a != b}


def predict(tables, layout, edition, split, broad):
    rows = {}
    for row in layout:
        page = row["page"]
        objects = {}
        for item in row["fragments"].split(","):
            ids = [int(n) for n in item.split("+")]
            by_ed = {ed: forms(t,page,ids,split) for ed,t in tables.items()}
            if edition == "accord":
                words = by_ed["H"] if by_ed["H"] == by_ed["ZL"] else []
            else:
                words = by_ed[edition]
            if not broad and (len(words) != 1 or len(ALG["EVA"].findall(words[0])) < 3):
                words = []
            objects[page+"."+item] = words
        key = page + "/" + row["rang"]
        assert key not in rows
        rows[key] = {"page": page, "pots": listed(row["pots"]), "objets": objects,
                     "prose": listed(row["prose"]), "paires": sorted(word_pairs(objects.values()))}
    return rows


def main(extended):
    geom = HERE/"rangees/pots_elargis.tsv" if extended else GEOMETRY
    with geom.open() as stream:
        layout = list(csv.DictReader(stream, delimiter="\t"))
    tables = {ed: load_labels(DATA/f) for ed,f in EDITIONS.items()}
    out = {"geometrie_sha256": sha(geom), "ivtff_sha256": {ed: sha(DATA/f) for ed,f in EDITIONS.items()},
           "paire_pot_fragment": ["okol","otoldy"], "conditions": {}}
    for ed,split,broad in itertools.product(("accord","H","ZL"), (False,True),(False,True)):
        name = "/".join((ed, "separe" if split else "joint","elargi" if broad else "strict"))
        out["conditions"][name] = predict(tables,layout,ed,split,broad)
    filename = "predictions_pots_elargis.json" if extended else "predictions.json"
    (HERE/filename).write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")


if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--pots-elargis", action="store_true")
    main(args.parse_args().pots_elargis)
