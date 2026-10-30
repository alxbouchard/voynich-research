#!/usr/bin/env python3
import collections,hashlib,json,math,re,subprocess,sys,time
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score,precision_recall_fscore_support,log_loss
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
sys.path.insert(0,str(BASE/'voynich_20261028'));from analyse import parse
COMPOSITES=['ckh','cth','cph','cfh','ch','sh','iiiin','iiin','iin','in']
LETTERS=list('abcdefghijklmnopqrstuvwxyz');SEED=20261107
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def spans(raw):
 raw=raw.replace('<->','#').replace('<~>','#');raw=re.sub(r'<[^>]*>','',raw);raw=re.sub(r'\[[^\]]*\]','#',raw)
 raw=re.sub(r'@\d+;','#',raw).replace('{','').replace('}','').lower();raw=re.sub('[^a-z.,]','#',raw)
 out=[]
 for piece in raw.split('#'):
  piece=piece.strip('.,')
  if not piece:continue
  assert not re.search('[.,]{2}',piece),piece
  text=[];labels=[];pending=0
  for c in piece:
   if c in '.,':pending=1 if c=='.' else 2
   else:
    if text:labels.append(pending)
    text.append(c);pending=0
  if len(text)>=4:out.append((''.join(text),labels))
 return out
def build_inputs():
 data={}
 for fn in ['ZL3b-n.txt','IT2a-n.txt']:
  out=[]
  for r in parse(fn)[0]:
   if not r['type'].startswith('P') or r['metadata'].get('L') not in ['A','B']:continue
   for j,(s,b) in enumerate(spans(r['raw'])):
    out.append({'text':s,'labels':b,'page':r['page'],'leaf':r['leaf'],'locus':r['locus'],'span':j,'group':r['metadata']['Q'],'currier':r['metadata']['L']})
  data[fn[:2]]=out
 controls=json.loads((BASE/'voynich_phase6/data/adjacency_inputs.json').read_text())[4:]
 for d in controls:
  out=[]
  for i,r in enumerate(d['lines']):
   assert all(w is not None for w in r['words'])
   for j,(s,b) in enumerate(spans('.'.join(r['words']))):out.append({'text':s,'labels':b,'page':r['page'],'leaf':r['page'],'locus':r['locus'],'span':j,'group':str(min(7,8*i//len(d['lines']))),'currier':'control'})
  data[d['case']]=out
 save(ROOT/'data/inputs.json',data);return data
def contexts(s,i):return s[i:i+2],s[max(0,i-1):i+3] if 0<i<len(s)-2 else '^'+s[max(0,i-1):i+3]+'$'
def fit(train):
 pair=collections.defaultdict(lambda:[0,0]);four=collections.defaultdict(lambda:[0,0]);count=[0,0]
 for r in train:
  for i,y in enumerate(r['labels']):
   if y==2:continue
   a,b=contexts(r['text'],i);pair[a][y]+=1;four[b][y]+=1;count[y]+=1
 return count,pair,four
def predict(r,model):
 count,pa,fo=model;prior=(count[1]+.5)/(sum(count)+1);p2=[];p4=[]
 for i in range(len(r['labels'])):
  a,b=contexts(r['text'],i);v=pa.get(a,[0,0]);p=(v[1]+16*prior)/(sum(v)+16);u=fo.get(b,[0,0]);p2.append(p);p4.append((u[1]+32*p)/(sum(u)+32))
 return p2,p4
def metrics(labels,p):
 y=np.array(labels);p=np.array(p);mask=y!=2;y=y[mask];p=p[mask];pr,rc,f,_=precision_recall_fscore_support(y,p>=.5,average='binary',zero_division=0)
 return {'positions':len(y),'spaces':int(y.sum()),'prevalence':float(y.mean()),'auc':float(roc_auc_score(y,p)),'precision':float(pr),'recall':float(rc),'f1':float(f),'accuracy':float(((p>=.5)==y).mean()),'logloss_bits':float(log_loss(y,p)/math.log(2)),'predicted_spaces':int((p>=.5).sum())}
def init_units(s,representation):
 inventory=LETTERS if representation=='raw' else LETTERS+COMPOSITES;idx={s:i for i,s in enumerate(inventory)};out=[];i=0
 while i<len(s):
  unit=next((u for u in sorted(COMPOSITES,key=lambda x:-len(x)) if s.startswith(u,i)),s[i]) if representation=='composed' else s[i]
  out.append((idx[unit],i,i+len(unit)));i+=len(unit)
 return out,inventory
def apply_rule(units,left,right,newid):
 out=[];i=0
 while i<len(units):
  if i+1<len(units) and units[i][0]==left and units[i+1][0]==right:out.append((newid,units[i][1],units[i+1][2]));i+=2
  else:out.append(units[i]);i+=1
 return out
def merged_flags(s,units):
 flags=np.zeros(len(s)-1,dtype=bool)
 for _,a,b in units:flags[a:b-1]=True
 return flags
def bootstrap(rows,field1,field2):
 # Paired cluster bootstrap: resample quires, aggregate counts, then take difference.
 rng=np.random.default_rng(SEED);groups=sorted({r['group'] for r in rows});sums=[]
 for g in groups:
  rr=[r for r in rows if r['group']==g];sums.append([sum(r[field1][0] for r in rr),sum(r[field1][1] for r in rr),sum(r[field2][0] for r in rr),sum(r[field2][1] for r in rr)])
 a=np.array(sums);draws=[]
 for _ in range(2000):
  x=a[rng.integers(len(a),size=len(a))].sum(axis=0)
  if x[1]>0 and x[3]>0:draws.append(x[0]/x[1]-x[2]/x[3])
 return {'clusters':len(groups),'valid_draws':len(draws),'q025':float(np.quantile(draws,.025)),'q975':float(np.quantile(draws,.975))} if draws else None
def run(name,records):
 start=time.time();groups=sorted({r['group'] for r in records});preds=[];bpe=[];models={}
 for group in groups:
  train=[r for r in records if r['group']!=group];test=[r for r in records if r['group']==group]
  assert not {r['leaf'] for r in train}&{r['leaf'] for r in test} if name in ['ZL','IT'] else True
  model=fit(train)
  for r in test:
   p2,p4=predict(r,model);preds.append(dict(r,pair=p2,four=p4))
  for rep in ['raw','composed']:
   encoded=[init_units(r['text'],rep)[0] for r in train];inv=init_units('a',rep)[1]
   tmp=ROOT/'tmp'/f'{name}_{group}_{rep}_train.txt';tmp.write_text('\n'.join(' '.join(str(t[0]) for t in seq) for seq in encoded)+'\n')
   merges=json.loads(subprocess.check_output([str(ROOT/'src/bpe'),str(tmp),str(len(inv)),'128'],text=True));models[group+'_'+rep]={'base':inv,'merges':merges,'train_groups':[g for g in groups if g!=group]}
   vocabulary=inv.copy()
   for a,b,n,c in merges:assert n==len(vocabulary);vocabulary.append(vocabulary[a]+vocabulary[b])
   models[group+'_'+rep]['vocabulary']=vocabulary
   for r in test:
    seq,_=init_units(r['text'],rep)
    for step in [0]+list(range(1,len(merges)+1)):
     if step:
      a,b,n,c=merges[step-1];seq=apply_rule(seq,a,b,n)
     if step not in [0,32,64,128]:continue
     flags=merged_flags(r['text'],seq);labels=np.array(r['labels']);stats={str(k):[int(flags[labels==k].sum()),int((labels==k).sum())] for k in [0,1,2]}
     item={'group':group,'currier':r['currier'],'locus':r['locus'],'span':r['span'],'representation':rep,'merges':step,'counts':stats,'tokens':len(seq),'characters':len(r['text'])}
     if step==64 and rep=='raw':item.update(flags=flags.astype(int).tolist(),labels=r['labels'],text=r['text'],units=[vocabulary[t[0]] for t in seq])
     bpe.append(item)
  print(name,group,'done',round(time.time()-start,1),flush=True)
 save(ROOT/'results'/f'{name}_models.json',models);save(ROOT/'results'/f'{name}_predictions.json',preds);save(ROOT/'results'/f'{name}_bpe.json',bpe)
 summary={'case':name,'groups':groups,'spans':len(records),'characters':sum(len(r['text']) for r in records),'boundary_prediction':{},'bpe':[]}
 for stratum in ['all']+(['A','B'] if name in ['ZL','IT'] else []):
  pp=[r for r in preds if stratum=='all' or r['currier']==stratum];labels=[y for r in pp for y in r['labels']]
  summary['boundary_prediction'][stratum]={kind:metrics(labels,[p for r in pp for p in r[kind]]) for kind in ['pair','four']}
  for kind in ['pair','four']:
   summary['boundary_prediction'][stratum][kind]['mean_probability_by_label']={str(k):float(np.mean([p for r in pp for y,p in zip(r['labels'],r[kind]) if y==k])) if k in labels else None for k in [0,1,2]}
  for rep in ['raw','composed']:
   for step in [0,32,64,128]:
    rows=[r for r in bpe if r['representation']==rep and r['merges']==step and (stratum=='all' or r['currier']==stratum)]
    counts={str(k):[sum(r['counts'][str(k)][0] for r in rows),sum(r['counts'][str(k)][1] for r in rows)] for k in [0,1,2]}
    rates={k:(a/b if b else None) for k,(a,b) in counts.items()};item={'stratum':stratum,'representation':rep,'merges':step,'counts':counts,'crossing_rates':rates}
    if counts['2'][1]>0:
     br=[dict(group=r['group'],uncertain=r['counts']['2'],definite=r['counts']['1']) for r in rows];item['uncertain_minus_definite']=rates['2']-rates['1'];item['difference_bootstrap']=bootstrap(br,'uncertain','definite')
    summary['bpe'].append(item)
 # Hidden-boundary null: shuffle original token lengths within each clear span.
 rows=[r for r in bpe if r['representation']=='raw' and r['merges']==64];rng=np.random.default_rng(SEED);draws=[]
 for _ in range(100):
  hit=np.zeros(3,dtype=int);total=np.zeros(3,dtype=int)
  for r in rows:
   pos=np.flatnonzero(np.array(r['labels'])>0)+1
   if not len(pos):continue
   lengths=np.diff(np.r_[0,pos,len(r['text'])]);fake=np.cumsum(rng.permutation(lengths))[:-1]-1;types=np.array(r['labels'])[pos-1];flags=np.array(r['flags'])
   for k in [1,2]:total[k]+=(types==k).sum();hit[k]+=flags[fake[types==k]].sum()
  draws.append({str(k):float(hit[k]/total[k]) if total[k] else None for k in [1,2]})
 summary['length_permutation_100']={str(k):{'mean':float(np.mean([d[str(k)] for d in draws])),'q025':float(np.quantile([d[str(k)] for d in draws],.025)),'q975':float(np.quantile([d[str(k)] for d in draws],.975))} for k in [1,2] if draws[0][str(k)] is not None}
 save(ROOT/'results'/f'{name}_length_null.json',draws);save(ROOT/'results'/f'{name}_summary.json',summary)
 print('SUMMARY',name,summary['boundary_prediction']['all'],flush=True);return summary
def main():
 assert spans('aa.[x:y].bb.cc,dd.ee<->ff')==[('bbccddee',[0,1,0,2,0,1,0])]
 data=build_inputs();res=[]
 for name,records in data.items():
  cache=ROOT/'results'/f'{name}_summary.json';res.append(json.loads(cache.read_text()) if cache.exists() and '--force' not in sys.argv else run(name,records))
 save(ROOT/'results/summary.json',res)
if __name__=='__main__':main()
