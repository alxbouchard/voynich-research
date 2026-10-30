#!/usr/bin/env python3
"""Frozen unknown-key controls; solver sees model files and ciphertext only.

CC BY-SA 4.0. See phase README for original method attribution.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import string
import subprocess
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
TMP = ROOT/'tmp/calibration'
DATA = ROOT/'data/calibration'
OUT = ROOT/'results/calibration'
ALPHABET = string.ascii_lowercase
PFILE = ROOT/'CALIBRATION_PROTOCOL.json'
EXECUTABLE = TMP/'joint_solver'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def read(path):
    return json.loads(path.read_text())


def protocol():
    p = read(PFILE)
    for path, expected in p['input_sha256'].items():
        assert sha(REPO/path) == expected, f'Changed source: {path}'
    for path, expected in p['code_sha256'].items():
        assert sha(ROOT/path) == expected, f'Changed calibration code: {path}'
    return p


def compile_solver():
    TMP.mkdir(parents=True, exist_ok=True)
    subprocess.run(['c++', '-O3', '-std=c++17', str(ROOT/'src/joint_solver.cpp'),
                    '-o', str(EXECUTABLE)], check=True)


def train_models(language):
    text = (REPO/f'voynich_phase10/data/{language}_train_boundary.txt').read_text()
    words = text.split()
    assert all(w and set(w) <= set(ALPHABET) for w in words)
    counts = Counter(words)
    vocab = sorted(set(words) | set(ALPHABET))
    ids = {w: i+1 for i, w in enumerate(vocab)}
    c1 = {w: counts[w]+(0.1 if len(w)==1 else 0.) for w in vocab}
    total = sum(c1.values())
    c2 = Counter(zip(words, words[1:]))
    c3 = Counter(zip(words, words[1:], words[2:]))
    previous1 = Counter(words[:-1])
    previous2 = Counter(zip(words[:-2], words[1:-1]))
    model = TMP/language
    model.mkdir(parents=True, exist_ok=True)
    (model/'words.tsv').write_text(''.join(f'{w}\t{c1[w]/total:.17g}\n' for w in vocab))
    (model/'bigrams.tsv').write_text(''.join(f'{ids[a]}\t{ids[b]}\t{n/previous1[a]:.17g}\n'
                                          for (a,b),n in sorted(c2.items())))
    (model/'trigrams.tsv').write_text(''.join(f'{ids[a]}\t{ids[b]}\t{ids[c]}\t{n/previous2[a,b]:.17g}\n'
                                           for (a,b,c),n in sorted(c3.items())))
    chars = np.array([26 if x==' ' else ord(x)-97 for x in text], dtype=np.int64)
    one = np.bincount(chars,minlength=27).astype(float)+.1
    (one/one.sum()).tofile(model/'char1.bin')
    for n in (2,3):
        gram = np.zeros(len(chars)-n+1,dtype=np.int64)
        for j in range(n):
            gram = gram*27+chars[j:j+len(gram)]
        counts_array = np.bincount(gram,minlength=27**n).reshape(-1,27).astype(float)
        den = counts_array.sum(axis=1,keepdims=True)
        np.divide(counts_array,den,out=np.zeros_like(counts_array),where=den!=0).tofile(model/f'char{n}.bin')
    letters = np.array([ord(x)-97 for x in ''.join(words)], dtype=np.int64)
    four = ((letters[:-3]*26+letters[1:-2])*26+letters[2:-1])*26+letters[3:]
    counts4 = np.bincount(four,minlength=26**4).astype(float)+.01
    np.log(counts4/counts4.sum()).tofile(model/'quad.bin')
    freq = np.bincount(letters,minlength=26).astype(float)+.5
    (freq/freq.sum()).tofile(model/'freq.bin')
    return {'language':language,'training_words':len(words),'dictionary_words':len(vocab),
            'training_file':str(Path('voynich_phase10/data')/f'{language}_train_boundary.txt'),
            'files':{p.name:sha(p) for p in sorted(model.iterdir())}}


def prepare():
    p = protocol()
    compile_solver()
    models = [train_models(lang) for lang in p['languages']]
    source = {x['case']: x for x in read(REPO/'voynich_phase10/data/source_inputs.json')}
    cases = []
    for li, (language, source_name) in enumerate(p['languages'].items()):
        words = [w for line in source[source_name]['lines'] for w in line['words'] if w]
        assert all(set(w)<=set(ALPHABET) for w in words)
        bin_size = len(words)//6
        for trial, length in enumerate(p['fit_letters']*p['repetitions']):
            rng = random.Random(p['selection_seed']+li*100+trial)
            start = trial*bin_size+rng.randrange(max(1,bin_size-800))
            cursor = start
            def take(n):
                nonlocal cursor
                out=[];letters=0
                while letters<n:
                    word=words[cursor];out.append(word);letters+=len(word);cursor+=1
                return ' '.join(out)
            fit = take(length)
            fit_end = cursor
            cursor += p['gap_words']
            test_start = cursor
            test = take(p['transfer_letters'])
            assert cursor <= (trial+1)*bin_size
            key_rng = random.Random(p['encryption_seed']+li*100+trial)
            key = list(ALPHABET);key_rng.shuffle(key);key=''.join(key)
            table = str.maketrans(ALPHABET,key)
            name = f'{language}_{length}_{trial//3+1}'
            cipher_fit = fit.replace(' ','').translate(table)
            cipher_test = test.replace(' ','').translate(table)
            (DATA/name).mkdir(parents=True,exist_ok=True)
            (DATA/name/'fit.txt').write_text(cipher_fit+'\n')
            (DATA/name/'transfer.txt').write_text(cipher_test+'\n')
            save(DATA/name/'truth.json', {'plaintext_fit':fit,'plaintext_transfer':test,
                 'encryption_key':key,'source':source_name,'source_word_ranges':{
                     'fit':[start,fit_end],'transfer':[test_start,cursor]},
                 'evaluation_only':True,'never_passed_to_key_search':True})
            cases.append({'case':name,'language':language,'fit_requested':length,
                          'fit_letters':len(cipher_fit),'transfer_letters':len(cipher_test),
                          'fit_sha256':sha(DATA/name/'fit.txt'),
                          'transfer_sha256':sha(DATA/name/'transfer.txt'),
                          'truth_sha256':sha(DATA/name/'truth.json')})
    save(DATA/'cases.json',cases)
    save(DATA/'models.json',models)
    save(DATA/'environment.json',{'compiler':subprocess.check_output(['c++','--version'],text=True),
         'python':subprocess.check_output(['python3','--version'],text=True).strip(),
         'numpy':np.__version__,'executable_sha256':sha(EXECUTABLE),
         'protocol_sha256':sha(PFILE),
         'freeze_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()})
    print(json.dumps({'prepared_cases':len(cases),'models':len(models)}),flush=True)


def run(command, output):
    identity = {'command':list(map(str,command)),'protocol_sha256':sha(PFILE),
                'solver_sha256':sha(EXECUTABLE),
                'argument_file_sha256':{str(x):sha(x) for x in command[1:] if isinstance(x,Path) and x.is_file()}}
    if output.exists():
        row=read(output)
        assert row['identity']==identity, 'Stale output; never silently reuse.'
        return row['result']
    start=time.monotonic()
    process=subprocess.run(list(map(str,command)),capture_output=True,text=True,check=True)
    if process.stderr:
        raise RuntimeError(process.stderr)
    result=json.loads(process.stdout)
    save(output,{'identity':identity,'seconds':time.monotonic()-start,'result':result})
    return result


def check_inputs():
    p=protocol()
    assert sha(EXECUTABLE)==read(DATA/'environment.json')['executable_sha256']
    for model in read(DATA/'models.json'):
        for name,digest in model['files'].items():
            assert sha(TMP/model['language']/name)==digest
    for case in read(DATA/'cases.json'):
        for name in ('fit','transfer','truth'):
            suffix='json' if name=='truth' else 'txt'
            assert sha(DATA/case['case']/f'{name}.{suffix}')==case[name+'_sha256']
    return p


def fit():
    p=check_inputs()
    for i,case in enumerate(read(DATA/'cases.json')):
        name=case['case'];folder=OUT/name;folder.mkdir(parents=True,exist_ok=True)
        model=TMP/case['language'];cipher=DATA/name/'fit.txt'
        print(json.dumps({'starting':name,'stage':'initializer','index':i+1,'total':12}),flush=True)
        initial=run([EXECUTABLE,model,'init',cipher,p['optimizer_seed']+i,
                     p['restarts'],p['steps']],folder/'initializer.json')
        keys=[]
        for row in initial['restarts']:
            if row['key'] not in keys:
                keys.append(row['key'])
            if len(keys)==p['refinement_starts']:
                break
        keyfile=TMP/(name+'_starts.txt');keyfile.write_text('\n'.join(keys)+'\n')
        for mode in ('greedy','exact'):
            print(json.dumps({'starting':name,'stage':mode}),flush=True)
            result=run([EXECUTABLE,model,mode,cipher,keyfile,p['refinement_passes']],folder/(mode+'.json'))
            print(json.dumps({'case':name,'mode':mode,'evaluations':result['evaluations'],
                              'fit_score':result['fit']['score']}),flush=True)


def boundaries(text):
    points=set();position=0
    for word in text.split()[:-1]:
        position+=len(word);points.add(position)
    return points


def metrics(actual,truth):
    a=actual.replace(' ','');t=truth.replace(' ','')
    assert len(a)==len(t)
    predicted=boundaries(actual);expected=boundaries(truth)
    tp=len(predicted&expected)
    precision=tp/len(predicted) if predicted else 0.
    recall=tp/len(expected) if expected else 0.
    return {'letters':len(t),'correct_letters':sum(x==y for x,y in zip(a,t)),
            'character_accuracy':sum(x==y for x,y in zip(a,t))/len(t),
            'boundary_precision':precision,'boundary_recall':recall,
            'boundary_f1':2*tp/(len(predicted)+len(expected)) if predicted or expected else 1.,
            'boundary_tp':tp,'boundary_fp':len(predicted-expected),'boundary_fn':len(expected-predicted)}


def evaluate():
    p=check_inputs();summary=[]
    # Require every fixed key to exist before loading any evaluation plaintext.
    for case in read(DATA/'cases.json'):
        for mode in ('greedy','exact'):
            assert (OUT/case['case']/(mode+'.json')).exists()
    for case in read(DATA/'cases.json'):
        name=case['case'];folder=OUT/name;model=TMP/case['language']
        truth=read(DATA/name/'truth.json');vocab={line.split('\t')[0] for line in (model/'words.tsv').read_text().splitlines()}
        first=read(folder/'initializer.json')['result']['restarts'][0]['key']
        key_inverse=''.join(ALPHABET[truth['encryption_key'].index(x)] for x in ALPHABET)
        rows={}
        for mode in ('initializer','greedy','exact','oracle_correct_letters'):
            key=first if mode=='initializer' else key_inverse if mode.startswith('oracle') else read(folder/(mode+'.json'))['result']['key']
            assert len(key)==26 and set(key)==set(ALPHABET)
            row={'key':key,'evaluation_only':mode.startswith('oracle')}
            for split in ('fit','transfer'):
                ciphertext=(DATA/name/(split+'.txt')).read_text().strip()
                decoded=ciphertext.translate(str.maketrans(ALPHABET,key))
                target=TMP/(name+'_'+mode+'_'+split+'.txt');target.write_text(decoded+'\n')
                segmentation_mode='greedy' if mode=='greedy' else 'exact'
                result=run([EXECUTABLE,model,'segment',target,segmentation_mode],folder/(mode+'_'+split+'_segmentation.json'))
                reference=truth['plaintext_'+split]
                row[split]=dict(metrics(result['segmentation'],reference),score=result['score'],
                                segmentation=result['segmentation'])
            observed=set((DATA/name/'fit.txt').read_text().strip())
            row['fit_observed_key_accuracy']=sum(key[ord(c)-97]==key_inverse[ord(c)-97] for c in observed)/len(observed)
            if mode in ('greedy','exact'):
                assert abs(row['fit']['score']-read(folder/(mode+'.json'))['result']['fit']['score'])<1e-8
            rows[mode]=row
        oov={split:sum(w not in vocab for w in truth['plaintext_'+split].split())/
             len(truth['plaintext_'+split].split()) for split in ('fit','transfer')}
        passed=(rows['exact']['transfer']['character_accuracy']>=p['gate']['character_accuracy'] and
                rows['exact']['transfer']['boundary_f1']>=p['gate']['boundary_f1'])
        row={'case':name,'language':case['language'],'dictionary_oov_token_fraction':oov,
             'rows':rows,'passes_gate':passed,'NOT_TRANSLATION':True}
        save(folder/'evaluation.json',row);summary.append(row)
        print(json.dumps({'case':name,'passes_gate':passed,'letter_accuracy':rows['exact']['transfer']['character_accuracy'],
                          'boundary_f1':rows['exact']['transfer']['boundary_f1']}),flush=True)
    save(OUT/'summary.json',{'cases':summary,'passed':sum(x['passes_gate'] for x in summary),
         'total':len(summary),'voynich_gate_open':all(x['passes_gate'] for x in summary),
         'scope':'Locally frozen controls. Analyst has seen source works in earlier phases; keys and plaintext never provided to optimizer.',
         'NOT_TRANSLATION':True})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','fit','evaluate'])
    args=parser.parse_args()
    {'prepare':prepare,'fit':fit,'evaluate':evaluate}[args.action]()
