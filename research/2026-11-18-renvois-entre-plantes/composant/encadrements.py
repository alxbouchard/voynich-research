"""Retrouver sur de nouvelles faces les répétitions des deux grandes plantes."""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from croiser import adjacent, corpus, leaf, loc, metadata, segment, texts
from corpus_dam import parse


def events(pages, editions):
    result = {}
    for page, rows in sorted(pages.items()):
        if not rows or leaf(page) in {18, 23}:
            continue
        for i, (a, b) in enumerate(zip(rows, rows[1:])):
            if b[0] != "dar" or not adjacent(a, b):
                continue
            letters = segment(a[0])
            if len(letters) < 4 or a[0] == "dar":
                continue
            c = rows[i + 2] if i + 2 < len(rows) and adjacent(b, rows[i + 2]) else None
            position = None
            if c:
                _, parts = parse(editions["H"][c[1]][3], "joints")
                position = "fin" if c[3][0] == sum(map(len, parts)) else "interieur"
            key = f"{b[1]}/{b[3][0]}"
            result[key] = {"ancre": a[0], "q_ol": letters[0] == "q" and letters[-2:] == ("o", "l"),
                           "page": page, "lu": c[0] if c else None, "position": position}
    return result


def scores(rows):
    groups = defaultdict(list)
    for r in rows:
        if r["lu"]:
            groups[r["page"], r["position"]].append((r["ancre"], r["lu"]))
    expectation = Fraction()
    variable = 0
    for group in groups.values():
        left, right = map(Counter, zip(*group))
        expectation += Fraction(sum(n * right[w] for w, n in left.items()), len(group))
        if len(left) > 1 and len(right) > 1 and left.keys() & right.keys():
            variable += len(group)
    return {"annonces": len(rows), "lisibles": sum(map(len, groups.values())),
            "exacts": sum(r["lu"] == r["ancre"] for r in rows), "esperance": str(expectation),
            "positions_dans_des_groupes_variables": variable}


def seven(page, editions, rows):
    seventh = []
    for ed in ("H", "ZL"):
        lines = [l for l, (p, kind, _, _) in editions[ed].items() if p == page and kind == "P0"]
        seventh.append(lines[6] if len(lines) >= 7 else None)
    if not seventh[0] or seventh[0] != seventh[1]:
        return {"septiemes": seventh, "triplets": 0, "repetitions": []}
    window = [r for r in rows if r[1] == seventh[0]]
    count = 0
    frames = []
    for a, b, c in zip(window, window[1:], window[2:]):
        if adjacent(a, b) and adjacent(b, c):
            count += 1
            if a[0] == c[0] and a[0] != b[0]:
                frames.append({"lieu": loc(a), "exterieur": a[0], "milieu": b[0]})
    return {"septiemes": seventh, "triplets": count, "repetitions": frames}


def one_insert(a, b):
    x, y = sorted((segment(a), segment(b)), key=len)
    return len(y) == len(x) + 1 and any(y[:i] + y[i + 1:] == x for i in range(len(y)))


def run():
    assert one_insert("qokol", "qokchol") and not one_insert("qokol", "qoksholx")
    pages = texts("tout", True)
    editions, _ = corpus()
    e = events(pages, editions)
    subsets = {"exact": [r for r in e.values() if r["ancre"] == "qokchol"],
               "q_ol": [r for r in e.values() if r["q_ol"]], "tous": list(e.values())}
    scores_by_anchor = {k: scores(v) for k, v in subsets.items()}
    scores_by_anchor["exact"]["qokol_ou_qokchol"] = sum(r["lu"] in ("qokol", "qokchol") for r in subsets["exact"])

    meta = metadata()
    bifolia = defaultdict(set)
    for page, attrs in meta.items():
        if attrs.get("Q") in tuple("ABCDEFGH") and attrs.get("B"):
            bifolia[attrs["Q"], attrs["B"]].add(leaf(page))
    lines = {}
    pairs = []
    for leaves in sorted(bifolia.values(), key=min):
        if len(leaves) != 2 or leaves & {18, 23}:
            continue
        low, high = sorted(leaves)
        for a, b in [(f"f{low}r", f"f{high}v"), (f"f{low}v", f"f{high}r")]:
            if any(meta.get(p, {}).get("I") != "H" for p in (a, b)):
                continue
            for p in (a, b):
                lines[p] = seven(p, editions, pages[p])
            hits = [[x, y] for x in lines[a]["repetitions"] for y in lines[b]["repetitions"]
                    if one_insert(x["exterieur"], y["exterieur"])]
            pairs.append({"faces": [a, b], "evaluables": bool(lines[a]["triplets"] and lines[b]["triplets"]),
                          "repetition_sur_les_deux": bool(lines[a]["repetitions"] and lines[b]["repetitions"]),
                          "insertion": hits})
    # Les grandes faces dont le feuillet conjugué est absent comptent dans le relevé par face.
    for p, m in sorted(meta.items()):
        if m.get("Q") in tuple("ABCDEFGH") and m.get("I") == "H" and leaf(p) not in {18, 23}:
            if p not in lines:
                lines[p] = seven(p, editions, pages[p])
    pilot = {p: seven(p, editions, pages[p]) for p in ("f18v", "f23r")}
    assert all(pilot[p]["repetitions"] for p in pilot)
    return {"apres_dar": e, "scores": scores_by_anchor, "pilote": pilot, "lignes": lines, "paires": pairs}


if __name__ == "__main__":
    (HERE / "ENCADREMENTS.json").write_text(json.dumps(run(), ensure_ascii=False, indent=1) + "\n")
