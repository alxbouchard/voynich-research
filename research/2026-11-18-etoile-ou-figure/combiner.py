"""Recombiner séparément deux répertoires d'étiquettes et ouvrir les légendes réservées."""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "2026-11-18-mois-automne/cle"))
from dechiffrer import segment

DATA = ROOT / "voynich_20261028/data"
FILES = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}
ROW = re.compile(r"^<((f(\d+)[rv]\d*)\.\d+),.([A-Za-z0-9]{2})>\s*(.*)$")
PATTERNS = {"ot_edy": ("ot", "edy"), "ote_dy": ("ote", "dy")}


def family(face, leaf, kind):
    if kind == "Ls" and face in ("f68r1", "f68r2"):
        return "etoiles"
    if kind == "Ls" and face in ("f68r3", "f67r2"):
        return face
    if 75 <= leaf <= 84 and kind in ("Ln", "Lt"):
        return "figures" if kind == "Ln" else "objets"
    if kind == "Lf" and 88 <= leaf <= 102:
        return "plantes"
    if kind == "Lz" and 70 <= leaf <= 72:
        return "zodiaque"
    return None


def records(which):
    views = {}
    geometry = {}
    for ed, filename in FILES.items():
        for split in (False, True):
            words = {}
            for line in (DATA / filename).read_text().splitlines():
                match = ROW.match(line)
                if not match:
                    continue
                loc, face, leaf, kind, raw = match.groups()
                category = family(face, int(leaf), kind)
                if category not in which:
                    continue
                geo = (category, face)
                assert geometry.setdefault(loc, geo) == geo
                raw = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)
                raw = raw.replace(",", "." if split else "").strip(".")
                if loc == "f99r.7" and "f99r.6" in words:
                    # Ces deux lignes forment une seule inscription, ici hors apprentissage.
                    words["f99r.6"] = None
                    continue
                words[loc] = raw if re.fullmatch(r"[a-z]+", raw) else None
            views[ed, split] = words
    geometry.pop("f99r.7", None)
    out = {}
    for loc, (category, face) in geometry.items():
        forms = {v.get(loc) for v in views.values()}
        word = forms.pop() if len(forms) == 1 else None
        out[loc] = {"lot": category, "face": face, "mot": word}
    return out


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True)+"\n")


def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def rank(weights):
    return sorted(weights, key=lambda word: (-weights[word], word))


def ends(words, n, start):
    return Counter((s[:n] if start else s[-n:]) for w in words if len(s := tuple(segment(w))) >= n)


def combine(left, right, n, attested):
    a, b = ends(left, n, True), ends(right, 5-n, False)
    weights = {}
    for x,y in product(a,b):
        word = "".join(x+y)
        if tuple(segment(word)) == x+y:
            weights[word] = a[x]*b[y]
    order = rank(weights)
    return {"20": order[:20], "5_inedits": [w for w in order if w not in attested][:5],
            "scores_20": [weights[w] for w in order[:20]]}


def announce():
    pool = records({"etoiles", "figures"})
    lists = {k: [r["mot"] for r in pool.values() if r["lot"] == k and r["mot"]] for k in ("etoiles","figures")}
    star, fig = lists["etoiles"], lists["figures"]
    both = star+fig
    predictions = {}
    for n in (2,3):
        predictions[str(n)] = {method:combine(l,r,n,set(both)) for method,l,r in
                               (("EF",star,fig),("FE",fig,star),("EE",star,star),("FF",fig,fig),("tous",both,both))}
    whole = Counter(w for w in both if len(segment(w)) == 5)
    write("ANNONCES.json", {"modeles":predictions, "entiers":rank(whole)[:20],
          "apprentissage":pool, "sha256":{k:digest(DATA/v) for k,v in FILES.items()}})


def profile(rows):
    valid = [r["mot"] for r in rows if r["mot"]]
    out = {"lieux":len(rows), "lisibles":len(valid)}
    for name, cohort in (("tous",valid),("cinq",[w for w in valid if len(segment(w))==5])):
        out[name] = {"n":len(cohort),"otedy":cohort.count("otedy")}
        for cut,(pre,suf) in PATTERNS.items():
            seen = Counter()
            for w in cohort:
                u = tuple(segment(w))
                a,b = u[:len(pre)]==tuple(pre),u[-len(suf):]==tuple(suf)
                seen["debut"] += a
                seen["fin"] += b
                seen["les_deux"] += a and b
            out[name][cut] = dict(seen)
    return out


def success(words, rows):
    return {w:sorted(loc for loc,r in rows.items() if r["mot"] == w) for w in words}


def verify():
    ann = json.loads((HERE/"ANNONCES.json").read_bytes())
    assert ann["sha256"] == {k:digest(DATA/v) for k,v in FILES.items()}
    rows = records({"etoiles","figures","objets","plantes","zodiaque","f67r2","f68r3"})
    assert all(rows[k]==r for k,r in ann["apprentissage"].items())
    panels = {}
    summary = {}
    for lot in sorted({r["lot"] for r in rows.values()}):
        group = {k:r for k,r in rows.items() if r["lot"]==lot}
        summary[lot] = profile(group.values())
        panels[lot] = {face:profile([r for r in group.values() if r["face"]==face])
                       for face in sorted({r["face"] for r in group.values()})}
    target = {k:r for k,r in rows.items() if r["lot"]=="zodiaque"}
    scores = {n:{method:{panel:success(v[panel],target) for panel in ("20","5_inedits")}
                 for method,v in models.items()} for n,models in ann["modeles"].items()}
    out = {"profils":summary, "par_face":panels,"resultats_modeles":scores,
           "mots_entiers":success(ann["entiers"],target),"releve":rows}
    write("RESULTATS.json",out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["annoncer","verifier"])
    if parser.parse_args().mode=="annoncer":
        announce()
    else:
        verify()
