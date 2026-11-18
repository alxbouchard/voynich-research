"""Prédire les groupes masqués à partir des seuls triplets d'apprentissage."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


# Indices relatifs des deux voisins, de gauche à droite. Le rang dans ce tuple
# va de la cible en première position à la cible en dernière position.
CADRES = ((1, 2), (-1, 1), (-2, -1))


def mot(entree, modele):
    if entree is None or entree[0] is None:
        return None
    if modele == "eva":
        return entree[0]
    if entree[1] is None:
        return None
    return tuple(entree)


def apprentissage(lignes, modele):
    frequences = Counter()
    occurrences = defaultdict(dict)
    for ligne in lignes:
        mots = [mot(x, modele) for x in ligne["words"]]
        frequences.update(x for x in mots if x is not None)
        for debut in range(len(mots) - 2):
            triple = tuple(mots[debut:debut + 3])
            if None not in triple:
                # Un feuillet a une seule voix, même avec plusieurs répétitions.
                occurrences[triple].setdefault(ligne["folio"], (ligne["id"], debut))
    return frequences, occurrences


def construire_regles(occurrences):
    candidats = defaultdict(list)
    for triple, feuilles in occurrences.items():
        for cible in range(3):
            voisins = triple[:cible] + triple[cible + 1:]
            candidats[cible, voisins].append((len(feuilles), triple))
    regles = {}
    for cle, choix in candidats.items():
        maximum = max(n for n, _ in choix)
        gagnants = [triple for n, triple in choix if n == maximum]
        if maximum >= 2 and len(gagnants) == 1:
            regles[cle] = gagnants[0]
    return regles


def references(feuilles, position):
    resultat = []
    for folio in sorted(feuilles)[:2]:
        identifiant, debut = feuilles[folio]
        resultat.append({"folio": folio, "id": identifiant, "i": debut + position})
    return resultat


def proposer(lignes, modele, regles, occurrences):
    annonces = []
    bilan = Counter(masques=0, sans_regle=0, cadres_en_conflit=0)
    for ligne in lignes:
        mots = [mot(x, modele) for x in ligne["words"]]
        for i in ligne["mask"]:
            bilan["masques"] += 1
            preuves = defaultdict(list)
            for cible, offsets in enumerate(CADRES):
                gauche, droite = (i + k for k in offsets)
                if gauche < 0 or droite >= len(mots):
                    continue
                voisins = (mots[gauche], mots[droite])
                triple = regles.get((cible, voisins))
                if triple is not None:
                    feuilles = occurrences[triple]
                    preuves[triple[cible]].append({
                        "decalages_voisins": offsets,
                        "voisins": voisins,
                        "n_folios": len(feuilles),
                        "attestations_cible": references(feuilles, cible),
                    })
            if len(preuves) == 1:
                prediction, justifications = next(iter(preuves.items()))
                annonces.append({"id": ligne["id"], "i": i, "predit": prediction,
                                 "preuves": justifications})
            elif preuves:
                bilan["cadres_en_conflit"] += 1
            else:
                bilan["sans_regle"] += 1
    return annonces, bilan


def inventaire(frequences, occurrences, regles, bilan):
    repetes = [triple for triple, feuilles in occurrences.items() if len(feuilles) >= 2]
    # Exemples choisis par soutien dans l'apprentissage uniquement.
    repetes.sort(key=lambda t: (-len(occurrences[t]), t))
    exemples = [
        {"groupes": t, "n_folios": len(occurrences[t]),
         "attestations_debut": references(occurrences[t], 0)}
        for t in repetes[:5]
    ]
    return {
        "positions_lisibles_apprentissage": sum(frequences.values()),
        "trigrammes_distincts": len(occurrences),
        "trigrammes_sur_plusieurs_folios": len(repetes),
        "exemples": exemples, "cadres_predictifs": len(regles),
        "bilan_reserve": bilan,
    }


def predire(train, reserve):
    if {l["folio"] for l in train} & {l["folio"] for l in reserve}:
        raise ValueError("Un feuillet est présent dans les deux lots.")
    for ligne in reserve:
        for i in ligne["mask"]:
            if ligne["words"][i] is not None:
                raise ValueError("Une cible demandée est visible.")
    resultats = {"temoins": {}, "inventaire": {}}
    for modele in ("eva", "croise"):
        freq, occurrences = apprentissage(train, modele)
        regles = construire_regles(occurrences)
        annonces, bilan = proposer(reserve, modele, regles, occurrences)
        resultats[modele] = annonces
        # Départage des ex æquo par ordre lexicographique des groupes.
        resultats["temoins"][modele] = min(freq, key=lambda x: (-freq[x], x)) if freq else None
        resultats["inventaire"][modele] = inventaire(freq, occurrences, regles, bilan)
    return resultats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("train", "reserve", "annonces"):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    resultats = predire(json.loads(args.train.read_bytes()), json.loads(args.reserve.read_bytes()))
    args.annonces.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
