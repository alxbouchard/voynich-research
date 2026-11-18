"""Direct manuscript-to-manuscript respelling, without any plaintext lexicon."""
from itertools import combinations, permutations
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from lecture import FOLIOS, compatible_keys, extract
from tables import possible

MODELS = ("bijection", "f67_vers_f72", "f72_vers_f67")
ANCHORS = (3, 6, 5)  # .27, .28, .30 on f72r3, in this reporting order.


def words(raw, alphabet, spacing, width):
    text = re.sub(r"<![^>]*>", "", raw)
    matches = re.search(r"\[([a-z]+):([a-z]+)\]", text)
    if matches:
        return set.union(*(words(text[:matches.start()] + c + text[matches.end():], alphabet, spacing, width)
                           for c in matches.groups()))
    groups = text.replace(",", "" if spacing == "join" else ".").split(".")
    chosen = groups[0] if width == "premier_groupe" else "".join(groups)
    assert re.fullmatch(r"[a-z]+", chosen)
    return {tuple(re.findall(r"ckh|cph|cth|cfh|ch|sh|.", chosen)) if alphabet == "EVA" else tuple(chosen)}


def make_panels(raw, editions, alphabet, spacings, width):
    return [tuple(set.union(*(words(raw[ed][f][i], alphabet, spacing, width) for ed in editions for spacing in spacings))
                  for i in range(7)) for f in FOLIOS]


def make_matrix(p, q, model):
    table = "bijection" if model == "bijection" else "glyph_to_letters"
    def cell(left, right):
        choices = set()
        for a in left:
            for b in right:
                src, dst = (b, a) if model == "f72_vers_f67" else (a, b)
                choices.update(possible(src, dst, table))
        return tuple(sorted(choices))
    return [[cell(a, b) for b in q] for a in p], table


def locus_pair(i):
    return [FOLIOS["f67r2"][i], FOLIOS["f72r3"][i]]


def predicted(i, p, q, model, key):
    """Complete readings produced without extending the partial anchor table."""
    lookup = dict(key)
    source, dest = (q, p) if model == "f72_vers_f67" else (p, q)
    for row in source[i]:
        if all(g in lookup for g in row):
            result = sum((lookup[g] for g in row), ())
            if result in dest[i]:
                return True
    return False


def evaluate(p, q, model):
    matrix, table = make_matrix(p, q, model)
    fixed = tuple(matrix[i][i] for i in range(7))
    anchor_fit = compatible_keys(tuple(fixed[i] for i in ANCHORS), table)
    rest = tuple(i for i in range(7) if i not in ANCHORS)
    all_fixed = compatible_keys(fixed, table)
    locked = [{"table": dict(key), "autres_paires_lues_sans_ajout":
               [locus_pair(i) for i in rest if predicted(i, p, q, model, key)]} for key in anchor_fit]
    for size in range(7, -1, -1):
        winners = [subset for subset in combinations(range(7), size)
                   if compatible_keys(tuple(fixed[i] for i in subset), table)]
        if winners:
            break
    free = []
    for assignment in permutations(range(7)):
        rows = tuple(matrix[i][j] for i, j in enumerate(assignment))
        if all(rows) and compatible_keys(rows, table):
            free.append([FOLIOS["f72r3"][j] for j in assignment])
    return {"nombre_tables_pour_chaque_paire": [len(r) for r in fixed],
            "trois_paires": [locus_pair(i) for i in ANCHORS], "tables_des_trois": len(anchor_fit),
            "table_figee": locked, "tables_sept_paires_publiees": len(all_fixed),
            "maximum_paires_publiees": size,
            "ensembles_maximaux": [[locus_pair(i) for i in a] for a in winners],
            "appariements_libres_complets": free}


def control():
    # All anchors together contain the four glyphs, so the other groups can be
    # read literally without extending the anchor table.
    primary = ["abbd", "cda", "cbad", "cab", "dca", "dabc", "bdca"]
    p = tuple({tuple(w)} for w in primary)
    substitution = dict(zip("abcd", ["Z", "X", "W", "Y"]))
    expanded = dict(zip("abcd", ["ZX", "K", "PWQ", "V"]))
    def coded(key):
        return tuple({tuple("".join(key[c] for c in w))} for w in primary)
    controls = {}
    for model, a, b in (("bijection", p, coded(substitution)), ("f67_vers_f72", p, coded(expanded)),
                         ("f72_vers_f67", coded(expanded), p)):
        good = evaluate(a, b, model)
        assert good["tables_sept_paires_publiees"] >= 1
        assert any(len(r["autres_paires_lues_sans_ajout"]) == 4 for r in good["table_figee"])
        controls[model] = good
    altered = list(coded(substitution))
    altered[0] = {tuple("ZXXZ")}  # Last glyph differs from the prediction ZXXY.
    bad = evaluate(p, altered, "bijection")
    assert bad["tables_des_trois"] == 1 and not bad["tables_sept_paires_publiees"]
    assert len(bad["table_figee"][0]["autres_paires_lues_sans_ajout"]) == 3
    controls["bijection_dernier_glyphe_altere_hors_trois"] = bad
    return controls


def main():
    controls = control()
    raw, hashes = extract()
    variants = {}
    for width in ("premier_groupe", "groupes_entiers_concat"):
        for alphabet in ("EVA", "ASCII"):
            choices = [(ed + "/" + space, [ed], [space]) for ed in raw for space in ("join", "split")]
            choices.append(("editions_espacements_au_choix", list(raw), ["join", "split"]))
            for variant, editions, spacings in choices:
                p, q = make_panels(raw, editions, alphabet, spacings, width)
                variants[f"{width}/{alphabet}/{variant}"] = {m: evaluate(p, q, m) for m in MODELS}
    output = {"ordre_f67_f72": [locus_pair(i) for i in range(7)], "sha256_editions": hashes,
              "etalonnage": controls, "variantes": variants}
    (HERE / "variation.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
