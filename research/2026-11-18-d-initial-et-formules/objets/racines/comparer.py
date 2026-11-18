"""Tester les mots et les finales communs entre fragments de feuillets différents."""

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

ICI = Path(__file__).resolve().parent
SOURCE = ICI.parents[2] / "2026-11-18-racines-fourchues"
sys.path.insert(0, str(SOURCE))
from annoncer import units

GRAINE = 415
MELANGES = 50_000


def main():
    octets = (SOURCE / "RESULTATS.json").read_bytes()
    fragments = json.loads(octets)["fragments"]
    retenus = [
        r for r in fragments
        if r["attache"] == "ordre_documente"
        and len(r["commun"] or []) == 1
        and r["votes"][0] == r["votes"][1]
        and r["votes"][0] in {"Y", "S", "M"}
    ]
    mots = [r["commun"][0] for r in retenus]
    unites = [tuple(units(mot, False)) for mot in mots]
    formes = [r["votes"][0] for r in retenus]
    panneaux = [r["page"] for r in retenus]
    feuillets = [re.fullmatch(r"f(\d+)[rv][12]?", p).group(1) for p in panneaux]
    indices = defaultdict(list)
    effectifs = defaultdict(Counter)
    for i, panneau in enumerate(panneaux):
        indices[panneau].append(i)
        effectifs[panneau][formes[i]] += 1
    paires = [(i, j) for i, j in combinations(range(len(retenus)), 2)
              if feuillets[i] != feuillets[j]]
    memes_mots = [(i, j) for i, j in paires if mots[i] == mots[j]]
    memes_finales = [(i, j) for i, j in paires
                     if min(len(unites[i]), len(unites[j])) >= 2
                     and unites[i][-2:] == unites[j][-2:]]
    attendu = Fraction(0)
    for i, j in memes_finales:
        a, b = effectifs[panneaux[i]], effectifs[panneaux[j]]
        attendu += Fraction(sum(a[k] * b[k] for k in "YSM"), sum(a.values()) * sum(b.values()))
    observe = sum(formes[i] == formes[j] for i, j in memes_finales)
    hasard = random.Random(GRAINE)
    au_moins = 0
    for _ in range(MELANGES):
        permutees = formes.copy()
        for ids in indices.values():
            tirage = [formes[i] for i in ids]
            hasard.shuffle(tirage)
            for i, forme in zip(ids, tirage):
                permutees[i] = forme
        succes = sum(permutees[i] == permutees[j] for i, j in memes_finales)
        au_moins += succes >= observe
    sortie = {
        "sha256_resultats_source": hashlib.sha256(octets).hexdigest(),
        "fragments_registre": len(fragments), "fragments_retenus": len(retenus),
        "identifiants_retenus": [r["fragment"] for r in retenus],
        "feuillets": sorted(set(feuillets), key=int), "formes_par_panneau": effectifs,
        "paires_interfeuillets": len(paires), "paires_meme_mot": len(memes_mots),
        "paires_meme_mot_meme_forme": sum(formes[i] == formes[j] for i, j in memes_mots),
        "paires_meme_finale": len(memes_finales),
        "finales": sorted({"".join(unites[i][-2:]) for i, _ in memes_finales}),
        "meme_finale_meme_forme": observe,
        "attendu_exact": str(attendu), "attendu_decimal": float(attendu),
        "graine": GRAINE, "melanges": MELANGES, "au_moins_autant": au_moins,
    }
    (ICI / "RESULTATS.json").write_text(json.dumps(sortie, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
