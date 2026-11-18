"""Test des prédictions figées, contrôle des identités et fréquence des coïncidences."""
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import numpy as np
from prevoir import HERE, PRIMARY, LIMIT_FIT, LIMIT_HIDDEN, charts, complex_xy, xy


def align(pred, hidden):
    coords = complex_xy([p['xy'] for p in pred])
    orders = list(permutations(range(len(hidden))))
    ordered = np.asarray(orders)
    distance = abs(coords-hidden[ordered])
    idx = int(np.argmin((distance**2).sum(axis=1)))
    return orders[idx],distance[idx]


def evaluate(proposal, diameter, points, tag):
    gold = points['reserve']
    pred = proposal['previsions']
    targets = complex_xy([[s['x'],s['y']] for s in gold])
    order,dist = align(pred,targets)
    ids = [gold[k]['id'] for k in order]
    fit_ids = [s['id'] for s in points['calage']]
    return {'noms_calage':proposal['ordre_calage'],'rms_calage':proposal['rms_relatif'],
            'diametre_calage_pixels':diameter,'distances_pixels':dist.tolist(),
            'erreur_max_relative':float(max(dist)/diameter),'rms_reserve_relatif':float(np.sqrt(np.mean(dist**2))/diameter),
            'passe':bool(proposal['rms_relatif'] <= LIMIT_FIT and max(dist)<=diameter*LIMIT_HIDDEN),
            'etoiles':[{'predite':p['nom'],'observee':name,'coord_pred':p['xy'],'coord_observee':xy(targets[k])}
                       for p,name,k in zip(pred,ids,order)],
            'identites_calage_correctes':sum(a==b for a,b in zip(fit_ids,proposal['ordre_calage'])) if tag!='voynich' else None,
            'identites_reserve_correctes':sum(name==p['nom'] for name,p in zip(ids,pred)) if tag!='voynich' else None}


def trial(models,points,slots):
    t=points[slots]
    remaining=sorted(set(range(7))-set(slots))
    hidden=points[remaining]
    radius=abs(t[:,None]-t).max()
    best=None
    for name in PRIMARY:
        model=models[name]
        index,_,corr=model.fit(t)
        est,ids,mir,rms=model.transform(index,corr,t)
        if best is None or rms<best[0]:
            best=(rms,name,est,ids)
    rms,name,est,ids=best
    missing=sorted(set(range(7))-set(ids))
    mappings=np.array(list(permutations(range(3))))
    err=abs(est[missing]-hidden[mappings])
    idx=int(np.argmin((err**2).sum(axis=1)))
    max_error=err[idx].max()/radius
    all_ids=['']*7
    for i,s in zip(slots,ids):
        all_ids[i]=models[name].names[s]
    for i,s in zip(mappings[idx],missing):
        all_ids[remaining[i]]=models[name].names[s]
    return {'choix':name,'rms_calage':float(rms),'max_reserve':float(max_error),
            'passe':bool(rms<=LIMIT_FIT and max_error<=LIMIT_HIDDEN),'identites':all_ids}


def summarize_trials(rows):
    return {'essais':len(rows),'passes':sum(r['passe'] for r in rows),
            'par_carte':{k:{'choix':sum(r['choix']==k for r in rows),
                          'passes':sum(r['choix']==k and r['passe'] for r in rows)} for k in PRIMARY}}


def synthetic(models):
    source='petite_ourse'
    model=models[source]
    points=(model.sky.conj()*(326-119j)+723+891j)
    inds=np.lexsort((points.imag,points.real))
    res=trial(models,points[inds],[0,2,4,6])
    assert res['choix']==source and res['passe'] and res['identites']==[model.names[i] for i in inds]
    return res


def main():
    models=charts()
    predictions=(HERE/'PREDICTIONS.json').read_bytes()
    raw=json.loads(predictions)
    reserve=json.loads((HERE/'reserve.json').read_text())
    results={}
    cross={}
    for tag,entry in raw.items():
        gold=reserve[tag]
        assert gold['empreinte']==entry['source_sha256']
        results[tag]={k:evaluate(fits[0],entry['diametre_calage'],gold,tag) for k,fits in entry['calages'].items()}
        data=sorted(gold['reserve']+gold['calage'],key=lambda p:(p['x'],p['y']))
        points=complex_xy([[r['x'],r['y']] for r in data])
        rows=[]
        for fit in combinations(range(7),4):
            r=trial(models,points,list(fit))
            r['rangs_entrainement']=[i+1 for i in fit]
            if tag=='bayer':
                r['sept_identites_vraies']=r['identites']==[row['id'] for row in data]
            rows.append(r)
        cross[tag]={'bilan':summarize_trials(rows),'details':rows}
        if tag=='bayer':
            cross[tag]['sept_identites_vraies']=sum(r['sept_identites_vraies'] for r in rows)
    result={'empreinte_predictions':sha256(predictions).hexdigest(),'choix_initiaux':{k:v['choix_primaire'] for k,v in raw.items()},
            'controle_synthetique':synthetic(models),'resultats':results,'partages_quatre_trois':cross}
    (HERE/'RESULTATS.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
