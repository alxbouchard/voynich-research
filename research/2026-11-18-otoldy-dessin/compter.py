"""Comparer les lectures en aveugle aux paires préenregistrées."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path

from contexte.compter import ED, DATA, clear, load

HERE = Path(__file__).resolve().parent
PHOTOS = HERE/'photos'

def read(file):
    return json.loads(file.read_text())

def as_votes(file):
    raw = read(file)
    rows = raw.get('votes', []) if isinstance(raw, dict) else raw
    assert len(rows) == 13
    assert all(row[trait] in ('oui','non','?') for row in rows for trait in ('A','B'))
    return {row['id']:row for row in rows}

def direction(target, control):
    if '?' in (target,control):
        return 'indéterminée'
    if target == control:
        return 'égalité'
    return 'favorable' if target == 'oui' else 'inverse'

def sign_test(favorable, inverse):
    n = favorable + inverse
    if not n:
        return None
    return str(Fraction(sum(comb(n,j) for j in range(favorable,n+1)), 2**n))

def paired(votes, pairs):
    by_pair = [(votes[a],votes[b]) for a,b in pairs]
    observed = Counter(direction(a,b) for a,b in by_pair)
    options = [set(direction(x,y) for x in (('non','oui') if a=='?' else [a])
                             for y in (('non','oui') if b=='?' else [b])) for a,b in by_pair]
    possible = sorted({(out.count('favorable'),out.count('inverse'),out.count('égalité')) for out in product(*options)})
    f = observed['favorable']
    i = observed['inverse']
    return {'paires':[{'cible':a,'témoin':b,'sens':direction(a,b)} for a,b in by_pair],
            'comptes':dict(observed), 'échange_exact_sur_paires_discordantes':sign_test(f,i),
            'résolutions_favorables_inverses_égales':possible,
            'critère_prévu_atteint': f>=4 and i==0 and len(pairs)-observed['indéterminée']>=4}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sortie',type=Path,default=HERE/'RESULTATS.json')
    args = ap.parse_args()
    key = {entry['face']: card for card,entry in read(PHOTOS/'CLE-CARTES.json').items()}
    pairs = [(r['cible'],r['témoin']) for r in read(PHOTOS/'ECHANTILLON.json')['paires']]
    faces = {page for pair in pairs for page in pair}
    result = {'paires':pairs,'volume_prose':{},'traits':{}}
    for ed, file in ED.items():
        volumes = {}
        for split in (True,False):
            totals = {p:{'champs':0,'simples':0,'lignes':0} for p in faces}
            for row in load(DATA/file,split):
                if row.page in faces and row.in_botanical_prose():
                    total = totals[row.page]
                    total['lignes'] += 1
                    total['champs'] += len(row.words)
                    total['simples'] += sum(clear(w) for w in row.words)
            volumes['séparés' if split else 'joints'] = dict(sorted(totals.items()))
        result['volume_prose'][ed] = volumes
    readers = [as_votes(PHOTOS/f'lecteur-{i}.json') for i in (1,2)]
    for trait in ('A','B'):
        individual = [{p:votes[card][trait] for p,card in sorted(key.items())} for votes in readers]
        first, second = individual
        together = {p:(first[p] if first[p]==second[p] else '?') for p in first}
        result['traits'][trait] = {
            'par_face':{p:[first[p],second[p],together[p]] for p in first},
            'accords_sur_dix_y_compris_double_abstention':sum(first[p]==second[p] for p in faces),
            'accords_déterminés_sur_dix':sum(together[p]!='?' for p in faces),
            'lecteur_1':paired(first,pairs),'lecteur_2':paired(second,pairs),'commun':paired(together,pairs)}
    args.sortie.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    main()
