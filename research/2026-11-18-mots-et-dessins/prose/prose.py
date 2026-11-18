"""Classifier les 40 premiers emplacements de prose d'un feuillet avec deux types d'images."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from math import log
from pathlib import Path
import random
import re

HERE = Path(__file__).resolve().parent
CLASSES = {'herbier': [26,31,33,34,39,40,43,46,50,55], 'bain': [75,76,77,78,79,82,83,84]}
TRAIN = {f: k for k, folios in CLASSES.items() for f in folios[::2]}
TRUTH = {f: k for k, folios in CLASSES.items() for f in folios[1::2]}
IDS = list('ABCDEFGHI')
random.Random(738108).shuffle(IDS)
ALIAS = dict(zip(sorted(TRUTH), IDS))
SOURCES = {'H':'IT2a-n.txt', 'ZL':'ZL3b-n.txt'}

def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)+'\n')

def prepare(filename, split_commas):
    page_head = re.compile(r'^<f(\d+)[rv]\d*>\s*(.*)')
    record = re.compile(r'^<(f\d+[rv]\d*)\.[^,]+,([^!])P0(?:;.)?>(.*)')
    current = None
    bins = defaultdict(list)
    for line in filename.open():
        header = page_head.match(line)
        if header:
            num = int(header[1])
            current = None
            if num in TRAIN or num in TRUTH:
                meta = dict(re.findall(r'\$(\w)=(\w+)',header[2]))
                if meta['H']=='2' and meta['L']=='B' and meta['I'] in ['B','H']:
                    assert num in CLASSES[{'B':'bain','H':'herbier'}[meta['I']]]
                    current = num
            continue
        if current is None or len(bins[current]) >= 40:
            continue
        match = record.match(line)
        if not match: continue
        # Neither edition splits these particular records across file lines.
        body = re.sub(r'<![^>]*>', '', match[3]).strip()
        assert '/' not in body, (current, match[1])
        body = re.sub(r'<[-~]>', '.', body)
        body = re.sub(r'<[%$]>|!', '', body)
        body = body.replace(',', '.' if split_commas else '')
        for slot in (s for s in body.split('.') if s):
            bins[current].append(slot if re.fullmatch(r'[a-z]+',slot) else None)
            if len(bins[current]) == 40: break
    assert set(bins)==set(TRAIN)|set(TRUTH)
    return bins

def features(slots):
    return Counter(s for s in slots if s is not None)

def classify(train, evaluation, truth_train):
    word_counts = {c:Counter() for c in CLASSES}
    for tag,counts in train.items():
        word_counts[truth_train[tag]].update(counts)
    vocab = set(word_counts['herbier']) | set(word_counts['bain'])
    denom = {c:sum(v.values())+len(vocab) for c,v in word_counts.items()}
    outcome={}
    for tag, counts in evaluation.items():
        known = {w:n for w,n in counts.items() if w in vocab}
        scores = {c:sum(n*log((word_counts[c][w]+1)/denom[c]) for w,n in known.items()) for c in CLASSES}
        delta=scores['herbier']-scores['bain']
        predicted=('herbier' if delta>0 else 'bain') if abs(delta)>1e-10 else 'abstention'
        outcome[tag]={'prediction':predicted,'log_p':scores,'exploitables':sum(counts.values()),'connus':sum(known.values())}
    return outcome

def reserve_key():
    return {ALIAS[f]: {'folio': f,'classe':k} for f,k in TRUTH.items()}

def permutation(train,evaluation,observed):
    hist=Counter()
    keys=sorted(train)
    slots=sorted(evaluation)
    pool=list(map(set,combinations(range(9),5)))
    assert len(pool)==126
    for sel in pool:
        labels={tag:('herbier' if i in sel else 'bain') for i,tag in enumerate(keys)}
        outcome=classify(train,evaluation,labels)
        pred=[outcome[tag]['prediction'] for tag in slots]
        for sel2 in pool:
            count=sum(p==('herbier' if i in sel2 else 'bain') for i,p in enumerate(pred))
            hist[count]+=1
    return {'histogramme':dict(sorted(hist.items())), 'total':sum(hist.values()),
            'au_moins_observe':sum(q for k,q in hist.items() if k>=observed)}

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument('mode',choices=['predire','evaluer'])
    arg.add_argument('source',type=Path,help='Répertoire contenant IT2a-n.txt et ZL3b-n.txt')
    args=arg.parse_args()
    entered={}
    if args.mode=='evaluer':
        entered=json.loads((HERE/'PREDICTIONS.json').read_text())
    output={}
    blind={}
    for tx,basename in SOURCES.items():
        for cut in [False,True]:
            key=tx+('_separe' if cut else '_joint')
            bins=prepare(args.source/basename,cut)
            training={f:features(bins[f]) for f in TRAIN}
            evaluation={alias:features(bins[f]) for f,alias in ALIAS.items()}
            pred=classify(training,evaluation,TRAIN)
            if args.mode=='predire':
                blind[key]=pred
                continue
            assert pred==entered[key]
            matrix={c: Counter() for c in CLASSES}
            decisions={}
            for tag,ref in reserve_key().items():
                p=pred[tag]
                matrix[ref['classe']][p['prediction']]+=1
                decisions[tag]={'folio':ref['folio'],'attendu':ref['classe'],**p}
            observed=sum(matrix[c][c] for c in CLASSES)
            output[key]={'matrice':matrix,'succes':observed,'reserve':decisions,
                'nul':permutation(training,evaluation,observed),
                'prelevement':{f:{'lues':len(v),'exploitables':sum(x is not None for x in v),'lot':'apprentissage' if f in TRAIN else 'reserve'} for f,v in bins.items()},
                'sha256_source':sha256((args.source/basename).read_bytes()).hexdigest()}
    if args.mode=='predire':
        write('PREDICTIONS.json',blind)
    else:
        write('RESULTATS.json',output)
        write('CLE.json',reserve_key())

if __name__=='__main__': main()
