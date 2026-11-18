"""Contrôle externe sur les six marques ouvertes de Galilée. Séparer prédiction et jugement."""
from itertools import permutations
import json
import sys
import numpy as np
from prevoir import HERE, PRIMARY, Chart, complex_xy
from evaluer import evaluate

FIT=[0,2,3,5]
TEST=[1,4]


def input_data():
    full=json.loads((HERE.parent/'catalogue/modeles.json').read_text())['models']
    source=json.loads((HERE.parent/'etalons/galilee1610_pleiades_six_points.json').read_text())
    rows=sorted(source['points'],key=lambda r:(r['x'],r['y']))
    return rows,{name:Chart(sorted(full[name],key=lambda r:r['mag'])[:6]) for name in PRIMARY}


def predict(xy,models):
    training=complex_xy(xy)
    fits={n:c.predictions(training) for n,c in models.items()}
    return {'choix_primaire':min(PRIMARY,key=lambda k:fits[k][0]['rms_relatif']),
            'diametre':float(abs(training[:,None]-training).max()),'calages':fits}


def six_all(model,points,truth):
    orders=np.asarray(list(permutations(range(6))))
    best=None
    for sky in (model.sky,model.sky.conj()):
        centered=sky-sky.mean()
        q=points-points.mean()
        denom=(abs(centered)**2).sum()
        scale=(centered[orders].conj()*q).sum(axis=1)/denom
        error=abs(scale[:,None]*centered[orders]-q)
        i=int(np.argmin((error**2).sum(axis=1)))
        rms=float(np.sqrt(np.mean(error[i]**2))/abs(q[:,None]-q).max())
        names=[model.names[idx] for idx in orders[i]]
        if best is None or rms<best['rms']:
            best={'rms':rms,'noms':names,'identites_confirmees':sum(a==b for a,b in zip(names,truth))}
    return best


def main(action):
    rows,models=input_data()
    if action=='predire':
        data=predict([[rows[i]['x'],rows[i]['y']] for i in FIT],models)
        dest='GALILEE-PREDICTIONS.json'
    elif action=='evaluer':
        p=json.loads((HERE/'GALILEE-PREDICTIONS.json').read_text())
        gold={'calage':[rows[i] for i in FIT],'reserve':[rows[i] for i in TEST]}
        target=complex_xy([[r['x'],r['y']] for r in rows])
        data={'choix':p['choix_primaire'],'reserve':{},'six':{}}
        for name,model in models.items():
            data['reserve'][name]=evaluate(p['calages'][name][0],p['diametre'],gold,tag='carte_identifiee')
            data['six'][name]=six_all(model,target,[r['id'] for r in rows])
        dest='GALILEE-RESULTATS.json'
    else:
        raise ValueError(action)
    (HERE/dest).write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main(sys.argv[1])
