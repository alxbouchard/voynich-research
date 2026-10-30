#!/usr/bin/env python3
"""Restricted homophonic experiment. Real candidates are NOT translations."""
import collections, concurrent.futures, hashlib, json, math, random, re, subprocess, sys, time, unicodedata
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'voynich_20261028'; P2=ROOT.parent/'voynich_phase2'
DATA=ROOT/'data'; OUT=ROOT/'results'; SEED=20261028
sys.path.insert(0,str(BASE))
from analyse import parse
UNITS=r'ckh|cth|cph|cfh|ch|sh|iiiin|iiin|iin|in|.'

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def clean(s):return re.sub('[^a-z]','',unicodedata.normalize('NFKD',s).lower()).replace('j','i').replace('k','c').replace('w','uu')
def grams(s):
 a=np.frombuffer(s.encode(),dtype=np.uint8).astype(np.int32)-97
 return ((a[:-3]*26+a[1:-2])*26+a[2:-1])*26+a[3:] if len(a)>=4 else np.array([],dtype=int)
def sources():
 raw=(P2/'data/dante.txt').read_text(); starts=list(re.finditer(r'INFERNO\nInferno\nCanto I\n',raw)); assert len(starts)==2
 unique=raw[:starts[1].start()]; assert raw[starts[1].start():].strip()==unique.strip()
 before,paradiso=unique.split('\nPARADISO\n',1)
 poem=lambda s:clean('\n'.join(l for l in s.splitlines() if l.strip() and not re.match(r'^(INFERNO|PURGATORIO|PARADISO|Inferno|Purgatorio|Paradiso|Canto\b)',l)))
 train={'latin':(P2/'data/latin_train.txt').read_text().strip(),'italian':poem(before)}
 target={'latin':clean((BASE/'controls/input/nathist_book16.txt').read_text()),'italian':poem(paradiso)}
 assert len(train['latin'])==317080 and len(train['italian'])==268869
 assert len(target['latin'])==52641 and len(target['italian'])==133933
 for lang,s in train.items():
  c=np.bincount(grams(s),minlength=26**4); lm=np.log2((c+.01)/(c.sum()+.01*26**4)); lm.tofile(DATA/(lang+'_lm.bin'))
  u=np.bincount(np.frombuffer(s.encode(),dtype=np.uint8)-97,minlength=26)+.5; q=u/u.sum()
  (DATA/(lang+'_freq.txt')).write_text(' '.join(map(str,q)))
  (DATA/(lang+'_train.txt')).write_text(s)
  (DATA/(lang+'_target.txt')).write_text(target[lang])
 return train,target
def metrics(lines,key,lm,q):
 decoded=[''.join(key[x] for x in s) for s in lines if len(s)>=4]
 ids=np.concatenate([grams(s) for s in decoded]); n=sum(map(len,decoded)); freq=collections.Counter(''.join(decoded))
 entropy=-sum((v/n)*math.log2(v/n) for v in freq.values())
 kl=sum((v/n)*math.log2((v/n)/q[ord(k)-97]) for k,v in freq.items())
 return {'chars':n,'quadgrams':len(ids),'bits_per_quadgram':float(-lm[ids].mean()),'output_unigram_entropy':entropy,'output_distinct_letters':len(freq),'kl_to_model_bits':kl},decoded
def run_case(name,lang,train,test,restarts=8,steps=60000,seed=SEED,lam=4,temp=.002,truth=None,extra=None):
 train=[s for s in train if len(s)>=4];test=[s for s in test if len(s)>=4]
 inp=DATA/(name+'_train.txt');inp.write_text('\n'.join(' '.join(map(str,s)) for s in train)+'\n')
 (DATA/(name+'_test.txt')).write_text('\n'.join(' '.join(map(str,s)) for s in test)+'\n')
 start=time.time();cmd=[str(ROOT/'src/homophonic'),str(DATA/(lang+'_lm.bin')),str(DATA/(lang+'_freq.txt')),str(inp),str(restarts),str(steps),str(seed),str(lam),str(temp)]
 p=subprocess.run(cmd,capture_output=True,text=True,check=True);res=json.loads(p.stdout)
 lm=np.fromfile(DATA/(lang+'_lm.bin'));q=np.loadtxt(DATA/(lang+'_freq.txt'))
 trainm,_=metrics(train,res['key'],lm,q);testm,decoded=metrics(test,res['key'],lm,q)
 expected=-trainm['quadgrams']*trainm['bits_per_quadgram']-lam*trainm['chars']*trainm['kl_to_model_bits']
 assert abs(expected-res['training_objective'])<1e-6*trainm['chars']
 res.update(case=name,language=lang,seconds=round(time.time()-start,2),temperature_multiplier=temp,seed=seed,train_metrics=trainm,test_metrics=testm,candidate_preview_NON_TRANSLATION='\n'.join(decoded)[:900],objective_independently_verified=True)
 if extra:res.update(extra)
 if truth is not None:
  expected=''.join(truth);actual=''.join(decoded);assert len(expected)==len(actual)
  res['heldout_character_accuracy']=sum(a==b for a,b in zip(expected,actual))/len(expected)
  res['heldout_errors']=sum(a!=b for a,b in zip(expected,actual))
  truthids=np.concatenate([grams(s) for s in truth]);res['true_plaintext_bits_per_quadgram']=float(-lm[truthids].mean())
 save(OUT/(name+'.json'),res)
 print(json.dumps({k:res[k] for k in ['case','seconds','heldout_character_accuracy'] if k in res}|{'bits':testm['bits_per_quadgram'],'letters':testm['output_distinct_letters']}),flush=True)
 return res
def chunks(s,n=80):return [s[i:i+n] for i in range(0,len(s),n) if len(s[i:i+n])>=4]
def control(lang,plain,trial=1,**params):
 rng=random.Random(SEED+trial+(0 if lang=='latin' else 100));alphabet=sorted(set(plain));q=np.loadtxt(DATA/(lang+'_freq.txt'))
 allocation={a:1 for a in alphabet}
 while sum(allocation.values())<48:
  a=max(alphabet,key=lambda a:q[ord(a)-97]/(allocation[a]+1));allocation[a]+=1
 ids=list(range(48));rng.shuffle(ids); enc={};cursor=0
 for a in alphabet:enc[a]=ids[cursor:cursor+allocation[a]];cursor+=allocation[a]
 cipher=[rng.choice(enc[a]) for a in plain];train=chunks(cipher[:24000]);test=chunks(cipher[24000:]);truth=chunks(plain[24000:])
 name=f'control_{lang}_{trial}'+params.pop('suffix','')
 save(DATA/(name+'_truth.json'),{'encryption_homophones':enc,'allocation':'minimum one per target alphabet letter; additional symbols allocated by language-model frequency','truth_test':truth,'not_passed_to_solver':True})
 return run_case(name,lang,train,test,truth=truth,extra={'control':True,'encryption_seed':SEED+trial+(0 if lang=='latin' else 100)},**params)
def units_from_raw(raw,mode):
 # All explicit alternatives, rare signs, unreadable signs and physical gaps
 # break the stream. Neither branch of [a:b] is silently selected.
 raw=re.sub(r'\[[^\]]*\]','?',raw)
 raw=raw.replace('<->','?').replace('<~>','?')
 raw=re.sub(r'<[^>]*>','',raw)
 raw=re.sub(r'@\d+;','?',raw).replace("'",'?').replace('{','').replace('}','').lower()
 words=re.split(r'[.,\s]+',raw)
 result=[]
 for word in words:
  word=re.sub('[^a-z?]','?',word)
  result.extend(re.findall(UNITS,word) if mode=='COMPOSED' else list(word))
 return result
def real_inputs():
 recs=parse('ZL3b-n.txt')[0];eligible=[r for r in recs if r['type'].startswith('P')]
 leaves=sorted({r['leaf'] for r in eligible});testleaves=set(leaves[::5]);cases=[];audit=[]
 for subset in ['A','B']:
  selected=[r for r in eligible if r['metadata'].get('L')==subset]
  trainrecords=[r for r in selected if r['leaf'] not in testleaves];testrecords=[r for r in selected if r['leaf'] in testleaves]
  for mode in ['EVA','COMPOSED']:
   freq=collections.Counter(u for r in trainrecords for u in units_from_raw(r['raw'],mode) if u!='?')
   symbols=[u for u,c in sorted(freq.items(),key=lambda v:(-v[1],v[0])) if c>=10][:64];mapping={u:i for i,u in enumerate(symbols)}
   def encode(records):
    lines=[];c=collections.Counter()
    for r in records:
     seq=units_from_raw(r['raw'],mode);span=[];c['units_total']+=len(seq)
     for u in seq:
      if u in mapping:span.append(mapping[u]);c['units_retained']+=1
      else:
       c['breaks']+=1
       if len(span)>=4:lines.append(span)
       span=[]
     if len(span)>=4:lines.append(span)
    return lines,dict(c)
   train,traincov=encode(trainrecords);test,testcov=encode(testrecords)
   used=[];n=0
   for s in train:
    if n+len(s)>24000:break
    used.append(s);n+=len(s)
   meta={'subset':subset,'units':mode,'symbols_ordered':symbols,'train_leaf_pool':sorted({r['leaf'] for r in trainrecords}),'test_leaves':sorted({r['leaf'] for r in testrecords}),'training_coverage_pool':traincov,'test_coverage':testcov,'training_cap':24000,'explicit_variants':'hard breaks','uncertain_commas':'word boundaries before within-word composed grouping'}
   assert not set(meta['train_leaf_pool'])&set(meta['test_leaves'])
   audit.append(meta)
   for direction in ['forward','reverse']:
    a=used if direction=='forward' else [s[::-1] for s in used];b=test if direction=='forward' else [s[::-1] for s in test]
    cases.append((f'{subset}_{mode}_{direction}',a,b,dict(meta,direction=direction)))
 save(OUT/'encoding_audit.json',audit)
 return cases
def run_real():
 valid=json.loads((OUT/'controls_summary.json').read_text());assert all(r['heldout_character_accuracy']>=.95 for r in valid) and len(valid)==4
 tasks=[]
 for lang in ['latin','italian']:
  for label,train,test,meta in real_inputs():
   tasks.append((f'voynich_{lang}_{label}',lang,train,test,dict(meta,control=False,shuffled=False)))
   rng=random.Random(SEED+177)
   def shuf(lines):
    out=[]
    for s in lines:t=s[:];rng.shuffle(t);out.append(t)
    return out
   tasks.append((f'null_{lang}_{label}',lang,shuf(train),shuf(test),dict(meta,control=False,shuffled=True)))
 def one(t):
  name,lang,a,b,extra=t;path=OUT/(name+'.json')
  return json.loads(path.read_text()) if path.exists() and '--force' not in sys.argv else run_case(name,lang,a,b,extra=extra)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,tasks))
 save(OUT/'real_summary.json',results)
if __name__=='__main__':
 _,targets=sources()
 if '--calibrate' in sys.argv:control('latin',targets['latin'],restarts=8,steps=60000)
 elif '--controls' in sys.argv:
  res=[]
  for lang in ['latin','italian']:
   for trial in [1,2]:
    p=OUT/f'control_{lang}_{trial}.json';res.append(json.loads(p.read_text()) if p.exists() and '--force' not in sys.argv else control(lang,targets[lang],trial))
  save(OUT/'controls_summary.json',res);assert all(r['heldout_character_accuracy']>=.95 for r in res),'Control failed: no real cases authorized by protocol'
 elif '--real' in sys.argv:run_real()
