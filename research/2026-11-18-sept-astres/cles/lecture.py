"""Global keys and one-to-one slot assignments for the two seven-label panels."""
import hashlib
import itertools
import json
import random
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parents[1] / "2026-11-18-secteurs-rouges"))
from tables import MODELS, groups, merge, normalize, options, spans

FOLIOS = {"f67r2": (15, 22, 28, 31, 34, 37, 47), "f72r3": (29, 32, 33, 27, 31, 30, 28)}
PLANETS = ("saturnus", "iupiter", "venus", "mercurius", "sol", "luna", "mars")
PUBLISHED = tuple(range(7))
SWAPPED = (0, 1, 2, 3, 5, 4, 6)
ALL = tuple(itertools.permutations(range(7)))


def extract():
    raw, digests = {}, {}
    for edition in ("IT2a-n", "ZL3b-n"):
        path = ROOT / "voynich_20261028/data" / (edition + ".txt")
        data = path.read_bytes()
        digests[edition] = hashlib.sha256(data).hexdigest()
        rows = {f: {} for f in FOLIOS}
        for line in data.decode().splitlines():
            rec = re.fullmatch(r"<(f67r2|f72r3)\.(\d+),[^>]+>\s+(\S+)\s*", line)
            if rec and int(rec[2]) in FOLIOS[rec[1]]:
                assert int(rec[2]) not in rows[rec[1]]
                rows[rec[1]][int(rec[2])] = rec[3]
        raw[edition] = {f: [rows[f].get(i) for i in ids] for f, ids in FOLIOS.items()}
    return raw, digests


def parse(txt, alphabet, spacing, omit_alternatives=False):
    if txt is None:
        return None
    txt = re.sub(r"<![^>]*>", "", txt)
    alt = re.search(r"\[([a-z]+):([a-z]+)\]", txt)
    if not alt:
        return groups(txt, alphabet, spacing)
    if omit_alternatives:
        return None
    variants = [parse(txt[:alt.start()] + replacement + txt[alt.end():], alphabet, spacing)
                for replacement in alt.groups()]
    return union(variants)


def union(variants):
    # An unresolved variant cannot disprove a word at this locus.
    if any(v is None for v in variants):
        return None
    return tuple(sorted({span for v in variants for span in v}))


def panel_variants(raw):
    for alphabet in ("EVA", "ASCII"):
        for edition, folios in raw.items():
            for spacing in ("join", "split"):
                omit_choices = (False, True) if edition == "ZL3b-n" else (False,)
                for omit in omit_choices:
                    label = f"{edition}/{alphabet}/{spacing}" + ("/omet_alternative" if omit else "")
                    yield label, {f: tuple(parse(t, alphabet, spacing, omit) for t in texts)
                                  for f, texts in folios.items()}
        label = f"editions_et_espacements_au_choix/{alphabet}"
        yield label, {f: tuple(union([parse(raw[ed][f][i], alphabet, spacing)
                                      for ed in raw for spacing in ("join", "split")])
                              for i in range(7)) for f in FOLIOS}


@lru_cache(maxsize=None)
def compatible_keys(rows, model):
    """All different partial tables sufficient for the selected observed rows."""
    keys = {()}
    for row in sorted(rows, key=len):
        if not row:
            return ()
        next_keys = set()
        for key in keys:
            for option in row:
                joined = merge(key, option, model == "bijection")
                if joined is not None:
                    next_keys.add(tuple(sorted(joined.items())))
        keys = next_keys
        if not keys:
            break
    return tuple(sorted(keys))


def matrix(panel, names, model):
    return [tuple(options(row, name, model) for name in names) if row is not None else None
            for row in panel]


def rows_for(mat, perm):
    return tuple(mat[i][j] for i, j in enumerate(perm) if mat[i] is not None)


def literal_names(panel, names, model, key):
    key = dict(key)
    def spell(x):
        return sum((key[c] for c in x), ()) if all(c in key for c in x) else None
    found = []
    for row in panel:
        if row is None:
            found.append(None)
        elif model == "letter_to_glyphs":
            found.append([i for i, name in enumerate(names) if spell(tuple(name)) in row])
        else:
            readings = {spell(span) for span in row}
            found.append([i for i, name in enumerate(names) if tuple(name) in readings])
    return found


def allowed_by_place(solutions):
    return [sorted({p[i] for p in solutions}) for i in range(7)]


@lru_cache(maxsize=None)
def single(panel, names, model):
    mat = matrix(panel, names, model)
    solutions = {}
    for perm in ALL:
        rows = rows_for(mat, perm)
        if all(rows):
            keys = compatible_keys(rows, model)
            if keys:
                solutions[perm] = keys
    return solutions


def details(panel, names, model, solutions):
    return [{
        "planet_indices": perm, "tables": [{
            "key": dict(key), "literal_names_per_slot": literal_names(panel, names, model, key)
        } for key in keys]
    } for perm, keys in solutions.items()]


def report_one(panel, names, model, solutions):
    mat = matrix(panel, names, model)
    def diagnostic(perm):
        solo = [i for i in range(7) if mat[i] is not None and mat[i][perm[i]]]
        for size in range(len(solo), -1, -1):
            best = [ix for ix in itertools.combinations(solo, size)
                    if compatible_keys(tuple(mat[i][perm[i]] for i in ix), model)]
            if best:
                break
        return {"individuellement": solo, "maximum_avec_table_commune": size,
                "sous_ensembles_maximaux": best}
    return {"effectif_evaluable": sum(row is not None for row in panel),
            "affectations_compatibles": len(solutions), "publiee": PUBLISHED in solutions,
            "soleil_lune_inversees": SWAPPED in solutions,
            "par_lieu_solutions_completes": allowed_by_place(solutions),
            "diagnostic_publie": diagnostic(PUBLISHED), "diagnostic_inverse": diagnostic(SWAPPED),
            "solutions": details(panel, names, model, solutions)}


def paired(panel_a, panel_b, names_a, names_b, model, a, b):
    hits = []
    for perm in sorted(a.keys() & b.keys()):
        common = set()
        for k1 in a[perm]:
            for k2 in b[perm]:
                joined = merge(k1, k2, model == "bijection")
                if joined is not None:
                    common.add(tuple(sorted(joined.items())))
        if common:
            locked = []
            for direction, train, test_panel, test_names in (
                    ("f67r2_vers_f72r3", a, panel_b, names_b),
                    ("f72r3_vers_f67r2", b, panel_a, names_a)):
                for key in train[perm]:
                    readings = literal_names(test_panel, test_names, model, key)
                    locked.append({"direction": direction, "table_source": dict(key),
                                   "lectures_de_la_table_figee": readings,
                                   "sept_noms_imposes": all(r == [name] for r, name in zip(readings, perm))})
            hits.append({"planet_indices": perm, "cles_communes": [dict(k) for k in sorted(common)],
                         "transfert_sans_reajustement": locked})
    return {"individuellement_sur_les_deux": len(a.keys() & b.keys()),
            "affectations_avec_table_commune": len(hits), "solutions": hits}


def calibration():
    names = tuple(normalize(x) for x in PLANETS)
    rng = random.Random(67172)
    actual = list(range(7))
    rng.shuffle(actual)
    actual = tuple(actual)
    symbols = sorted(set("".join(names)))
    encrypted = [f"g{i}" for i in range(len(symbols))]
    rng.shuffle(encrypted)
    private = dict(zip(symbols, encrypted))
    plain = [names[i] for i in actual]
    encoded = [tuple(private[x] for x in w) for w in plain]
    panel_a = tuple((w,) for w in encoded)
    panel_b = tuple(spans([("!",), w[:2], w[2:], ("?",)]) for w in encoded)
    a = single(panel_a, names, "bijection")
    b = single(panel_b, names, "bijection")
    assert set(a) == set(b) == {actual}
    assert len(a[actual]) == 1 and {c: v[0] for c, v in a[actual][0]} == {v:k for k,v in private.items()}
    result = paired(panel_a, panel_b, names, names, "bijection", a, b)
    assert result["affectations_avec_table_commune"] == 1
    assert all(row["sept_noms_imposes"] for row in result["solutions"][0]["transfert_sans_reajustement"])
    perturbed = list(panel_a)
    idx = actual.index(4)  # Reverse sol only, preserving length and its internal equality pattern.
    perturbed[idx] = (tuple(reversed(encoded[idx])),)
    bad = single(tuple(perturbed), names, "bijection")
    assert not bad
    cases = {}
    for model in MODELS[1:]:
        if model == "glyph_to_letters":
            cipher = [tuple(private[c] if len(c) == 1 else "X_" + c
                            for c in re.findall("sat|ur|.", w)) for w in plain]
        else:
            code = {c: (g,) for c,g in private.items()}
            code["s"] = ("S0", "S1", "S2")
            code["u"] = ("U0", "U1")
            cipher = [sum((code[c] for c in w), ()) for w in plain]
        panel = tuple((seq,) for seq in cipher)
        hits = single(panel, names, model)
        strict = single(panel, names, "bijection")
        assert actual in hits and not strict
        cases[model] = {"vraie_affectation_retrouvee": True, "affectations": len(hits),
                        "tables_vraie_affectation": len(hits[actual]), "bijection": len(strict)}
    return {"graine": 67172, "vraie_affectation": actual, "cle_par_lettre": private,
            "solution_serie_simple": details(panel_a, names, "bijection", a),
            "transfert_fixture": result, "contre_exemple_sol_inverse": len(bad), "largeurs_variables": cases}


def manuscript():
    raw, hashes = extract()
    source = HERE.parent / "temoin" / "sept-astres-schedel.json"
    witness = {row["test_ascii"]: row for row in json.loads(source.read_text())["planets"]}
    nom = tuple(witness[p]["nominative_expanded"] for p in PLANETS)
    assert tuple(map(normalize, nom)) == tuple(map(normalize, PLANETS))
    lists = {"nominatif": nom, "genitif": tuple(witness[p]["ring_legend_genitive"] for p in PLANETS)}
    # Different historical lists can share a normalized spelling (especially under truncation).
    spellings = {f"{kind}_{length}": tuple(normalize(x) if length == "entier" else normalize(x)[:3]
                                           for x in words)
                 for kind, words in lists.items() for length in ("entier", "trois")}
    assert all(len(xs) == len(set(xs)) == 7 for xs in spellings.values())
    output = {"loci_dans_ordre_commun": FOLIOS, "noms_par_indice": PLANETS, "graphies": lists,
              "epreuves_normalisees": spellings, "sha256_editions": hashes, "notations_IVTFF": raw,
              "permutations_par_recherche": len(ALL), "variantes": {}}
    for variant, panels in panel_variants(raw):
        singles, doubles = [], []
        p, q = panels.values()
        for model in MODELS:
            fits = {}
            for f, panel in panels.items():
                for kind, names in spellings.items():
                    fit = single(panel, names, model)
                    fits[f, kind] = fit
                    singles.append({"folio": f,"forme": kind, "table": model,
                                    **report_one(panel, names, model, fit)})
            for kind_a, ns_a in spellings.items():
                for kind_b, ns_b in spellings.items():
                    pair = paired(p, q, ns_a, ns_b, model, fits["f67r2", kind_a], fits["f72r3", kind_b])
                    doubles.append({"f67r2_forme": kind_a, "f72r3_forme": kind_b, "table": model, **pair})
        output["variantes"][variant] = {"separement": singles, "ensemble": doubles}
    return output


if __name__ == "__main__":
    mode, = sys.argv[1:]
    result = {"etalonnage": calibration, "manuscrit": manuscript}[mode]()
    (HERE / (mode + ".json")).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
