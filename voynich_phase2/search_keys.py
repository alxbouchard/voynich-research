#!/usr/bin/env python3
"""Restricted unknown-key search. Output candidates are NOT translations."""
import sys,os,subprocess,json,math,collections,re,random,time,unicodedata
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'voynich_20261028'
sys.path.insert(0,str(BASE))
from analyse import parse
DATA=ROOT/'data';OUT=ROOT/'results';SEED=20261029

def clean(s):return re.sub('[^a-z]','',unicodedata.normalize('NFKD',s).lower()).replace('j','i').replace('k','c').replace('w','uu')
def arr(s):return np.frombuffer(s.encode(),dtype=np.uint8).astype(np.int32)-97
def grams(s):
 a=arr(s)
 if len(a)<4:return np.array([],dtype=int)
 return ((a[:-3]*26+a[1:-2])*26+a[2:-1])*26+a[3:]
def lm_build():
 s=clean((DATA/'latin_train.txt').read_text()); c=np.bincount(grams(s),minlength=26**4).reshape(-1,26)
 # Joint quadgram scoring avoids rewarding unseen contexts with a uniform
 # conditional distribution. Calibrated on the synthetic control only.
 lm=np.log2((c+.01)/(c.sum()+.01*26**4)).ravel();lm.astype('float64').tofile(DATA/'latin_lm.bin')
 rank=''.join(sorted('abcdefghijklmnopqrstuvwxyz',key=lambda ch:(-s.count(ch),ch)))
 return lm,rank
def score(segments,key,lm):
 table=str.maketrans('abcdefghijklmnopqrstuvwxyz',key)
 ids=[grams(x.translate(table)) for x in segments if len(x)>=4]
 ids=np.concatenate(ids) if ids else np.array([],dtype=int)
 return float(-lm[ids].mean()) if len(ids) else None
def run_case(name,train,test,lm,rank,truth=None,restarts=8,steps=40000):
 path=DATA/(name+'_train.txt');path.write_text('\n'.join(train)+'\n')
 t=time.time();r=subprocess.run([str(ROOT/'src/solve'),str(DATA/'latin_lm.bin'),str(path),str(restarts),str(steps),str(SEED),rank],capture_output=True,text=True,check=True)
 result=json.loads(r.stdout);key=result['key'];result['case']=name;result['seconds']=round(time.time()-t,2)
 result['heldout_cross_entropy_bits']=score(test,key,lm)
 result['training_chars']=sum(map(len,train));result['test_chars']=sum(map(len,test))
 table=str.maketrans('abcdefghijklmnopqrstuvwxyz',key)
 result['candidate_preview_NON_TRANSLATION']='\n'.join(x.translate(table) for x in test)[:500]
 if truth is not None:
  expected=''.join(truth);actual=''.join(x.translate(table) for x in test)
  assert len(actual)==len(expected)
  result['heldout_character_accuracy']=sum(a==b for a,b in zip(actual,expected))/len(expected)
  result['true_plaintext_heldout_cross_entropy_bits']=score(truth,'abcdefghijklmnopqrstuvwxyz',lm)
 (OUT/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='candidate_preview_NON_TRANSLATION'}),flush=True)
 return result

def main():
 OUT.mkdir(exist_ok=True)
 lm,rank=lm_build(); rng=random.Random(SEED)
 plain=clean((BASE/'controls/input/nathist_book16.txt').read_text())
 alphabet=list('abcdefghijklmnopqrstuvwxyz');rng.shuffle(alphabet);encrypt=str.maketrans('abcdefghijklmnopqrstuvwxyz',''.join(alphabet))
 hidden=plain.translate(encrypt)
 # Control: a different author from the language model, hidden permutation.
 control=run_case('latin_hidden_key_control',[hidden[:24000]],[hidden[24000:]],lm,rank,truth=[plain[24000:]])
 assert control['heldout_character_accuracy']>=.95,'Control failed; do not claim failed real cases rule out the family'
 corpora={n:parse(n)[0] for n in ['ZL3b-n.txt','IT2a-n.txt']}
 for name,recs in corpora.items():
  for variant in (['all','A','B'] if name.startswith('ZL') else ['all']):
   eligible=[r for r in recs if r['type'].startswith('P') and (variant=='all' or r['metadata'].get('L')==variant)]
   leaves=sorted({r['leaf'] for r in eligible});testleaves=set(leaves[::5])
   def strings(istest):return [''.join(r['clean']) for r in eligible if (r['leaf'] in testleaves)==istest]
   train=strings(False);test=strings(True)
   # Bound the optimisation cost without looking at the held-out text.
   used=[];size=0
   for s in train:
    if size+len(s)>26000:break
    used.append(s);size+=len(s)
   run_case('eva_'+name[:2]+'_'+variant,used,test,lm,rank)
 # Naibbe table structure is known, plaintext letter assignments are permuted.
 os.chdir(BASE/'controls');sys.path.insert(0,str(BASE/'controls'))
 import decrypt_naibbe as dec
 import pandas as pd
 maps=dec.build_reverse_mappings(pd.read_csv('references/naibbe_tables.csv'))
 reverse=lambda w:dec.decrypt_naibbe_token(w,*maps,basic=True,compound=False)
 synthetic=(BASE/'controls/generated/naibbe_ciphertext.txt').read_text().splitlines()
 parsed=[''.join(reverse(w) for w in line.split()) for line in synthetic]
 assert not any(re.search('[^a-z]',x) for x in parsed)
 recovered=''.join(parsed);assert recovered==plain
 # Simulates concealed global labels after the fixed morphological parse.
 ciphertext=recovered.translate(encrypt)
 run_case('naibbe_global_permutation_control',[ciphertext[:24000]],[ciphertext[24000:]],lm,rank,truth=[plain[24000:]])
 for name,recs in corpora.items():
  train=[];test=[];coverage=collections.Counter()
  eligible=[r for r in recs if r['type'].startswith('P')]
  leaves=sorted({r['leaf'] for r in eligible});testleaves=set(leaves[::5])
  for r in eligible:
   span='';segments=[]
   for word in r['tokens']:
    read=reverse(word);coverage['all']+=1
    if re.fullmatch('[a-z]+',read):span+=read;coverage['unique']+=1
    else:
     if len(span)>=4:segments.append(span)
     span=''
   if len(span)>=4:segments.append(span)
   (test if r['leaf'] in testleaves else train).extend(segments)
  result=run_case('naibbe_permutation_'+name[:2],train,test,lm,rank)
  result['token_coverage']=dict(coverage)
  (OUT/(result['case']+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 print('KEY SEARCH COMPLETE',flush=True)

if __name__=='__main__':main()
