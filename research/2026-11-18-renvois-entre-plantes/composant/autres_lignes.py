"""Exploration : faire varier la ligne, le rang ou la grande plante opposée."""
from collections import defaultdict
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from croiser import adjacent, corpus, metadata, texts
from encadrements import one_insert


def frames(page, rows, editions):
    ordinals = {}
    for edition in ("H", "ZL"):
        lines = [l for l, (p, k, _, _) in editions[edition].items() if p == page and k == "P0"]
        ordinals[edition] = {l: i + 1 for i, l in enumerate(lines)}
    out = []
    for a, b, c in zip(rows, rows[1:], rows[2:]):
        if a[0] != c[0] or a[0] == b[0] or not adjacent(a, b) or not adjacent(b, c):
            continue
        order = ordinals["H"][a[1]]
        if ordinals["ZL"].get(a[1]) != order or len(set(a[3])) != 1:
            continue
        out.append({"ligne": order, "lieu": a[1], "rang": a[3][0], "mots": [a[0], b[0], c[0]]})
    return out


def compare(a, b, steps):
    hits = []
    for x in a:
        for y in b:
            if x["mots"][1] == y["mots"][1] or not one_insert(x["mots"][0], y["mots"][0]):
                continue
            steps["insertion_et_centres_distincts"] += 1
            if x["ligne"] == y["ligne"]:
                steps["meme_ligne"] += 1
            if x["rang"] == y["rang"]:
                steps["meme_rang"] += 1
            if x["ligne"] == y["ligne"] and x["rang"] == y["rang"]:
                hits.append([x, y])
    return hits


def run():
    paired = json.loads((HERE / "ENCADREMENTS.json").read_text())["paires"]
    pairs = [tuple(r["faces"]) for r in paired]
    pages = texts("plantes", True)
    ed, _ = corpus()
    meta = metadata()
    data = {p: frames(p, pages[p], ed) for p in sorted({p for pair in pairs for p in pair} | {"f18v", "f23r"})}
    pilot = compare(data["f18v"], data["f23r"], defaultdict(int))
    assert any(x["ligne"] == 7 and x["rang"] == 4 for x, _ in pilot)
    pools = defaultdict(list)
    for a, b in pairs:
        pools[meta[a]["Q"], a[-1]].append((a, b))
    result = {}
    for name, comparison in [
        ("conjugues", pairs),
        ("autres_grandes_faces_du_cahier", [(a, d) for pool in pools.values()
          for a, b in pool for _, d in pool if b != d])]:
        rates = defaultdict(int)
        hits = []
        for a, b in comparison:
            hits.extend(compare(data[a], data[b], rates))
        result[name] = {"couples": len(comparison), "avec_encadrement_des_deux_cotes":
                        sum(bool(data[a] and data[b]) for a,b in comparison), "comptes": dict(rates),
                        "meme_ligne_et_rang": hits}
    return {"decouverte": pilot, "comparaisons": result, "encadrements": data}


if __name__ == "__main__":
    (HERE / "AUTRES-LIGNES.json").write_text(json.dumps(run(), ensure_ascii=False, indent=1) + "\n")
