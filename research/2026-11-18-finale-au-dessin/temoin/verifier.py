"""Vérifie la couverture de l'édition et calcule les résultats du dépouillement."""
from collections import Counter
import csv
from pathlib import Path
import re

ICI = Path(__file__).resolve().parent
EDITION = ICI.parents[1] / "2026-11-18-opcheor-paralleles/latin/vers.tsv"


def charger(path):
    with path.open(encoding="utf-8") as source:
        return list(csv.DictReader(source, delimiter="\t"))


def verifier():
    mots = charger(ICI / "mots.tsv")
    bouts = charger(ICI / "bouts.tsv")
    lignes = {int(ligne["vers"]): ligne for ligne in bouts}
    assert len(lignes) == len(bouts) == 53
    attendus = set()
    for vers in charger(EDITION):
        numero = int(vers["rang_du_vers"])
        if numero in lignes:
            tokens = re.findall(r"[A-Za-zÀ-ÿ]+", vers["texte_edite"])
            for index, mot in enumerate(tokens, start=1):
                if mot.lower().endswith("m"):
                    attendus.add((lignes[numero]["folio"], numero, index, mot))
    observes = {(m["folio"], int(m["vers"]), int(m["index_edition"]), m["mot_edition"]) for m in mots}
    assert observes == attendus, (observes - attendus, attendus - observes)
    assert len(mots) == len(observes) == 49
    assert all(m["code"] in {"B", "G", "R", "P", "V"} for m in mots)
    for folio in ("f3r", "f4v"):
        selection = [m for m in mots if m["folio"] == folio]
        repere = max(int(b["x_fin_repere"]) for b in bouts if b["folio"] == folio)
        for position in ("fin", "intérieur"):
            effectifs = Counter(m["code"] for m in selection if m["position_sur_image"] == position)
            marques = sum(effectifs[c] for c in ("B", "R", "G"))
            evaluables = marques + effectifs["P"]
            print(folio, position, dict(effectifs), "B/R/G", f"{marques}/{evaluables}",
                  "hors G", f"{marques-effectifs['G']}/{evaluables-effectifs['G']}")
        for m in selection:
            if m["position_sur_image"] == "fin":
                bande = repere - int(lignes[int(m["vers"])]["x_fin_repere"])
                print(folio, m["vers"], m["forme_vue"], "écart en px à hauteur 1070", bande)


if __name__ == "__main__":
    verifier()
