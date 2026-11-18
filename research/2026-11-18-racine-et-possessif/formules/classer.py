"""Chercher un pivot après deux familles, puis éprouver la règle sur des notices réservées."""
from collections import Counter, defaultdict
import csv
from hashlib import sha256
from fractions import Fraction
from itertools import chain, permutations
import json
from math import comb, factorial, log
from pathlib import Path
import random
import re

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
EDIT = RESEARCH / '2026-11-18-opcheor-paralleles/latin'
SOURCE = RESEARCH / '2026-11-18-legendes-repetitions/temoin/occurrences.tsv'
PROTOCOL_SHA = '7ba17171163e58024cbf3206cf3a3f74e4f685f2011442ec7d9dd251c3835b93'
SEED = 147831

def notices():
    text = json.loads((EDIT/'corpus.json').read_bytes())
    with (EDIT/'vers.tsv').open() as src:
        for row in csv.DictReader(src, delimiter='\t'):
            title = row['titre']
            words = text[title][int(row['premier_mot_notice'])-1:int(row['dernier_mot_notice'])]
            yield dict(chapter=int(row['notice']),title=title,line=int(row['rang_du_vers']),
                       words=[w.replace('j','i') for w in words])

def family(word):
    return word[:3] if len(word)>=3 else None

def families_of(rows):
    lexicon=defaultdict(set)
    for row in rows:
        for word in row['words']:
            if family(word):
                lexicon[family(word)].add(word)
    return {f for f,words in lexicon.items() if len(words)>=2}

def ranks(scored):
    # Scores égaux au douzième chiffre décimal reçoivent le même rang.
    order=sorted(scored.items(),key=lambda p:(-round(p[1],12),p[0]))
    rval=0;prev=None
    result={}
    for i,(key,val) in enumerate(order,1):
        val=round(val,12)
        if val!=prev:
            rval=i
            prev=val
        result[key]=rval
    return result

def score(rows):
    accepted=families_of(rows)
    actual=Counter();expected=Counter();pages=defaultdict(set);partners=defaultdict(set)
    for row in rows:
        words=row['words'];n=len(words)
        for x,y in zip(words,words[1:]):
            f=family(x)
            if f in accepted:
                actual[f,y]+=1
                pages[f,y].add(row['chapter'])
                partners[f,y].add(x)
        fac=Counter(family(w) for w in words if family(w) in accepted)
        for y,ny in Counter(words).items():
            for f,nf in fac.items():
                expected[f,y]+=ny*(nf-int(f==family(y)))/n
    scores=defaultdict(dict)
    for (f,y),observed in actual.items():
        e=expected[f,y]
        if len(pages[f,y])>=2 and observed>e:
            scores[y][f]=2*(observed*log(observed/e)-observed+e)
    gains={y:sum(sorted(s.values(),reverse=True)[:2]) for y,s in scores.items() if len(s)>=2}
    return dict(rangs=ranks(gains),gains=gains,rangs_familles={y:ranks(s) for y,s in scores.items()},
                scores=scores,observes=actual,attendus=expected,notices=pages,voisins=partners)

def scrambled(rows):
    alphabet=sorted(set(''.join(chain.from_iterable(r['words'] for r in rows))))
    letters=[chr(0xE000+n) for n in range(len(alphabet))]
    random.Random(408).shuffle(letters)
    e=dict(zip(alphabet,letters))
    return [{**r,'words':[''.join(e[ch] for ch in w) for w in r['words']]} for r in rows],e

def enrich(y,analytics):
    return {
        'mot':y,'rang':analytics['rangs'].get(y),'score':round(analytics['gains'].get(y,0),8),
        'familles':[dict(famille=f,rang=rank,occurrences=analytics['observes'][f,y],
                         esperance=round(analytics['attendus'][f,y],8),
                         score=round(analytics['scores'][y][f],8),
                         notices=sorted(analytics['notices'][f,y]),
                         formes=sorted(analytics['voisins'][f,y]))
                    for f,rank in analytics['rangs_familles'].get(y,{}).items()]}

def truth_rows(rows, marker, organ_forms):
    counts=Counter();found=[]
    for row in rows:
        for i,(a,b) in enumerate(zip(row['words'],row['words'][1:]),1):
            if b==marker and family(a) in ('rad','fol'):
                counts[family(a)]+=1
                found.append(dict(notice=row['chapter'],titre=row['title'],vers=row['line'],
                             rang=i,mot_gauche=a,mot_droit=b,organe=organ_forms.get(a),contexte=' '.join(row['words'])))
    return counts,found

def shuffle_reserve(rows,marker):
    rng=random.Random(SEED);dist=Counter()
    for _ in range(999):
        n=0
        for row in rows:
            if marker not in row['words'] or not any(family(w) in ('rad','fol') for w in row['words']):
                continue
            ws=row['words'].copy()
            rng.shuffle(ws)
            n+=sum(b==marker and family(a) in ('rad','fol') for a,b in zip(ws,ws[1:]))
        dist[n]+=1
    return dist

def line_distribution(n, a, b):
    # Fusionner k paires orientées disjointes et permuter les n-k unités.
    moments = [Fraction(comb(a,k)*comb(b,k)*factorial(k)*factorial(n-k),factorial(n))
               for k in range(min(a,b)+1)]
    return {i:sum((-1)**(k-i)*comb(k,i)*moments[k] for k in range(i,len(moments)))
            for i in range(len(moments))}

def exact_reserve(rows, marker, observed):
    toy='ffmmx'
    brute=Counter(sum(a=='f' and b=='m' for a,b in zip(w,w[1:])) for w in permutations(toy))
    assert line_distribution(5,2,2)=={i:Fraction(n,factorial(5)) for i,n in brute.items()}
    dist={0:Fraction(1)}; informing=0
    for row in rows:
        words=row['words']
        a=sum(family(w) in ('rad','fol') for w in words)
        b=words.count(marker)
        if not a or not b:
            continue
        informing+=1
        per_line=line_distribution(len(words),a,b)
        convolution=Counter()
        for previous,prob in dist.items():
            for new,weight in per_line.items():
                convolution[previous+new]+=prob*weight
        dist=convolution
    assert sum(dist.values())==1
    tail=sum(p for i,p in dist.items() if i>=observed)
    return {'vers_contributifs':informing,'loi':{k:str(v) for k,v in dist.items()},
            'esperance':float(sum(k*p for k,p in dist.items())),
            'queue_exacte':str(tail),'queue_decimale':float(tail)}

def main():
    assert sha256((HERE/'PROTOCOLE.md').read_bytes()).hexdigest()==PROTOCOL_SHA
    full=list(notices())
    # Les titres sont contrôlés avant le calcul. Le nom de la chélidoine est Celidonia dans la tradition manuscrite.
    omit=[r for r in full if re.search(r'^[Cc]h?elid',r['title'])]
    assert len({r['title'] for r in omit})==1
    known={r['chapter'] for r in omit}
    train=[r for r in full if r['chapter'] not in known and r['chapter']%2]
    held=[r for r in full if r['chapter'] not in known and not r['chapter']%2]
    assert len({r['chapter'] for r in train+held})==76
    model=score(train)
    masked,key=scrambled(train);check=score(masked)
    mask=lambda w:''.join(key[ch] for ch in w)
    assert len(check['rangs'])==len(model['rangs'])
    assert all(check['rangs'][mask(w)]==n for w,n in model['rangs'].items())
    assert all(check['rangs_familles'][mask(w)][mask(f)]==n for w,fs in model['rangs_familles'].items() for f,n in fs.items())
    marker='eius'
    families=model['rangs_familles'].get(marker,{})
    identifiable=model['rangs'].get(marker,10**9)<=3 and all(families.get(k,10**9)<=5 for k in ['rad','fol'])
    with SOURCE.open() as f:
        pos={r['forme'].replace('j','i'):r['lemme'] for r in csv.DictReader(f,delimiter='\t')}
    counts,extracted=truth_rows(held,marker,pos)
    counts1,extracted1=truth_rows(train,marker,pos)
    perm=shuffle_reserve(held,marker)
    total=sum(counts.values());tail=sum(n for k,n in perm.items() if k>=total)
    transferred=identifiable and {'radix','folium'} <= {r['organe'] for r in extracted} and tail/999<.05
    report=dict(sources={f.name:sha256(f.read_bytes()).hexdigest() for f in [SOURCE,EDIT/'corpus.json',EDIT/'vers.tsv']},
                notice_ecartee=sorted(known),notices_developpement=len({r['chapter'] for r in train}),
                notices_reserve=len({r['chapter'] for r in held}),vers=[len(train),len(held)],
                nb_mots_droits_tous=len({b for r in train for b in r['words'][1:]}),
                nb_mots_avec_deux_familles=len(model['gains']),
                classement_mots=[dict(mot=k,rang=v,score=round(model['gains'][k],8)) for k,v in model['rangs'].items()],
                premiers=[enrich(y,model) for y,n in model['rangs'].items() if n<=3],
                audit_cle=enrich(marker,model),anonymisation_rangs_identiques=True,identification=identifiable,
                developpement_cible=extracted1,reserve_cible=extracted,melanges_999=dict(sorted(perm.items())),
                au_moins_autant=tail,p_avec_correction=(1+tail)/1000,
                permutation_exacte=exact_reserve(held,marker,total),
                transfert_autorise=transferred)
    (HERE/'resultats.json').write_text(json.dumps(report,ensure_ascii=False,indent=1)+'\n')
    print('Reservé',report['notice_ecartee'],report['notices_developpement'],report['notices_reserve'],report['vers'])
    print('Mots', report['nb_mots_droits_tous'],report['nb_mots_avec_deux_familles'],report['classement_mots'][:6])
    print('eius',report['audit_cle']['rang'],'familles',[(f['famille'],f['rang'],f['occurrences']) for f in report['audit_cle']['familles']][:12])
    print('Vérité',dict(counts1),dict(counts),'mélanges',dict(perm),tail,'transfert',transferred)

if __name__=='__main__':
    main()
