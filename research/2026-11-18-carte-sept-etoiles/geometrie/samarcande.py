"""Calcul distinct sur le f. 28r du témoin d'al-Sufi désigné avant mesure."""
import json
import sys
from prevoir import HERE, PRIMARY, charts, complex_xy
from six import predict
from evaluer import evaluate
from global7 import prepare, classify, known


def main(action):
    path=HERE.parent/'medieval'
    data=json.loads((path/'bnf-arabe5036-f28r-points.json').read_text())
    rows=sorted(data['points'],key=lambda r:(r['x'],r['y']))
    models=charts()
    if action=='predire':
        result=predict([[r['x'],r['y']] for r in rows[::2]],models)
        out='PREDICTIONS.json'
    elif action=='evaluer':
        given=json.loads((path/'PREDICTIONS.json').read_text())
        gold={'calage':rows[::2],'reserve':rows[1::2]}
        points=complex_xy([[r['x'],r['y']] for r in rows])
        prepared=prepare(models)
        result={'choix':given['choix_primaire'],'reserve':{
            name:evaluate(fits[0],given['diametre'],gold,'carte_identifiee') for name,fits in given['calages'].items()},
            'sept':classify(prepared,points),'ordre_comparaison':[r['id'] for r in rows],
            'rms_noms_documentes':known(prepared['grande_ourse'],points,[r['id'] for r in rows])}
        out='RESULTATS.json'
    else:
        raise ValueError(action)
    (path/out).write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main(sys.argv[1])
