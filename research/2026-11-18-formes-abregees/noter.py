"""Noter les développements anonymes après vérification du sceau des annonces."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


def lire(chemin):
    brut = chemin.read_bytes()
    return json.loads(brut), sha256(brut).hexdigest()


def insertion(court, long):
    ecart = len(long) - len(court)
    return 1 <= ecart <= 3 and any(
        long[:i] + long[i + ecart:] == court for i in range(len(court) + 1)
    )


def valider_annonces(reserve, annonces):
    index = {ligne["id"]: ligne["words"] for ligne in reserve}
    if len(index) != len(reserve):
        raise ValueError("Identifiant de vers réservé dupliqué.")
    table = {}
    for annonce in annonces:
        lieu = (annonce["id"], annonce["index"])
        mots = index[lieu[0]]
        pos = lieu[1]
        if type(pos) is not int or not 0 < pos < len(mots) - 1:
            raise ValueError(f"Position non intérieure {lieu}.")
        court = mots[pos]
        if len(court) < 2 or court != annonce["observe"] or lieu in table:
            raise ValueError(f"Forme observée, éligibilité ou unicité en défaut {lieu}.")
        for champ in ("predit", "base_frequente"):
            if not isinstance(annonce[champ], str) or not insertion(court, annonce[champ]):
                raise ValueError(f"Expansion invalide {champ} {lieu}.")
        table[lieu] = annonce
    return table


def rapport_compteurs(comptes):
    eligibles = comptes["eligibles"]
    total = comptes["annonces"]
    nombre_abreges = comptes["abreges_editoriaux"]
    colonnes = (
        "eligibles", "abreges_editoriaux", "insertion_editoriale_1_a_3",
        "annonces", "exactes", "erreurs_sur_forme_pleine",
        "erreurs_sur_abreviation", "exactes_identite", "exactes_base_frequente",
    )
    return {
        **{col: comptes[col] for col in colonnes},
        "abstentions": eligibles - total,
        "abstentions_sur_abreviation": nombre_abreges - comptes["exactes"]
        - comptes["erreurs_sur_abreviation"],
        "couverture": total / eligibles if eligibles else None,
        "precision": comptes["exactes"] / total if total else None,
        "rappel_abreges_editoriaux": comptes["exactes"] / nombre_abreges if nombre_abreges else None,
    }


def noter(reserve, corrige, table, temoin):
    if set(corrige) != {ligne["id"] for ligne in reserve}:
        raise ValueError("Les identifiants de la réserve et du corrigé diffèrent.")
    par_passus = defaultdict(Counter)
    formes = set()
    exemples = defaultdict(list)
    for ligne in reserve:
        identifiant = ligne["id"]
        observe = ligne["words"]
        oracles = corrige[identifiant]
        if len(oracles) != len(observe):
            raise ValueError(f"Longueur différente dans le vers {identifiant}.")
        comptes = par_passus[ligne["passus"]]
        for pos in range(1, len(observe) - 1):
            court = observe[pos]
            if len(court) < 2:
                continue
            attendu = oracles[pos]
            abrege = court != attendu
            comptes["eligibles"] += 1
            comptes["abreges_editoriaux"] += abrege
            comptes["insertion_editoriale_1_a_3"] += insertion(court, attendu)
            annonce = table.get((identifiant, pos))
            if annonce is None:
                continue
            formes.add(court)
            comptes["annonces"] += 1
            comptes["exactes_identite"] += court == attendu
            comptes["exactes_base_frequente"] += annonce["base_frequente"] == attendu
            if annonce["predit"] == attendu:
                categorie = "exactes"
            elif abrege:
                categorie = "erreurs_sur_abreviation"
            else:
                categorie = "erreurs_sur_forme_pleine"
            comptes[categorie] += 1
            if len(exemples[categorie]) < 4:
                exemples[categorie].append({**annonce, "attendu": attendu})

    total = sum(par_passus.values(), Counter())
    annonces = total["annonces"]
    if annonces != len(table):
        raise ValueError("Au moins une annonce n’a pas été notée.")
    n_temoin = temoin["eligibles"]
    faux = temoin["fausses_expansions"]
    if (type(n_temoin) is not int or type(faux) is not int
            or not 0 <= faux <= n_temoin or temoin["annonces"] != faux):
        raise ValueError("Témoin sans message incohérent.")
    n_passus = sum(c["annonces"] > 0 for c in par_passus.values())
    criteres = {
        "au_moins_20_annonces": annonces >= 20,
        "au_moins_3_passus_avec_annonce": n_passus >= 3,
        "au_moins_5_formes_courtes": len(formes) >= 5,
        "precision_au_moins_80_pct": annonces > 0 and total["exactes"] * 5 >= 4 * annonces,
        "depasse_identite": total["exactes"] > total["exactes_identite"],
        "depasse_base_frequente": total["exactes"] > total["exactes_base_frequente"],
        "temoin_au_plus_1_pct": n_temoin > 0 and faux * 100 <= n_temoin,
    }
    return {
        "total": rapport_compteurs(total),
        "par_passus": {p: rapport_compteurs(c) for p, c in sorted(par_passus.items())},
        "passus_avec_annonce": n_passus,
        "formes_courtes_distinctes_annoncees": len(formes),
        "temoin": {"eligibles": n_temoin, "fausses_expansions": faux,
                   "taux": faux / n_temoin if n_temoin else None},
        "exemples": exemples,
        "criteres": criteres,
        "calibration_reussie": all(criteres.values()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for nom in ("reserve", "corrige", "annonces", "temoin", "sceau", "sortie"):
        parser.add_argument(nom, type=str if nom == "sceau" else Path)
    args = parser.parse_args()
    reserve, h_reserve = lire(args.reserve)
    annonces, h_annonces = lire(args.annonces)
    if h_annonces != args.sceau.lower():
        parser.error("L’empreinte des annonces ne concorde pas avec le sceau.")
    table = valider_annonces(reserve, annonces)
    temoin, h_temoin = lire(args.temoin)
    corrige, h_corrige = lire(args.corrige)
    bilan = noter(reserve, corrige, table, temoin)
    bilan["sha256"] = {"reserve": h_reserve, "annonces": h_annonces,
                       "corrige": h_corrige, "temoin": h_temoin}
    args.sortie.write_text(json.dumps(bilan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
