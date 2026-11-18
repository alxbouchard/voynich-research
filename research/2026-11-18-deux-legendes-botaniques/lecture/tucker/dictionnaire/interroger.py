"""Interroger le GDN sur les deux listes figées (Python 3, curl, accès réseau)."""

import hashlib
import html
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode

DOSSIER = Path(__file__).resolve().parent
LISTES = DOSSIER.parent / "MOTS-A-VERIFIER.json"
SORTIE = DOSSIER / "resultats.json"
GDN = "https://gdn.iib.unam.mx"
PARAMETRES = {
    "queryPartePalabra": "completa",
    "queryBuscarEn": "nahuatlGrafiaNormalizada",
    "queryLimiteRegistros": "500",
}
TEMOINS = {"positif": "atl", "negatif": "zzzxqvzzzz"}
PERIODES = ("xvie", "xviie_xviiie", "depuis_1801", "date_indeterminee")
CHAINE = r"'((?:\\.|[^'\\])*)'"
CHAMPS = ("pk", "paleografia", "grafiaNormalizada", "traduccion", "fuente")
FICHE = re.compile(r"\{" + ",".join(k + ":" + CHAINE for k in CHAMPS) + r",\},", re.S)


def valeur(texte):
    return html.unescape(re.sub(r"\\(['\"/\\])", r"\1", texte))


def classer(source):
    date, _, nom = source.partition(" ")
    # Par exemple 1551-95 Docs_México, 17?? Bnf_362 et 1780 ? Bnf_361.
    if re.match(r"15\d\d", date) or date == "1600":
        periode = "xvie"
    elif re.match(r"1[67]", date) or date == "1800":
        periode = "xviie_xviiie"
    elif re.match(r"(18|19|20)\d\d", date):
        periode = "depuis_1801"
    else:
        periode = "date_indeterminee"
    return date, nom, periode


def interroger(mot):
    params = {"queryCreiterio": mot, **PARAMETRES}
    url = f"{GDN}/termino/search?{urlencode(params)}"
    curl = subprocess.run(
        ["curl", "--silent", "--show-error", "--location", "--max-time", "45",
         "--retry", "2", "--retry-delay", "4", "--write-out", "\n%{http_code}", url],
        capture_output=True, check=True,
    )
    brut, statut = curl.stdout.rsplit(b"\n", 1)
    texte = brut.decode("utf-8")
    resultat = {
        "url": url, "http": int(statut), "sha256_html": hashlib.sha256(brut).hexdigest(),
        "consulte_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if statut != b"200":
        return {**resultat, "etat": "erreur_http"}
    if "No se han encontrado registros" in texte and "var mydata =" not in texte:
        return {**resultat, "etat": "aucune_fiche", "total": 0}
    tableau = re.search(r"var mydata\s*=\s*\[(.*?)\];\s*craearGrid\(mydata\)", texte, re.S)
    if tableau is None:
        raise ValueError(f"{mot}: réponse non reconnue")
    donnees = tableau.group(1)
    fiches = FICHE.findall(donnees)
    if not fiches or FICHE.sub("", donnees).strip():
        raise ValueError(f"{mot}: tableau incomplet ou mal interprété")
    if len(fiches) >= int(PARAMETRES["queryLimiteRegistros"]):
        raise ValueError(f"{mot}: limite potentiellement atteinte")
    entrees = {periode: [] for periode in PERIODES}
    ids = set()
    for colonnes in fiches:
        numero, paleo, graphie, glose, source = map(valeur, colonnes)
        if graphie != mot or numero in ids:
            raise ValueError(f"{mot}: {numero}, graphie inattendue ou doublon")
        ids.add(numero)
        date, nom, periode = classer(source)
        entrees[periode].append({
            "id": numero, "date_gdn": date, "source": nom, "paleographie": paleo,
            "glose_index": glose, "url": f"{GDN}/diccionario/{quote(graphie)}/{numero}",
        })
    return {**resultat, "etat": "fiches", "graphie_normalisee": mot, "total": len(fiches),
            "entrees": {p: fiches for p, fiches in entrees.items() if fiches}}


def synthese(listes, reponses):
    resume = {}
    for nom, mots in listes.items():
        positions = []
        for i, mot in enumerate(mots, start=1):
            graphies = mot["formes_sans_diacritiques"]
            positions.append({
                "position": i, "eva": mot["eva"], "graphies": graphies,
                "graphies_xvie": [
                    g for g in graphies if reponses[g].get("entrees", {}).get("xvie")
                ],
                "erreurs": [g for g in graphies if reponses[g]["etat"] == "erreur_http"],
            })
        chaines = []
        for p in positions:
            if p["graphies_xvie"]:
                i = p["position"]
                if chaines and chaines[-1][-1] == i - 1:
                    chaines[-1].append(i)
                else:
                    chaines.append([i])
        resume[nom] = {"positions": positions, "suites_xvie": chaines}
    return resume


def main():
    listes = json.loads(LISTES.read_text())
    mots = dict.fromkeys(g for sens in listes.values() for mot in sens for g in mot["formes_sans_diacritiques"])
    reponses = {}
    for mot in [*TEMOINS.values(), *mots]:
        if reponses:
            time.sleep(1.4)
        reponses[mot] = interroger(mot)
        print(mot, reponses[mot]["etat"], reponses[mot].get("total", ""), flush=True)
    contenu = {
        "sha256_listes": hashlib.sha256(LISTES.read_bytes()).hexdigest(),
        "parametres_communs": PARAMETRES, "temoins": TEMOINS,
        "reponses": reponses, "comparaison": synthese(listes, reponses),
    }
    SORTIE.write_text(json.dumps(contenu, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
