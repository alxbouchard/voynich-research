"""Sensibilité à une seule lecture concurrente de la légende des rosettes fRos.45."""
import argparse
from collections import defaultdict
from dataclasses import replace
import json
from pathlib import Path

from compter import DATA, ED, HERE, load, rosettes


LOCUS = "fRos.45"
FORMS = (("otchdy","otoldy"),("oteedy","otoldy"))
PAIRS = {*FORMS, *(word[::-1] for word in FORMS)}


def measure(rows):
    locations = defaultdict(list)
    for row in rows:
        for i, pair in enumerate(zip(row.words, row.words[1:])):
            if i+1 not in row.gaps and pair in PAIRS:
                locations[pair].append([row.locus, i+1, row.kind])
    labels = rosettes(rows)
    return {
        "lieux_paires": {".".join(pair):locations[pair] for pair in sorted(PAIRS)},
        "lignes_du_dépliant": labels["fRos_lignes"],
        "étiquettes_de_deux_mots": labels["étiquettes_de_deux_mots_lisibles"],
        "reprises_dans_la_prose_botanique": labels["étiquettes_avec_reprise_en_prose_botanique"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sortie",type=Path,default=HERE/"VARIANTE_ROSETTE.json")
    args = parser.parse_args()
    out = {}
    for ed, filename in ED.items():
        modes = out[ed] = {}
        for separated, name in ((True,"séparés"),(False,"joints")):
            rows = list(load(DATA/filename, separated))
            run = modes[name] = {"édition":measure(rows)}
            local = [r for r in rows if r.locus == LOCUS]
            if not local:
                assert ed == "H"
                run["variante"] = None
                continue
            assert len(local)==1 and tuple(local[0].words)==FORMS[0] and not local[0].gaps
            changed = [replace(r,words=list(FORMS[1])) if r.locus == LOCUS else r for r in rows]
            run["variante"] = measure(changed)
    args.sortie.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')


if __name__ == "__main__":
    main()
