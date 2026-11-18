"""Contrôle exploratoire après transfert : mélanger uniquement les légendes simples d'un même panneau."""
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import permutations
import random
import sys
sys.dont_write_bytecode=True
from ajuster import MODELES, equations,load,save,solve

def compare():
    rows=load('REGISTRE.json.gz')
    panels=defaultdict(list); edges=defaultdict(list); words={}
    for row in rows:
        f=row['fragments']; p=row['page']
        for item in f:
            if item['mots'] and len(item['mots'])==1:
                panels[p].append(item['id']);words[item['id']]=item['mots']
        edges[p].extend((a['id'],b['id']) for a,b in zip(f,f[1:]) if a['id'] in words and b['id'] in words)
    result={}
    for mode in ('qualificatifs','allemand'):
        good=set(); expectation=Fraction(0)
        for p,ids in panels.items():
            count=0
            for a,b in permutations(ids,2):
                eq=equations(words[a],words[b],mode,'direct')
                if next(solve(eq),None) is not None:
                    good.add((a,b));count+=1
            if len(ids)>1:
                expectation+=len(edges[p])*Fraction(count,len(ids)*(len(ids)-1))
        observed=sum(e in good for pairs in edges.values() for e in pairs)
        samples=25000; rng=random.Random(951496)
        hist=Counter()
        for _ in range(samples):
            total=0
            for p,items in panels.items():
                if not edges[p]:continue
                values=items.copy();rng.shuffle(values);d=dict(zip(items,values))
                total+=sum((d[a],d[b]) in good for a,b in edges[p])
            hist[total]+=1
        result[mode]={'observe':observed,'moyenne_exacte':str(expectation),'paires_orientees_compatibles_meme_panneau':len(good),
                      'paires_orientees_meme_panneau':sum(len(ns)*(len(ns)-1) for ns in panels.values()),
                      'tirages':samples,'graine':951496,'histogramme':dict(sorted(hist.items())),
                      'tirages_au_moins_observe':sum(v for k,v in hist.items() if k>=observed)}
    save('CONTROLE.json',result)

if __name__=='__main__':compare()
