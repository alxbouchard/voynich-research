#!/usr/bin/env python3
"""Phase-21 shared I/O and locally trained open-vocabulary model. CC BY-SA 4.0."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
OLD=REPO/'voynich_phase20'
sys.path.insert(0,str(OLD/'src'))
import calibration as previous
TMP=ROOT/'tmp'
DATA=ROOT/'data'
OUT=ROOT/'results'
EXE=TMP/'open_solver'
ALPHABET=previous.ALPHABET
MAX_UNKNOWN=24
WL=np.array([.129793302623898,.226872659329747,.643334038046355])
CL=np.array([.0950848948641174,.229797965264228,.675117139871655])


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def compile_solver():
    TMP.mkdir(parents=True,exist_ok=True)
    subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'src/open_solver.cpp'),'-o',str(EXE)],check=True)


def build_model(language):
    # Rebuild the closed model locally through the frozen phase-20 routine.
    # Its output path is rebound, so no phase-20 file is modified.
    previous.TMP=TMP/'closed';closed_info=previous.train_models(language)
    folder=TMP/'open'/language;folder.mkdir(parents=True,exist_ok=True)
    for n in (1,2,3):shutil.copyfile(TMP/'closed'/language/f'char{n}.bin',folder/f'char{n}.bin')
    raw=(REPO/f'voynich_phase10/data/{language}_train_boundary.txt').read_text().split()
    counts=Counter(raw);known=sorted(w for w,n in counts.items() if n>=2)
    assert max(map(len,counts))<=MAX_UNKNOWN
    tokens=[w if counts[w]>=2 else '<unk>' for w in raw]
    words=['<unk>']+known;ids={w:i+1 for i,w in enumerate(words)}
    c1=Counter(tokens);c2=Counter(zip(tokens,tokens[1:]));c3=Counter(zip(tokens,tokens[1:],tokens[2:]))
    prev1=Counter(tokens[:-1]);prev2=Counter(zip(tokens[:-2],tokens[1:-1]))
    (folder/'words.tsv').write_text(''.join(f'{w}\t{c1[w]/len(tokens):.17g}\n' for w in words))
    (folder/'bigrams.tsv').write_text(''.join(f'{ids[a]}\t{ids[b]}\t{n/prev1[a]:.17g}\n' for (a,b),n in sorted(c2.items())))
    (folder/'trigrams.tsv').write_text(''.join(f'{ids[a]}\t{ids[b]}\t{ids[c]}\t{n/prev2[a,b]:.17g}\n' for (a,b,c),n in sorted(c3.items())))
    # One occurrence per training word type; BOS=27, EOS=26. Recursive
    # interpolation backs off with strength 5; base pseudocount is 0.1.
    ct=[np.zeros((28**n,27),dtype=np.float64) for n in range(4)]
    for word in counts:
        history=[27,27,27]
        for nxt in [*[ord(c)-97 for c in word],26]:
            for n in range(4):
                idx=0
                for h in history[-n:] if n else []:idx=idx*28+h
                ct[n][idx,nxt]+=1
            history=(history+[nxt])[-3:]
    base=(ct[0]+.1)/(ct[0].sum()+2.7)
    probs=base
    for n in range(1,4):
        lower=probs[np.arange(28**n)%(28**(n-1))]
        probs=(ct[n]+5*lower)/(ct[n].sum(axis=1,keepdims=True)+5)
    assert np.allclose(probs.sum(axis=1),1)
    np.log(probs).tofile(folder/'spelling.bin')
    lengths=np.full(MAX_UNKNOWN,.5)
    for word,n in counts.items():
        if n==1:lengths[len(word)-1]+=1
    np.log(lengths/lengths.sum()).tofile(folder/'length.bin')
    return {'language':language,'known_types':len(known),'unknown_training_tokens':c1['<unk>'],
            'training_tokens':len(raw),'maximum_unknown_length':MAX_UNKNOWN,
            'open_files':{p.name:sha(p) for p in sorted(folder.iterdir())},'closed':closed_info}


def batch(language,rows,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(f'{beta} {penalty} {text}\n' for beta,penalty,text in rows))
    proc=subprocess.run([str(EXE),str(TMP/'open'/language),'batch',str(path)],capture_output=True,text=True,check=True)
    if proc.stderr:raise RuntimeError(proc.stderr)
    results=[json.loads(line) for line in proc.stdout.splitlines()]
    assert len(results)==len(rows)
    return results
