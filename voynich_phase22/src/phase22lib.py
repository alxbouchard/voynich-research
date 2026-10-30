#!/usr/bin/env python3
"""Phase-22 shared I/O and training-only boundary classifier. CC BY-SA 4.0."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parent
P20=REPO/'voynich_phase20';P21=REPO/'voynich_phase21'
sys.path.insert(0,str(P21/'src'))
import common as p21
TMP=ROOT/'tmp';DATA=ROOT/'data';OUT=ROOT/'results';EXE=TMP/'boundary_solver'
BASE_EXE=TMP/'phase21_solver';INIT_EXE=TMP/'initializer'
p21.TMP=TMP
ALPHABET=p21.ALPHABET


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def compile_solvers():
    TMP.mkdir(parents=True,exist_ok=True)
    expected=(P21/'src/open_solver.cpp').read_text().split('int main(int argc,char**argv)')[0]
    assert (ROOT/'src/phase21_model.hpp').read_text()==expected
    for source,target in ((ROOT/'src/boundary_solver.cpp',EXE),(P21/'src/open_solver.cpp',BASE_EXE),(P20/'src/joint_solver.cpp',INIT_EXE)):
        subprocess.run(['c++','-O3','-std=c++17',str(source),'-o',str(target)],check=True)


def build_model(language):
    p21.TMP=TMP;info=p21.build_model(language);folder=TMP/'open'/language
    words=(REPO/f'voynich_phase10/data/{language}_train_boundary.txt').read_text().split()
    letters=np.frombuffer(''.join(words).encode(),dtype=np.uint8).astype(np.int64)-97
    labels=np.zeros(len(letters)-1,dtype=float)
    cuts=np.cumsum([len(w) for w in words])[:-1];labels[cuts-1]=1.
    prior=float(labels.mean());padded=np.pad(letters,3,constant_values=26)
    six=np.zeros(len(labels),dtype=np.int64)
    for offset in range(6):six=six*27+padded[offset+1:offset+1+len(labels)]
    four=(six//27)%(27**4);two=(four//27)%(27**2)
    count1=np.bincount(two,minlength=27**2);space1=np.bincount(two,weights=labels,minlength=27**2)
    prob1=(space1+20*prior)/(count1+20)
    count2=np.bincount(four,minlength=27**4);space2=np.bincount(four,weights=labels,minlength=27**4)
    backoff=prob1[(np.arange(27**4)//27)%(27**2)]
    prob2=(space2+20*backoff)/(count2+20)
    unique,inverse=np.unique(six,return_inverse=True)
    count3=np.bincount(inverse);space3=np.bincount(inverse,weights=labels)
    prob3=(space3+20*prob2[(unique//27)%(27**4)])/(count3+20)
    assert (prob2>0).all() and (prob2<1).all() and (prob3>0).all() and (prob3<1).all()
    prob1.tofile(folder/'boundary1.bin');prob2.tofile(folder/'boundary2.bin')
    (folder/'boundary3.tsv').write_text(''.join(f'{idx}\t{p:.17g}\n' for idx,p in zip(unique,prob3)))
    # No labels or statistics from the target works enter this classifier.
    info.update(boundary_training_gaps=len(labels),boundary_training_spaces=int(labels.sum()),
                boundary_prior=prior,boundary_backoff_strength=20,
                open_files={p.name:sha(p) for p in sorted(folder.iterdir())})
    return info


def batch(language,jobs,path):
    path=Path(path);path.write_text(''.join(f'{weight} {threshold} {text}\n' for weight,threshold,text in jobs))
    proc=subprocess.run([str(EXE),str(TMP/'open'/language),'batch',str(path)],capture_output=True,text=True,check=True)
    if proc.stderr:raise RuntimeError(proc.stderr)
    outputs=[json.loads(line) for line in proc.stdout.splitlines()];assert len(outputs)==len(jobs)
    return outputs


def old_cases():
    for phase,root in ((20,P20/'data/calibration'),(21,P21/'data/controls')):
        for path in sorted(root.glob('*/truth.json')):
            name=path.parent.name
            yield phase,name,name.split('_')[0],path,read(path)


def cuts(text):
    result=set();position=0
    for char in text:
        if char==' ':result.add(position)
        else:position+=1
    result.discard(0);result.discard(position);return result


def differences(baseline,corrected,truth):
    old=cuts(baseline);new=cuts(corrected);gold=cuts(truth)
    assert old<=new,'An original boundary was removed'
    assert baseline.replace(' ','')==corrected.replace(' ','')
    added=new-old
    return {'added_correct_cuts':len(added&gold),'added_false_cuts':len(added-gold),
            'baseline_fp':len(old-gold),'corrected_fp':len(new-gold),
            'baseline_fn':len(gold-old),'corrected_fn':len(gold-new),
            'baseline_f1':2*len(old&gold)/(len(old)+len(gold)),
            'corrected_f1':2*len(new&gold)/(len(new)+len(gold))}
