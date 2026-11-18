"""Contrôler les positions scellées, puis mesurer le succès de chaque annonce."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re

from emplacements import ANCRE, FEUILLETS_DE_DECOUVERTE, SOURCES, lot_du_feuillet
from hasard import mesurer


CIBLE = ("qokeey", "qokeey", "4ohC9")
LOTS = ("principal", "complement")


def verifier_locus(lieu, folio, lot):
    ref = re.fullmatch(r"f([0-9]+)[rv][A-Za-z0-9]*\.[0-9]+", lieu)
    if (not ref or type(folio) is not int or int(ref[1]) != folio
            or folio in FEUILLETS_DE_DECOUVERTE or lot != lot_du_feuillet(folio)):
        raise ValueError(f"Locus, feuillet ou lot hors protocole : {lieu}")


def ouvrir_annonces(path, sceau):
    brut = path.read_bytes()
    if sha256(brut).hexdigest() != sceau.lower():
        raise ValueError("Le fichier d'annonces ne correspond pas à l'empreinte scellée.")
    objet = json.loads(brut)
    if tuple(objet["ancre"]) != ANCRE or tuple(objet["cible"]) != CIBLE:
        raise ValueError("Graphies annoncées différentes du protocole.")
    lieux = {lot: set() for lot in LOTS}
    for annonce in objet["annonces"]:
        if set(annonce) != {"id", "folio", "lot", "i"}:
            raise ValueError("Champs inattendus dans les annonces.")
        ident, folio, lot, i = (annonce[k] for k in ("id", "folio", "lot", "i"))
        verifier_locus(ident, folio, lot)
        if type(i) is not int or i < 1 or (ident, i) in lieux[lot]:
            raise ValueError(f"Indice cible invalide ou dupliqué : {ident}/{i}")
        lieux[lot].add((ident, i))
    return lieux


def verifier_lignes(lignes, annonces):
    vues = set()
    retrouvees = {lot: set() for lot in LOTS}
    for ligne in lignes:
        ident, folio, lot, mots = (ligne[k] for k in ("id", "folio", "lot", "words"))
        verifier_locus(ident, folio, lot)
        if ident in vues:
            raise ValueError(f"Ligne dupliquée : {ident}")
        vues.add(ident)
        for i, mot in enumerate(mots):
            if len(mot) != 3:
                raise ValueError(f"Nombre de relevés incorrect : {ident}/{i}")
            for forme, motif in zip(mot, (r"[a-z]+", r"[a-z]+", r"[A-Za-z0-9]+")):
                if forme is not None and not re.fullmatch(motif, forme):
                    raise ValueError(f"Graphie non canonique dans les entrées : {ident}/{i}")
            if i + 1 < len(mots) and tuple(mot) == ANCRE:
                retrouvees[lot].add((ident, i + 1))
    if retrouvees != annonces:
        raise ValueError("Les positions scellées diffèrent des ancres suivies d'un groupe.")


def incertitude(mot):
    manquants = [nom for nom, valeur in zip(SOURCES, mot) if valeur is None]
    if manquants:
        return "lecture_non_disponible_" + "_".join(manquants)
    it, zl, gc = mot
    if it != zl:
        return "desaccord_entre_releves_EVA"
    if (it == ANCRE[0]) != (gc == ANCRE[2]):
        return "desaccord_sur_statut_chedy"
    if (it == CIBLE[0]) != (gc == CIBLE[2]):
        return "desaccord_sur_statut_qokeey"
    return None


def bilan(lignes, annonces):
    index = {l["id"]: l for l in lignes}
    def ordre(position):
        ident, i = position
        face, numero = ident.rsplit(".", 1)
        return index[ident]["folio"], face, int(numero), i

    par_feuillet = defaultdict(Counter)
    par_releve = {nom: Counter(lisibles=0, conformes=0) for nom in SOURCES}
    details = []
    for lieu, i in sorted(annonces, key=ordre):
        ligne = index[lieu]
        mot = ligne["words"][i]
        motif = incertitude(mot)
        etat = "indetermine" if motif else ("succes" if tuple(mot) == CIBLE else "echec")
        folio = ligne["folio"]
        par_feuillet[folio][etat] += 1
        for nom, lu, attendu in zip(SOURCES, mot, CIBLE):
            par_releve[nom]["lisibles"] += int(lu is not None)
            par_releve[nom]["conformes"] += int(lu == attendu)
        details.append({"id": lieu, "folio": folio, "rang_cible_base_1": i + 1,
                        "lectures": dict(zip(SOURCES, mot)), "etat": etat, "raison": motif})

    def resume(c):
        return {"annonces": sum(c.values()), "verifiables": c["succes"] + c["echec"],
                "succes": c["succes"], "echecs": c["echec"], "indeterminees": c["indetermine"]}

    total = resume(sum(par_feuillet.values(), Counter()))
    hasard = {s: mesurer(lignes, annonces, strate=s) for s in ("face", "ligne")}
    for test in hasard.values():
        if (test["annonces_lisibles"], test["succes_observes"]) != (total["verifiables"], total["succes"]):
            raise ValueError("La notation détaillée et le test conditionnel divergent.")
    return {
        **total, "feuillets_avec_annonce": len(par_feuillet),
        "feuillets_avec_succes": sum(c["succes"] > 0 for c in par_feuillet.values()),
        "succes_possibles_sur_toutes_annonces": [total["succes"], total["succes"] + total["indeterminees"]],
        "par_feuillet_avec_annonce": {f: resume(c) for f, c in sorted(par_feuillet.items())},
        "par_releve_sur_les_annonces": par_releve,
        "hasard_par_face": hasard["face"], "hasard_par_ligne": hasard["ligne"],
        "detail": details,
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("annonces", type=Path)
    cli.add_argument("sceau")
    cli.add_argument("lignes_privees", type=Path)
    cli.add_argument("resultats", type=Path)
    args = cli.parse_args()
    annonces = ouvrir_annonces(args.annonces, args.sceau)
    brut = args.lignes_privees.read_bytes()
    lignes = json.loads(brut)
    verifier_lignes(lignes, annonces)
    rapport = {lot: bilan([l for l in lignes if l["lot"] == lot], annonces[lot]) for lot in LOTS}
    rapport["sha256"] = {"annonces": args.sceau.lower(), "lignes_privees": sha256(brut).hexdigest()}
    args.resultats.write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
