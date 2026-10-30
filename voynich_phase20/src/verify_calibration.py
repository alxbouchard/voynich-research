#!/usr/bin/env python3
"""Independent Python rescoring and segmentation checks for the C++ solver.

CC BY-SA 4.0; original combined scoring: Hauer, Hayward & Kondrak (2014).
"""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import numpy as np
import audit_author_segmentation as reference
import calibration as study

ROOT=study.ROOT


def load_model(folder):
    words=[''];tables={}
    rows=[]
    for line in (folder/'words.tsv').read_text().splitlines():
        word,p=line.split();words.append(word);rows.append((word,float(p)))
    tables['word',1]={(w,):p for w,p in rows}
    for n,name in ((2,'bigrams.tsv'),(3,'trigrams.tsv')):
        tables['word',n]={}
        for line in (folder/name).read_text().splitlines():
            fields=line.split();key=tuple(words[int(x)] for x in fields[:n])
            tables['word',n][key]=float(fields[n])
    chars='abcdefghijklmnopqrstuvwxyz_'
    for n in (1,2,3):
        values=np.fromfile(folder/f'char{n}.bin',dtype=np.float64)
        tables['char',n]={tuple(chars[x] for x in coordinates):float(values[i])
                          for i,coordinates in enumerate(itertools.product(range(27),repeat=n)) if values[i]}
    return tables


def segment(folder,text,mode):
    file=study.TMP/'verification_input.txt';file.write_text(text+'\n')
    result=subprocess.run([str(study.EXECUTABLE),str(folder),'segment',str(file),mode],capture_output=True,text=True,check=True)
    assert not result.stderr
    return json.loads(result.stdout)


def development():
    study.compile_solver()
    # Translate the previously audited, reduced author model, without fitting.
    reduced=study.read(ROOT/'tmp/reduced_model_tables.json')
    folder=study.TMP/'author_diagnostic';folder.mkdir(parents=True,exist_ok=True)
    words=sorted(w for w,p in reduced['word1'] if set(w)<=set(study.ALPHABET))
    ids={w:i+1 for i,w in enumerate(words)}
    one=dict(reduced['word1'])
    (folder/'words.tsv').write_text(''.join(f'{w}\t{one[w]:.17g}\n' for w in words))
    for n,name in ((2,'bigrams.tsv'),(3,'trigrams.tsv')):
        lines=[]
        for key,p in reduced['word'+str(n)]:
            ws=key.split('\t')
            if all(w in ids for w in ws):
                lines.append('\t'.join(map(str,[*(ids[w] for w in ws),p]))+'\n')
        (folder/name).write_text(''.join(lines))
    for n in (1,2,3):
        values=np.zeros(27**n)
        for key,p in reduced['char'+str(n)]:
            cs=key.split('\t')
            if all(c in study.ALPHABET+'_' and len(c)==1 for c in cs):
                index=0
                for c in cs:index=index*27+(26 if c=='_' else ord(c)-97)
                values[index]=p
        values.tofile(folder/f'char{n}.bin')
    np.zeros(26**4).tofile(folder/'quad.bin');np.ones(26).tofile(folder/'freq.bin')
    audit=study.read(ROOT/'results/authors_exact_segmentation_audit.json')
    checks=[]
    for row in audit['rows']:
        for mode in ('greedy','exact'):
            cpp=segment(folder,row['letters'],mode)
            expected=row['greedy_segmentation'] if mode=='greedy' else row['exact']['segmentation']
            score=row['greedy_scores']['combined_score_ln'] if mode=='greedy' else row['exact']['score_ln']
            assert cpp['segmentation']==expected and abs(cpp['score']-score)<1e-9
            checks.append({'candidate':row['candidate'],'mode':mode,'difference':abs(cpp['score']-score)})
    # Randomized exhaustive short cases exercise one-letter and long-word history.
    for language in ('latin','italian'):
        study.train_models(language)
        folder=study.TMP/language;tables=load_model(folder)
        vocab={x[0] for x in tables['word',1]}
        rng=random.Random(902+len(language))
        for _ in range(12):
            text=''.join(rng.choice('aeirst') for _ in range(9))
            edges=reference.edges_for(text,vocab)
            exhaustive=reference.exhaustive_check(edges,tables)
            cpp=segment(folder,text,'exact')
            assert abs(cpp['score']-exhaustive['best_score_ln'])<1e-9
            greedy=segment(folder,text,'greedy')
            expected=reference.greedy(text,vocab)
            assert greedy['segmentation']==expected
            assert abs(greedy['score']-reference.full_score(expected,tables)['combined_score_ln'])<1e-9
            checks.append({'language':language,'letters':text,'paths':exhaustive['paths_enumerated'],
                           'difference':abs(cpp['score']-exhaustive['best_score_ln'])})
    study.save(ROOT/'results/calibration_development_checks.json',{'passed':True,'checks':checks,
             'scope':'Known development fixture and short random strings; no reserved calibration plaintext or encryption keys used.'})
    print(json.dumps({'development_checks':len(checks),'passed':True}),flush=True)


def independent_metrics(actual,truth):
    def parse(s):
        letters=[];ends=set()
        for c in s:
            if c==' ':ends.add(len(letters))
            else:letters.append(c)
        ends.discard(0);ends.discard(len(letters))
        return letters,ends
    a,ap=parse(actual);b,bp=parse(truth)
    assert len(a)==len(b)
    correct=sum(x==y for x,y in zip(a,b));tp=len(ap&bp)
    return {'character_accuracy':correct/len(b),'boundary_f1':2*tp/(len(ap)+len(bp))}


def final():
    p=study.check_inputs();summary=study.read(study.OUT/'summary.json');checked=0;optima=0;max_error=0.
    for language in p['languages']:
        tables=load_model(study.TMP/language);vocab={x[0] for x in tables['word',1]}
        for case in summary['cases']:
            if case['language']!=language:continue
            name=case['case'];truth=study.read(study.DATA/name/'truth.json')
            for mode,row in case['rows'].items():
                key=row['key'];assert len(key)==26 and len(set(key))==26
                for split in ('fit','transfer'):
                    cipher=(study.DATA/name/(split+'.txt')).read_text().strip()
                    decoded=''.join(key[ord(c)-97] for c in cipher)
                    reported=row[split]['segmentation']
                    assert decoded==reported.replace(' ','')
                    expected=truth['plaintext_'+split]
                    encrypted=''.join(truth['encryption_key'][ord(c)-97] for c in expected if c!=' ')
                    assert encrypted==cipher
                    measured=independent_metrics(reported,expected)
                    for field,value in measured.items():assert abs(value-row[split][field])<1e-12
                    score=reference.full_score(reported,tables)['combined_score_ln']
                    error=abs(score-row[split]['score']);max_error=max(max_error,error)
                    assert error<1e-8*len(decoded)
                    if mode in ('exact','oracle_correct_letters'):
                        edges=reference.edges_for(decoded,vocab)
                        optimal=reference.exact_segment(decoded,edges,tables)
                        assert abs(optimal['score_ln']-score)<1e-8*len(decoded)
                        optima+=1
                    checked+=1
            result=case['rows']['exact']['transfer']
            passed=result['character_accuracy']>=p['gate']['character_accuracy'] and result['boundary_f1']>=p['gate']['boundary_f1']
            assert passed==case['passes_gate']
            print(json.dumps({'verified':name}),flush=True)
    assert len(summary['cases'])==12
    assert summary['passed']==sum(x['passes_gate'] for x in summary['cases'])
    assert summary['voynich_gate_open']==all(x['passes_gate'] for x in summary['cases'])
    study.save(study.OUT/'verification.json',{'passed':True,'scored_outputs_checked':checked,
        'exact_segmentations_recomputed':optima,'maximum_score_difference':max_error,
        'cipher_reconstruction':True,'keys_are_bijective':True,'gate_recomputed':True,
        'scope':'Independent Python scorer and dynamic program; common source models. Not external peer review.',
        'NOT_TRANSLATION':True})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--development',action='store_true')
    args=parser.parse_args()
    development() if args.development else final()
