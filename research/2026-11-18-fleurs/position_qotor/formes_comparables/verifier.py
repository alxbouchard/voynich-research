"""Vérification indépendante des positions EVA de qotor et des formes de comparaison."""
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re


def inventaire(path, meme_main=False):
    positions = defaultdict(list)
    face = None
    lignes = lisibles = premieres = 0
    for ligne in path.read_text().splitlines():
        if not ligne.startswith("<f"):
            continue
        address, body = ligne[1:].split(">", 1)
        if "," not in address:
            feuille = re.fullmatch(r"f(\d+)[rv]\d*", address)
            champs = {k: v for k, v in re.findall(r"\$([A-Z])=([^\s>]+)", body)}
            face = address if feuille and int(feuille[1]) >= 25 and champs.get("I") == "H" else None
            if meme_main and (champs.get("H"), champs.get("L")) != ("1", "A"):
                face = None
            continue
        if not face:
            continue
        locus, type_position = address.split(",", 1)
        if type_position[1:] != "P0" or type_position.startswith("!"):
            continue
        assert locus.startswith(face + ".")
        texte = re.sub(r"<![^>]*>", "", body).strip()
        texte = texte.replace("<->", ".").replace("<~>", ".").replace("<%>", "").replace("<$>", "")
        texte = texte.replace("!", "").replace(",", "")
        groupes = [s for s in texte.split(".") if s]
        lignes += 1
        for rang, mot in enumerate(groupes, start=1):
            if not re.fullmatch("[a-z]+", mot):
                continue
            lisibles += 1
            if rang == 1:
                premieres += 1
            if len(mot) == 5 and mot.startswith("qo"):
                positions[mot].append((locus, rang))
    return positions, {"lignes": lignes, "lisibles": lisibles, "premieres_lisibles": premieres}


def resultats(positions, vol):
    minimum = max(2, (len(positions['qotor']) + 1) // 2)
    maximum = 2 * len(positions['qotor'])
    chiffres = {mot: (sum(r == 1 for _, r in points), len(points))
                for mot, points in positions.items() if minimum <= len(points) <= maximum}
    taux = {mot: Fraction(debut, total) for mot, (debut, total) in chiffres.items()}
    etalon = taux.get('qotor')
    liste = []
    for mot in sorted(taux, key=lambda w: (-taux[w], w)):
        premiers = [l for l, r in positions[mot] if r == 1]
        interieurs = [[l, r] for l, r in positions[mot] if r != 1]
        liste.append({"mot": mot, "debut": chiffres[mot][0], "total": chiffres[mot][1], "fraction": str(taux[mot]),
                      "premiers_lieux": premiers, "autres_exemples": interieurs[:3]})
    return {"occasions": vol, "frequence_min_max": [minimum, maximum], "nombre": len(liste),
            "au_moins_qotor": sum(score >= etalon for score in taux.values()) if etalon is not None else None,
            "egalite_qotor": sum(score == etalon for score in taux.values()) if etalon is not None else None,
            "groupes": liste, "qotor_loci_positions": positions["qotor"]}


def intersection(a, b):
    a, b = set(a), set(b)
    return {"communs": sorted(a & b), "H_seul": sorted(a - b), "ZL_seul": sorted(b - a)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('donnees', type=Path)
    parser.add_argument('sortie', type=Path)
    args = parser.parse_args()
    noms = {'H': 'IT2a-n.txt', 'ZL': 'ZL3b-n.txt'}
    out = {"empreintes": {t: sha256((args.donnees / n).read_bytes()).hexdigest() for t, n in noms.items()}}
    for nom_lot, sous_groupe in [('toutes', False), ('main_1_Currier_A', True)]:
        editions = {e: resultats(*inventaire(args.donnees / n, sous_groupe)) for e, n in noms.items()}
        a, b = [editions[t]['qotor_loci_positions'] for t in noms]
        editions["concordance"] = {
            "premiers": intersection([j for j, r in a if r == 1], [j for j, r in b if r == 1]),
            "lignes_tout_rang": intersection([j for j, r in a], [j for j, r in b]),
            "lignes_et_rangs": intersection(a, b)}
        out[nom_lot] = editions
    args.sortie.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")


if __name__ == '__main__':
    main()
