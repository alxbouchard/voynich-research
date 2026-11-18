"""Garder les préfixes et suffixes alignés à l'extérieur des séparations douteuses."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from preparer import EVA, V101, FEUILLETS_EXEMPLES, LOCUS, ecrire, simple, tirage


def charger(path):
    brut = path.read_bytes()
    lignes = {}
    for ligne in brut.decode("latin-1").splitlines():
        match = LOCUS.match(ligne)
        if match is None or match["type"] != "P0":
            continue
        ident = match["id"]
        if ident in lignes:
            raise ValueError(f"Locus dupliqué dans {path.name} : {ident}")
        texte = match["texte"].strip().replace("<%>", "").replace("<$>", "")
        raison = None
        if "<" in texte or ">" in texte:
            raison = "chevrons"
        elif texte.endswith("/"):
            raison = "ligne_continuee"
        champs = texte.split(".")
        if not raison and "" in champs:
            raison = "champ_vide"
        lignes[ident] = (int(match["folio"]), champs, raison)
    if not lignes:
        raise ValueError(f"Aucune ligne P0 dans {path.name}")
    return lignes, sha256(brut).hexdigest()


def bornes(champs):
    incertains = [i for i, groupe in enumerate(champs) if any("," in x for x in groupe)]
    if not incertains:
        return len(champs), len(champs)
    return incertains[0], incertains[-1] + 1


def preparer(it_path, zl_path, gc_path, premier_path, sortie):
    it, h_it = charger(it_path)
    zl, h_zl = charger(zl_path)
    gc, h_gc = charger(gc_path)
    brut_premier = premier_path.read_bytes()
    deja = {ligne["id"] for ligne in json.loads(brut_premier)}
    train, reserve, reponses = [], [], {}
    stats = {"train": Counter(), "reserve": Counter()}
    exclus = Counter()
    for ident in sorted(it.keys() | zl.keys() | gc.keys()):
        lignes = [ed.get(ident) for ed in (it, zl, gc)]
        folio = next(l[0] for l in lignes if l is not None)
        en_reserve = tirage("voynich-suites-v1|folio|" + str(folio), 4) == 0
        if folio in FEUILLETS_EXEMPLES:
            exclus["feuillet_exemple_deja_discute"] += 1
            continue
        if en_reserve and ident in deja:
            exclus["ligne_de_reserve_du_premier_essai"] += 1
            continue
        motifs = []
        for nom, ligne in zip(("IT", "ZL", "GC"), lignes):
            if ligne is None:
                motifs.append(nom + "_absent_P0")
            elif ligne[2]:
                motifs.append(nom + "_" + ligne[2])
        if motifs:
            exclus["+".join(motifs)] += 1
            continue
        groupes = [l[1] for l in lignes]
        if len({len(g) for g in groupes}) != 1:
            exclus["nombres_de_champs_differents"] += 1
            continue
        champs = list(zip(*groupes))
        debut, fin = bornes(champs)
        if max(debut, len(champs) - fin) < 3:
            exclus["aucun_segment_de_trois_champs"] += 1
            continue

        compte = stats["reserve" if en_reserve else "train"]
        compte["lignes"] += 1
        compte["positions"] += len(champs)
        compte["lignes_avec_zone_incertaine"] += int(debut < fin)
        compte["champs_dans_zone_incertaine"] += fin - debut
        offset = tirage("voynich-suites-v1|ligne|" + ident, 5)
        mots, masques, corrige = [], [], {}
        for i, (a, b, c) in enumerate(champs):
            incertain = debut <= i < fin
            if incertain:
                a = b = c = None
            else:
                a, b, c = simple(a, EVA), simple(b, EVA), simple(c, V101)
            if en_reserve and i % 5 == offset:
                masques.append(i)
                corrige[str(i)] = [a, b, c]
                mots.append(None)
                compte["masques_dans_zone_incertaine"] += int(incertain)
            else:
                mots.append([a if a == b else None, c])
        compte["masques"] += len(masques)
        ligne = {"id": ident, "folio": folio, "words": mots, "mask": masques}
        if en_reserve:
            reserve.append(ligne)
            reponses[ident] = corrige
        else:
            train.append(ligne)

    for lot, lignes in (("train", train), ("reserve", reserve)):
        stats[lot]["feuillets"] = len({l["folio"] for l in lignes})
    bilan = {
        "sha256": {"IT": h_it, "ZL": h_zl, "GC": h_gc, "premiere_reserve": sha256(brut_premier).hexdigest()},
        "union_locus_P0": len(it.keys() | zl.keys() | gc.keys()),
        "exclusions": exclus, "train": stats["train"], "reserve": stats["reserve"],
        "lignes_dans_premiere_reserve": len(deja),
    }
    sortie.mkdir(parents=True, exist_ok=True)
    for nom, donnees in (("train", train), ("reserve", reserve), ("reponses", reponses),
                         ("extraction", bilan)):
        ecrire(sortie / (nom + ".json"), donnees)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for nom in ("it", "zl", "gc", "premiere_reserve", "sortie"):
        p.add_argument(nom, type=Path)
    args = p.parse_args()
    preparer(args.it, args.zl, args.gc, args.premiere_reserve, args.sortie)
