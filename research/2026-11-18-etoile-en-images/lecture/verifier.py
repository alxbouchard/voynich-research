"""Recompter les solutions par affectation récursive, indépendamment de la coupe par partitions."""
import json
from collections import Counter
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
read = lambda name: json.loads((HERE/name).read_text())
unit = re.compile('c[ktpf]h|[cs]h|[a-z]').findall


def solve(signs, word, size, old=None):
    def visit(rest, text, key):
        if not rest:
            return [key] if not text else []
        sign, *tail = rest
        if sign in key:
            value = key[sign]
            return visit(tail,text[len(value):],key) if text.startswith(value) else []
        answers = []
        for n in range(1,min(size,len(text))+1):
            value = text[:n]
            if value not in key.values():
                answers += visit(tail,text[n:],dict(key,**{sign:value}))
        return answers
    return visit(list(signs),word,dict(old or {}))


def keyset(keys):
    return sorted(tuple(sorted(k.items())) for k in keys)


def main():
    a,b = read('RESULTATS.json'),read('SUITE.json')
    for w, model in a['modeles'].items():
        width=int(w)
        for loc,row in model['formes_voynich'].items():
            assert keyset(solve(unit(row['EVA']),'stella',width))==keyset(r['table'] for r in row['tables'])
            for table in row['tables']:
                for candidate, keys in table['doaro_completions'].items():
                    expected=solve('doaro',candidate.replace('v','u'),width,table['table'])
                    assert keyset(expected)==keyset(keys)
                decoded=[]
                for spot,eva in a['prose_valide']:
                    if eva == row['EVA'] or any(s not in table['table'] for s in unit(eva)):
                        continue
                    guess=''.join(table['table'][s] for s in unit(eva))
                    if guess!='stella' and len(guess)>=3:
                        decoded.append((spot,eva,guess))
                assert decoded==[(p['lieu'],p['EVA'],p['latin']) for p in table['prose']]
        for item in model['controle']['origines']:
            assert len(solve(item['graphie'],'stella',width))==item['tables']
        for form, keys in model['otor'].items():
            assert keyset(solve('otor',form,width))==keyset(keys)
    assert len(a['prose_valide'])==52
    positive=a['modeles']['3']['controle']['tables_et_lectures']
    right=[r['lecture'] for line in positive if line['graphie']=='stella'
           for r in line['prose'] if len(r['lecture'])>=3]
    false=[r for line in positive if line['graphie']!='stella'
           for r in line['prose'] if len(r['lecture'])>=3]
    assert right==['stellae','est'] and len(false)==8 and not any(x['exact'] or x['dans_vocabulaire'] for x in false)
    numads=Counter(loc.split('.')[0] for loc in b['legendes_reservees_admissibles'])
    assert numads=={'f68r2':16,'f68r3':3}
    for group in b['flexions'].values():
        for word,result in group.items():
            assert word[0] not in word[1:-1] and not result['segmentations']
    silent, = b['o_muet']
    assert solve('otor','stella',3,{'o':''})==[silent['table']]
    for w,solutions in silent['amas']['completions'].items():
        assert keyset(solve('doaro',w.replace('v','u'),3,silent['table']))==keyset(solutions)
    assert silent['prose']['f68r1.3/6']['lecture']=='llalla' and not silent['legendes_reservees']
    print('Contrôles des tables, des transferts, des 19 formes et du signe muet réussis.')


if __name__=='__main__':
    main()
