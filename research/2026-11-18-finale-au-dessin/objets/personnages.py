"""Éprouver le mot sélectionné dans les bains sur le corpus de légendes et sur le latin."""
from collections import Counter
from pathlib import Path
import json
import re
import sys

from comparer import MACER, RESEARCH, classes

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH / "2026-11-18-carte-sept-etoiles/lecture"))
from essai import tables
sys.path.insert(0, str(RESEARCH / "2026-11-18-opcheor-paralleles/variantes"))
from compter import corpus, runs

TARGETS = ("otoly", "otedy")


def item_index():
    records = classes()
    return {kind: {"n": len(labels), **{w: [loc for loc, word in labels.items() if word == w]
                                         for w in TARGETS}} for kind, labels in records.items()}


def line_index():
    editions, _ = corpus()
    output = {}
    for kind in sorted(classes()):
        views = {}
        for edition, rows in editions.items():
            for cut in ("joints", "separes"):
                view = {}
                for loc, (_, code, _, raw) in rows.items():
                    if code != kind:
                        continue
                    raw = re.sub(r"\{[^}]*\}", "?", raw)
                    view[loc] = {w for span in runs(raw, cut) for _, w in span}
                views[f"{edition}-{cut}"] = view
        loci = sorted(set.union(*(set(v) for v in views.values())))
        views["accord"] = {loc: set.intersection(*(v.get(loc, set()) for v in views.values())) for loc in loci}
        output[kind] = {
            name: {"lignes": len(view), "avec_groupe_lisible": sum(map(bool, view.values())),
                   **{w: [loc for loc in sorted(view) if w in view[loc]] for w in TARGETS}}
            for name, view in views.items()
        }
    return output


def latin():
    frequency = Counter(word for body in json.loads(MACER.read_text()).values() for word in body)
    paradigms = {"femina": "femina feminae feminam feminarum feminis feminas",
                 "mulier": "mulier mulieris mulieri mulierem muliere mulieres mulierum mulieribus"}
    control = list(tables("otoly", "abacum", 3))
    assert {"o": "a", "t": "b", "l": "c", "y": "um"} in control
    readings = {}
    for form in " ".join(paradigms.values()).split():
        if frequency[form]:
            readings[form] = {"occurrences": frequency[form],
                              "tables": {w: list(tables(w, form, 3)) for w in TARGETS}}
    return {"paradigmes": paradigms, "attestations": readings, "controle_abacum": control}


def main():
    result = {"un_mot": item_index(), "toutes_lignes": line_index(), "latin": latin()}
    (HERE / "OTOLY.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for kind, views in result["toutes_lignes"].items():
        print(kind, result["un_mot"][kind], views["accord"])
    print({k: (v["occurrences"], {w: len(t) for w, t in v["tables"].items()})
           for k, v in result["latin"]["attestations"].items()})


if __name__ == "__main__":
    main()
