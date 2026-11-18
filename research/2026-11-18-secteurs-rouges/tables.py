"""Exact finite search over contiguous inscription groups and fixed spelling tables."""
import argparse
import hashlib
import json
import random
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parents[1] / "voynich_20261028/data"
MONTHS = "ianuarius februarius martius aprilis maius iunius iulius augustus september october november december".split()
SIGNS = "aries taurus gemini cancer leo virgo libra scorpio sagittarius capricornus aquarius pisces".split()
HELD = (2, 5, 8, 11)
TRAIN = tuple(n for n in range(12) if n not in HELD)
MODELS = ("bijection", "glyph_to_letters", "letter_to_glyphs")
FULL = range(12)


def normalize(word):
    plain = unicodedata.normalize("NFD", word.lower())
    return "".join(c for c in plain if not unicodedata.combining(c)).replace("v", "u").replace("j", "i")


def inscriptions(edition):
    path = CORPUS / (edition + ".txt")
    raw = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"<f67r2\.(\d+),[^>]+>\s+(\S+)\s*", line)
        if match:
            raw[int(match[1])] = match[2]
    return raw, hashlib.sha256(path.read_bytes()).hexdigest()


def spans(words):
    return tuple(dict.fromkeys(sum(words[begin:end], ()) for begin in range(len(words))
                               for end in range(begin+1, len(words)+1)))


def groups(raw, alphabet, spaces):
    if raw is None or not re.fullmatch(r"[a-z]+(?:[.,][a-z]+)*", raw):
        return None
    text = raw.replace(",", "." if spaces == "split" else "")
    pattern = r"ckh|cth|cph|cfh|ch|sh|." if alphabet == "EVA" else "."
    return spans([tuple(re.findall(pattern, part)) for part in text.split(".")])


@lru_cache(maxsize=None)
def possible(source, target, model):
    limit = 1 if model == "bijection" else 3
    solutions = set()

    def visit(i, j, key):
        left = len(source) - i
        to_cover = len(target) - j
        if not left <= to_cover <= limit * left:
            return
        if not left:
            solutions.add(tuple(sorted(key.items())))
            return
        unit = source[i]
        if unit in key:
            mapped = key[unit]
            if target[j:j+len(mapped)] == mapped:
                visit(i+1, j+len(mapped), key)
            return
        for size in range(1, min(limit, to_cover)+1):
            mapped = target[j:j+size]
            if model == "bijection" and mapped in key.values():
                continue
            key[unit] = mapped
            visit(i+1, j+size, key)
            del key[unit]

    visit(0, 0, {})
    return tuple(sorted(solutions))


@lru_cache(maxsize=None)
def options(candidates, name, model):
    letters = tuple(name)
    solutions = set()
    for seq in candidates:
        src, dst = (letters, seq) if model == "letter_to_glyphs" else (seq, letters)
        solutions.update(possible(src, dst, model))
    return tuple(sorted(solutions))


def merge(key, extension, bijective):
    joined = dict(key)
    for symbol, value in extension:
        if symbol in joined and joined[symbol] != value:
            return None
        joined[symbol] = value
    if bijective and len(set(joined.values())) != len(joined):
        return None
    return joined


def solve(choices, positions, model):
    # A locus with no transcription is unconstrained. An empty domain is a conflict.
    rows = [choices[i] for i in positions if choices[i] is not None]
    if any(not row for row in rows):
        return None
    rows.sort(key=len)

    def search(i, key):
        if i == len(rows):
            return key
        for extension in rows[i]:
            joined = merge(key, extension, model == "bijection")
            if joined is not None:
                solution = search(i+1, joined)
                if solution is not None:
                    return solution
        return None

    return search(0, {})


def name_at(order, sector, start, step):
    return order[((sector-start)*step) % 12]


def scan(panel, order, model, capture=False):
    passes = []
    local_best = 0
    for start in FULL:
        for step in (1, -1):
            rows = [None if panel[i] is None else options(panel[i], name_at(order, i, start, step), model)
                    for i in FULL]
            local_best = max(local_best, sum(bool(row) for row in rows))
            key = solve(rows, TRAIN, model)
            if key is None:
                continue
            valid = {i+1: solve(rows, (*TRAIN, i), model) is not None
                     for i in HELD if rows[i] is not None}
            whole = solve(rows, FULL, model)
            result = {"first_name_at": start+1, "clockwise": step == 1,
                      "validation_individuelle": valid, "serie_compatible": whole is not None}
            if capture:
                result["training_key"] = key
            passes.append(result)
    return {"apprentissage_evaluable": sum(panel[i] is not None for i in TRAIN),
            "reserve_evaluable": sum(panel[i] is not None for i in HELD),
            "maximum_compatible_avec_une_table_par_secteur": local_best,
            "orientations_apprentissage": passes}


def controls():
    order = [normalize(word) for word in MONTHS]
    letters = sorted(set("".join(order)))
    shuffled = letters.copy()
    random.Random(2391).shuffle(shuffled)
    private_key = dict(zip(letters, shuffled))
    start, step = 4, -1
    reference = [name_at(order, i, start, step) for i in FULL]
    ciphertext = [tuple(private_key[c] for c in name) for name in reference]
    out = {}
    for filler in (False, True):
        words = []
        for i, seq in enumerate(ciphertext):
            chunks = [seq[:2], seq[2:]] if filler and i % 2 == 0 else [seq]
            if filler:
                chunks = [("!",), *chunks, ("!", "!")]
            words.append(chunks)
        panel = [spans(parts) for parts in words]
        training_panel = [None if i in HELD else panel[i] for i in FULL]
        training = scan(training_panel, order, "bijection", capture=True)
        assert len(training["orientations_apprentissage"]) == 1
        hit = training["orientations_apprentissage"][0]
        assert (hit["first_name_at"], hit["clockwise"]) == (start+1, False)
        key = hit["training_key"]
        # Decode every whole-group span using only the training table. Keep unknowns explicit.
        predictions = {i+1: ["".join(key.get(c, ("?",))[0] for c in seq) for seq in panel[i]] for i in HELD}
        selected = ["".join(key.get(c, ("?",))[0] for c in ciphertext[i]) for i in HELD]
        assert all(all(a in (b, "?") for a,b in zip(pred, reference[i]))
                   for pred,i in zip(selected,HELD))
        res = scan(panel, order, "bijection")
        assert res["orientations_apprentissage"][0]["serie_compatible"]
        out["avec_remplissage" if filler else "simple"] = {
            "scan": res, "decodages_avant_comparaison": predictions,
            "verification_des_vrais_groupes": dict(zip((i+1 for i in HELD),selected)),
            "noms_masques": {i+1:reference[i] for i in HELD},
            "exact_sur_vrais_groupes": sum(pred == reference[i] for pred,i in zip(selected,HELD)),
            "positions_connues_sur_vrais_groupes": sum(len(pred)-pred.count("?") for pred in selected),
            "positions_totales_sur_vrais_groupes": sum(map(len,selected))}
    mixed = list(ciphertext)
    random.Random(1142).shuffle(mixed)
    out["ordre_melange"] = scan([(x,) for x in mixed], order, "bijection")
    assert not out["ordre_melange"]["orientations_apprentissage"]
    # The two variable-width fixtures require 2- and 3-unit mappings in opposite directions.
    for model in MODELS[1:]:
        if model == "glyph_to_letters":
            coded = [tuple(re.findall("ius|ar|.", x)) for x in reference]
        else:
            coded = [tuple("".join({"a":"!@", "r":"#$%"}.get(c,c) for c in x)) for x in reference]
        panel = [(seq,) for seq in coded]
        res = scan(panel, order, model)
        assert any(hit["serie_compatible"] and (hit["first_name_at"],hit["clockwise"]) == (start+1,False)
                   for hit in res["orientations_apprentissage"])
        strict = scan(panel, order, "bijection")
        assert not any(hit["serie_compatible"] for hit in strict["orientations_apprentissage"])
        out[model] = {"scan":res, "controle_bijection":strict}
    return out


def manuscript():
    lists = {"reference_mois": MONTHS, "reference_signes": SIGNS}
    lists.update(json.loads((HERE/"sources/listes-historiques.json").read_text()))
    raw_by_edition = {}
    results = []
    for edition in ("IT2a-n", "ZL3b-n"):
        raw, digest = inscriptions(edition)
        raw_by_edition[edition] = {"sha256":digest, "rubriques": [raw.get(i) for i in range(1,13)],
                                   "visages":[raw.get(i) for i in range(52,64)]}
        for track, base in (("rubriques",1), ("visages",52)):
            for alphabet in ("EVA","ASCII"):
                for spaces in ("split","join"):
                    panel = [groups(raw.get(i+base),alphabet,spaces) for i in FULL]
                    for source, names in lists.items():
                        assert len(names) == 12 and all(re.fullmatch("[a-z]+",normalize(n)) for n in names)
                        for form in ("entier","trois"):
                            order = [normalize(n) if form == "entier" else normalize(n)[:3] for n in names]
                            for model in MODELS:
                                res = scan(panel,order,model)
                                results.append({"edition":edition,"serie":track,"unites":alphabet,
                                                "espaces":spaces,"liste":source,"graphie":form,"table":model,**res})
    return {"inscriptions":raw_by_edition, "listes":lists, "tests":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("etalonnage","manuscrit"))
    args = parser.parse_args()
    result = controls() if args.mode == "etalonnage" else manuscript()
    path = HERE / (args.mode + ".json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
