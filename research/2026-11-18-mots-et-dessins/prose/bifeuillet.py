"""Masque pour chaque cible son conjugué matériel dans l'apprentissage."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import re
import sys
from prose import ALIAS, CLASSES, HERE, SOURCES, TRAIN, TRUTH, classify, features, prepare, write

def material(path):
    flags = {}
    for line in path.open():
        m=re.match(r'^<f(\d+)[rv]\d*>\s*(.*)',line)
        if not m: continue
        fol=int(m[1])
        if fol not in TRAIN and fol not in TRUTH: continue
        d=dict(re.findall(r'\$(\w)=(\w+)',m[2]))
        if d['I'] in ('H','B') and d['H']=='2' and d['L']=='B':
            flags[fol] = (d['Q'],d['B'])
    return flags

def predict(train,test,flags,labels):
    decisions={}
    for fol,v in test.items():
        if flags is None:
            partial=train
        else:
            partial={f:c for f,c in train.items() if flags[f]!=flags[fol]}
        decisions[fol]=classify(partial,{fol:v},labels)[fol]
    return decisions

def main():
    source=Path(sys.argv[1])
    out={}
    for name, file in SOURCES.items():
        path=source/file
        flags=material(path)
        for split in [False,True]:
            sample=prepare(path,split)
            train={f:features(sample[f]) for f in TRAIN}
            test={f:features(sample[f]) for f in TRUTH}
            actual=predict(train,test,flags,TRAIN)
            matched={f:[g for g in train if flags[f]==flags[g]] for f in test}
            correct=sum(p['prediction']==TRUTH[f] for f,p in actual.items())
            histogram=Counter()
            for candidate in combinations(sorted(train),5):
                selection=set(candidate)
                truth={f:('herbier' if f in selection else 'bain') for f in train}
                predictions=predict(train,test,flags,truth)
                for other in combinations(sorted(test),5):
                    s=set(other)
                    acc=sum(p['prediction']==('herbier' if f in s else 'bain') for f,p in predictions.items())
                    histogram[acc]+=1
            out[name+('_separe' if split else '_joint')]={
                'succes':correct, 'exclusions':matched,'bifeuillets':flags,
                'resultat':{f:{**p,'attendu':TRUTH[f]} for f,p in actual.items()},
                'nul':{'histogramme':dict(histogram),'au_moins_observe':sum(n for k,n in histogram.items() if k>=correct),'total':sum(histogram.values())}}
    write('BIFEUILLET.json',out)
if __name__=='__main__': main()
