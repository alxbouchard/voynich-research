"""Sensibilité du classement à l'exclusion des feuillets conjugués selon ZL."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from statistics import mean
import json
import re

from comparer import HERE, INVENTORY, RESEARCH, classes, compare, folio, mixed

ZL = RESEARCH.parent / "voynich_phase17/data/ZL3b-n.txt"


def materiel():
    """Vérifie que toutes les faces d'un feuillet portent le même couple Q/B."""
    feuillets = {}
    for ligne in ZL.read_text().splitlines():
        face = re.match(r"^<(f\d+[rv]\d*)>", ligne)
        if face:
            attributs = dict(re.findall(r"\$([A-Z])=([A-Za-z0-9]+)", ligne))
            if "Q" in attributs and "B" in attributs:
                numero = folio(face[1])
                groupe = attributs["Q"] + "/" + attributs["B"]
                assert feuillets.setdefault(numero, groupe) == groupe
    return feuillets


def epreuve(faces, groupes):
    feuillets = sorted({folio(face) for face in faces})
    familles = {g: [f for f in feuillets if groupes[f] == g] for g in sorted({groupes[f] for f in feuillets})}
    assert len(familles) >= 2
    detail = {}
    scores = defaultdict(list)
    totaux = Counter()
    for reserve, serie in faces.items():
        g = groupes[folio(reserve)]
        appr = [s for f, s in faces.items() if groupes[folio(f)] != g]
        freq = [Counter(mot for s in appr for mot in s[c]) for c in (0, 1)]
        n = [c.total() for c in freq]
        assert all(n)
        rang = {mot: Fraction(freq[0][mot], n[0]) - Fraction(freq[1][mot], n[1])
                for mots in serie for mot in mots}
        cas = Counter((rang[a] > rang[b]) - (rang[a] < rang[b]) for a in serie[0] for b in serie[1])
        s = Fraction(cas[1]*2 + cas[0], 2*cas.total())
        scores[folio(reserve)].append(s)
        totaux.update(cas)
        detail[reserve] = {"Q/B": g, "reserve_mixe": familles[g], "effectifs": list(map(len, serie)),
                           "apprentissage": n, "justes": cas[1], "erreurs": cas[-1],
                           "egalites": cas[0], "score_exact": str(s)}
    par_f = {f: mean(v) for f, v in scores.items()}
    par_b = {g: mean(par_f[f] for f in fs) for g, fs in familles.items()}
    s_f, s_b = mean(par_f.values()), mean(par_b.values())
    return {
        "faces": detail, "groupes_mixtes": familles,
        "n_faces": len(faces), "n_feuillets": len(feuillets), "n_bifeuillets": len(familles),
        "effectifs": [sum(len(s[c]) for s in faces.values()) for c in (0, 1)],
        "justes": totaux[1], "erreurs": totaux[-1], "egalites": totaux[0],
        "score_meme_poids_par_feuillet": float(s_f), "exact_par_feuillet": str(s_f),
        "score_meme_poids_par_bifeuillet": float(s_b), "exact_par_bifeuillet": str(s_b),
        "scores_par_bifeuillet": {g: str(s) for g, s in par_b.items()},
    }


def main():
    sources = json.loads(INVENTORY.read_text())
    rows = classes()
    conjugaison = materiel()
    bilan = {
        "sources_sha256": {str(p.relative_to(RESEARCH.parent)): sha256(p.read_bytes()).hexdigest() for p in (INVENTORY, ZL)},
        "methode": "Seules les faces mixtes contribuent. Toutes les faces du même couple ZL Q/B sont exclues de l'apprentissage. Deux pondérations descriptives, sans nouvelle permutation.",
        "epreuves": {}, "otoly": {},
    }
    regroupes = dict(rows, Ln=sources["par_code"]["Ln"]["mots_par_locus"])
    for nom, premier, second, r in [
        ("fragments_recipients", "Lf", "Lc", rows),
        ("personnages_lignes_bains", "Ln", "Lt", rows),
        ("personnages_objets_bains", "Ln", "Lt", regroupes),
    ]:
        for cle, tronquer in [("entier", False), ("sans_derniere_unite", True)]:
            faces = mixed(r, premier, second, tronquer)
            individuels = {folio(f): folio(f) for f in faces}
            assert epreuve(faces, individuels)["exact_par_feuillet"] == str(compare(faces)[0])
            bilan["epreuves"][nom + "_" + cle] = epreuve(faces, conjugaison)
        if premier == "Ln":
            locs = {l: conjugaison[folio(l)] for l, w in r[premier].items() if w == "otoly"}
            mixtes = mixed(r, premier, second, False)
            bilan["otoly"][nom] = {"inscriptions_Ln": len(r[premier]), "otoly_Ln": locs,
                                     "nombre_bifeuillets_avec_otoly": len(set(locs.values())),
                                     "loci_sur_faces_mixtes": [l for l in locs if l.split(".")[0] in mixtes]}
    (HERE / "BIFEUILLETS.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
