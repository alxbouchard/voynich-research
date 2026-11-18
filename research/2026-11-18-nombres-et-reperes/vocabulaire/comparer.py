"""Tester l'hypothèse de désignations fixes sans reconstruire un ordre des figures."""
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_20261028" / "data"
PANELS = {"Poissons": ["f70v2"], "Bélier": ["f70v1", "f71r"], "Taureau": ["f71v", "f72r1"],
          "Gémeaux": ["f72r2"], "Cancer": ["f72r3"], "Lion": ["f72v3"], "Vierge": ["f72v2"],
          "Balance": ["f72v1"], "Scorpion": ["f73r"], "Sagittaire": ["f73v"]}
SIGN = {p: s for s, pp in PANELS.items() for p in pp}
LABEL = re.compile(r"^<([^.]+)\.(\d+),([@&])Lz>\s*(.*)")
UNIT = re.compile(r"(?:@\d{3};|c[kptf]h|ch|sh|[a-z?])'*")
DIGITS = ("o", "r", "y", "e", "@140;")


def parse(path, split):
    rows = defaultdict(list)
    for line in path.read_text().splitlines():
        m = LABEL.match(line)
        if not m:
            continue
        panel, n, _, raw = m.groups()
        plain = re.sub(r"<![^>]*>|!", "", raw).replace(",", "." if split else "")
        alternatives = re.split(r"(\[[^\[\]]*\])", plain)
        choices = [a[1:-1].split(":") if a.startswith("[") else [a] for a in alternatives]
        variants = set()
        for parts in product(*choices):
            words = "".join(parts).replace("{", "").replace("}", "").split(".")
            variant = tuple(tuple(UNIT.findall(w)) for w in words if w)
            assert ["".join(g) for g in variant] == [w for w in words if w], (raw, words)
            variants.add(variant)
        rows[SIGN[panel]].append((f"{panel}.{n}", variants))
    assert [len(rows[s]) for s in PANELS] == [30, 30, 30, 29, 30, 30, 30, 30, 30, 30]
    return rows


def project(variant, mode):
    if mode == "entier":
        return ".".join("".join(w) for w in variant)
    flat = tuple(u for w in variant for u in w)
    units = flat[:2] if mode == "debut2" else flat[-2:]
    return " ".join(units)


def known_form(variants, mode):
    forms = {project(v, mode) for v in variants}
    if len(forms) == 1:
        value = forms.pop()
        if "?" not in value:
            return value
    return None


def overlaps(rows, mode):
    known, missing = {}, {}
    for sign, labels in rows.items():
        counts = Counter(known_form(v, mode) for _, v in labels)
        missing[sign] = counts.pop(None, 0)
        known[sign] = counts
    pairs = []
    for a, b in combinations(PANELS, 2):
        common = sum((known[a] & known[b]).values())
        na, nb = len(rows[a]), len(rows[b])
        upper = min(na, nb, common + missing[a] + missing[b])
        upper30 = min(30, common + missing[a] + missing[b] + 60 - na - nb)
        pairs.append([a, b, common, upper, upper30])
    best = max(row[2] for row in pairs)
    examples = []
    for a, b, count, _, _ in pairs:
        if count != best:
            continue
        common_forms = sorted((known[a] & known[b]).keys())
        examples.append({"signes": [a, b], "lieux": {
            form: {s: [loc for loc, variants in rows[s] if known_form(variants, mode) == form]
                   for s in (a, b)} for form in common_forms}})
    return {"incertains": missing, "intersection_dix": reduce(Counter.__and__, known.values()),
            "paires_observees_plafond_loci_plafond_sur30": pairs,
            "meilleures_paires_formes_et_lieux": examples,
            "plafond_commun_10_sur30": min(row[-1] for row in pairs)}


def values(variant, field):
    if field == "entier":
        return {project(variant, "entier")}
    if field == "mot":
        return {"".join(w) for w in variant}
    return {variant[0][0] if field == "initial" else variant[-1][-1]}


def match_count(edges):
    # At most five signs. Each label may be used once.
    masks = {0}
    for allowed in edges:
        masks.update(mask | bit for mask in tuple(masks) for bit in allowed if not mask & bit)
    return max(x.bit_count() for x in masks)


def digit_coverage(labels, field, digits):
    edges, relaxed = [], []
    hits = defaultdict(list)
    for loc, variants in labels:
        read = [values(v, field) for v in variants]
        stable = set.intersection(*read)
        allowed = set.union(*read)
        wildcard = any("?" in x for x in allowed)
        edges.append([1 << i for i, d in enumerate(digits) if d in stable])
        relaxed.append([1 << i for i, d in enumerate(digits) if d in allowed or wildcard])
        for d in digits:
            if d in stable:
                hits[d].append(loc)
    return {"certain": match_count(edges), "optimiste_loci": match_count(relaxed),
            "optimiste_sur30": match_count(relaxed + [list(1 << i for i in range(len(digits)))] * (30-len(labels))),
            "lieux_certains": dict(hits)}


def word_usage(rows):
    by_sign = {}
    for sign, labels in rows.items():
        counts = Counter()
        for _, variants in labels:
            certain = set.intersection(*(values(v, "mot") for v in variants))
            counts.update(w for w in certain if "?" not in w)
        by_sign[sign] = counts
    total = sum(by_sign.values(), Counter())
    train = sum((by_sign[s] for s in list(PANELS)[:7]), Counter())
    top = [w for w in train if train[w] == max(train.values())]
    return {"max_299": sorted(total.items(), key=lambda t: (-t[1], t[0]))[:10], "mots_en_commun_10": sorted(reduce(set.intersection, map(set, by_sign.values()))),
            "plus_frequents_7_et_nombre_par_signe": {w: {s: counts[w] for s, counts in by_sign.items()} for w in sorted(top)}}


def measure(rows):
    result = {}
    for key, rr in [("tous", rows), ("sans_centre_poissons", {s:[r for r in li if r[0] != "f70v2.33"] for s, li in rows.items()})]:
        result[key] = {"vocabulaire": {mode: overlaps(rr, mode) for mode in ("entier", "debut2", "fin2")},
                       "numeraux": {field: {str(n): {s: digit_coverage(labels, field, DIGITS[:n]) for s, labels in rr.items()}
                                           for n in (4, 5)} for field in ("entier", "mot", "initial", "final")}}
    result["mots_visibles"] = word_usage(rows)
    return result


def calibrate():
    roman = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]
    result = {}
    for system in ("decimal", "romain_soustractif"):
        series = [str(i) if system == "decimal" else "x" * (i // 10) + roman[i % 10] for i in range(1, 31)]
        # Same forms with an independent, arbitrary rearrangement in each sign.
        tables = {s: [(str(j), {(tuple(series[(j * 7 + k) % 30]),)}) for j in range(30)]
                  for k, s in enumerate(PANELS)}
        score = overlaps(tables, "entier")
        result[system] = {"numeraux": series, "intersection_des_10": sum(score["intersection_dix"].values()),
                          "minimum_des_45_paires": min(row[2] for row in score["paires_observees_plafond_loci_plafond_sur30"])}
        assert result[system]["minimum_des_45_paires"] == result[system]["intersection_des_10"] == 30
    return result


def main():
    output = {"calibration": calibrate(), "panneaux": PANELS, "empreintes": {}, "lectures": {}}
    for short, name in [("H", "IT2a-n.txt"), ("ZL", "ZL3b-n.txt")]:
        path = DATA / name
        output["empreintes"][short] = hashlib.sha256(path.read_bytes()).hexdigest()
        for split in (False, True):
            output["lectures"][short + ("_separe" if split else "_joint")] = measure(parse(path, split))
    (HERE / "resultats.json").write_text(json.dumps(output, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
