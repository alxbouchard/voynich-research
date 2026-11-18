"""Independent constraint check: all cuts, then backtracking over slot/name pairs."""
from itertools import combinations, product
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent


def spans(texts, eva):
    out = set()
    for raw in texts:
        clean = re.sub(r"<![^>]*>", "", raw)
        # The only alternative present in the selected fourteen loci.
        matches = [clean.replace("[m:g]", c) for c in ("m", "g")]
        for match in matches:
            assert re.fullmatch(r"[a-z.,]+", match)
            for sep in ("", "."):
                parts = match.replace(",", sep).split(".")
                glyphs = [tuple(re.findall(r"c[kptf]h|[cs]h|.", part)) if eva else tuple(part)
                          for part in parts]
                for a, b in combinations(range(len(parts) + 1), 2):
                    out.add(sum(glyphs[a:b], ()))
    return out


def partkeys(glyphs, name, model):
    left, right = (tuple(name), glyphs) if model == "letter_to_glyphs" else (glyphs, tuple(name))
    max_len = 1 if model == "bijection" else 3
    if not len(left) <= len(right) <= len(left) * max_len:
        return
    # In contrast with the main solver, cut the entire target at all candidate offsets first.
    for offsets in combinations(range(1, len(right)), len(left) - 1):
        bounds = (0, *offsets, len(right))
        pieces = tuple(right[a:b] for a, b in zip(bounds, bounds[1:]))
        if max(map(len, pieces)) > max_len:
            continue
        key = dict(zip(left, pieces))
        if tuple(key[c] for c in left) != pieces:
            continue
        if model == "bijection" and len(set(pieces)) != len(key):
            continue
        yield tuple(sorted(key.items()))


def can_fill(ix, domains, model):
    """Choose both a fresh name and its spelling constraints during the search."""
    if any(not domains[i] for i in ix):
        return False
    order = sorted(ix, key=lambda i: len(domains[i]))
    def assign(n, used, table):
        if n == len(order):
            return True
        for j, rule in domains[order[n]]:
            if j in used or any(s in table and table[s] != t for s, t in rule):
                continue
            combined = {**table, **dict(rule)}
            if model == "bijection" and len(set(combined.values())) != len(combined):
                continue
            if assign(n + 1, used | {j}, combined):
                return True
        return False
    return assign(0, set(), {})


def main():
    data = json.loads((HERE / "manuscrit.json").read_text())
    names = data["epreuves_normalisees"]
    # Re-read the corpus directly; the output of the first solver supplies only
    # list metadata and is cross-checked against the extracted source.
    folios = {"f67r2": (15, 22, 28, 31, 34, 37, 47), "f72r3": (29, 32, 33, 27, 31, 30, 28)}
    corpus = HERE.parents[2] / "voynich_20261028" / "data"
    records = {}
    for edition in ("ZL3b-n", "IT2a-n"):
        records[edition] = {}
        for f, loci in folios.items():
            lookup = dict(re.findall(r"^<" + f + r"\.(\d+),[^>]+>[ \t]*(\S+)", (corpus / (edition + ".txt")).read_text(), re.M))
            rows = [lookup[str(n)] for n in loci]
            assert rows == data["notations_IVTFF"][edition][f]
            records[edition][f] = rows
    checks = []
    for f, alphabet, (name_kind, words), model in product(
            folios, ("EVA", "ASCII"), names.items(), ("bijection", "glyph_to_letters", "letter_to_glyphs")):
        panels = [spans({fs[f][i] for fs in records.values()}, alphabet == "EVA") for i in range(7)]
        domains = [sorted({(j, key) for j, name in enumerate(words) for seq in row for key in partkeys(seq, name, model)})
                   for row in panels]
        maxima = None
        for n in range(7, -1, -1):
            maxima = [subset for subset in combinations(range(7), n) if can_fill(subset, domains, model)]
            if maxima:
                break
        assert n < 7
        skip_alt = can_fill([0, 1, 3, 4, 5, 6], domains, model) if f == "f67r2" else None
        assert skip_alt is not True
        checks.append({"folio": f, "alphabet": alphabet, "graphie": name_kind, "modele": model,
                       "maximum_affectation_libre": n,
                       "sous_ensembles_maximaux_loci": [[folios[f][i] for i in sub] for sub in maxima],
                       "complet_apres_omission_f67r2_28": skip_alt})
    path = HERE / "verification.json"
    path.write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
