"""Mesurer les positions sur les trois photographies natives du manuscrit."""
from itertools import combinations
from pathlib import Path
from statistics import median
import json
import math


ICI = Path(__file__).resolve().parent


def centre(reperes):
    boites = [r['boite'] for r in reperes]
    return [(min(b[0] for b in boites) + max(b[2] for b in boites)) / 2,
            (min(b[1] for b in boites) + max(b[3] for b in boites)) / 2]


def pente_prose(lignes, largeur):
    pentes = {}
    for numero, ligne in lignes.items():
        pts = [centre([r]) for r in ligne['repere']]
        if ligne['type'] != 'P0' or len(pts) < 4:
            continue
        if max(p[0] for p in pts) - min(p[0] for p in pts) < largeur / 4:
            continue
        echanges = [(b[1] - a[1]) / (b[0] - a[0]) for a, b in combinations(pts, 2)
                     if abs(b[0] - a[0]) >= largeur / 5]
        pentes[numero] = median(echanges)
    return pentes


def proj(p, m):
    return (p[0] + m * p[1]) / math.hypot(1, m)


def classer(p, centres, m):
    valeurs = [(n, abs(proj(c, m) - proj(p, m))) for n, c in centres.items()]
    return sorted(valeurs, key=lambda nd: nd[1])


def analyser(f):
    lignes = f['lignes']
    lig = lignes[str(f['ligne_prose'])]
    lu = next(r for r in lig['repere'] if r['rang'] == f['rang_prose'])
    p = centre([lu])
    centres = {n: centre(lignes[str(n)]['repere']) for n in f['rangee']}
    pentes = pente_prose(lignes, f['dimensions'][0])
    m = median(pentes.values())
    classements = {}
    for axe, a in [('redresse', m), ('horizontal_photo', 0)]:
        ordre = classer(p, centres, a)
        classements[axe] = [{'numero': n, 'distance': round(d, 2),
                             'rang': 1 + sum(dist < d - 1e-8 for _, dist in ordre)}
                            for n, d in ordre]

    def tombe_sur_cible(point, pente):
        ordre = classer(point, centres, pente)
        return ordre[0][0] == f['cible'] and ordre[1][1] - ordre[0][1] > 1e-8

    controles = [r for r in lig['repere'] if r['rang'] != f['rang_prose']]
    # Combien des autres mots du même contexte auraient pointé au même endroit ?
    meme_colonne = [r['rang'] for r in controles if tombe_sur_cible(centre([r]), m)]
    tous = {int(n): centre(l['repere']) for n,l in lignes.items() if l['type'] == 'Lf'}
    ordre_panneau = classer(p, tous, m)
    tous_les_rangs = [{'numero': n, 'distance': round(d, 2)} for n,d in ordre_panneau]
    candidats = sorted(abs(proj(c, m) - proj(p, m)) for c in centres.values())
    return {'mot': lu['mot_H'], 'prose': p, 'etiquettes': centres, 'cible': f['cible'],
            'pentes_par_ligne': pentes, 'pente': m, 'angle_degres': math.degrees(math.atan(m)),
            'etiquettes_Lf_tout_le_panneau': tous_les_rangs,
            'classements': classements, 'marge_distances': round(candidats[1] - candidats[0], 2),
            'autres_mots_meme_ligne': {'reperes': len(controles), 'total': lig['taille'] - 1,
                                       'rangs_plus_proches_de_cible': meme_colonne},
            'sensibilite_pentes': {'cible_premiere': sum(tombe_sur_cible(p, v) for v in pentes.values()),
                                   'nombre': len(pentes)}}


if __name__ == '__main__':
    source = json.loads((ICI / 'REPERES.json').read_text())
    print(json.dumps({k: analyser(f) for k, f in source.items()}, indent=2, ensure_ascii=False))
