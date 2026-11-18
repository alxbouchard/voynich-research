"""Compare les sept secteurs occupés sur le cadran de f67r2 aux motifs historiques."""

from collections import Counter
from itertools import combinations
import json


# Le secteur 1 est centré vers 9 h 30. Numérotation horaire jusqu’à 8 h 30.
VISUEL = {1, 3, 5, 6, 7, 8, 11}
STOLFI_DEPUIS_8H30 = {2, 4, 6, 7, 8, 9, 12}
MODELES = {
    "exaltations": {1, 2, 4, 6, 7, 10, 12},
    "mois_de_31_jours": {1, 3, 5, 7, 8, 10, 12},
}


def placements(motif):
    for sens in (1, -1):
        for origine in range(1, 13):
            secteurs = {(origine - 1 + sens * (i - 1)) % 12 + 1 for i in motif}
            yield (origine, sens, secteurs)


def analyse():
    assert VISUEL == {(x - 2) % 12 + 1 for x in STOLFI_DEPUIS_8H30}
    nuls = list(map(set, combinations(range(1, 13), 7)))
    assert len(nuls) == 792
    resultat = {"secteurs_observes": sorted(VISUEL), "modeles": {}}
    distributions = {}
    for nom, modele in MODELES.items():
        phases = list(placements(modele))
        score = max(len(VISUEL & s) for _, _, s in phases)
        ex_aequo = [
            {"origine": o, "sens": d, "secteurs": sorted(s),
             "attendus_absents": sorted(s - VISUEL), "presents_imprevus": sorted(VISUEL - s)}
            for o, d, s in phases if len(VISUEL & s) == score
        ]
        max_nuls = [max(len(n & s) for _, _, s in phases) for n in nuls]
        distributions[nom] = max_nuls
        resultat['modeles'][nom] = {
            'score': score, 'placements_testes': len(phases),
            'masques_distincts': len({frozenset(s) for _, _, s in phases}),
            'ex_aequo': ex_aequo, 'distribution_des_maxima': dict(sorted(Counter(max_nuls).items())),
            'au_moins_aussi_bon_sur_792': sum(s >= score for s in max_nuls),
        }
    premier, second = MODELES
    ecarts = [a - b for a, b in zip(distributions[premier], distributions[second])]
    resultat['distribution_ecart_exaltations_moins_mois'] = dict(sorted(Counter(ecarts).items()))
    ecart_observe = resultat['modeles'][premier]['score'] - resultat['modeles'][second]['score']
    resultat['ecart_observe'] = ecart_observe
    resultat['ecart_absolu_au_moins_aussi_grand_sur_792'] = sum(abs(e) >= abs(ecart_observe) for e in ecarts)
    max_joint = [max(a, b) for a, b in zip(distributions[premier], distributions[second])]
    resultat['distribution_meilleur_des_deux'] = dict(sorted(Counter(max_joint).items()))
    return resultat


if __name__ == '__main__':
    print(json.dumps(analyse(), indent=2))
