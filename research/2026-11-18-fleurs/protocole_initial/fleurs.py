"""Tester une association entre un mot entier de prose et une fleur visible."""
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import log
from pathlib import Path
import re

EDITIONS = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}
CLASSES = ("oui", "non")
MODELES = ("mot", "vocabulaire", "majorite")
TYPES_AVIS = {*CLASSES, "incertain"}
FACE = re.compile(r"^<(f(\d+)[rv]\d*)>\s+(.*)")
LIGNE = re.compile(r"^<(f\d+[rv]\d*)\.[^,]+,[^!]P0(?:;[^>]+)?>\s*(.*)")


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def read(path):
    return json.loads(path.read_text())


def empreinte(path):
    return sha256(path.read_bytes()).hexdigest()


@dataclass
class Page:
    numero: int
    cahier: str
    bifeuillet: str
    positions: int
    mots: Counter


def charger(path, separe, cahiers=("B", "C")):
    pages = {}
    face = None
    for ligne in path.read_text().splitlines():
        entete = FACE.match(ligne)
        if entete:
            nom, numero, champs = entete.groups()
            meta = dict(re.findall(r"\$(\w)=(\w+)", champs))
            face = None
            if (meta.get("Q") in cahiers
                    and (meta.get("I"), meta.get("H"), meta.get("L")) == ("H", "1", "A")):
                face = nom
                pages[nom] = Page(int(numero), meta["Q"], meta["B"], 0, Counter())
            continue
        if not face or pages[face].positions >= 40:
            continue
        record = LIGNE.match(ligne)
        if not record:
            continue
        assert record[1] == face
        texte = re.sub(r"<![^>]*>|<[%$]>|!", "", record[2])
        texte = re.sub(r"<[-~]>", ".", texte).strip().replace(",", "." if separe else "")
        for mot in (x for x in texte.split(".") if x):
            pages[face].positions += 1
            if re.fullmatch("[a-z]+", mot):
                pages[face].mots[mot] += 1
            if pages[face].positions == 40:
                break
    return {k: p for k, p in pages.items() if p.positions}


def valider_avis(avis, noms):
    if set(avis) != set(noms):
        raise ValueError(f"Faces différentes. Attendues {sorted(noms)}, reçues {sorted(avis)}")
    for k, v in avis.items():
        if not isinstance(v, list) or len(v) != 2 or any(val not in TYPES_AVIS for val in v):
            raise ValueError(f"Avis invalide pour {k}: {v!r}")


def consensus(avis):
    return {k: a for k, (a, b) in avis.items() if a == b and a in CLASSES}


def entrainer(pages, etiquettes):
    par_classe = {c: [p for p in etiquettes if etiquettes[p] == c] for c in CLASSES}
    n = {c: len(v) for c, v in par_classe.items()}
    compte_feuillets = {c: len({pages[p].numero for p in v}) for c, v in par_classe.items()}
    elements = {"faces": n, "feuillets": compte_feuillets, "candidat": None, "ex_aequo": []}
    if min(compte_feuillets.values()) < 2:
        elements["motif_abstention"] = "moins de deux feuillets distincts dans une classe"
        return elements, None
    occurrences = {}
    jetons = {}
    supports = defaultdict(set)
    for c, noms in par_classe.items():
        rec, freq = Counter(), Counter()
        for f in noms:
            freq.update(pages[f].mots)
            rec.update(pages[f].mots.keys())
            if c == "oui":
                for w in pages[f].mots:
                    supports[w].add(pages[f].numero)
        occurrences[c] = rec
        jetons[c] = freq
    candidats = {}
    for w, feuillets in supports.items():
        if len(feuillets) < 2:
            continue
        delta = Fraction(occurrences["oui"][w], n["oui"]) - Fraction(occurrences["non"][w], n["non"])
        if delta > 0:
            candidats[w] = (delta, len(feuillets))
    if candidats:
        maximum = max(candidats.values())
        premiers = sorted(w for w, v in candidats.items() if v == maximum)
        w = premiers[0]
        elements.update(candidat=w, ex_aequo=premiers, difference=str(maximum[0]), feuillets_oui=sorted(supports[w]),
                        avec_mot={c: occurrences[c][w] for c in CLASSES})
    else:
        elements["motif_abstention"] = "aucun mot assez répété avec une différence positive"
    vocab = set(jetons["oui"]) | set(jetons["non"])
    denom = {c: sum(freq.values()) + len(vocab) for c, freq in jetons.items()}
    return elements, (jetons, vocab, denom)


def predire(pages, appris, recherches):
    fiche, vocabulaire = appris
    decisions = {}
    for nom in recherches:
        mots = pages[nom].mots
        mot = fiche["candidat"]
        m = ("oui" if mot in mots else "non") if mot else "abstention"
        v, connus, marge = "abstention", 0, None
        if vocabulaire is not None:
            jetons, vocab, denom = vocabulaire
            observes = {w: k for w, k in mots.items() if w in vocab}
            connus = sum(observes.values())
            if connus:
                score = {c: sum(k * log((jetons[c][w] + 1) / denom[c]) for w, k in observes.items()) for c in CLASSES}
                marge = score["oui"] - score["non"]
                if abs(marge) > 1e-10:
                    v = "oui" if marge > 0 else "non"
        n = fiche["faces"]
        majorite = ("oui" if n["oui"] > n["non"] else "non") if n["oui"] + n["non"] else "abstention"
        decisions[nom] = {"mot": m, "vocabulaire": v, "majorite": majorite, "positions": pages[nom].positions,
                          "mots_lisibles": sum(mots.values()), "jetons_connus": connus, "marge_vocabulaire": marge}
    return decisions


def matrice(predict, etiquettes, modele):
    mat = {c: {z: 0 for z in (*CLASSES, "abstention")} for c in CLASSES}
    for f, truth in etiquettes.items():
        mat[truth][predict[f][modele]] += 1
    denom = {c: sum(v.values()) for c, v in mat.items()}
    recall = {c: mat[c][c]/v if v else None for c, v in denom.items()}
    return {"matrice": mat, "corrects": sum(mat[c][c] for c in CLASSES), "n": sum(denom.values()),
            "reponses": sum(denom.values()) - sum(mat[c]["abstention"] for c in CLASSES),
            "rappels": recall, "rappel_moyen": sum(recall.values())/2 if all(denom.values()) else None,
            "constante_corrects": denom}


def controle_apparie(pages, predict, etiquettes, modele):
    par_folio = defaultdict(list)
    for f in etiquettes:
        par_folio[pages[f].numero].append(f)
    paires = [(a, b) for v in par_folio.values() if len(v) == 2 for a, b in [tuple(v)] if etiquettes[a] != etiquettes[b]]
    obs = sum(predict[f][modele] == truth for f, truth in etiquettes.items())
    deltas = []
    for a, b in paires:
        normal = int(predict[a][modele] == etiquettes[a]) + int(predict[b][modele] == etiquettes[b])
        echange = int(predict[a][modele] == etiquettes[b]) + int(predict[b][modele] == etiquettes[a])
        deltas.append(echange - normal)
    hist = Counter(obs + sum(bit * delta for bit, delta in zip(bits, deltas)) for bits in product((0, 1), repeat=len(paires)))
    return {"paires_opposees": paires, "informatives": sum(d != 0 for d in deltas),
            "histogramme": hist, "combinaisons": sum(hist.values()),
            "au_moins_observe": sum(v for k, v in hist.items() if k >= obs) if any(deltas) else None}


def croiser(pages, secteur, avis):
    decisions, details = {}, []
    groupes = sorted({page.bifeuillet for page in pages.values() if page.cahier == secteur})
    for pli in groupes:
        apprentissage = {f: classe for f, classe in avis.items() if pages[f].bifeuillet != pli}
        epreuve = [f for f in avis if pages[f].bifeuillet == pli]
        modele = entrainer(pages, apprentissage)
        dec = predire(pages, modele, epreuve)
        details.append({"bifeuillet_reserve": pli, "modele": modele[0], "predictions": dec})
        decisions.update(dec)
    return {"plis": details, "bilan": {m: matrice(decisions, avis, m) for m in MODELES}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["predire", "verifier"])
    parser.add_argument("--donnees", type=Path, required=True)
    parser.add_argument("--sortie", type=Path, required=True)
    parser.add_argument("--b", type=Path, required=True)
    parser.add_argument("--c", type=Path)
    args = parser.parse_args()
    if (args.action == "verifier") != bool(args.c):
        parser.error("L'épreuve doit être fournie seulement à la vérification.")
    args.sortie.mkdir(parents=True, exist_ok=True)
    path_pred = args.sortie / "PREDICTIONS.json"
    if args.action == "verifier":
        scelle = read(path_pred)
    b = read(args.b)
    result, decision = {}, {}
    admission = None
    for edition, filename in EDITIONS.items():
        for split in (False, True):
            key = edition + ("_separe" if split else "_joint")
            pages = charger(args.donnees / filename, split)
            groupes = {q: {f for f, p in pages.items() if p.cahier == q} for q in ("B", "C")}
            if admission is not None:
                assert groupes == admission
            admission = groupes
            assert len(groupes["B"]) == 14 and len(groupes["C"]) == 16
            valider_avis(b, groupes["B"])
            labels_b = consensus(b)
            fit = entrainer(pages, labels_b)
            pred = predire(pages, fit, sorted(groupes["C"]))
            fiche = {"modele": fit[0], "predictions": pred, "sha256_source": empreinte(args.donnees / filename),
                     "sha256_avis_apprentissage": empreinte(args.b),
                     "echantillon": {f: {"n": p.positions, "lisibles": sum(p.mots.values()), "cahier": p.cahier,
                                         "bifeuillet": p.bifeuillet} for f, p in pages.items()}}
            decision[key] = fiche
            if args.action == "verifier":
                assert fiche == scelle[key], f"Différence avec les décisions enregistrées {key}"
                c = read(args.c)
                valider_avis(c, groupes["C"])
                labels_c = consensus(c)
                result[key] = {
                    "B_vers_C": {m: dict(matrice(pred, labels_c, m),
                                         permutation_recto_verso=controle_apparie(pages, pred, labels_c, m))
                                  for m in MODELES},
                    "interne": {q: croiser(pages, q, lab) for q, lab in (("B", labels_b), ("C", labels_c))},
                    "exclusions": {q: {f: v for f, v in avis.items() if f not in lab}
                                   for q, avis, lab in (("B", b, labels_b), ("C", c, labels_c))},
                    "sha256_avis_controle": empreinte(args.c)}
    if args.action == "predire":
        dump(path_pred, decision)
    else:
        dump(args.sortie / "RESULTATS.json", result)


if __name__ == "__main__":
    main()
