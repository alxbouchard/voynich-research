"""Prédictions de voisinage dans les rangées de légendes pharmaceutiques."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
import json
import math
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH/'2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, tokens

GEOMETRY = json.loads((HERE/'RANGEES.json').read_text())
REGISTRY = json.loads((RESEARCH/'2026-11-18-noms-dans-les-notices/registre/registre.json').read_text())
WEAK = {r['fragment'] for r in REGISTRY['fragments'] if r['attachment'] in ('faible','multiple')}
WEAK.update(n for m in REGISTRY['montages_indetermines'] for n in [a['fragment'] for a in m['alternatives']])
SEED = 194736
SAMPLES = 19999


def write(name, value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=1)+'\n')


def form(raw, spacing):
    raw = re.sub(r'\{[^}]*\}', '?', raw)
    words = tokens(raw,spacing)
    if not words:
        return ()
    return tuple(re.findall(r'c[kptf]h|ch|sh|.',words[0]))


def read(slot, page, editions):
    if not slot['loci']:
        return {},None
    loc = page+'.'+str(slot['loci'][0])
    forms = []
    for edition in editions.values():
        if loc not in edition or edition[loc][1]!='Lf':
            return {},None
        forms.extend(form(edition[loc][3],sp) for sp in ('joints','separes'))
    full = ''.join(forms[0]) if len(set(forms))==1 and re.fullmatch('[a-z]+',''.join(forms[0])) else None
    agreed = {}
    for n in (1,2):
        prefixes = {f[:n] for f in forms}
        if len(prefixes)!=1:
            continue
        prefix,=prefixes
        if len(prefix)!=n or not all(u.isascii() and u.isalpha() for u in prefix):
            continue
        # Before a damaged sign we may not distinguish ch/sh/ckh from c/s.
        if any(f[n-1] in ('c','s') and any(not u.isalpha() for u in f[n:n+2]) for f in forms):
            continue
        agreed[n] = '.'.join(prefix)
    return agreed,full


def rowdata(q, editions, mode='all'):
    data=[]
    for r in GEOMETRY:
        if r['cahier']!=q or r['niveau']=='non_attribuee':
            continue
        pos=[]
        for i,p in enumerate(r['positions']):
            prefixes,complete = read(p,r['page'],editions) if mode=='all' or i%2==0 else ({},None)
            pos.append(dict(fragment=p['fragment'],loci=p['loci'],prefixes=prefixes,complete=complete))
        data.append(dict(page=r['page'],rang=r['rang'],niveau=r['niveau'],positions=pos))
    return data


def baseline(data):
    out = {}
    for n in (1,2):
        count=Counter(p['prefixes'][n] for r in data for p in r['positions'][::2] if n in p['prefixes'])
        out[n]=sorted(count,key=lambda w:(-count[w],w))[0] if count else None
    return out


def calls(data):
    predicted=[]
    for r in data:
        for left,right in zip(r['positions'][::2],r['positions'][1::2]):
            if left['prefixes']:
                predicted.append(dict(page=r['page'],rang=r['rang'],source=left['fragment'],
                    cible=right['fragment'],prefixes=left['prefixes']))
    return predicted


def prepare(editions):
    train=rowdata(15,editions)
    test=rowdata(19,editions,'odds')
    write('PREDICTIONS.json',dict(cahier=19,majoritaire=baseline(train),appels=calls(test),
          apprentissage=quick(train)))


def edges(row, every=False):
    return [(i,i+1) for i in range(0,len(row)-1,1 if every else 2)]


def score(row, pairs, remove_equal=False):
    hits=trials=0
    for i,j in pairs:
        a,b=row[i],row[j]
        if a is None or b is None:
            continue
        if remove_equal and a[1] is not None and a[1]==b[1]:
            continue
        trials+=1
        hits+=a[0]==b[0]
    return hits,trials


def counts(rows,n,every=False,restrict=False):
    out=[]
    for r in rows:
        if restrict and r['niveau']=='attribution_discutee':
            continue
        slots=[]
        for p in r['positions']:
            prefix=p['prefixes'].get(n)
            slots.append((prefix,p['complete']) if prefix and (not restrict or p['fragment'] not in WEAK) else None)
        out.append((r['page'],r['rang'],slots,edges(slots,every)))
    return out


def quick(rows):
    data={}
    for n in (1,2):
        arr=counts(rows,n)
        data[n]={'succes':sum(score(row,edge)[0] for _,_,row,edge in arr),
                 'comparables':sum(score(row,edge)[1] for _,_,row,edge in arr)}
    return data


def convolve(a,b):
    h=Counter()
    for x,m in a.items():
        for y,k in b.items():h[x+y]+=m*k
    return h


def summary(hist,observed):
    tot=hist.total()
    p=Fraction(sum(k for x,k in hist.items() if x>=observed),tot)
    return dict(espere=sum(x*k for x,k in hist.items())/tot,au_moins_observe=str(p),
                p=float(p),total=tot,histogramme=dict(sorted(hist.items())))


@lru_cache(None)
def local_null(pattern,mask,edgeset,remove_equal):
    # Un objet distinct par emplacement, même lorsque les formes sont identiques.
    # Les tirs au sort portent sur les seules positions lisibles.
    where=[i for i,good in enumerate(mask) if good]
    if not where:
        return Counter({0:1})
    byidx={actual:i for i,actual in enumerate(where)}
    pairs=[(byidx[a],byidx[b]) for a,b in edgeset if a in byidx and b in byidx]
    # En l'absence d'arête informative, toutes les permutations donnent zéro.
    if not pairs:
        return Counter({0:math.factorial(len(where))})
    return Counter(score(p,pairs,remove_equal)[0] for p in permutations(pattern))


def analyze(rows,n,every=False,restrict=False,remove_equal=False):
    arr=counts(rows,n,every,restrict)
    combined=Counter({0:1})
    total=valid=hits=calls_made=informative=0
    detail=[]
    for page,rank,row,pairs in arr:
        observed,num=score(row,pairs,remove_equal)
        mask=tuple(x is not None for x in row)
        present=tuple(x if remove_equal else (x[0],None) for x in row if x is not None)
        h=local_null(present,mask,tuple(pairs),remove_equal)
        combined=convolve(combined,h)
        total+=len(pairs)
        calls_made+=sum(row[i] is not None for i,_ in pairs)
        valid+=num
        hits+=observed
        informative+=len(h)>1
        detail.append(dict(page=page,rang=rank,comparables=num,succes=observed,permutable=len(h)>1))
    return dict(positions=total,appels=calls_made,comparables=valid,succes=hits,rangees=len(arr),
                rangees_avec_comparaisons=sum(v['comparables']>0 for v in detail),
                rangees_informatives=informative,par_rangee=detail,condition_rangee=summary(combined,hits))


def panel_null(rows,n):
    """Les groupes indépendants sont les panneaux, les rangées gardent leurs emplacements masqués."""
    pools=defaultdict(list)
    for page,_,row,pairs in counts(rows,n):
        pools[page].append((row,pairs))
    measured=0
    expectation=Fraction()
    # Simuler tous les panneaux à chaque tirage, sans estimer un histogramme par panneau.
    rng=random.Random(SEED+n)
    setups=[]
    for group in pools.values():
        readable=[]
        pairs=[]
        for row,edgeset in group:
            ids={}
            for i,item in enumerate(row):
                if item:
                    ids[i]=len(readable);readable.append(item[0])
            pairs.extend((ids[i],ids[j]) for i,j in edgeset if i in ids and j in ids)
        measured+=sum(readable[a]==readable[b] for a,b in pairs)
        k=Counter(readable);N=len(readable)
        if N>=2:
            expectation+=Fraction(len(pairs)*sum(t*(t-1) for t in k.values()),N*(N-1))
        setups.append((readable,pairs))
    favorable=0
    for _ in range(SAMPLES):
        h=0
        for items,pr in setups:
            rng.shuffle(items)
            h+=sum(items[a]==items[b] for a,b in pr)
        favorable+=h>=measured
    return dict(espere=float(expectation),succes=measured,simulations=SAMPLES,graine=SEED+n,
                tirages_au_moins_observe=favorable,p_plus_un=(favorable+1)/(SAMPLES+1))


def validation(editions):
    pred=json.loads((HERE/'PREDICTIONS.json').read_text())
    data={}
    for q in (15,19):
        rows=rowdata(q,editions)
        measured={}
        for n in (1,2):
            raw=counts(rows,n)
            std=analyze(rows,n)
            b=pred['majoritaire'][str(n)]
            std['reference_constante']={'forme':b,
                'succes':sum(row[j][0]==b for _,_,row,pr in raw for i,j in pr if row[i] and row[j])}
            std['condition_panneau']=panel_null(rows,n)
            measured[n]=dict(principal=std,chaque_arete=analyze(rows,n,True),
                             moins_discute=analyze(rows,n,restrict=True),
                             sans_doublons=analyze(rows,n,remove_equal=True))
        data[q]=dict(initiales=measured,objets=rows)
        if q==19:
            calls_file=json.loads(json.dumps(calls(rows)))
            assert calls_file==pred['appels']
            byfrag={p['fragment']:p for r in rows for p in r['positions']}
            data[q]['confrontation']=[dict(v,observe=byfrag[v['cible']]['prefixes']) for v in calls_file]
    witness={}
    for name,sequence in [('classe','aaaabbbb'),('alterne','abababab')]:
        mock=[dict(page='artificiel',rang=i,niveau='temoin',positions=[
           dict(fragment=i*8+j,prefixes={1:x},complete=x+str(j)) for j,x in enumerate(sequence)])
           for i in range(3)]
        witness[name]=analyze(mock,1)
    write('RESULTATS.json',dict(cahiers=data,temoin=witness))


if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument('mode',choices=['predire','verifier'])
    which=args.parse_args().mode
    editions,_=corpus()
    (prepare if which=='predire' else validation)(editions)
