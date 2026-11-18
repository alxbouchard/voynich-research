"""Faux dessins et incertitude des centres après une sélection à quatre points."""
import json
from collections import Counter
import numpy as np
from global7 import best_rms, dessins_nuls, prepare
from evaluer import trial, summarize_trials
from prevoir import HERE, PRIMARY, charts, complex_xy


def sort_x(points):
    return points[np.lexsort((points.imag,points.real))]


def quantiles(values):
    return dict(zip(('min','p05','mediane','p95','max'),np.quantile(values,[0,.05,.5,.95,1]).tolist()))


def main():
    models=charts()
    slots=[0,2,4,6]
    results=json.loads((HERE/'RESULTATS.json').read_text())
    source=results['choix_initiaux']['voynich']
    cutoff=results['resultats']['voynich'][source]['erreur_max_relative']
    out={}
    for kind in ('disque','carre'):
        rows=[trial(models,sort_x(p),slots) for p in dessins_nuls(kind,2000)]
        out[kind]={'bilan':summarize_trials(rows),'max_au_plus_voynich':sum(r['max_reserve']<=cutoff for r in rows),
                   'distribution_erreur':quantiles([r['max_reserve'] for r in rows])}
    measure=json.loads((HERE.parent/'voynich/f68r3-centres.json').read_text())
    centered=complex_xy([[s['x'],s['y']] for s in measure['points']])
    dx=np.array([s['uncertainty_x_px'] for s in measure['points']])
    dy=np.array([s['uncertainty_y_px'] for s in measure['points']])
    rng=np.random.default_rng(1408)
    draws = centered + dx*rng.uniform(-1,1,(1000,7)) + 1j*dy*rng.uniform(-1,1,(1000,7))
    rows=[trial(models,sort_x(p),slots) for p in draws]
    prepared=prepare({key:models[key] for key in PRIMARY})
    rms=best_rms(prepared,draws)
    winner=np.argmin(np.array([rms[n] for n in PRIMARY]),axis=0)
    out['tolerance']={'bilan':summarize_trials(rows),'erreurs_max_reserve':quantiles([r['max_reserve'] for r in rows]),
                     'rms_7_par_carte':{k:quantiles(v) for k,v in rms.items()},
                     'choix_7':{k:int(np.sum(winner==i)) for i,k in enumerate(PRIMARY)}}
    (HERE/'SENSIBILITE.json').write_text(json.dumps(out,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
