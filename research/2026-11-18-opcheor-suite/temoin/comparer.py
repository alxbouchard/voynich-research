"""Tester les noms latin et allemand d'une même entrée de l'herbier de 1485."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import random
from fractions import Fraction

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "2026-11-18-ordre-des-noms/temoin/NOMS.json"
F89 = ["opcheor", "opcheol"]
F100 = ["okeor", "okeol"]
F96 = ["cpheol", "cpheor"]


def units(word):
    return re.findall(r"c[kptf]h|ch|sh|[a-z]", word)


def extend(pattern, word, key):
    if not pattern:
        if not word:
            yield key
        return
    sign = pattern[0]
    if sign in key:
        value = key[sign]
        if word.startswith(value):
            yield from extend(pattern[1:], word[len(value):], key)
        return
    for width in range(0 if "" not in key.values() else 1, min(len(word), 2) + 1):
        yield from extend(pattern[1:], word[width:], {**key, sign: word[:width]})


def fit(patterns, words, key=None):
    keys = [key or {}]
    for pattern, word in zip(patterns, words, strict=True):
        keys = [result for k in keys for result in extend(units(pattern), word, k)]
    return keys


def project(word, key):
    return "".join(key[sign] for sign in units(word))


def shuffled_titles(entries):
    rng = random.Random(1485107)
    matrices = []
    expectation = Fraction()
    observed = 0
    for view in ("718", "719"):
        pairs = [words for row, words in entries if row["colonne"][:3] == view]
        matrix = [[bool(fit(F89, [lat, ger])) for _, ger in pairs] for lat, _ in pairs]
        matrices.append(matrix)
        expectation += Fraction(sum(sum(row) for row in matrix), len(matrix))
        observed += sum(row[i] for i, row in enumerate(matrix))
    scores = Counter()
    for _ in range(9999):
        total = 0
        for matrix in matrices:
            ids = list(range(len(matrix)))
            rng.shuffle(ids)
            total += sum(row[j] for row, j in zip(matrix, ids, strict=True))
        scores[total] += 1
    return dict(observe=observed, esperance_exacte=str(expectation), histogramme=scores,
                melanges_au_moins_aussi_hauts=sum(n for s, n in scores.items() if s >= observed))


def main():
    records = json.loads(SOURCE.read_bytes())
    entries = [(r, [r["latin"].lower(), (r["allemand"] or "").lower()]) for r in records]
    admitted = [(r, words) for r, words in entries if all(w.isalpha() for w in words)]
    results = []
    for row, words in admitted:
        keys = fit(F89, words)
        if not keys:
            continue
        row_out = {"chapitre": row["chapitre"], "vue": row["colonne"][:3], "noms": words, "tables": keys}
        for label, patterns in (("f100v", F100), ("f96r", F96)):
            matches = []
            for i, key in enumerate(keys):
                for candidate, candidate_words in admitted:
                    newer = fit(patterns, candidate_words, key)
                    if newer:
                        matches.append(dict(table=i, chapitre=candidate["chapitre"], noms=candidate_words, nombre=len(newer)))
            row_out[label] = matches
        if row["chapitre"] == 107:
            extensions = fit([*F89, "shody"], [*words, "costus"])
            row_out["apres_reprise_du_nom"] = dict(tables=extensions,
                                                   sorties=sorted({project("sholdy", k) for k in extensions}),
                                                   sorties_si_tous_signes_distincts=sorted({
                                                       project("sholdy", k) for k in extensions
                                                       if len(set(k.values())) == len(k)}))
        observations = {53: ("betonica", "latine"), 107: ("costus", "grece"),
                        130: ("corallus", "latine")}
        if row["chapitre"] in observations:
            first, second = observations[row["chapitre"]]
            starts = {}
            for spelling in (first, first[1:]):
                augmented = fit([*F89, "shody"], [*words, spelling])
                fourth = sorted({project("sholdy", k) for k in augmented})
                starts[spelling] = {"nombre_tables": len(augmented), "quatriemes": fourth,
                                   "mot_du_temoin": second, "conforme": second in fourth}
            row_out["lecture_avec_ou_sans_initiale_restituee"] = starts
        if row["chapitre"] == 107:
            same = fit([*F89, "shody", *F100], [*words, "costus", *words])
            row_out["suite_f100v_si_meme_rubrique"] = {
                "tables": same, "lecture_dy": sorted({project("dy", k) for k in same}),
                "prose_attendue": "costus"}
        results.append(row_out)
    control_key = {"o":"a","p":"su","ch":"m","e":"i","r":"ra","l":"li","k":"vi"}
    learned = fit(F89, [project(w, control_key) for w in F89])
    extendable = [k for k in learned if fit(F100, [project(w, control_key) for w in F100], k)]
    assert control_key in [key for k in extendable for key in fit(F100, [project(w, control_key) for w in F100], k)]
    assert len(records) == 96
    data = dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                lignes=Counter(row["colonne"][:3] for row, _ in entries),
                entrees_admises=Counter(row["colonne"][:3] for row, _ in admitted),
                resultats=results,
                melanges_des_gloses_dans_chaque_vue=shuffled_titles(admitted),
                controle_artificiel={"clair": [project(w, control_key) for w in F89+F100],
                                     "tables_initiales":len(learned), "tables_initiales_compatibles":len(extendable),
                                     "table_generatrice_retrouvee":True})
    (HERE / "RESULTATS.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
