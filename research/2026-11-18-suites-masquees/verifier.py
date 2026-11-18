"""Ouvrir le corrigé uniquement après contrôle du sceau et du masquage."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import re


MODELES = ("eva", "croise")
GRAINE = 20261118
TIRAGES = 5000


def empreinte(valeur):
    return hashlib.sha256(valeur).hexdigest()


def reste(prefixe, valeur, modulo):
    cle = f"voynich-suites-v1|{prefixe}|{valeur}".encode()
    return int.from_bytes(hashlib.sha256(cle).digest(), "big") % modulo


def forme(valeur, modele):
    if modele == "eva":
        if not isinstance(valeur, str) or not re.fullmatch(r"[a-z]+", valeur):
            raise ValueError(f"Forme EVA invalide {valeur!r}")
        return valeur
    if not isinstance(valeur, list) or len(valeur) != 2:
        raise ValueError(f"Forme croisée invalide {valeur!r}")
    eva, gc = valeur
    if not isinstance(gc, str) or not re.fullmatch(r"[A-Za-z0-9]+", gc):
        raise ValueError(f"Forme v101 invalide {gc!r}")
    return forme(eva, "eva"), gc


def valider_reserve(reserve):
    """Vérifier les centres et le partage en feuillets sans lire les réponses."""
    lignes = {}
    for ligne in reserve:
        if set(ligne) != {"id", "folio", "words", "mask"}:
            raise ValueError("Champs inattendus dans une ligne de réserve")
        lieu, folio, mots = ligne["id"], ligne["folio"], ligne["words"]
        if lieu in lignes or reste("folio", folio, 4) != 0:
            raise ValueError(f"Ligne dupliquée ou feuillet hors réserve {lieu}")
        debut = reste("ligne", lieu, 5)
        masques = list(range(debut, len(mots), 5))
        if ligne["mask"] != masques or any(mots[i] is not None for i in masques):
            raise ValueError(f"Masques incomplets ou valeurs de cible accessibles {lieu}")
        lignes[lieu] = ligne
    return lignes


def valider_annonces(lignes, document):
    propositions = {}
    for modele in MODELES:
        base = document["temoins"][modele]
        if base is not None:
            forme(base, modele)
        table = {}
        for annonce in document[modele]:
            lieu, i = annonce["id"], annonce["i"]
            if (lieu not in lignes or type(i) is not int or i not in lignes[lieu]["mask"]
                    or (lieu, i) in table or not annonce["preuves"]):
                raise ValueError(f"Annonce dupliquée, non masquée ou sans preuve {modele} {lieu}/{i}")
            table[lieu, i] = forme(annonce["predit"], modele)
        if table and base is None:
            raise ValueError(f"Réponse de fréquence absente pour {modele}")
        propositions[modele] = table
    return propositions


def valider_corrige(lignes, corrige):
    lieux_attendus = {lieu for lieu, l in lignes.items() if l["mask"]}
    if not lieux_attendus <= set(corrige) <= set(lignes):
        raise ValueError("Lignes du corrigé incompatibles avec les masques")
    for lieu, ligne in lignes.items():
        contenu = corrige.get(lieu, {})
        if set(contenu) != {str(i) for i in ligne["mask"]}:
            raise ValueError(f"Cibles du corrigé incompatibles {lieu}")
        for triple in contenu.values():
            if not isinstance(triple, list) or len(triple) != 3:
                raise ValueError(f"Corrigé invalide {lieu}")
            for code, motif in zip(triple, (r"[a-z]+", r"[a-z]+", r"[A-Za-z0-9]+")):
                if code is not None and (not isinstance(code, str) or not re.fullmatch(motif, code)):
                    raise ValueError(f"Composante du corrigé invalide {lieu}")


def attendu(triple, modele):
    it, zl, gc = triple
    if not it or it != zl:
        return None
    if modele == "eva":
        return it
    return (it, gc) if gc else None


def classe(i, longueur):
    if i == 0:
        return "debut"
    return "fin" if i == longueur - 1 else "interieur"


def permutations(lignes, oracle, annonces, score):
    strates = defaultdict(list)
    for position, terme in oracle.items():
        lieu, i = position
        cle = (lieu.rsplit(".", 1)[0], classe(i, len(lignes[lieu]["words"])))
        strates[cle].append((terme, annonces.get(position)))
    fixe, mobiles = 0, []
    strates_utiles, strates_fixes, annonces_fixes = 0, 0, 0
    theorie = 0.0
    n_annonces = 0
    for population in strates.values():
        actifs = [(i, prop) for i, (_, prop) in enumerate(population) if prop is not None]
        if not actifs:
            continue
        strates_utiles += 1
        n_annonces += len(actifs)
        valeurs = [terme for terme, _ in population]
        effectifs = Counter(valeurs)
        theorie += sum(effectifs[prop] / len(valeurs) for _, prop in actifs)
        if len(effectifs) == 1:
            strates_fixes += 1
            annonces_fixes += len(actifs)
            fixe += sum(prop == valeurs[0] for _, prop in actifs)
        else:
            mobiles.append((valeurs, actifs))
    hist = Counter()
    rng = random.Random(GRAINE)
    if n_annonces:
        for _ in range(TIRAGES):
            succes = fixe
            for valeurs, actifs in mobiles:
                melange = valeurs.copy()
                rng.shuffle(melange)
                succes += sum(melange[i] == prop for i, prop in actifs)
            hist[succes] += 1
    return {
        "graine": GRAINE, "tirages": sum(hist.values()),
        "strates_lisibles": len(strates), "strates_avec_annonce": strates_utiles,
        "strates_avec_annonce_immobiles": strates_fixes, "annonces_strates_immobiles": annonces_fixes,
        "esperance_exacte": theorie if n_annonces else None,
        "moyenne": sum(s * n for s, n in hist.items()) / TIRAGES if n_annonces else None,
        "p_ge_corrige": (1 + sum(n for s, n in hist.items() if s >= score)) / (1 + TIRAGES) if n_annonces else None,
        "histogramme": dict(sorted(hist.items())),
    }


def noter(modele, lignes, corrige, annonces, baseline):
    base = forme(baseline, modele) if baseline is not None else None
    oracle = {}
    masques = sum(len(l["mask"]) for l in lignes.values())
    for lieu, ligne in lignes.items():
        for i in ligne["mask"]:
            cible = attendu(corrige[lieu][str(i)], modele)
            if cible is not None:
                oracle[lieu, i] = cible
    notes = []
    for position, annonce in annonces.items():
        lieu, i = position
        reponse = oracle.get(position)
        note = {"id": lieu, "i": i, "folio": lignes[lieu]["folio"], "predit": annonce,
                "lectures": corrige[lieu][str(i)], "attendu": reponse,
                "exact": annonce == reponse if reponse is not None else None,
                "base_exacte": base == reponse if reponse is not None else None}
        if modele == "croise":
            it, zl, gc = note["lectures"]
            note["eva_exacte"] = annonce[0] == it if it and it == zl else None
            note["v101_exacte"] = annonce[1] == gc if gc is not None else None
        notes.append(note)
    evaluables = [note for note in notes if note["exact"] is not None]
    score = sum(note["exact"] for note in evaluables)
    base_score = sum(note["base_exacte"] for note in evaluables)
    return {
        "masques": masques, "lisibles": len(oracle), "annonces": len(notes),
        "annonces_verifiables": len(evaluables), "indeterminees": len(notes) - len(evaluables),
        "exactes": score, "erreurs": len(evaluables) - score,
        "abstentions": masques - len(notes), "abstentions_sur_lisibles": len(oracle) - len(evaluables),
        "folios_avec_masque": len({l["folio"] for l in lignes.values() if l["mask"]}),
        "folios_annonces": len({n["folio"] for n in notes}),
        "folios_verifiables": len({n["folio"] for n in evaluables}),
        "folios_avec_succes": len({n["folio"] for n in evaluables if n["exact"]}),
        "base_frequente": base, "base_exactes": base_score,
        "permutations": permutations(lignes, oracle, annonces, score), "detail": notes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for nom in ("reserve", "reponses", "annonces", "sceau", "resultats"):
        parser.add_argument(nom, type=str if nom == "sceau" else Path)
    args = parser.parse_args()
    brut = args.annonces.read_bytes()
    if empreinte(brut) != args.sceau.lower():
        parser.error("Le sceau SHA-256 des annonces ne concorde pas")
    document = json.loads(brut)
    cas = args.reserve.read_bytes()
    lignes = valider_reserve(json.loads(cas))
    propositions = valider_annonces(lignes, document)
    reponses = args.reponses.read_bytes()
    corrige = json.loads(reponses)
    valider_corrige(lignes, corrige)
    resultats = {m: noter(m, lignes, corrige, propositions[m], document["temoins"][m]) for m in MODELES}
    resultats["sha256"] = {"reserve": empreinte(cas), "annonces": empreinte(brut), "reponses": empreinte(reponses)}
    args.resultats.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
