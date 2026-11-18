"""Vérifie indépendamment les emplacements et le témoin avec les répétitions capturées en regex."""
import json
from pathlib import Path
import re
import sys

from lecture import HERE, SOURCES, load_all


def pattern(template, width):
    seen = set()
    parts = []
    for token in template.split():
        if token == "/":
            parts.append(" ")
        elif token in seen:
            parts.append("(?P=" + token + ")")
        else:
            parts.append("(?P<" + token + ">[^ ]{1,%d})" % width)
            seen.add(token)
    return re.compile("".join(parts))


if __name__ == "__main__":
    corpora = load_all(Path(sys.argv[1]), SOURCES / "RIDGES.json")
    predictions = json.loads((HERE/"PREDICTIONS.json").read_text())
    control = json.loads((HERE/"TEMOIN-LEXIQUE.json").read_text())
    for name, groups in predictions.items():
        for g in groups:
            width, edition = g["width"], g["edition"]
            third = "sh e o r" if edition == "H" else "sh o a r"
            full = pattern("d a r / ch e o r / " + third, width)
            pair = pattern("d a r / ch e o r", width)
            found = set()
            pairs = 0
            for section, row in corpora[name].items():
                for i in range(1,len(row)-1):
                    if pair.fullmatch(" ".join(row[i-1:i+1])):
                        pairs += 1
                    if full.fullmatch(" ".join(row[i-1:i+2])):
                        found.add((section,i))
            assert found == {(r["section"],r["center"]) for r in g["records"]}
            assert pairs == g["pair"]
    for name, widths in control.items():
        for w, record in widths.items():
            full = pattern("ch e o r / ch e e k e y", int(w))
            found = {(section, i) for section,row in corpora[name].items()
                     for i in range(len(row)-1) if full.fullmatch(" ".join(row[i:i+2]))}
            assert found == {(r["section"],r["position"]) for r in record["occurrences"]}
    print("16 séries de triplets et 4 séries de couples concordent.")
