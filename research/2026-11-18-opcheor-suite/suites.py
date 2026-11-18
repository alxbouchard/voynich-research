"""Tester le troisième mot en conservant les quatre lectures et les bords de ligne."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, segment

EXCLUDED = {88, 89, 96, 100}
DONORS = [("opcheo", "shody"), ("okeo", "dy")]


def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        row = [i]
        for j, y in enumerate(b, 1):
            row.append(min(prev[j] + 1, row[-1] + 1, prev[j - 1] + (x != y)))
        prev = row
    return prev[-1]


def adjacent(a, b):
    return (a["troncon"] == b["troncon"] and
            all(int(y) == int(x) + 1 for x, y in zip(a["rangs_quatre"].split("/"), b["rangs_quatre"].split("/"))))


def windows():
    editions, sections = corpus()
    for loc, (page, kind, *_) in editions["H"].items():
        if kind != "P0" or loc not in editions["ZL"] or editions["ZL"][loc][1] != kind:
            continue
        leaf = int(re.match(r"f(\d+)", page)[1])
        if leaf in EXCLUDED:
            continue
        rows = list(aligned(editions, loc, page, sections[page], leaf, Counter()))
        for i, (a, b) in enumerate(zip(rows, rows[1:])):
            if not adjacent(a, b):
                continue
            c = rows[i + 2] if i + 2 < len(rows) and adjacent(b, rows[i + 2]) else None
            u, v = segment(a["mot"]), segment(b["mot"])
            key = f"{loc}/{a['troncon']}/{a['rang_troncon_IT']}"
            direction = "".join((u[-1], v[-1])) if len(u) >= 3 and u[:-1] == v[:-1] else ""
            yield key, page, a["mot"], b["mot"], c, direction


def announce():
    out = {}
    for key, page, a, b, _, direction in windows():
        if direction not in ("rl", "lr"):
            continue
        base = segment(a)[:-1]
        choices = sorted((distance(base, segment(src)), len(w), w) for src, w in DONORS)
        out[key] = dict(face=page, paire=[a, b], sens=direction, base_en_eo=base[-2:] == ("e", "o"),
                        exact=choices[0][2] if direction == "rl" else "chodar",
                        finale="dy" if direction == "rl" else "ar")
    return out


def edge(row):
    return next((s for s in ("fin", "avant") if s in row["positions"]), "interieur")


def open_words(predictions):
    controls = defaultdict(Counter)
    obs = {}
    for key, page, a, b, c, direction in windows():
        if key in predictions:
            obs[key] = c
        # Le contrôle écarte aussi les paires identiques et celles à toute autre alternance finale.
        if c and segment(a)[:-1] != segment(b)[:-1]:
            controls[page, segment(b)[-1], edge(c)][c["mot"]] += 1
    assert obs.keys() == predictions.keys()
    results = {}
    for key, p in predictions.items():
        c = obs[key]
        detail = {**p, "lu": c["mot"] if c else None}
        if c:
            ctrl = controls[p["face"], segment(p["paire"][1])[-1], edge(c)]
            detail.update(bord=edge(c), temoins=sum(ctrl.values()), exact_temoin=ctrl[p["exact"]],
                          finale_temoin=sum(n for w, n in ctrl.items() if w.endswith(p["finale"])))
        results[key] = detail
    return results


def score(data):
    read = [x for x in data if x["lu"] is not None]
    matched = [x for x in read if x["temoins"]]
    out = dict(paires=len(data), tiers_lisibles=len(read), lieux_temoins=len(matched))
    for k in ["exact", "finale"]:
        def hit(x):
            return x["lu"] == x[k] if k == "exact" else x["lu"].endswith(x[k])
        out[k] = {"reussites": sum(map(hit, read)), "reussites_avec_temoins": sum(map(hit, matched)),
                  "attendues_aux_lieux_avec_temoins": sum(x[k + "_temoin"] / x["temoins"] for x in matched)}
    return out


def main(mode):
    file = HERE / "ANNONCES.json"
    if mode == "annoncer":
        out = announce()
    else:
        pred = json.loads(file.read_bytes())
        assert pred == announce()
        opened = open_words(pred)
        out = {"lieux": opened, "bilan": {}}
        for direction in ("rl", "lr"):
            for group in ("tout", "eo"):
                rows = [x for x in opened.values() if x["sens"] == direction and (group == "tout" or x["base_en_eo"])]
                out["bilan"][direction + "/" + group] = score(rows)
        file = HERE / "OUVERTURE.json"
    file.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["annoncer", "ouvrir"])
    main(parser.parse_args().mode)
