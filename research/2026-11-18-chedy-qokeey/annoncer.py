"""Enregistrer la même réponse pour toutes les ancres, sans accès aux successeurs."""

import argparse
import json
from pathlib import Path


def annoncer(ancres):
    annonces = []
    positions = set()
    for item in ancres:
        if set(item) != {"id", "folio", "lot", "i"}:
            raise ValueError("Une ancre contient un champ imprévu.")
        position = (item["id"], item["i"])
        if position in positions or type(item["i"]) is not int or item["i"] < 1:
            raise ValueError(f"Rang dupliqué ou invalide : {position}")
        positions.add(position)
        annonces.append(item)
    annonces.sort(key=lambda a: (a["folio"], a["id"], a["i"]))
    return {"ancre": ["chedy", "chedy", "1c89"], "cible": ["qokeey", "qokeey", "4ohC9"],
            "annonces": annonces}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ancres", type=Path)
    parser.add_argument("sortie", type=Path)
    args = parser.parse_args()
    document = annoncer(json.loads(args.ancres.read_bytes()))
    args.sortie.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
