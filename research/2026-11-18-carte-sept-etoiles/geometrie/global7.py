"""Ajustement descriptif exhaustif des sept centres, sur leur diamètre complet."""
from dataclasses import dataclass
from itertools import permutations
import json

import numpy as np
from prevoir import HERE, PRIMARY, charts

ORDERS = np.array(list(permutations(range(7))), dtype=int)
N = len(ORDERS)

@dataclass
class Prepared:
    names: tuple
    sky: np.ndarray
    coeff: np.ndarray

def prepare(chart_dict):
    """Préparer une fois les coefficients complexes des deux sens et 5 040 bijections."""
    out = {}
    for key, chart in chart_dict.items():
        z = chart.sky - chart.sky.mean()
        normalized = z / np.linalg.norm(z)
        direct = normalized[ORDERS].conj()
        out[key] = Prepared(tuple(chart.names), z, np.concatenate((direct, direct.conj())))
    return out

def dessins_nuls(kind, n):
    """Un appel random((7,2)) par dessin. Sortie complexe (n,7), avant tout tri."""
    if kind not in ('disque', 'carre', 'carré'):
        raise ValueError(kind)
    rng = np.random.default_rng(1492 if kind == 'disque' else 1453)
    out = np.empty((n, 7), dtype=complex)
    for i in range(n):
        u = rng.random((7, 2))
        if kind == 'disque':
            r = np.sqrt(u[:, 0])
            phi = 2 * np.pi * u[:, 1]
            out[i] = r * np.cos(phi) + 1j * (r * np.sin(phi))
        else:
            out[i] = u[:, 0] + 1j * u[:, 1]
    return out

def best_rms(prepared, drawings):
    """{nom: array(n,)} des meilleurs RMS / diamètre des 7, pour input (7,) ou (n,7)."""
    p = np.atleast_2d(np.asarray(drawings, dtype=complex))
    if p.ndim != 2 or p.shape[1] != 7 or not np.isfinite(p).all():
        raise ValueError('Chaque dessin doit avoir sept centres complexes finis')
    centered = p - p.mean(axis=1, keepdims=True)
    diameter = abs(p[:, :, None] - p[:, None, :]).max(axis=(1, 2))
    if np.any(diameter == 0):
        raise ValueError('Diamètre nul')
    energy = np.sum(abs(centered)**2, axis=1)
    scores = {}
    for key, model in prepared.items():
        result = np.empty(len(p))
        for start in range(0, len(p), 32):
            part = slice(start, start + 32)
            # Projection orthogonale sur le modèle centré de norme 1.
            corr = model.coeff @ centered[part].T
            best_sq = np.square(abs(corr).max(axis=0))
            residual_sq = np.maximum(energy[part] - best_sq, 0.0)
            result[part] = np.sqrt(residual_sq / 7) / diameter[part]
        scores[key] = result
    return scores

def solution(model, p, idx):
    order = ORDERS[idx % N]
    mirror = bool(idx >= N)
    z = model.sky[order]
    if mirror:
        z = z.conj()
    alpha = np.vdot(z, p - p.mean()) / np.vdot(z, z).real
    diameter = abs(p[:, None] - p).max()
    distances = abs(alpha * z + p.mean() - p) / diameter
    return {'noms': [model.names[i] for i in order], 'miroir': mirror,
            'rms': float(np.sqrt(np.mean(distances**2))), 'maximum': float(distances.max()),
            'distances_par_point': distances.tolist()}

def classify(prepared, p):
    fits = {}
    for key, model in prepared.items():
        corr = abs(model.coeff @ (p - p.mean()))
        best, runner = np.argsort(-corr, kind='stable')[:2]
        a, b = solution(model, p, best), solution(model, p, runner)
        fits[key] = {'meilleure': a, 'deuxieme': b, 'ecart_rms': b['rms'] - a['rms']}
    rank = sorted(PRIMARY, key=lambda key: fits[key]['meilleure']['rms'])
    best, runner = rank[:2]
    candidates = sorted([(fits[key][variant]['rms'], key, variant)
                         for key in PRIMARY for variant in ('meilleure','deuxieme')])
    runner_all = candidates[1]
    return {'diametre_px': float(abs(p[:, None]-p).max()), 'modeles': fits, 'classement_primaire': rank,
            'ecart_entre_les_deux_premieres_cartes': fits[runner]['meilleure']['rms'] - fits[best]['meilleure']['rms'],
            'deuxieme_solution_toutes_affectations_primaires': {'carte': runner_all[1], 'rang_dans_carte': runner_all[2],
                'ecart_rms_au_premier': runner_all[0]-candidates[0][0]}}

def read_points(path):
    features = sorted(json.loads(path.read_text())['points'], key=lambda f: (f['x'], f['y']))
    return np.array([f['x']+1j*f['y'] for f in features]), features

def known(model, p, labels):
    order = np.array([model.names.index(n) for n in labels])
    k = int(np.flatnonzero((ORDERS == order).all(axis=1))[0])
    return min((solution(model,p,k),solution(model,p,k+N)), key=lambda s:s['rms'])

def null_result(kind, prepared, real):
    n = 2000
    drawings = dessins_nuls(kind,n)
    scores = best_rms({k:prepared[k] for k in PRIMARY}, drawings)
    arr = np.array([scores[k] for k in PRIMARY])
    mins, winners = arr.min(axis=0), arr.argmin(axis=0)
    summary = {'n': n, 'graine': 1492 if kind=='disque' else 1453,
               'quantiles_meilleur_rms_primaire': dict(zip(['p01','p05','p25','p50','p75','p95'],
                       np.quantile(mins,[.01,.05,.25,.5,.75,.95]).tolist())),
               'comptes_premier': {k:int((winners==i).sum()) for i,k in enumerate(PRIMARY)},
               'comparaisons':{}}
    for tag, observed in real.items():
        vals = [observed['modeles'][k]['meilleure']['rms'] for k in PRIMARY]
        count = int((mins <= min(vals)).sum())
        summary['comparaisons'][tag] = {'meilleur_rms_observe': min(vals),
            'n_meilleur_rms_inferieur_ou_egal': count, 'frequence': count/n, 'p_monte_carlo_plus_un': (count+1)/(n+1),
            'n_inferieur_ou_egal_meme_carte':{k:int((scores[k]<=v).sum()) for k,v in zip(PRIMARY,vals)}}
    return summary

def main():
    prepared = prepare(charts())
    p, pts = read_points(HERE.parent/'voynich/f68r3-centres.json')
    v = classify(prepared,p)
    v['ordre_points'] = [f['id'] for f in pts]
    p, pts = read_points(HERE.parent/'etalons/bayer1603_UMA_points.json')
    b = classify(prepared,p)
    labels = [f['id'] for f in pts]
    b['ordre_points'] = labels
    b['lettres'] = [f['bayer'] for f in pts]
    truth = known(prepared['grande_ourse'],p,labels)
    b['verite_gravee'] = truth
    b['identites_vraies_retrouvees_par_la_meilleure_grande_ourse'] = sum(x==y for x,y in zip(labels,b['modeles']['grande_ourse']['meilleure']['noms']))
    b['ecart_rms_verite_moins_optimum_grande_ourse'] = truth['rms'] - b['modeles']['grande_ourse']['meilleure']['rms']
    real = {'voynich':v,'bayer':b}
    synthetic_model='petite_ourse'
    model=prepared[synthetic_model]
    artificial=217 * np.exp(.73j)*model.sky.conj() + 460 + 783j
    order=np.lexsort((artificial.imag,artificial.real))
    s=classify(prepared,artificial[order])
    truth_s=[model.names[i] for i in order]
    recovered=s['modeles'][synthetic_model]['meilleure']
    assert s['classement_primaire'][0]==synthetic_model and recovered['miroir']
    assert recovered['noms']==truth_s and recovered['rms'] < 1e-12
    for key, tag, pos in [('voynich','voynich/f68r3-centres.json',v),('bayer','etalons/bayer1603_UMA_points.json',b)]:
        check_p,_=read_points(HERE.parent/tag)
        batch = best_rms(prepared,check_p)
        assert all(abs(batch[name][0]-pos['modeles'][name]['meilleure']['rms'])<1e-12 for name in prepared)
    output = {'unite':'fraction du diamètre des sept centres du dessin', 'bijections_par_sens': N,
              'nombre_sens':2, 'cartes_primaires': PRIMARY, 'images':real,
              'synthetique':{'carte':synthetic_model,'construction':'ciel centré conjugué × 217 exp(0,73i) + 460 + 783i, puis tri x,y',
                            'noms_vrais':truth_s,'classement_primaire':s['classement_primaire'],'solution':recovered},
              'nuls':{k:null_result(k,prepared,real) for k in ('disque','carre')}}
    (HERE/'GLOBAL7.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    main()
