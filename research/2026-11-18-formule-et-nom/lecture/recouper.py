"""Contrôler directement les motifs des deux mots et du mot suivant, sans tables."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
from phrase import HERE, corpus, windows


def pattern(symbols, width, marker):
    seen = set()
    parts = []
    for sign in symbols.split():
        if sign=="/":
            parts.append(" ")
        elif marker and sign=="ch":
            continue
        elif sign in seen:
            parts.append(f"(?P={sign})")
        else:
            seen.add(sign)
            parts.append(f"(?P<{sign}>[^ ]{{1,{width}}})")
    return re.compile("".join(parts))


if __name__=="__main__":
    data = corpus(Path(sys.argv[1]))
    for marker in (False,True):
        suffix = "-MARQUE" if marker else ""
        results = json.loads((HERE/f"VERIFICATION{suffix}.json").read_text())
        for width in (2,3):
            base="ch o d y / ch e o r"
            double=pattern(base,width,marker)
            triple=pattern(base+" / ch e y",width,marker)
            control=pattern(base+" / ch y e",width,marker)
            for name, sections in data.items():
                counts=Counter()
                for _,i,row in windows(sections):
                    two=" ".join(row[i+1:i+3])
                    three=two+" "+row[i+3]
                    counts["fit_two"] += bool(double.fullmatch(two))
                    counts["predicted_right"] += bool(triple.fullmatch(three))
                    counts["displaced_right"] += bool(control.fullmatch(three))
                expected=results[name][str(width)]["counts"]
                assert all(expected.get(k,0)==v for k,v in counts.items()), (name,width,marker)
    print("20 comparaisons indépendantes des amorces, prédictions et contrôles concordent.")
