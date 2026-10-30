#!/usr/bin/env python3
"""A restricted syllabic/homophonic experiment, never an automatic translation."""
import collections,concurrent.futures,hashlib,json,math,random,subprocess,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;P4=ROOT.parent/'voynich_phase4'
sys.path.insert(0,str(P4))
import run_homophonic as prev
DATA=ROOT/'data';OUT=ROOT/'results';SEED=20261030;M=32
LETTERS='abcdefghilmnopqrstuvxyz';VOWELS=set('aeiou')
assert len(LETTERS)==23
def save(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def quad(a):
 a=np.asarray(a,dtype=np.int32)
 return ((a[:-3]*M+a[1:-2])*M+a[2:-1])*M+a[3:]
def tokenize(text,inventory):
 idx={s:i for i,s in enumerate(inventory)};i=0;out=[]
 while i<len(text):
  pair=text[i:i+2]
  if len(pair)==2 and pair in idx:out.append(idx[pair]);i+=2
  else:out.append(idx[text[i]]);i+=1
 return out
def models():
 info={}
 for lang in ['latin','italian']:
  train=(P4/'data'/f'{lang}_train.txt').read_text();target=(P4/'data'/f'{lang}_target.txt').read_text()
  assert set(train+target)<=set(LETTERS)
  for kind in ['CV','VC']:
   def permitted(a,b):return (a not in VOWELS and b in VOWELS) if kind=='CV' else (a in VOWELS and b not in VOWELS)
   counts=collections.Counter(train[i:i+2] for i in range(len(train)-1) if permitted(train[i],train[i+1]))
   pairs=[p for p,n in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:9]]
   inventory=list(LETTERS)+pairs;assert len(set(inventory))==32
   encoded=tokenize(train,inventory);truth=tokenize(target,inventory)
   assert ''.join(inventory[x] for x in encoded)==train
   assert ''.join(inventory[x] for x in truth)==target
   c=np.bincount(quad(encoded),minlength=M**4);lm=np.log2((c+.01)/(c.sum()+.01*M**4));lm.tofile(DATA/f'{lang}_{kind}_lm.bin')
   u=np.bincount(encoded,minlength=M)+.5;q=u/u.sum();(DATA/f'{lang}_{kind}_freq.txt').write_text(' '.join(map(str,q)))
   meta={'language':lang,'kind':kind,'inventory':inventory,'pairs':pairs,'training_letters':len(train),'training_units':len(encoded),'target_letters':len(target),'target_units':len(truth),'train_sha256':hashlib.sha256(train.encode()).hexdigest(),'target_sha256':hashlib.sha256(target.encode()).hexdigest(),'training_bigram_counts':{p:counts[p] for p in pairs},'normalization':'phase 4 corpus, no spaces, greedy pair first; not phonological syllabification'}
   save(DATA/f'{lang}_{kind}_dictionary.json',meta);info[(lang,kind)]=(meta,truth)
 return info
def metrics(lines,key,lang,kind):
 info=json.loads((DATA/f'{lang}_{kind}_dictionary.json').read_text());inventory=info['inventory']
 lm=np.fromfile(DATA/f'{lang}_{kind}_lm.bin');q=np.loadtxt(DATA/f'{lang}_{kind}_freq.txt')
 decoded=[[key[x] for x in line] for line in lines if len(line)>=4]
 ids=np.concatenate([quad(s) for s in decoded]);flat=[x for s in decoded for x in s];n=len(flat);freq=collections.Counter(flat)
 text=[''.join(inventory[x] for x in line) for line in decoded]
 reseg=[tokenize(s,inventory) for s in text]
 canonical=sum(a==b for a,b in zip(decoded,reseg))
 return {'units':n,'quadgrams':len(ids),'bits_per_four_units':float(-lm[ids].mean()),'output_unit_entropy':-sum((c/n)*math.log2(c/n) for c in freq.values()),'output_distinct_units':len(freq),'kl_to_model_bits':sum((c/n)*math.log2((c/n)/q[x]) for x,c in freq.items()),'output_characters':sum(map(len,text)),'characters_per_unit':sum(map(len,text))/n,'canonical_segments':canonical,'segments':len(decoded),'canonical_segment_fraction':canonical/len(decoded)},decoded,text
def run_case(name,lang,kind,train,test,truth=None,extra=None,**settings):
 params={'restarts':8,'steps':60000,'lam':4,'temp':.002};params.update(settings)
 train=[s for s in train if len(s)>=4];test=[s for s in test if len(s)>=4]
 for part,lines in [('train',train),('test',test)]:
  (DATA/f'{name}_{part}.txt').write_text('\n'.join(' '.join(map(str,s)) for s in lines)+'\n')
 start=time.time();cmd=[str(ROOT/'src/syllabic'),str(DATA/f'{lang}_{kind}_lm.bin'),str(DATA/f'{lang}_{kind}_freq.txt'),str(DATA/f'{name}_train.txt'),str(params['restarts']),str(params['steps']),str(SEED),str(params['lam']),str(params['temp'])]
 proc=subprocess.run(cmd,capture_output=True,text=True,check=True);r=json.loads(proc.stdout)
 trainm,_,_=metrics(train,r['key'],lang,kind);testm,dec,txt=metrics(test,r['key'],lang,kind)
 obj=-trainm['quadgrams']*trainm['bits_per_four_units']-params['lam']*trainm['units']*trainm['kl_to_model_bits']
 assert abs(obj-r['training_objective'])<1e-6*trainm['units']
 r.update(case=name,language=lang,kind=kind,seconds=round(time.time()-start,2),settings=params,seed=SEED,train_metrics=trainm,test_metrics=testm,candidate_preview_NOT_TRANSLATION='\n'.join(txt)[:1000],objective_verified=True)
 # The C++ field name is inherited. It counts cipher/plaintext units, not letters.
 r['training_units']=r.pop('training_chars')
 if extra:r.update(extra)
 if truth is not None:
  expected=[x for s in truth for x in s];actual=[x for s in dec for x in s];assert len(expected)==len(actual)
  errors=sum(a!=b for a,b in zip(expected,actual));r['heldout_unit_accuracy']=1-errors/len(expected);r['heldout_unit_errors']=errors
  inv=json.loads((DATA/f'{lang}_{kind}_dictionary.json').read_text())['inventory'];expectedtext=''.join(inv[x] for x in expected)
  r['true_output_characters']=len(expectedtext);r['full_plaintext_exact']=expectedtext==''.join(txt)
  lm=np.fromfile(DATA/f'{lang}_{kind}_lm.bin');r['truth_bits_per_four_units']=float(-lm[np.concatenate([quad(s) for s in truth])].mean())
 save(OUT/f'{name}.json',r)
 print(json.dumps({'case':name,'seconds':r['seconds'],'unit_accuracy':r.get('heldout_unit_accuracy'),'bits':testm['bits_per_four_units'],'expansion':testm['characters_per_unit'],'canonical':testm['canonical_segment_fraction']}),flush=True)
 return r
def control(lang,kind,trial,info,**params):
 meta,truth=info[(lang,kind)];q=np.loadtxt(DATA/f'{lang}_{kind}_freq.txt')
 rng=random.Random(SEED+trial+(100 if lang=='italian' else 0)+(1000 if kind=='VC' else 0));present=sorted(set(truth));allocation={x:1 for x in present}
 while sum(allocation.values())<48:
  x=max(present,key=lambda x:q[x]/(allocation[x]+1));allocation[x]+=1
 ids=list(range(48));rng.shuffle(ids);enc={};cursor=0
 for x in present:enc[x]=ids[cursor:cursor+allocation[x]];cursor+=allocation[x]
 cipher=[rng.choice(enc[x]) for x in truth];train=prev.chunks(cipher[:24000]);test=prev.chunks(cipher[24000:]);expected=prev.chunks(truth[24000:])
 suffix=params.pop('suffix','');name=f'control_{lang}_{kind}_{trial}'+suffix
 save(DATA/f'{name}_truth.json',{'truth_test':expected,'encryption_homophones':enc,'key_not_passed_to_solver':True,'same_text_across_two_keys':True})
 return run_case(name,lang,kind,train,test,truth=expected,extra={'control':True,'trial':trial},**params)
def real_inputs():
 records=prev.parse('ZL3b-n.txt')[0];eligible=[r for r in records if r['type'].startswith('P')]
 leaves=sorted({r['leaf'] for r in eligible});testleaves=set(leaves[::5]);cases=[]
 for subset in ['A','B']:
  selected=[r for r in eligible if r['metadata'].get('L')==subset]
  fitting=[r for r in selected if r['leaf'] not in testleaves];testing=[r for r in selected if r['leaf'] in testleaves]
  for mode in ['EVA','COMPOSED']:
   freq=collections.Counter(u for r in fitting for u in prev.units_from_raw(r['raw'],mode) if u!='?')
   symbols=[u for u,n in sorted(freq.items(),key=lambda v:(-v[1],v[0])) if n>=10][:64];mp={u:i for i,u in enumerate(symbols)}
   def encode(rs):
    lines=[];stats=collections.Counter()
    for r in rs:
     span=[]
     for u in prev.units_from_raw(r['raw'],mode):
      stats['all_units']+=1
      if u in mp:span.append(mp[u]);stats['known_units']+=1
      else:
       stats['breaks']+=1
       if len(span)>=4:lines.append(span)
       span=[]
     if len(span)>=4:lines.append(span)
    return lines,dict(stats)
   full,tc=encode(fitting);test,vc=encode(testing);train=[];n=0
   for s in full:
    if n+len(s)>24000:break
    train.append(s);n+=len(s)
   assert {x for s in train for x in s}==set(range(len(symbols)))
   meta={'subset':subset,'units':mode,'symbols_ordered':symbols,'fit_leaf_pool':sorted({r['leaf'] for r in fitting}),'test_leaves':sorted({r['leaf'] for r in testing}),'fit_pool_coverage':tc,'test_coverage':vc,'fit_cap_units':24000}
   assert not set(meta['fit_leaf_pool'])&set(meta['test_leaves'])
   for direction in ['forward','reverse']:
    a=train if direction=='forward' else [s[::-1] for s in train];b=test if direction=='forward' else [s[::-1] for s in test]
    cases.append((f'{subset}_{mode}_{direction}',a,b,dict(meta,direction=direction)))
 save(OUT/'encoding_audit.json',[x[3] for x in cases]);return cases
def controls(info):
 tasks=[(lang,kind,t) for lang in ['latin','italian'] for kind in ['CV','VC'] for t in [1,2]]
 def one(t):
  lang,kind,trial=t;p=OUT/f'control_{lang}_{kind}_{trial}.json'
  return json.loads(p.read_text()) if p.exists() and '--force' not in sys.argv else control(lang,kind,trial,info)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(one,tasks))
 save(OUT/'controls_summary.json',res)
 return res
def real():
 ctl=json.loads((OUT/'controls_summary.json').read_text());assert len(ctl)==8
 allowed={(lang,kind) for lang in ['latin','italian'] for kind in ['CV','VC'] if all(r['heldout_unit_accuracy']>=.95 for r in ctl if r['language']==lang and r['kind']==kind)}
 save(OUT/'validation_gate.json',{'allowed_models':sorted(allowed),'excluded_models':sorted(set((l,k) for l in ['latin','italian'] for k in ['CV','VC'])-allowed),'criterion':'both keys >=95% exact heldout unit recovery'})
 cases=real_inputs();tasks=[]
 for lang,kind in sorted(allowed):
  for label,train,test,meta in cases:
   tasks.append((f'voynich_{lang}_{kind}_{label}',lang,kind,train,test,dict(meta,control=False,shuffled=False)))
   rng=random.Random(SEED+177)
   def shuffle(lines):
    out=[]
    for s in lines:t=s[:];rng.shuffle(t);out.append(t)
    return out
   tasks.append((f'null_{lang}_{kind}_{label}',lang,kind,shuffle(train),shuffle(test),dict(meta,control=False,shuffled=True)))
 def one(t):
  name,lang,kind,a,b,meta=t;p=OUT/f'{name}.json'
  return json.loads(p.read_text()) if p.exists() and '--force' not in sys.argv else run_case(name,lang,kind,a,b,extra=meta)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(one,tasks))
 save(OUT/'real_summary.json',res)
if __name__=='__main__':
 info=models()
 if '--controls' in sys.argv:controls(info)
 elif '--real' in sys.argv:real()
