"""Dédupliquer les prédictions et compter celles qui ont une attestation dans le témoin."""
import gzip
import json
from chercher import HERE, corpus

def summarize(lang):
    data = corpus(lang)
    words = {word for chapter in data.values() for word in chapter}
    models = json.loads(gzip.decompress((HERE/lang/'PREDICTIONS.json.gz').read_bytes()))
    verified = json.loads((HERE/lang/'VERIFICATION.json').read_text())['branches']
    occurrences = set()
    for name, model in models.items():
        step = int(name.split('/')[3])
        for r in model['reservations']:
            for word in r['sorties']:
                occurrences.add((r['segment'],r['rang_physique_historique_depart'],step,word))
    proposed = {row[-1] for row in occurrences}
    return {'segments':len(data),'mots':sum(map(len,data.values())),
            'positions_de_quatre_mots_par_sens':sum(max(0,len(w)-3) for w in data.values()),
            'regles':len(models),'regles_qui_prevoient':sum(bool(b['trois_mots']) for b in models.values()),
            'regles_sans_signe_muet_qui_prevoient':sum(bool(b['trois_mots']) for k,b in models.items() if k.endswith('/0')),
            'positions_orientees_avec_prediction':len({row[:3] for row in occurrences}),
            'segments_avec_prediction':len({row[0] for row in occurrences}),
            'formes_et_positions_orientees':len(occurrences),'formes_distinctes':len(proposed),
            'formes_presentes_n_importe_ou_dans_ce_temoin':sorted(proposed & words),
            'regles_avec_succes':sum(bool(b['sites_corrects']) for b in verified.values())}

if __name__=='__main__':
    (HERE/'BILAN.json').write_text(json.dumps({lang:summarize(lang) for lang in ['latin','francais']},
                                              ensure_ascii=False,indent=2)+'\n')
