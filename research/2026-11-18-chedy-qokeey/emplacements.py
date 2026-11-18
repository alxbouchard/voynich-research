"""Enregistrer les emplacements annoncés avant de lire les groupes qui les suivent."""

import argparse
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2026-11-18-suites-masquees"))
from preparer import EVA, V101, FEUILLETS_EXEMPLES, ecrire, simple, tirage
from preparer_local import bornes, charger


SOURCES = ("IT", "ZL", "GC")
FEUILLETS_DE_DECOUVERTE = {81, 82, 103, 112, 113}
ANCRE = ("chedy", "chedy", "1c89")


def lot_du_feuillet(folio):
    if folio in FEUILLETS_EXEMPLES or tirage(f"voynich-suites-v1|folio|{folio}", 4) == 0:
        return "principal"
    return "complement"


def preparer(it_path, zl_path, gc_path, sortie):
    editions = {}
    empreintes = {}
    for nom, chemin in zip(SOURCES, (it_path, zl_path, gc_path)):
        editions[nom], empreintes[nom] = charger(chemin)
    identifiants = set().union(*(edition.keys() for edition in editions.values()))
    lignes, ancres = [], []
    exclusions = Counter()
    effectifs = {lot: Counter(lignes=0, positions=0, feuillets=0, ancres_avec_successeur=0,
                             ancres_en_fin_de_ligne=0) for lot in ("principal", "complement")}
    for ident in sorted(identifiants):
        releves = [editions[nom].get(ident) for nom in SOURCES]
        folio = next(r[0] for r in releves if r is not None)
        if folio in FEUILLETS_DE_DECOUVERTE:
            exclusions["feuillet_de_decouverte"] += 1
            continue
        motifs = []
        for nom, releve in zip(SOURCES, releves):
            if releve is None:
                motifs.append(nom + "_absent_P0")
            elif releve[2]:
                motifs.append(nom + "_" + releve[2])
        if motifs:
            exclusions["+".join(motifs)] += 1
            continue
        groupes = [r[1] for r in releves]
        if len({len(g) for g in groupes}) != 1:
            exclusions["nombres_de_champs_differents"] += 1
            continue

        champs = list(zip(*groupes))
        debut, fin = bornes(champs)
        lot = lot_du_feuillet(folio)
        compte = effectifs[lot]
        compte["lignes"] += 1
        compte["positions"] += len(champs)
        compte["lignes_avec_espace_incertain"] += int(debut < fin)
        compte["positions_dans_zone_incertaine"] += fin - debut
        mots = []
        for rang, (it, zl, gc) in enumerate(champs):
            if debut <= rang < fin:
                mot = (None, None, None)
            else:
                mot = (simple(it, EVA), simple(zl, EVA), simple(gc, V101))
            mots.append(mot)
            if mot == ANCRE:
                if rang + 1 == len(champs):
                    compte["ancres_en_fin_de_ligne"] += 1
                else:
                    # La décision n'accède à aucun caractère du champ suivant.
                    ancres.append({"id": ident, "folio": folio, "lot": lot, "i": rang + 1})
                    compte["ancres_avec_successeur"] += 1
        lignes.append({"id": ident, "folio": folio, "lot": lot, "words": mots})

    for lot, compte in effectifs.items():
        compte["feuillets"] = len({l["folio"] for l in lignes if l["lot"] == lot})
    bilan = {
        "sha256": empreintes, "union_locus_P0": len(identifiants),
        "locus_P0_par_source": {nom: len(releves) for nom, releves in editions.items()},
        "feuillets_de_decouverte_exclus": sorted(FEUILLETS_DE_DECOUVERTE),
        "exclusions": exclusions, "lots": effectifs,
        "indice_i": "rang cible en base zéro dans la ligne, juste après l'ancre",
    }
    sortie.mkdir(mode=0o700, parents=True, exist_ok=True)
    ecrire(sortie / "ancres.json", ancres)
    ecrire(sortie / "extraction.json", bilan)
    ecrire(sortie / "lignes.json", lignes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for nom in ("it", "zl", "gc", "sortie"):
        parser.add_argument(nom, type=Path)
    args = parser.parse_args()
    preparer(args.it, args.zl, args.gc, args.sortie)
