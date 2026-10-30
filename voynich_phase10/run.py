#!/usr/bin/env python3
"""Phase 10: restricted context-dependent substitution, NOT a translation."""
import collections, concurrent.futures, hashlib, json, math, random, subprocess, sys, time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'; OUT=ROOT/'results'; SEED=20261110
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def grams(s,base=26):
 a=np.frombuffer(s.encode(),dtype=np.uint8).astype(np.int32)-97
 if base==27:a[a<0]=26
 return ((a[:-3]*base+a[1:-2])*base+a[2:-1])*base+a[3:]
def cap(lines):
 out=[]; n=0
 for r in lines:
  m=sum(len(w) for w in r['words'] if w)
  if n+m>24000: break
  out.append(r); n+=m
 return out
def spans(lines,boundary=False):
 """Same position/quadgram cohort for both models; None is a hard break."""
 out=[]
 for r in lines:
  s=[]; prev=None
  for j,w in enumerate(r['words']):
   if w is None:
    if len(s)>=4: out.append(s)
    s=[];prev=None;continue
   if boundary and prev is not None:s.append((' ',0,' ',j,-1))
   for i,ch in enumerate(w):
    truth=r.get('truth_words',r['words'])[j][i]
    s.append((ch,int(i==0 and prev is not None and prev.endswith('y')),truth,j,i))
   prev=w
  if len(s)>=4:out.append(s)
 return out
def control(lang,trial,lines):
 # The split is determined before encryption; state resets at every line.
 trainplain=cap(lines); split=len(trainplain); rng=random.Random(SEED+100*trial+(lang=='italian'))
 end=collections.Counter(w[-1] for r in trainplain for w in r['words'] if w).most_common(1)[0][0]
 alphabet=list('abcdefghijklmnopqrstuvwxyz'); vals=alphabet[:];rng.shuffle(vals)
 iy=vals.index('y');ie=ord(end)-97;vals[iy],vals[ie]=vals[ie],vals[iy]
 base=dict(zip(alphabet,vals));altvals=alphabet[:];rng.shuffle(altvals);alt=dict(zip(alphabet,altvals))
 encoded=[]
 for r in lines:
  prev=None; ws=[]
  for w in r['words']:
   assert w is not None
   z=''.join((alt if i==0 and prev is not None and prev.endswith('y') else base)[ch] for i,ch in enumerate(w))
   ws.append(z);prev=z
  encoded.append(dict(r,words=ws,truth_words=r['words']))
 name=f'control_{lang}_{trial}'
 save(DATA/(name+'_truth.json'),{'base_encryption':base,'after_y_encryption':alt,'trigger_plaintext_final':end,'seed':SEED+100*trial+(lang=='italian'),'note':'Never passed to C++ solver; constructed toy cipher, no historical attribution.'})
 return {'name':name,'language':lang,'train':encoded[:split],'test':encoded[split:],'control':True}
def prepare(trials=(1,2)):
 sources=json.loads((DATA/'source_inputs.json').read_text()); by={x['case']:x for x in sources}
 controls=[]
 for lang,src in [('latin','Latin_Pliny'),('italian','Italian_Paradiso')]:
  for trial in trials:controls.append(control(lang,trial,by[src]['lines']))
 save(DATA/('controls8.json' if len(trials)==4 else 'controls.json'),controls)
 leaves=sorted({r['physical_leaf'] for x in sources[:4] for r in x['lines']}); testset=set(leaves[::5]);real=[]
 for c in sources[:4]:
  tr=cap([r for r in c['lines'] if r['physical_leaf'] not in testset]);te=[r for r in c['lines'] if r['physical_leaf'] in testset]
  real.append({'name':c['case'],'train':tr,'test':te,'control':False})
 save(DATA/'real.json',real);save(DATA/'split.json',{'all_physical_leaves':leaves,'test_physical_leaves':sorted(testset),'rule':'lexicographic sorted leaves, zero-based indices 0,5,10,...'})
 return controls,real
def score_train(seqs,key,lang,boundary=False):
 suffix='_boundary' if boundary else '';base=27 if boundary else 26
 lm=np.fromfile(DATA/(lang+'_lm'+suffix+'.bin'));q=np.loadtxt(DATA/(lang+'_freq'+suffix+'.txt'))
 text=[''.join(key[x] for x in s) for s in seqs];counts=collections.Counter(''.join(text));n=sum(counts.values())
 ids=np.concatenate([grams(s,base) for s in text]);kl=sum(c/n*math.log2(c/n/q[26 if a==' ' else ord(a)-97]) for a,c in counts.items())
 ll=float(lm[ids].sum())
 return {'characters':n,'quadgrams':len(ids),'bits_per_quadgram':-ll/len(ids),'kl_bits':kl,'objective':ll-4*n*kl}
def fit(case,model):
 name=case['name']+'_'+model; resultpath=OUT/(name+'.json')
 if resultpath.exists():return json.loads(resultpath.read_text())
 boundary=case.get('boundary',False);suffix='_boundary' if boundary else ''
 train=spans(case['train'],boundary);test=spans(case['test'],boundary);lang=case['language']
 def label(x):return (x[0],x[1] if model=='context' else 0)
 count=collections.Counter(label(x) for s in train for x in s); symbols=sorted(count);mp={x:i for i,x in enumerate(symbols)}
 if case.get('permutation'):
  symbols=[(chr(97+i),st) for st in range(2 if model=='context' else 1) for i in range(26)]+[(' ',0)]
  mp={x:i for i,x in enumerate(symbols)}
 assert len(symbols)<=64
 seqs=[[mp[label(x)] for x in s] for s in train]
 inp=DATA/(name+'_train.txt');inp.write_text('\n'.join(' '.join(map(str,s)) for s in seqs)+'\n')
 start=time.time();cmd=[str(ROOT/('tmp/context_boundary' if boundary else 'tmp/homophonic')),str(DATA/(lang+'_lm'+suffix+'.bin')),str(DATA/(lang+'_freq'+suffix+'.txt')),str(inp),'8','60000',str(case.get('seed',SEED)),'4','.002']
 if boundary:cmd.append(str(mp[(' ',0)]))
 if case.get('permutation'):cmd[0]=str(ROOT/'tmp/context_permutation')
 p=subprocess.run(cmd,capture_output=True,text=True,check=True)
 out=json.loads(p.stdout)
 if boundary:out['key']=out['key'].replace('{',' ')
 mapping={s:out['key'][i] for i,s in enumerate(symbols)}
 tr=score_train(seqs,out['key'],lang,boundary);assert abs(tr['objective']-out['training_objective'])<1e-6*tr['characters']
 decoded=[''.join(mapping.get(label(x),'?') for x in s) for s in test]
 truth=[''.join(x[2] for x in s) for s in test]
 alln=sum(len(s)-s.count(' ') for s in decoded);unknown=sum(s.count('?') for s in decoded)
 unseen=sum(x[0]!=' ' and count[label(x)]==0 for s in test for x in s)
 out.update(name=name,model=model,language=lang,boundary=boundary,permutation=bool(case.get('permutation')),control=case['control'],seconds=round(time.time()-start,3),train=tr,test_characters=alln,test_unknown=unknown,test_unseen_training=unseen,test_coverage=1-unseen/alln,
  key_mapping=[{'cipher':ch,'after_y':st,'output':mapping[(ch,st)],'training_occurrences':count[(ch,st)]} for ch,st in symbols],
  test_decoded_NOT_TRANSLATION=decoded,seed=case.get('seed',SEED))
 if case['control']:
  errors=sum(a!=b for a,b in zip(''.join(decoded),''.join(truth)))
  ctx=[(x,pred) for s,ds in zip(test,decoded) for x,pred in zip(s,ds) if x[1]]
  errs=sum(x[2]!=pred for x,pred in ctx)
  out.update(heldout_accuracy=1-errors/alln,heldout_errors=errors,context_characters=len(ctx),context_errors=errs,context_accuracy=1-errs/len(ctx))
 save(resultpath,out)
 print(json.dumps({'name':name,'seconds':out['seconds'],'accuracy':out.get('heldout_accuracy'),'context_accuracy':out.get('context_accuracy'),'coverage':out['test_coverage']}),flush=True)
 return out
def compare(case):
 a=fit(case,'blind');b=fit(case,'context');boundary=case.get('boundary',False);suffix='_boundary' if boundary else '';base=27 if boundary else 26
 lm=np.fromfile(DATA/(case['language']+'_lm'+suffix+'.bin'))
 scores=[[],[]];known=0;total=0
 for x,y in zip(a['test_decoded_NOT_TRANSLATION'],b['test_decoded_NOT_TRANSLATION']):
  assert len(x)==len(y)
  for i in range(len(x)-3):
   total+=1;sa=x[i:i+4];sb=y[i:i+4]
   if '?' in sa or '?' in sb:continue
   known+=1
   for j,s in enumerate([sa,sb]):scores[j].append(float(lm[grams(s,base)[0]]))
 row={'name':case['name'],'language':case['language'],'control':case['control'],'null_index':case.get('null_index'),
  'heldout_quadgrams':known,'all_heldout_quadgrams':total,'quadgram_coverage':known/total,
  'blind_bits':-float(np.mean(scores[0])),'context_bits':-float(np.mean(scores[1])),
  'gain_bits':float(np.mean(scores[1])-np.mean(scores[0])),'blind_symbols':a['symbols'],'context_symbols':b['symbols']}
 if case['control']:row.update(blind_accuracy=a['heldout_accuracy'],contextual_accuracy=b['heldout_accuracy'],trigger_accuracy=b['context_accuracy'],trigger_n=b['context_characters'],gate_passed=b['heldout_accuracy']>=.95 and b['context_accuracy']>=.90 and b['test_coverage']>=.995)
 save(OUT/(case['name']+'_comparison.json'),row);return row
def shuffled(case,index):
 rng=random.Random(SEED+1000+index);out={k:v for k,v in case.items() if k not in ['train','test']}
 for split in ['train','test']:
  result=[]
  for r in case[split]:
   words=r['words'][:];ix=[j for j in range(1,len(words)-1) if words[j] is not None];vals=[words[j] for j in ix];rng.shuffle(vals)
   for j,w in zip(ix,vals):words[j]=w
   assert collections.Counter(w for w in words if w)==collections.Counter(w for w in r['words'] if w)
   result.append(dict(r,words=words))
  out[split]=result
 out.update(name=case['name']+f'_null{index:02}',null_index=index)
 return out
def main():
 perm=any('--permutation' in x for x in sys.argv)
 controls,real=prepare((1,2,3,4) if perm else (1,2))
 boundary=perm or any('--boundary' in x for x in sys.argv)
 if boundary:
  controls=[dict(c,name=c['name']+'_wb',boundary=True) for c in controls]
  real=[dict(c,name=c['name']+'_wb',boundary=True) for c in real]
 suffix='_boundary' if boundary else ''
 if perm:
  suffix='_permutation'
  controls=[dict(c,name=c['name']+'_perm',permutation=True) for c in controls]
  real=[dict(c,name=c['name']+'_perm',permutation=True) for c in real]
 if any(x in sys.argv for x in ['--controls','--boundary-controls','--permutation-controls']):
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:res=list(pool.map(compare,controls))
  save(OUT/('controls'+suffix+'_summary.json'),res);print('GATE',all(x['gate_passed'] for x in res),flush=True)
 elif any(x in sys.argv for x in ['--real','--boundary-real','--permutation-real']):
  gate=json.loads((OUT/('controls'+suffix+'_summary.json')).read_text());assert len(gate)==(8 if perm else 4) and all(x['gate_passed'] for x in gate),'Calibration gate failed; real application stopped.'
  cases=[]
  for c in real:
   for lang in ['latin','italian']:
    base=dict(c,language=lang,name=c['name']+'_'+lang);cases.append(base)
    if c['name'].startswith('ZL'):
     cases.extend(shuffled(base,i) for i in range(1,20))
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:res=list(pool.map(compare,cases))
  save(OUT/('real'+suffix+'_summary.json'),res)
 else:print('Use --controls, then --real if gate passed.')
if __name__=='__main__':main()
