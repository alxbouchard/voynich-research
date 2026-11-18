"""Annoncer une forme longue dans un cadre attesté, sur des signes anonymes."""

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


def formes_courtes(longue):
    """Toutes les formes obtenues en enlevant un seul segment de 1 à 3 signes."""
    return {
        longue[:debut] + longue[debut + taille:]
        for taille in range(1, min(3, len(longue) - 2) + 1)
        for debut in range(len(longue) - taille + 1)
    }


def positions(vers):
    mots = vers["words"]
    for i in range(1, len(mots) - 1):
        if len(mots[i]) >= 2:
            yield i, (mots[i - 1], mots[i + 1]), mots[i]


class Modele:
    def __init__(self, apprentissage):
        frequences = Counter()
        self.cadres = defaultdict(set)
        for vers in apprentissage:
            frequences.update(vers["words"])
            for _, cadre, centre in positions(vers):
                self.cadres[cadre].add(centre)

        # La première forme dans l'ordre fixé est la base sans contexte.
        self.bases = {}
        self.expansions = defaultdict(set)
        for longue in sorted(frequences, key=lambda mot: (-frequences[mot], mot)):
            for courte in formes_courtes(longue):
                self.bases.setdefault(courte, longue)
                self.expansions[courte].add(longue)

    def base_frequente(self, courte):
        return self.bases.get(courte)

    def annonces(self, reserve):
        for vers in reserve:
            for i, cadre, courte in positions(vers):
                formes = self.cadres.get(cadre)
                if not formes or courte not in formes:
                    continue
                choix = formes.intersection(self.expansions.get(courte, ()))
                if len(choix) == 1:
                    yield {"id": vers["id"], "index": i, "observe": courte,
                           "predit": choix.pop(), "base_frequente": self.base_frequente(courte)}


def copie_modifiee(vers_anterieurs, alphabet, rng):
    insertion = rng.random() < 0.5
    while True:
        mots = list(rng.choice(vers_anterieurs)["words"])
        indices = list(range(len(mots))) if insertion else [i for i, m in enumerate(mots) if len(m) > 2]
        if indices:
            break
    i = rng.choice(indices)
    mot = mots[i]
    if insertion:
        taille = rng.randint(1, 3)
        debut = rng.randrange(len(mot) + 1)
        nouveaux = "".join(rng.choices(alphabet, k=taille))
        mots[i] = mot[:debut] + nouveaux + mot[debut:]
    else:
        taille = rng.randint(1, min(3, len(mot) - 2))
        debut = rng.randrange(len(mot) - taille + 1)
        mots[i] = mot[:debut] + mot[debut + taille:]
    return mots


def temoin():
    rng = random.Random(20261118)
    alphabet = "abcdefghijklmnop"
    vocabulaire = []
    while len(vocabulaire) < 96:
        mot = "".join(rng.choices(alphabet, k=rng.randint(2, 7)))
        if mot not in vocabulaire:
            vocabulaire.append(mot)
    vers = []
    for i in range(6000):
        mots = rng.choices(vocabulaire, k=8) if i < 1000 else copie_modifiee(vers, alphabet, rng)
        vers.append({"id": str(i), "words": mots})
    modele = Modele(vers[:5000])
    reserve = vers[5000:]
    eligibles = sum(1 for ligne in reserve for _ in positions(ligne))
    annonces = sum(1 for _ in modele.annonces(reserve))
    return {"graine": 20261118, "vers_initiaux": 1000, "copies_apprentissage": 4000,
            "copies_reserve": len(reserve), "eligibles": eligibles, "annonces": annonces,
            "fausses_expansions": annonces}


def autotest():
    def lignes(*mots):
        return [{"id": str(i), "words": texte.split()} for i, texte in enumerate(mots)]

    modele = Modele(lignes("l ab r", "l axb r", "t abz u", "v abz w", "x ab y"))
    annonces = list(modele.annonces(lignes("l ab r", "x ab y", "ab r", "l ab")))
    assert annonces == [{"id": "0", "index": 1, "observe": "ab", "predit": "axb", "base_frequente": "abz"}]
    assert not list(Modele(lignes("l ab r", "l axb r", "l abz r")).annonces(lignes("l ab r")))
    assert not list(Modele(lignes("l axb r")).annonces(lignes("l ab r")))
    assert Modele(lignes("zab", "abz")).base_frequente("ab") == "abz"
    assert Modele(lignes("ab")).base_frequente("ab") is None
    assert "ab" in formes_courtes("abxyz") and "ab" in formes_courtes("xyzab")
    assert "abc" not in formes_courtes("axbzc") and "ab" not in formes_courtes("axyzxb")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fichiers", nargs="*", type=Path)
    parser.add_argument("--temoin", type=Path, metavar="RESULTAT")
    args = parser.parse_args()
    autotest()
    if args.temoin and not args.fichiers:
        sortie, resultat = args.temoin, temoin()
    elif not args.temoin and len(args.fichiers) == 3:
        train, reserve, sortie = args.fichiers
        modele = Modele(json.loads(train.read_text(encoding="utf-8")))
        resultat = list(modele.annonces(json.loads(reserve.read_text(encoding="utf-8"))))
    else:
        parser.error("TRAIN RESERVE ANNONCES ou --temoin RESULTAT")
    sortie.write_text(json.dumps(resultat, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
