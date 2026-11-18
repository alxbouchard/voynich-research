"""Comparer les prédictions déjà enregistrées aux deux votes masqués."""
from collections import Counter
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE/name).read_text())


def matches(pairs):
    return sum(a==b for a,b in pairs if a is not None and b is not None)


def report(guess,gold):
    pairs = list(zip(guess,gold))
    known = [(a,b) for a,b in pairs if a is not None and b is not None]
    observed = matches(pairs)
    rotations = [matches(zip(guess[n:]+guess[:n],gold)) for n in range(len(guess))]
    frequency = Counter(b for _,b in known)
    return {'positions':len(pairs),'comparables':len(known),'justes':observed,
         'couples':[[a,b,sum((x,y)==(a,b) for x,y in known)] for a,b in sorted(set(known))],
         'meilleure_constante':max(frequency.values(),default=0),
         'justes_apres_rotations':rotations,
         'rotations_au_moins_aussi_bonnes':sum(r>=observed for r in rotations),
         'predictions_ordonnees':guess,'observations_ordonnees':gold}


def unanimous(values):
    return values[0] if all(x == values[0] for x in values) else None


def radial():
    pred = read('PREDICTIONS.json')
    k = read('reperes/cle.json')['cards']
    votes = [read('vote-radial-'+n+'.json') for n in ('I','II')]
    results = {}
    for name in ('multiplicite','rayons'):
        batch = 'A' if name=='multiplicite' else 'B'
        entries = {c:r for c,r in k.items() if c.startswith(batch)}
        assert all(set(v[batch])==set(entries) for v in votes)
        for assoc in ('locus','alternative_locus') if batch=='A' else ('locus',):
            ordered = sorted(entries,key=lambda c:int(entries[c][assoc].split('.')[1]))
            gold = [unanimous([v[batch][c] for v in votes]) for c in ordered]
            for var in ('nombre',) if batch=='A' else ('otor','premier_ot'):
                readings = {}
                for ed,by_cut in pred[name].items():
                    for cut,raw in by_cut.items():
                        readings[ed+'_'+cut] = [raw[entries[c][assoc]][var] for c in ordered]
                readings['accord'] = [unanimous(vals) for vals in zip(*readings.values())]
                d = {s:report(p,gold) for s,p in readings.items()}
                if batch=='A':
                    common=[i for i,val in enumerate(readings['accord']) if val is not None]
                    d['positions_accord']=[ordered[i] for i in common]
                d['ordre'] = [(c,entries[c][assoc]) for c in ordered]
                results['_'.join([batch,assoc,var])] = d
            if batch=='B':
                frequency={}
                for ed,by_cut in pred[name].items():
                    for cut,raw in by_cut.items():
                        cts={str(b):Counter() for b in (True,False)}
                        for code,b in zip(ordered,gold):
                            if b is None:continue
                            r=raw[entries[code][assoc]]
                            cts[str(b)].update({'positions':len(r['groupes']),'lisibles':r['lisibles'],
                                               'ot_nimporte_ou':len(r['ot_partout_rangs'])})
                        frequency[ed+'_'+cut] = cts
                results['B_exposition_tous_les_groupes'] = frequency
    return results


if __name__=='__main__':
    (HERE/'RESULTATS-RAYONS.json').write_text(json.dumps(radial(),indent=1,ensure_ascii=False)+'\n')
