"""Chiffrer deux composés réels du Gart, puis les identifier sans fournir la clé."""
import json

from essayer import HERE, segment, extend


def generator(names):
    # Ces alphabets servent uniquement au générateur.
    units = {"d": "wu", "a": "r", "r": "tz"}
    rest = iter("bfgjkmnopsuvxyz")
    words = []
    for name in names:
        i = 0
        cipher = []
        while i < len(name):
            matched = next(((g, s) for g, s in units.items() if name.startswith(s, i)), None)
            if matched is None:
                matched = next(rest), name[i]
                units[matched[0]] = matched[1]
            glyph, chars = matched
            cipher.append(glyph)
            i += len(chars)
        words.append("".join(cipher))
    return words


def solve(root, core, encrypted, candidates):
    starts = list(extend(segment(core), root, 2, {}))
    result = []
    for first in candidates:
        for start in starts:
            for partial in extend(segment(encrypted[0]), first, 2, start):
                for other in candidates:
                    if first == other:
                        continue
                    for key in extend(segment(encrypted[1]), other, 2, partial):
                        result.append({"premier":first, "second":other, "table":key})
    return result


if __name__ == "__main__":
    data = json.loads((HERE / "RESULTATS.json").read_bytes())
    carriers = data["corpus"]["RIDGES"]["concepts"]["racine"]["wurtz"]["porteurs"]
    true_pair = ["epichwurtzel", "petersilgwurtzel"]
    hidden = generator(["wurtz", *true_pair])
    solution = solve("wurtz", hidden[0], hidden[1:], list(carriers))
    assert hidden[0] == "dar"
    assert {(r["premier"],r["second"]) for r in solution} == {tuple(true_pair)}
    print(json.dumps({"controle_apres_recherche":True,"base": "wurtz",
                      "chiffres":hidden,"porteurs":sorted(carriers),"solutions":solution},
                     indent=1,ensure_ascii=False))
