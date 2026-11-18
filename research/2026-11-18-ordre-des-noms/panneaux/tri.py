"""Simulation des mêmes rangées triées ; recoupement exact sur les couples disjoints."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
import json
import random
from voisins import HERE, SAMPLES, convolve, write


@lru_cache(None)
def matched_pairs(frequencies, edges):
    if not edges:
        return {0:Fraction(1)}
    law=Counter()
    size=sum(frequencies)
    for i,a in enumerate(frequencies):
        for j,b in enumerate(frequencies):
            ways=a*(b-(i==j))
            if not ways:
                continue
            rest=list(frequencies)
            rest[i]-=1
            rest[j]-=1
            remaining=tuple(sorted(v for v in rest if v))
            weight=Fraction(ways,size*(size-1))
            for h,p in matched_pairs(remaining,edges-1).items():
                law[h+int(i==j)] += weight*p
    return dict(law)


def observed_layout(data):
    result=[]
    for row in data:
        labels=[p['prefixes'].get('1') for p in row['positions']]
        counts=Counter(x for x in labels if x)
        compact={i:sum(v is not None for v in labels[:i]) for i,v in enumerate(labels) if v}
        pairs=[(compact[i],compact[i+1]) for i in range(0,len(labels)-1,2) if i in compact and i+1 in compact]
        result.append((counts,pairs))
    return result


def evaluation(record,q):
    layout=observed_layout(record['objets'])
    stats=record['initiales']['1']['principal']['condition_rangee']
    law=Counter({0:Fraction(1)})
    for counts,pairs in layout:
        law=convolve(law,matched_pairs(tuple(sorted(counts.values())),len(pairs)))
    assert all(law[h]*stats['total']==m for h,m in ((int(k),v) for k,v in stats['histogramme'].items()))
    assert sum(law.values())==1
    tail=Fraction(0)
    threshold=max(law)+1
    for n in sorted(law,reverse=True):
        tail+=law[n]
        if tail>Fraction(1,20):
            break
        threshold=n
    letters=sorted(set().union(*(set(c) for c,_ in layout)))
    caches=[{} for _ in layout]
    def hits(i,order):
        freq,pairs=layout[i]
        local=tuple(x for x in order if x in freq)
        if local not in caches[i]:
            flat=[x for x in local for _ in range(freq[x])]
            caches[i][local]=sum(flat[a]==flat[b] for a,b in pairs)
        return caches[i][local]
    best=sum(max(hits(i,o) for o in permutations(c)) for i,(c,_) in enumerate(layout))
    histogram=Counter()
    rng=random.Random(30719+q)
    for _ in range(SAMPLES):
        rng.shuffle(letters)
        histogram[sum(hits(i,letters) for i in range(len(layout)))] += 1
    exhaustive=Counter()
    for order in permutations(sorted(letters)):
        exhaustive[sum(hits(i,order) for i in range(len(layout)))] += 1
    returns=[]
    for row in record['objets']:
        visible=[(p['fragment'],p['prefixes']['1']) for p in row['positions'] if '1' in p['prefixes']]
        witness=next(([a,b,c] for i,a in enumerate(visible) for j,b in enumerate(visible[i+1:],i+1)
                      for c in visible[j+1:] if a[1]==c[1] and a[1]!=b[1]),None)
        if witness:
            returns.append(dict(page=row['page'],rang=row['rang'],trois_fragments=witness))
    return dict(retours=returns,alphabets_exhaustifs=dict(sorted(exhaustive.items())),
                exhaustifs_au_seuil=sum(v for h,v in exhaustive.items() if h>=threshold),seuil_critique=threshold,initiales=sorted(letters),graine=30719+q,
                repetitions=SAMPLES,histogramme=dict(sorted(histogram.items())),
                au_seuil=sum(v for h,v in histogram.items() if h>=threshold),
                moyenne=sum(k*v for k,v in histogram.items())/SAMPLES,
                maximum_si_ordre_par_rangee=best)


if __name__=='__main__':
    results=json.loads((HERE/'RESULTATS.json').read_text())
    write('TRI-TEMOIN.json',{q:evaluation(r,int(q)) for q,r in results['cahiers'].items()})
