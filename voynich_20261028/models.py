#!/usr/bin/env python3
"""Out-of-leaf and out-of-quire structural models, with an explicit null control."""
import collections
import json
import math
import random
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupKFold

from analyse import ROOT, OUT, PROTOCOL, SEED, parse, write_json

ALPHABET = 'abcdefghijklmnopqrstuvwxyz?'
ALPHA = 0.5


def train(records, order):
    counts=collections.defaultdict(collections.Counter)
    totals=collections.Counter()
    for r in records:
        for word in r['clean']:
            padded='^'*order+word
            for i,c in enumerate(word):
                ctx=padded[i:i+order] if order else ''
                counts[ctx][c]+=1;totals[ctx]+=1
    return counts,totals


def evaluate(records,order,model):
    counts,totals=model
    loss=n=0
    for r in records:
        for word in r['clean']:
            padded='^'*order+word
            for i,c in enumerate(word):
                ctx=padded[i:i+order] if order else ''
                probability=(counts.get(ctx,{}).get(c,0)+ALPHA)/(totals[ctx]+ALPHA*len(ALPHABET))
                loss-=math.log2(probability);n+=1
    return loss,n


def grouped_scores(records, groupfield):
    groups=[r['leaf'] if groupfield=='leaf' else r['metadata']['Q'] for r in records]
    splits=list(GroupKFold(n_splits=5).split(records,groups=groups))
    output=[]
    for order in range(4):
        folds=[]
        for fold,(traini,testi) in enumerate(splits):
            training=[records[i] for i in traini];test=[records[i] for i in testi]
            assert not (set(groups[i] for i in traini)&set(groups[i] for i in testi))
            loss,n=evaluate(test,order,train(training,order))
            folds.append(dict(fold=fold,bits_per_EVA_char=loss/n,total_bits=loss,characters=n,
                              train_groups=sorted(set(groups[i] for i in traini)),test_groups=sorted(set(groups[i] for i in testi))))
        output.append(dict(order=order,bits_per_EVA_char=sum(f['total_bits'] for f in folds)/sum(f['characters'] for f in folds),folds=folds))
        print(groupfield,'context',order,round(output[-1]['bits_per_EVA_char'],5),flush=True)
    return output


def shuffle_words(records):
    rng=random.Random(SEED)
    result=[]
    for r in records:
        words=[]
        for word in r['clean']:
            chars=list(word);rng.shuffle(chars);words.append(''.join(chars))
        # Same record order, exact word lengths, exact per-word and per-page
        # letter frequencies. Original metadata remain only for grouping.
        result.append(dict(r,clean=words))
    return result


def main():
    # Parse and authenticate both before modelling either.
    corpora={n:parse(n)[0] for n in PROTOCOL['corpora']}
    assert all(x['gate_pass'] for x in json.loads((OUT/'integrity.json').read_text()))
    results={}
    for name,records in corpora.items():
        print('MODELLING',name,flush=True)
        # Exclude extraneous marginalia and invalid/spurious loci.
        records=[r for r in records if r['type']!='Lx' and r['locator']!='!' and r['clean']]
        results[name]=dict(real_leaf=grouped_scores(records,'leaf'),
                           real_quire=grouped_scores(records,'quire'),
                           shuffled_leaf=grouped_scores(shuffle_words(records),'leaf'))
    write_json('models.json',dict(seed=SEED,predicted_alphabet=ALPHABET,alpha=ALPHA,
                                 unit='bits per lowercase EVA character, within clean words, word start conditioned, no end marker',
                                 interpretation='Structure prediction only. This is not a cipher solver or a semantic decoding test.',corpora=results))
    print('MODELS COMPLETE',flush=True)


if __name__=='__main__':main()
