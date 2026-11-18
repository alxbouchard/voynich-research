"""Compte les formes EVA de l'épreuve des luminaires, sans suppléer un signe inconnu."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path
import re

DIR = Path(__file__).resolve().parent
DATA = DIR.parents[2] / "voynich_20261028" / "data"
FILES = {"ZL3b": "ZL3b-n.txt", "IT2a": "IT2a-n.txt"}
ZONES = {"f68r1.5": "soleil", "f68r1.6": "soleil", "f68r1.7": "soleil",
         "f68r1.37": "lune", "f68r2.6": "lune", "f68r2.31": "soleil"}
TARGETS = (("ytoa", True), ("ytoaiin", False), ("ytoar", False))
ROW = re.compile(r"^<([^,>]+)\.([0-9]+),.(\w+)>\s*(.*)$")
CATEGORIES = {"L": "legendes_L", "P": "paragraphes_P", "R": "radial_R", "C": "circulaire_C"}


def split_slots(body, split):
    body = re.sub(r"<[-~]>", ".", body)
    body = re.sub(r"<![^>]*>|<@[^>]*>|<[%$]>", "", body)
    assert not any(c in body for c in "<>/ ")
    return [s for s in body.replace(",", "." if split else "").split(".") if s]


@lru_cache(maxsize=None)
def readings(slot):
    # Each encoded high-ASCII sign is one distinct sign; the basic-EVA experiment
    # cannot assign it the identity of a basic glyph, or treat it as a demonstrated mismatch.
    value = re.sub(r"@\d{3};", "§", slot).replace("{", "").replace("}", "")
    parts = re.split(r"(\[[^\[\]]*\])", value)
    choices = [part[1:-1].split(":") if part.startswith("[") else [part] for part in parts]
    assert all(not any(c in val for c in ":[]") for choice in choices for val in choice)
    return tuple(sorted(set("".join(seq) for seq in product(*choices))))


def known(c):
    return 'a' <= c <= 'z'


def match_one(reading, pattern, prefix):
    for i, c in enumerate(reading):
        if i == len(pattern):
            return "oui" if prefix else "non"
        if not known(c):
            return "indetermine"
        if c != pattern[i]:
            return "non"
    return "oui" if len(reading) == len(pattern) else "non"


@lru_cache(maxsize=None)
def slot_result(slot):
    variants = readings(slot)
    fields = {}
    for k, parts in (("initiale", {v[:1] for v in variants}), ("debut_4", {v[:4] for v in variants}),
                     ("mot_entier", set(variants))):
        fields[k + "_eva_lisible"] = int(len(parts) == 1 and all(s and all(map(known, s)) for s in parts))
    for pat, prefix in TARGETS:
        states = {match_one(v, pat, prefix) for v in variants}
        fields[pat] = next(iter(states)) if len(states) == 1 else "indetermine"
    return fields


def new_counts():
    return Counter(loci=0, slots=0, initiale_eva_lisible=0, debut_4_eva_lisible=0, mot_entier_eva_lisible=0,
                   **{f"{p}_{v}": 0 for p,_ in TARGETS for v in ("oui", "non", "indetermine")})


def summarize(path, split):
    groups = defaultdict(new_counts)
    focus, hits, unknown_focus, f2r_all = [], [], [], []
    n_parsed = 0
    for line in path.read_text().splitlines():
        if not re.match(r"^<[^>,]+,[^>]+>", line):
            continue
        m = ROW.match(line)
        if not m:
            raise ValueError(line)
        n_parsed += 1
        panel, num, typ, body = m.groups()
        locus = f"{panel}.{num}"
        slots = split_slots(body, split)
        assert slots
        categories = ["manuscrit", "manuscrit/" + CATEGORIES[typ[0]]]
        if panel == "f2r":
            f2r_all.append(locus)
        if panel in ("f68r1", "f68r2"):
            zone = ZONES.get(locus)
            categories.extend([panel, f"{panel}/" + (zone or "reste"),
                               "deux_panneaux/" + ("luminaires" if zone else "reste")])
            if zone:
                categories.append("luminaires/" + zone)
            else:
                categories.append(f"{panel}/reste/{typ}")
        if locus in ZONES or locus == "f2r.14":
            focus.append({"locus": locus, "type": typ, "texte": body, "groupes": slots})
        for cat in categories:
            groups[cat]["loci"] += 1
        for position,slot in enumerate(slots, 1):
            result = slot_result(slot)
            if result["ytoa"] == "oui":
                hits.append({"locus": locus, "type": typ, "rang": position, "groupe": slot})
            if locus in ZONES and any(result[p] == "indetermine" for p, _ in TARGETS):
                unknown_focus.append({"locus": locus, "rang": position, "groupe": slot,
                                      "etats": {p: result[p] for p, _ in TARGETS}})
            for cat in categories:
                cnt = groups[cat]
                cnt["slots"] += 1
                for key, val in result.items():
                    if isinstance(val, int):
                        cnt[key] += val
                    else:
                        cnt[f"{key}_{val}"] += 1
    assert n_parsed == groups["manuscrit"]["loci"]
    for cnt in groups.values():
        cnt["initiale_eva_non_resolue"] = cnt["slots"] - cnt["initiale_eva_lisible"]
        cnt["debut_4_eva_non_resolu"] = cnt["slots"] - cnt["debut_4_eva_lisible"]
        for p, _ in TARGETS:
            assert sum(cnt[f"{p}_{s}"] for s in ("oui", "non", "indetermine")) == cnt["slots"]
    assert len(hits) == groups["manuscrit"]["ytoa_oui"]
    for k in groups["manuscrit"]:
        assert groups["manuscrit"][k] == sum(groups["manuscrit/" + v][k] for v in CATEGORIES.values())
    return {"groupes": dict(groups), "occurrences_confirmees": hits,
            "loci_verifies": focus, "possibilites_non_resolues_dans_les_luminaires": unknown_focus,
            "tous_les_loci_f2r": f2r_all}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--donnees", type=Path, default=DATA)
    args = parser.parse_args()
    results = {}
    for edition, filename in FILES.items():
        path = args.donnees / filename
        cases = {mode: summarize(path, mode == "separe") for mode in ("joint", "separe")}
        results[edition] = {"fichier": filename, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "entete": path.read_text().splitlines()[:3], "modes": cases}
    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
