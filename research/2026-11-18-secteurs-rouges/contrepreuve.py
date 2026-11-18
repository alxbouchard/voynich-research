"""Vérification indépendante par l'équation des longueurs et des certificats locaux."""
import hashlib
import itertools
import json
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRAIN = (1, 2, 4, 5, 7, 8, 10, 11)
HELD = (3, 6, 9, 12)
DIRECTIONS = (1, -1)
MODELS = ("bijection", "glyph_to_letters", "letter_to_glyphs")
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
FIELDS = ("edition", "serie", "unites", "espaces", "liste", "graphie", "table")
MONTHS = "ianuarius februarius martius aprilis maius iunius iulius augustus september october november december".split()
SIGNS = "aries taurus gemini cancer leo virgo libra scorpio sagittarius capricornus aquarius pisces".split()


def read_json(path):
    return json.loads(path.read_text())


def read_edition(edition):
    path = HERE.parents[1] / "voynich_20261028" / "data" / (edition + ".txt")
    lines = {}
    for line in path.read_text().splitlines():
        if line.startswith("<f67r2."):
            label, body = line.split(">", 1)
            sector = int(label.partition(".")[2].partition(",")[0])
            if sector in lines:
                raise ValueError(f"Locus répété {label}")
            lines[sector] = body.strip()
    return {**{name: [lines.get(n) for n in range(base, base + 12)]
               for name, base in (("rubriques", 1), ("visages", 52))},
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def group_tokens(word, alphabet):
    units = []
    while word:
        unit = word[0]
        if alphabet == "EVA":
            for compound in ("ckh", "cth", "cfh", "cph", "sh", "ch"):
                if word.startswith(compound):
                    unit = compound
                    break
        units.append(unit)
        word = word[len(unit):]
    return tuple(units)


def windows(raw, alphabet, spaces):
    if raw is None or any(c not in "abcdefghijklmnopqrstuvwxyz,." for c in raw):
        return None
    if any(not item for item in raw.replace(",", ".").split(".")):
        return None
    words = raw.replace(",", "." if spaces == "split" else "").split(".")
    units = [group_tokens(item, alphabet) for item in words]
    found = set()
    for end in range(1, len(units) + 1):
        span = ()
        for i in reversed(range(end)):
            span = units[i] + span
            found.add(span)
    return tuple(sorted(found))


@lru_cache(None)
def widths(frequencies, size, bound):
    """Solve sum(frequency[s] * width[s]) = total before assigning any letters."""
    if not frequencies:
        return ((),) if size == 0 else ()
    if not sum(frequencies) <= size <= bound * sum(frequencies):
        return ()
    return tuple((width,) + rest for width in range(1, bound + 1)
                 for rest in widths(frequencies[1:], size - width * frequencies[0], bound))


@lru_cache(None)
def choices(spans, name, model):
    solutions = set()
    for span in spans:
        source, target = (tuple(name), span) if model == "letter_to_glyphs" else (span, tuple(name))
        counts = Counter(source)
        for lengths in widths(tuple(counts.values()), len(target), 1 if model == "bijection" else 3):
            sizes = dict(zip(counts, lengths))
            offset = 0
            pairs = set()
            for symbol in source:
                after = offset + sizes[symbol]
                pairs.add((symbol, target[offset:after]))
                offset = after
            if len(pairs) != len(counts):
                continue
            if model == "bijection" and len({value for _, value in pairs}) != len(pairs):
                continue
            solutions.add(frozenset(pairs))
    return frozenset(solutions)


def compatible(assignment, other, unique):
    union = assignment | other
    return (len({s for s, _ in union}) == len(union)
            and (not unique or len({t for _, t in union}) == len(union)))


def has_clique(domains, unique):
    """Nodes are local spellings. Pick one per sector with all edges present."""
    if not domains:
        return True
    first, *later = sorted(domains, key=len)
    for node in first:
        subgraph = [[other for other in part if compatible(node, other, unique)] for part in later]
        if all(subgraph) and has_clique(subgraph, unique):
            return True
    return False


def certificate(rows, unique):
    for size in range(1, len(rows) + 1):
        for positions in itertools.combinations(rows, size):
            if not has_clique([rows[p] for p in positions], unique):
                return positions
    return ()


def orientations(names):
    for first in range(1, 13):
        for step in DIRECTIONS:
            assigned = {}
            sector = first
            for name in names:
                assigned[sector] = name
                sector += step
                if sector > 12:
                    sector = 1
                if sector < 1:
                    sector = 12
            yield first, step, assigned


def calibrate():
    # All pairs intersect, but the intersection of all three spelling domains is empty.
    duos = ("x.y", "y.z", "x.z")
    rows = {i: choices(windows(text, "ASCII", "split"), "a", "letter_to_glyphs")
            for i, text in enumerate(duos, 1)}
    assert certificate(rows, False) == (1, 2, 3)
    assert certificate({1: rows[1], 2: rows[1]}, False) == ()
    for model, raw, name, fits in (
        ("glyph_to_letters", "x.x", "abab", True),
        ("glyph_to_letters", "x.x", "abac", False),
        ("glyph_to_letters", "x", "abcd", False),
        ("letter_to_glyphs", "abc.abc", "xx", True),
        ("letter_to_glyphs", "abc.abd", "xx", False),
        ("bijection", "xy", "aa", False),
        ("glyph_to_letters", "xy", "aa", True),
    ):
        assert bool(choices(windows(raw, "ASCII", "split"), name, model)) == fits
    # Recover the actual location and orientation from the training positions.
    names = ["a" * k + "b" for k in range(1, 13)]
    raw = {}
    for i, name in enumerate(names):
        sector = (7 - i) % 12 + 1
        raw[sector] = windows("z." + name.translate(str.maketrans("ab", "xy")) + ".z", "EVA", "split")
    passing = []
    for first, step, assigned in orientations(names):
        rows = {p: choices(raw[p], assigned[p], "bijection") for p in TRAIN}
        if has_clique(list(rows.values()), True):
            passing.append((first, step))
    assert passing == [(8, -1)]
    return {"orientations_bijection": passing, "premiere_contradiction_ternaire": [1, 2, 3],
            "cas_unitaires_controles": 7}


def plain(word):
    return "".join(c for c in unicodedata.normalize("NFKD", word.casefold())
                   if not unicodedata.combining(c)).translate(str.maketrans("jv", "iu"))


def run():
    controls = calibrate()
    original = read_json(HERE / "manuscrit.json")
    editions = {key: read_edition(key) for key in ("IT2a-n", "ZL3b-n")}
    names = {"reference_mois": MONTHS, "reference_signes": SIGNS,
             **read_json(HERE / "sources" / "listes-historiques.json")}
    assert names == original["listes"] and editions == original["inscriptions"]
    reports = {tuple(row[field] for field in FIELDS): (i, row) for i, row in enumerate(original["tests"])}
    grid = list(itertools.product(editions, ("rubriques", "visages"), ("EVA", "ASCII"),
                                  ("split", "join"), names, ("entier", "trois"), MODELS))
    assert set(reports) == set(grid) and len(grid) == len(original["tests"])
    totals, by_model, by_track = Counter(), {key: Counter() for key in MODELS}, {}
    certificates, vectors, exceptions, differences = [], {}, [], []
    digest = hashlib.sha256((HERE / "manuscrit.json").read_bytes()).hexdigest()

    for spec in grid:
        edition, track, alphabet, spacing, list_name, spelling, model = spec
        index, reference = reports[spec]
        panel = {i: windows(raw, alphabet, spacing) for i, raw in enumerate(editions[edition][track], 1)}
        order = [plain(word) for word in names[list_name]]
        if spelling == "trois":
            order = [word[:3] for word in order]
        evaluable = [sum(panel[p] is not None for p in positions) for positions in (TRAIN, HELD)]
        if evaluable != [reference["apprentissage_evaluable"], reference["reserve_evaluable"]]:
            differences.append([index, "positions_evaluables", evaluable])
        vector, passing, maximum = [], [], 0
        for first, step, orientation in orientations(order):
            local = {p: choices(spans, orientation[p], model) for p, spans in panel.items() if spans is not None}
            maximum = max(maximum, sum(map(bool, local.values())))
            witness = certificate({p: local[p] for p in TRAIN if p in local}, model == "bijection")
            totals[len(witness)] += 1
            by_model[model][len(witness)] += 1
            by_track.setdefault(track, Counter())[len(witness)] += 1
            if not witness:
                passing.append((first, step == 1))
                exceptions.append([index, first, step, "apprentissage compatible"])
            if witness not in certificates:
                certificates.append(witness)
            vector.append(DIGITS[certificates.index(witness)])
        expected = [(hit["first_name_at"], hit["clockwise"]) for hit in reference["orientations_apprentissage"]]
        if maximum != reference["maximum_compatible_avec_une_table_par_secteur"] or expected != passing:
            differences.append([index, "maximum_local_et_orientations", maximum, passing])
        vectors.setdefault("".join(vector), []).append(index)

    return {"source_sha256_manuscrit_json": digest, "etalonnage": controls,
            "variantes": len(grid), "orientations": sum(totals.values()),
            "taille_minimale_contradiction": totals, "par_table": by_model, "par_serie": by_track,
            "exceptions": exceptions, "discordances_avec_manuscrit": differences,
            "lecture": "Chaque vecteur de 24 caractères regroupe les indices (base 0) de tests dans manuscrit.json. Les caractères sont ordonnés par départ 1 à 12, à chaque départ sens + puis −. La légende donne les positions de secteur (base 1) dont les tables ne peuvent coexister. Un certificat vide désigne une orientation compatible.",
            "legende": {DIGITS[i]: v for i, v in enumerate(certificates)}, "vecteurs_et_indices": vectors}


if __name__ == "__main__":
    report = run()
    (HERE / "contrepreuve.json").write_text(json.dumps(report, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("vecteurs_et_indices", "legende")}, ensure_ascii=False))
    if report["discordances_avec_manuscrit"]:
        raise SystemExit(1)
