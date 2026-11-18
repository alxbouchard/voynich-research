"""Apprentissage d'une forme et évaluation prospective sur les cahiers D–G."""
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import re
import sys

from cartes import DATA, HERE, eligible

EDITIONS = {'H': 'IT2a', 'ZL': 'ZL3b'}
HASH = {'H':'7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5',
        'ZL':'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc'}
ROW = re.compile(r'^<(f\d+[rv])\.(\d+),[^!]P0>\s*(.*)')
UNIT = re.compile(r'c[kptf]h|ch|sh|[a-z]')
SPLITS = ('joints','separes')
N_PERMS = 19999


def read(name):
    return json.loads((HERE/name).read_text())


def save(name, data):
    (HERE/name).write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True)+'\n')


def tokens(faces, split):
    result = {}
    for edition, stem in EDITIONS.items():
        raw = (DATA/(stem+'-n.txt')).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == HASH[edition]
        pages = {f:[] for f in faces}
        for line in raw.decode().splitlines():
            row = ROW.match(line)
            if not row or row[1] not in pages:
                continue
            value = re.sub(r'<![^>]*>|<[%$]>|!', '', row[3])
            value = re.sub(r'<[-~]>', '.', value).replace(',', '.' if split == 'separes' else '')
            assert not any(c in value for c in '<>/ ')
            for i,word in enumerate((w for w in value.split('.') if w),1):
                basic = word.replace('{','').replace('}','')
                word = basic if re.fullmatch('[a-z]+',basic) else None
                pages[row[1]].append((f'{row[1]}.{row[2]}/{i}',word))
        result[edition] = pages
    return result


def extract(pages, face, rule):
    shared = []
    for pages_ed in pages.values():
        records = pages_ed[face] if rule=='otoldy' else pages_ed[face][:60]
        repertoire = defaultdict(list)
        for loc, w in records:
            if not w:
                continue
            if rule == 'finale':
                units = UNIT.findall(w)
                for size in (2,3):
                    if len(units)>size:
                        repertoire[' '.join(units[-size:])].append((loc,w))
            else:
                repertoire[w].append((loc,w))
        shared.append(repertoire)
    h,z = shared
    return {form:{'H':h[form], 'ZL':z[form]} for form in h.keys() & z.keys()}


def votes(lot):
    mapping = read('cle-'+lot+'.json')
    readers = [read('lecteur-'+r+'-'+lot+'.json') for r in ('I','II')]
    assert all(set(r)==set(mapping) for r in readers)
    judgments, joint = {},{}
    for code, record in mapping.items():
        v = [reader[code]['vote'] for reader in readers]
        assert all(x in ('O','N','?') for x in v)
        face = record['face']
        judgments[face] = v
        if v[0]==v[1] and v[0]!='?':
            joint[face]=v[0]
    return judgments,joint


def train(pages, labels, quires):
    pos = [f for f,t in labels.items() if t=='O']
    neg = [f for f,t in labels.items() if t=='N']
    rows = []
    if pos and neg:
        for form in set.union(set(),*(set(pages[f]) for f in pos)):
            yes = [f for f in pos if form in pages[f]]
            if len(yes)<3 or len({quires[f] for f in yes})<2:
                continue
            no = [f for f in neg if form in pages[f]]
            difference = Fraction(len(yes),len(pos))-Fraction(len(no),len(neg))
            rows.append((difference,len(yes),form,yes,no))
    rows.sort(key=lambda item:(-item[0],-item[1],item[2]))
    if not rows or rows[0][0]<=0:
        return {'forme':None,'candidats_admissibles':len(rows)}
    score,support,form,yes,no = rows[0]
    return {'forme':form,'score':str(score),'positifs':sorted(yes),'negatifs':sorted(no),
            'candidats_admissibles':len(rows),'ex_aequo_avant_ordre_alphabetique':
                [f for s,n,f,_,_ in rows if (s,n)==(score,support)]}


def frozen():
    quires = eligible()
    _, labels = votes('apprentissage')
    result = {'entrees_sha256':HASH, 'cotation_apprentissage':labels, 'conventions':{}}
    for split in SPLITS:
        all_tokens = tokens(quires,split)
        rules = {}
        for rule in ('mot','finale','otoldy'):
            forms = {f:extract(all_tokens,f,rule) for f in quires}
            model = train(forms,labels,quires) if rule!='otoldy' else {'forme':'otoldy'}
            selected = model['forme']
            model['presence'] = {f: selected in words if selected else None for f,words in forms.items()}
            model['lieux'] = {f:words[selected] for f,words in forms.items() if selected in words}
            rules[rule] = model
        result['conventions'][split] = {'regles':rules, 'positions':{ed:{f:len(a) for f,a in ps.items()}
                                                                   for ed,ps in all_tokens.items()}}
    return result


def counts(truth,pred):
    totals = Counter((v,pred[f]) for f,v in truth.items())
    tp,fn,fp,tn = [totals[key] for key in [('O',True),('O',False),('N',True),('N',False)]]
    advantage = None if not ((tp+fn) and (fp+tn)) else Fraction(tp,tp+fn)-Fraction(fp,fp+tn)
    return {'VP':tp,'FN':fn,'FP':fp,'VN':tn, 'score':str(advantage) if advantage is not None else None}


def permutations(truth, pred, quires):
    # Tous les feuillets de réserve offrent deux faces éligibles dans le corpus courant.
    # Brouiller le vecteur des prédictions avant d'appliquer le masque de cotation.
    strata = defaultdict(list)
    for f,q in quires.items():
        if q in 'DEFG' and f.endswith('r'):
            number=f[:-1]
            assert quires[number+'v']==q
            strata[q].append(number)
    by_leaf = {f:(pred[f+'r'],pred[f+'v']) for leaves in strata.values() for f in leaves}
    np = sum(y=='O' for y in truth.values())
    nn = sum(y=='N' for y in truth.values())
    if min(np,nn)==0:
        return None
    observed = counts(truth,pred)
    threshold = observed['VP']*nn - observed['FP']*np
    parts = [[(f,nn*(truth.get(f+'r')=='O')-np*(truth.get(f+'r')=='N'),
                  nn*(truth.get(f+'v')=='O')-np*(truth.get(f+'v')=='N')) for f in ff] for ff in strata.values()]
    vectors = [[by_leaf[f] for f,_,_ in block] for block in parts]
    rng = random.Random(1453)
    ge = 0
    for _ in range(N_PERMS):
        total = 0
        for weights, original in zip(parts,vectors):
            shuffled = original.copy()
            rng.shuffle(shuffled)
            total += sum(a*wr+b*wv for ((_,wr,wv),(a,b)) in zip(weights,shuffled))
        ge += total>=threshold
    return {'tirages':N_PERMS,'au_moins_observe':ge,'p_plus_un':(ge+1)/(N_PERMS+1)}


def previous_pages():
    old = json.loads((HERE.parent/'2026-11-18-otoldy-dessin/photos/CLE-CARTES.json').read_text())
    return {r['face'] for r in old.values() if r['face'] in eligible()}


def evaluate():
    prediction = read('PREDICTIONS.json')
    assert prediction == json.loads(json.dumps(frozen())), 'Écart avec les prédictions figées'
    qs = eligible()
    a, tr = votes('apprentissage')
    b, te = votes('reserve')
    out = {'votes':a|b,'reserve_primaire':te,'formes':{},'anciens_dessins':sorted(previous_pages())}
    for split, convention in prediction['conventions'].items():
        for rule, model in convention['regles'].items():
            if model['forme'] is None:
                out['formes'][split+'_'+rule]=None
                continue
            pred=model['presence']
            summary = {'forme':model['forme'],'apprentissage':counts(tr,pred),'reserves':{}}
            tests = {'ensemble':te,'hors_anciennes':{f:y for f,y in te.items() if f not in previous_pages()}}
            tests.update({q:{f:y for f,y in te.items() if qs[f]==q} for q in 'DEFG'})
            for name,subset in tests.items():
                summary['reserves'][name] = counts(subset,pred)
                if name in ('ensemble','hors_anciennes'):
                    summary['reserves'][name]['permutations'] = permutations(subset,pred,qs)
            out['formes'][split+'_'+rule]=summary
    return out


if __name__ == '__main__':
    if sys.argv[1:]==['predire']:
        save('PREDICTIONS.json',frozen())
    elif sys.argv[1:]==['evaluer']:
        save('RESULTATS.json',evaluate())
    else:
        sys.exit('Employer predire ou evaluer')
