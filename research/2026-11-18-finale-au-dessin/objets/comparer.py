"""Comparer deux légendes d'une même face après apprentissage sur d'autres feuillets."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from random import Random
from statistics import mean
import json
import re

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
INVENTORY = RESEARCH / "2026-11-18-deux-legendes-botaniques/lecture/tucker/prefixe/resultats.json"
MACER = RESEARCH / "2026-11-18-opcheor-paralleles/latin/corpus.json"
SIGNS = re.compile(r"c[kptf]h|ch|sh|[a-z]")
TRIALS = 1999


def folio(face):
    return re.match(r"^f[0-9]+", face).group()


def feature(word, grouped):
    signs = tuple(SIGNS.findall(word))
    assert "".join(signs) == word
    return ("radical", signs[:-1]) if grouped and len(signs) >= 3 else ("entier", signs)


def classes():
    inventory = json.loads(INVENTORY.read_text())
    rows = dict(inventory["par_code"])
    rows["Ln"] = inventory["Ln_un_locus_par_ligne_sans_reunir_les_paires_de_f75v"]
    return {kind: row["mots_par_locus"] for kind, row in rows.items()}


def ceilings(records):
    count = Counter(records.values())
    best = max(count.values())
    return {
        "inscriptions": len(records), "formes": len(count),
        "feuillets": sorted({folio(loc) for loc in records}),
        "maximum": best, "mots_et_lieux": {
            w: sorted(loc for loc, value in records.items() if value == w)
            for w in sorted(count) if count[w] == best
        },
    }


def mixed(records, a, b, grouped):
    faces = defaultdict(lambda: [[], []])
    for side, kind in enumerate((a, b)):
        for locus, word in sorted(records[kind].items()):
            faces[locus.split(".")[0]][side].append(feature(word, grouped))
    return {face: groups for face, groups in sorted(faces.items()) if all(groups)}


def compare(faces):
    totals = [Counter(), Counter()]
    per_folio = defaultdict(lambda: [Counter(), Counter()])
    for face, groups in faces.items():
        for i, words in enumerate(groups):
            totals[i].update(words)
            per_folio[folio(face)][i].update(words)
    if len(per_folio) < 2:
        raise ValueError("Deux feuillets mixtes sont nécessaires")
    metrics, detail = defaultdict(list), {}
    for page, held in per_folio.items():
        train = [total - omit for total, omit in zip(totals, held)]
        na, nb = [sum(c.values()) for c in train]
        for face, (first, second) in faces.items():
            if folio(face) != page:
                continue
            score = {w: train[0][w]*nb - train[1][w]*na for w in set(first + second)}
            counts = Counter((score[a] > score[b]) - (score[a] < score[b])
                             for a in first for b in second)
            auc = Fraction(2*counts[1] + counts[0], 2*sum(counts.values()))
            metrics[page].append(auc)
            detail[face] = {"n": [len(first), len(second)], "apprentissage": [na, nb],
                            "justes": counts[1], "erreurs": counts[-1], "egalites": counts[0],
                            "score": float(auc)}
    return mean(mean(v) for v in metrics.values()), detail


def evaluate(faces):
    obs, details = compare(faces)
    rng = Random(20261118)
    upper = 0
    for _ in range(TRIALS):
        scrambled = {}
        for face, (first, second) in faces.items():
            items = first + second
            rng.shuffle(items)
            scrambled[face] = [items[:len(first)], items[len(first):]]
        upper += compare(scrambled)[0] >= obs
    return {"faces": details, "score": float(obs), "score_exact": str(obs),
            "feuillets": len({folio(p) for p in faces}), "tirages": TRIALS,
            "au_moins_aussi_haut": upper, "p": (upper+1)/(TRIALS+1)}


def historical():
    chapters = json.loads(MACER.read_text())
    words = {
        "radix": "radix radicis radici radicem radice radices radicum radicibus",
        "herba": "herba herbae herbam herbarum herbis herbas",
    }
    results = {}
    for lemma, paradigm in words.items():
        forms = set(paradigm.split())
        windows = {"titre": {}, "debut": {}, "entier": {}}
        for title, body in chapters.items():
            for label, content in [("titre", re.findall(r"[a-z]+", title.lower())),
                                   ("debut", body[:24]), ("entier", body)]:
                windows[label][title] = {w: n for w, n in Counter(content).items() if w in forms}
        results[lemma] = {label: {"notices": sum(map(bool, hits.values())),
                                  "occurrences": sum(sum(row.values()) for row in hits.values()),
                                  "releve": hits} for label, hits in windows.items()}
    # Vérification ajoutée après le calcul fixé : -que peut être soudé au nom latin.
    with_que = {}
    for lemma, paradigm in words.items():
        forms = set(paradigm.split())
        suffixed = {form + "que" for form in forms}
        hits = {title: [w for w in body if w in suffixed]
                for title, body in chapters.items()}
        extra_titles = [t for t, row in hits.items() if row and not results[lemma]["entier"]["releve"][t]]
        with_que[lemma] = {"occurrences_ajoutees": {t: v for t, v in hits.items() if v},
                           "notices_supplementaires": extra_titles}
    return {"sensibilite_que": with_que, "total_notices": len(chapters), "total_mots": sum(map(len, chapters.values())),
            "debut_mots": sum(min(24, len(row)) for row in chapters.values()),
            "formes": words, "par_lemme": results}


def main():
    for grouped in (False, True):
        f = lambda s: feature(s, grouped)
        demo = {"f1r": [[f("abc")], [f("def")]], "f2r": [[f("abc")], [f("def")]]}
        assert compare(demo)[0] == 1
        demo["f2r"] = [[f("def")], [f("abc")]]
        assert compare(demo)[0] == 0
        assert compare({p: [[f("abc")], [f("abc")]] for p in demo})[0] == Fraction(1, 2)
    rows = classes()
    tests = {}
    for first, second in [("Lf", "Lc"), ("Ln", "Lt")]:
        for name, grouped in [("mot", False), ("finale", True)]:
            tests[f"{first}-{second}-{name}"] = evaluate(mixed(rows, first, second, grouped))
    ordered = sorted(tests.values(), key=lambda t: t["p"])
    lower = 0
    for index, test in enumerate(ordered):
        lower = max(lower, min(1, (len(ordered)-index)*test["p"]))
        test["p_holm"] = lower
    result = {"empreintes_entrees": {p.name + ":" + p.parent.name: sha256(p.read_bytes()).hexdigest()
                                     for p in (INVENTORY, MACER)},
              "maxima": {k: ceilings(v) for k, v in rows.items()},
              "epreuves": tests, "macer": historical()}
    (HERE / "RESULTATS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for k, t in tests.items():
        print(k, {key: val for key, val in t.items() if key != "faces"},
              {s: sum(x[s] for x in t["faces"].values()) for s in ("justes", "erreurs", "egalites")})
    for k, t in result["maxima"].items():
        print(k, t["maximum"], t["inscriptions"], sorted(t["mots_et_lieux"]), t["feuillets"])
    for k, t in result["macer"]["par_lemme"].items():
        print(k, {a: (v["notices"], v["occurrences"]) for a, v in t.items()})


if __name__ == "__main__":
    main()
