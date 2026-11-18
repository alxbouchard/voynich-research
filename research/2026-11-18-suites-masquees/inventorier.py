"""Cataloguer les triplets répétés et tous leurs loci dans le seul lot d'apprentissage."""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


def catalogue(lignes, croise):
    index = defaultdict(list)
    for ligne in lignes:
        if ligne["mask"]:
            raise ValueError("L'entrée contient des masques réservés au contrôle.")
        for i0 in range(len(ligne["words"]) - 2):
            trois = ligne["words"][i0:i0 + 3]
            if any(mot is None or mot[0] is None for mot in trois):
                continue
            if croise and any(mot[1] is None for mot in trois):
                continue
            cle = tuple(tuple(mot) if croise else mot[0] for mot in trois)
            index[cle].append({"folio": ligne["folio"], "id": ligne["id"], "debut_i0": i0})

    repetes = []
    for cle, positions in index.items():
        feuilles = sorted({lieu["folio"] for lieu in positions})
        if len(feuilles) >= 2:
            repetes.append({
                "groupes": cle, "folios": feuilles,
                "n_folios": len(feuilles), "n_occurrences": len(positions),
                "positions": positions,
            })
    return sorted(repetes, key=lambda entree: (-entree["n_folios"], entree["groupes"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("train", type=Path)
    parser.add_argument("sortie", type=Path)
    args = parser.parse_args()
    entree = args.train.read_bytes()
    lignes = json.loads(entree)
    rapport = {
        "sha256_train": sha256(entree).hexdigest(),
        "convention": "debut_i0 est l'indice du premier groupe du triplet, à partir de zéro dans le locus id.",
        "eva": catalogue(lignes, False),
        "croise": catalogue(lignes, True),
    }
    args.sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
