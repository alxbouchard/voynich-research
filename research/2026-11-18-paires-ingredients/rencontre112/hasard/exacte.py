"""Independent exhaustive calculation for opchy/otol, with one instance each per eligible page."""
from collections import defaultdict
from fractions import Fraction
import json
from math import prod

from melanger import HERE, PAIR, inputs, tokens


def exact(blocks, lines, condition_block, pair=PAIR):
    classes = defaultdict(list)
    hits = defaultdict(lambda: defaultdict(list))
    contents = []
    for block_index, block in enumerate(blocks):
        page = block[0].split(".")[0]
        for locus in block:
            line = tokens(lines[locus], False)
            for i, word in enumerate(line):
                role = "interieur"
                if len(line) == 1:
                    role = "seul"
                elif not i:
                    role = "debut"
                elif i == len(line) - 1:
                    role = "fin"
                key = ((page, block_index) if condition_block else (page,), role)
                classes[key].append(len(contents))
                contents.append(block_index)
                if word in pair:
                    hits[page][word].append(key)
    pieces = {}
    for page, words in hits.items():
        if set(words) != set(pair):
            continue
        u, v = (words[word] for word in pair)
        assert len(u) == len(v) == 1
        first, second = classes[u[0]], classes[v[0]]
        total = len(first) * len(second) - (len(first) if u == v else 0)
        positives = sum(0 < abs(x-y) <= 8 and contents[x] == contents[y] for x in first for y in second)
        pieces[page] = {"emplacements_valides": positives, "emplacements_possibles": total}
    joint = 1 - prod(1 - Fraction(p["emplacements_valides"], p["emplacements_possibles"]) for p in pieces.values())
    return {"par_face": pieces, "fraction_exacte": str(joint), "probabilite": float(joint)}


def main():
    pairs, blocks, raw = inputs()
    mc = json.loads((HERE / "resultats.json").read_text())
    output = {}
    for ed, rows in raw.items():
        output[ed] = {}
        for mode, conditioned in (("par_page", False), ("par_troncon", True)):
            result = exact(blocks, rows, conditioned)
            assert set(result["par_face"]) == {"f106r", "f106v", "f112v"}
            m = mc[ed][mode]
            assert abs(result["probabilite"] - m["fractions"]["fixe"]) < 4 * m["erreurs_types_mc"]["fixe"]
            output[ed][mode] = result
        # With block frequencies fixed, all family hits are confined to blocks
        # holding one pair, with one copy of each member. Blocks shuffle independently.
        eligible = {}
        for b in blocks:
            words = {word for loc in b for word in tokens(rows[loc], False)}
            possible = [pair for pair in pairs if set(pair) <= words]
            if not possible:
                continue
            assert len(possible) == 1
            pair = possible[0]
            result = exact([b], rows, True, pair)
            eligible[b[0]] = {"paire": pair, "fraction_exacte": result["fraction_exacte"]}
        family = 1 - prod(1 - Fraction(p["fraction_exacte"]) for p in eligible.values())
        m = mc[ed]["par_troncon"]
        assert abs(float(family) - m["fractions"]["famille"]) < 4 * m["erreurs_types_mc"]["famille"]
        output[ed]["famille_par_troncon"] = {"admissibles": eligible,
                                             "fraction_exacte": str(family), "probabilite": float(family)}
    print(json.dumps(output, indent=2))
    (HERE / "exacte.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
