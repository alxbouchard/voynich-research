"""Recompter les autres finales en m dans les rangées déjà cotées, sans ajouter de votes."""
from collections import Counter, defaultdict
import json
from pathlib import Path
from corpus_dam import HERE, save

PREVIOUS = HERE.parent / "2026-11-18-racines-fourchues"


def category(word):
    if word.endswith("dam") and len(word)>3:
        return "dam"
    if word.endswith("am"):
        return "autres_am"
    if word.endswith("m"):
        return "autres_m"
    return "autre_fin"


def main():
    data = json.loads((PREVIOUS/"RESULTATS.json").read_bytes())["fragments"]
    stats = defaultdict(Counter)
    rows = []
    for row in data:
        value = row["commun"]
        if row["attache"]!="ordre_documente" or not value or len(value)!=1:
            continue
        a,b = row["votes"]
        tag = category(value[0])
        group = a if a==b and a in "YSM" else "indetermine"
        stats[row["lot"]+"/"+tag][group] += 1
        rows.append([row["fragment"],row["page"],value[0],tag,group])
    save("ETIQUETTES.json",{"detail":rows,"lots":stats})


if __name__=="__main__":
    main()
