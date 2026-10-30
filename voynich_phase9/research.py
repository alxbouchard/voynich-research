#!/usr/bin/env python3
"""Frozen, out-of-quire edge prediction with positional controls."""
import collections,json,math,re,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
COMPOSITES=['ckh','cth','cph','cfh','ch','sh','iiiin','iiin','iin','in']
ALPHA=list('abcdefghijklmnopqrstuvwxyz')
RX=re.compile('|'.join(COMPOSITES)+'|.')

def read(p):return json.loads(p.read_text())
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def rows_for(case,representation='raw',mode='primary',lag=1):
 inv=ALPHA+COMPOSITES if representation=='composed' else ALPHA
 ix={x:i for i,x in enumerate(inv)};rows=[]
 for line in case['lines']:
  w=line['words'];n=len(w)
  if mode=='clean_line' and any(x is None for x in w):continue
  for j in range(4 if mode=='lag' else 2,n-1):
   distance=3 if mode=='lag' else 1
   if any(x is None for x in w[j-distance:j+1]):continue
   if mode=='no_repeat' and w[j-1]==w[j]:continue
   prev=w[j-lag];target=w[j];a=RX.findall(prev)[-1] if representation=='composed' else prev[-1];b=RX.findall(target)[0] if representation=='composed' else target[0]
   assert 0<j-lag<n-1 and 0<j<n-1
   rows.append({'page':line['page'],'leaf':line['physical_leaf'],'group':line['group'],'locus':line['locus'],'slot':j,'line_slots':n,'section':line['section'],'hand':line['hand'],'vertical':line['vertical'],'horizontal':min(3,4*j//n),'source_token':prev,'target_token':target,'source_end':a,'target_initial':b,'x':ix[a],'y':ix[b]})
 return rows,inv

def encode(rows,inv):
 styles=sorted({(r['section'],r['hand']) for r in rows});si={s:i for i,s in enumerate(styles)}
 s=np.array([si[r['section'],r['hand']] for r in rows]);pos=s*20+np.array([r['vertical']*4+r['horizontal'] for r in rows]);x=np.array([r['x'] for r in rows]);y=np.array([r['y'] for r in rows]);g=np.array([r['group'] for r in rows]);K=len(inv)
 return {'s':s,'pos':pos,'x':x,'y':y,'g':g,'K':K,'ns':len(styles),'np':len(styles)*20,'groups':sorted(set(g)),'styles':styles}

def count(ids,y,n,K):return np.bincount(ids*K+y,minlength=n*K).reshape(n,K)
def baseline(e,alpha):
 s,pos,y,g,K=e['s'],e['pos'],e['y'],e['g'],e['K'];N=len(y);base=np.empty((N,K));style=np.empty((N,K));prior=np.empty((N,K));folds=[]
 for group in e['groups']:
  train=g!=group;test=~train
  glob=np.bincount(y[train],minlength=K);p0=(glob+.5)/(glob.sum()+.5*K)
  cs=count(s[train],y[train],e['ns'],K);ps=(cs+alpha*p0)/(cs.sum(axis=1,keepdims=True)+alpha)
  cp=count(pos[train],y[train],e['np'],K);pp=(cp+alpha*ps[np.arange(e['np'])//20])/(cp.sum(axis=1,keepdims=True)+alpha)
  base[test]=pp[pos[test]];style[test]=ps[s[test]];prior[test]=p0
  folds.append((train,test,pp))
 assert np.allclose(base.sum(axis=1),1)
 return base,style,prior,folds

def evaluate(e,alpha=32,x_override=None,cache=None,details=False):
 K=e['K'];x=e['x'] if x_override is None else x_override;y=e['y'];pos=e['pos'];xx=pos*K+x
 base,style,prior,folds=baseline(e,alpha) if cache is None else cache
 prob=np.empty_like(base)
 for train,test,pp in folds:
  cx=count(xx[train],y[train],e['np']*K,K);pr=(cx+alpha*pp[np.arange(e['np']*K)//K])/(cx.sum(axis=1,keepdims=True)+alpha)
  prob[test]=pr[xx[test]]
 assert np.allclose(prob.sum(axis=1),1)
 idx=np.arange(len(y));by=base[idx,y];ny=prob[idx,y];gain=np.log2(ny/by)
 result={'n':len(y),'folds':len(e['groups']),'gain_bits':float(gain.mean()),'position_loss_bits':float(-np.log2(by).mean()),'neighbor_loss_bits':float(-np.log2(ny).mean()),'position_accuracy':float((base.argmax(axis=1)==y).mean()),'neighbor_accuracy':float((prob.argmax(axis=1)==y).mean()),'position_gain_over_style_bits':float(np.log2(by/style[idx,y]).mean()),'style_gain_over_global_bits':float(np.log2(style[idx,y]/prior[idx,y]).mean())}
 if details:
  q=ALPHA.index('q');isq=y==q;bq=base[:,q];nq=prob[:,q]
  binary=np.log2(np.where(isq,nq,1-nq)/np.where(isq,bq,1-bq));rest=np.where(isq,0,np.log2(ny/by)-binary)
  assert np.allclose(gain,binary+rest)
  result.update(q_binary_gain_bits=float(binary.mean()),non_q_within_gain_bits=float(rest.mean()),q_target_count=int(isq.sum()))
  return result,{'p_base':by,'p_neighbor':ny,'base_q':bq,'neighbor_q':nq,'gain':gain,'q_binary_gain':binary,'non_q_gain':rest,'base_prediction':base.argmax(axis=1),'neighbor_prediction':prob.argmax(axis=1)}
 return result

def bootstrap(e,detail):
 groups=e['groups'];a=np.array([[sum(e['g']==g),detail['gain'][e['g']==g].sum(),detail['q_binary_gain'][e['g']==g].sum(),detail['non_q_gain'][e['g']==g].sum()] for g in groups]);rng=np.random.default_rng(20261028);pick=rng.integers(len(a),size=(2000,len(a)));z=a[pick].sum(axis=1);ci=np.quantile(z[:,1:]/z[:,:1],[.025,.975],axis=0).T
 return {'clusters':len(groups),'draws':2000,'gain_ci':ci[0].tolist(),'q_binary_ci':ci[1].tolist(),'non_q_ci':ci[2].tolist(),'note':'Fixed held-out scores, no refit; overlapping training sets and common transcription source limit independence.'}

def run(case):
 name=case['case'];t=time.time();rows,inv=rows_for(case);e=encode(rows,inv);cache=baseline(e,32);primary,detail=evaluate(e,32,cache=cache,details=True)
 report={'case':name,'layout':case['layout'],'primary':primary,'bootstrap':bootstrap(e,detail),'folds':[]}
 for group in e['groups']:
  ix=e['g']==group;testleaves={r['leaf'] for r in rows if r['group']==group};trainleaves={r['leaf'] for r in rows if r['group']!=group};assert not testleaves&trainleaves
  report['folds'].append({'group':group,'n':int(ix.sum()),'gain_bits':float(detail['gain'][ix].mean())})
 pairs=collections.defaultdict(list)
 for i,r in enumerate(rows):pairs[r['source_end'],r['target_initial']].append(float(detail['gain'][i]))
 report['edge_contributions']=[{'source_end':a,'target_initial':b,'n':len(v),'mean_gain':sum(v)/len(v),'contribution_per_all_targets':sum(v)/len(rows)} for (a,b),v in sorted(pairs.items(),key=lambda kv:-sum(kv[1]))]
 pred=[dict(r,**{k:float(v[i]) if k not in ['base_prediction','neighbor_prediction'] else inv[int(v[i])] for k,v in detail.items()}) for i,r in enumerate(rows)]
 save(ROOT/'results'/f'{name}_predictions.json',pred)
 report['sensitivity']={}
 for alpha in [8,128]:report['sensitivity']['alpha_'+str(alpha)]=evaluate(e,alpha)
 for mode in ['clean_line','no_repeat']:
  rr,ii=rows_for(case,mode=mode);report['sensitivity'][mode]=evaluate(encode(rr,ii))
 rr,ii=rows_for(case,representation='composed');report['sensitivity']['composed']=evaluate(encode(rr,ii))
 report['lags']={}
 for lag in [1,2,3]:
  rr,ii=rows_for(case,mode='lag',lag=lag);report['lags'][str(lag)]=evaluate(encode(rr,ii))
 # Conditional permutation of source-end labels at equal page and position strata.
 buckets=collections.defaultdict(list)
 for i,r in enumerate(rows):buckets[r['page'],r['horizontal'],r['vertical']].append(i)
 ixgroups=[np.array(v) for v in buckets.values() if len(v)>1];movable=sum(len(v) for v in ixgroups if len(set(e['x'][v]))>1)
 rng=np.random.default_rng(20261028);null=[];moved=[]
 for it in range(199):
  xx=e['x'].copy()
  for ix in ixgroups:xx[ix]=rng.permutation(xx[ix])
  if it==0:
   for ix in ixgroups:assert sorted(xx[ix])==sorted(e['x'][ix])
  null.append(evaluate(e,32,xx,cache=cache)['gain_bits']);moved.append(float((xx!=e['x']).mean()))
  if it in [0,49,99,149,198]:print(name,'null',it+1,round(time.time()-t,2),'seconds',flush=True)
 report['null']={'draws':199,'seed':20261028,'mean':float(np.mean(null)),'q025':float(np.quantile(null,.025)),'q975':float(np.quantile(null,.975)),'conditional_randomization_upper_tail':(1+sum(z>=primary['gain_bits'] for z in null))/200,'fraction_rows_permutable_with_different_ends':movable/len(rows),'mean_fraction_changed':float(np.mean(moved)),'caution':'Source labels shuffled, not whole text; finite, exploratory, unadjusted across cases and sensitivities.'}
 save(ROOT/'results'/f'{name}_null_draws.json',null);save(ROOT/'results'/f'{name}_summary.json',report)
 print('RESULT',name,json.dumps(primary),flush=True);return report

def main():
 cases=read(ROOT/'data/inputs.json');reports=[run(case) for case in cases];save(ROOT/'results/summary.json',reports)
if __name__=='__main__':main()
