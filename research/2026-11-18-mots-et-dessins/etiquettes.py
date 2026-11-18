"""Associer les mots entiers aux types d'objets en gardant les feuillets de contrôle à part."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "voynich_20261028/data"
FILES = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}
SETS = {
    "Ls": ("La", [67], [68]),
    "Ln": ("Lt", [75, 77, 78], [82, 83, 84]),
    "Lf": ("Lc", [88, 89], [99, 100, 101, 102]),
}
ROW = re.compile(r"^<((f(\d+)[rv]\d*)\.([^,>]+)),([^!])([A-Za-z0-9]{2})>\s*(.*)")
VALID_TYPES = {kind for target, (control, _, _) in SETS.items() for kind in (target, control)}


def parse(path, leaves, split_uncertain):
    out = {}
    for line in path.read_text().splitlines():
        match = ROW.match(line)
        if not match:
            continue
        key, face, leaf, _, _, kind, raw = match.groups()
        if int(leaf) not in leaves or kind not in VALID_TYPES:
            continue
        cleaned = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)
        cleaned = re.sub(r"<[-~]>", ".", cleaned).strip().replace(",", "." if split_uncertain else "")
        fields = [w for w in cleaned.split(".") if w]
        words = fields if fields and all(re.fullmatch(r"[a-z]+", w) for w in fields) else None
        assert key not in out, key
        out[key] = (face, int(leaf), kind, words)
    return out


def corpus(edition, leaves, split):
    tables = {name: parse(DATA / filename, leaves, split) for name, filename in FILES.items()}
    if edition in FILES:
        return tables[edition]
    h, z = tables["H"], tables["ZL"]
    merged = {}
    for key in h.keys() | z.keys():
        face, leaf, kind, _ = h.get(key) or z[key]
        if key in h and key in z:
            assert h[key][:3] == z[key][:3], key
        merged[key] = (face, leaf, kind, h[key][3] if key in h and h[key] == z.get(key) else None)
    return merged


def subset(table, kind, control, leaves):
    pages = {face for face, leaf, k, _ in table.values() if k == kind and leaf in leaves}
    peers = {face for face, leaf, k, _ in table.values() if k == control and leaf in leaves}
    subsets = {}
    for name, target, allowed in [("cible", kind, pages), ("temoin", control, pages & peers),
                                  ("cible_faces_mixtes", kind, pages & peers)]:
        subsets[name] = {key: row for key, row in table.items() if row[0] in allowed and row[2] == target}
    return subsets


def forms(rows):
    counts = Counter()
    leaves = defaultdict(set)
    for _, leaf, _, words in rows.values():
        for w in set(words or []):
            counts[w] += 1
            leaves[w].add(leaf)
    return counts, leaves


def learn(subsets):
    pos, leaves = forms(subsets["cible"])
    neg, _ = forms(subsets["temoin"])
    ranks = {w: (len(leaves[w]), count, -neg[w]) for w, count in pos.items() if count >= 2}
    best = max(ranks.values(), default=None)
    ties = sorted(w for w, v in ranks.items() if v == best)
    return {"mot": ties[0] if ties else None, "ex_aequo": ties, "rang": list(best) if best else None}


def score(rows, word):
    hits = sorted(key for key, row in rows.items() if row[3] and word in row[3])
    return {"total": len(rows), "lisibles": sum(bool(row[3]) for row in rows.values()),
            "touches": len(hits), "lieux": hits}


def ceiling(rows):
    counts, _ = forms(rows)
    best = max(counts.values(), default=0)
    return {"maximum": best, "mots": sorted(w for w, n in counts.items() if n == best),
            "lisibles": sum(bool(row[3]) for row in rows.values()), "total": len(rows)}


def run(mode):
    prereg = HERE / "PREDICTIONS.json"
    frozen = json.loads(prereg.read_text()) if mode == "verifier" else {}
    out = {}
    for edition in ["accord", *FILES]:
        for split in [False, True]:
            condition = edition + ("_separe" if split else "_joint")
            out[condition] = {}
            for kind, (control, training, heldout) in SETS.items():
                train = corpus(edition, training, split)
                a = subset(train, kind, control, training)
                candidate = learn(a)
                if mode == "apprendre":
                    out[condition][kind] = candidate
                    continue
                assert candidate == frozen[condition][kind]
                reserve = corpus(edition, heldout, split)
                b = subset(reserve, kind, control, heldout)
                total = dict(a["cible"], **b["cible"])
                word = candidate["mot"]
                out[condition][kind] = {
                    **candidate, "apprentissage": {k: score(v, word) for k, v in a.items()},
                    "reserve": {k: score(v, word) for k, v in b.items()},
                    "reserve_ex_aequo": {w: {k: score(v, w) for k, v in b.items()} for w in candidate["ex_aequo"]},
                    "maximum_tous_feuillets": ceiling(total),
                }
    target = prereg if mode == "apprendre" else HERE / "RESULTATS.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["apprendre", "verifier"])
    parser.add_argument("--donnees", type=Path, default=DATA, help="Dossier des deux fichiers IVTFF")
    args = parser.parse_args()
    DATA = args.donnees
    run(args.mode)
