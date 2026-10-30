#!/usr/bin/env python3
import collections,json,time
from pathlib import Path
import numpy as np
import research as h
ROOT=h.ROOT

def evaluate(e,alpha=32,x_override=None,cache=None,details=False):
 K=e['K'];x=e['x'] if x_override is None else x_override;y=e['y'];base,style,prior,folds=h.baseline(e,alpha) if cache is None else cache
 prob=np.empty_like(base)
 for train,test,unused in folds:
  p0=prior[test][0];c=h.count(x[train],y[train],K,K);edge=(c+alpha*p0)/(c.sum(axis=1,keepdims=True)+alpha)
  raw=base[test]*edge[x[test]]/p0;prob[test]=raw/raw.sum(axis=1,keepdims=True)
 assert np.allclose(prob.sum(axis=1),1)
 ix=np.arange(len(y));by=base[ix,y];ny=prob[ix,y];gain=np.log2(ny/by);q=h.ALPHA.index('q');isq=y==q;bq=base[:,q];nq=prob[:,q]
 binary=np.log2(np.where(isq,nq,1-nq)/np.where(isq,bq,1-bq));rest=np.where(isq,0,gain-binary);assert np.allclose(gain,binary+rest)
 result={'n':len(y),'folds':len(e['groups']),'gain_bits':float(gain.mean()),'position_loss_bits':float(-np.log2(by).mean()),'neighbor_loss_bits':float(-np.log2(ny).mean()),'position_accuracy':float((base.argmax(axis=1)==y).mean()),'neighbor_accuracy':float((prob.argmax(axis=1)==y).mean()),'q_binary_gain_bits':float(binary.mean()),'non_q_within_gain_bits':float(rest.mean()),'q_target_count':int(isq.sum())}
 if details:return result,{'p_base':by,'p_neighbor':ny,'base_q':bq,'neighbor_q':nq,'gain':gain,'q_binary_gain':binary,'non_q_gain':rest,'base_prediction':base.argmax(axis=1),'neighbor_prediction':prob.argmax(axis=1)}
 return result

def coverage(rows,e):
 out=[]
 for g in e['groups']:
  train=[r for r in rows if r['group']!=g];test=[r for r in rows if r['group']==g]
  styles={(r['section'],r['hand']) for r in train};ctx={(r['section'],r['hand'],r['horizontal'],r['vertical'],r['source_end']) for r in train}
  out.append({'group':g,'n':len(test),'unseen_style':sum((r['section'],r['hand']) not in styles for r in test),'unseen_joint_neighbor_context':sum((r['section'],r['hand'],r['horizontal'],r['vertical'],r['source_end']) not in ctx for r in test)})
 return {'folds':out,'unseen_style_fraction':sum(r['unseen_style'] for r in out)/len(rows),'unseen_joint_context_fraction':sum(r['unseen_joint_neighbor_context'] for r in out)/len(rows)}

def synthetic(dependent):
 rng=np.random.default_rng(20261028+(0 if dependent else 1));chars=list('abcd');lines=[]
 for group in range(8):
  for line in range(80):
   words=[];prev=str(rng.choice(chars))
   for j in range(10):
    first=prev if dependent else str(rng.choice(chars));end=str(rng.choice(chars));words.append(first+'m'+end);prev=end
   lines.append({'page':f'p{group}','physical_leaf':f'p{group}','group':str(group),'locus':f'toy{group}.{line}','section':f'unique{group}','hand':str(group),'vertical':min(3,4*line//80),'words':words})
 return {'case':'Toy_dependent' if dependent else 'Toy_independent','layout':'Synthetic unique style in each block, no manuscript content','lines':lines}

def run(case):
 name=case['case'];t=time.time();rows,inv=h.rows_for(case);e=h.encode(rows,inv);cache=h.baseline(e,32);primary,detail=evaluate(e,32,cache=cache,details=True)
 report={'case':name,'model':'Posthoc pooled multiplicative correction, fixed addendum before results','primary':primary,'bootstrap':h.bootstrap(e,detail),'coverage_original_joint_model':coverage(rows,e),'folds':[]}
 pred=[dict(r,**{k:float(v[i]) if k not in ['base_prediction','neighbor_prediction'] else inv[int(v[i])] for k,v in detail.items()}) for i,r in enumerate(rows)];h.save(ROOT/'results'/f'{name}_pooled_predictions.json',pred)
 for g in e['groups']:
  ix=e['g']==g;report['folds'].append({'group':g,'n':int(ix.sum()),'gain_bits':float(detail['gain'][ix].mean())})
 report['sensitivity']={}
 for alpha in [8,128]:report['sensitivity']['alpha_'+str(alpha)]=evaluate(e,alpha)
 for mode in ['clean_line','no_repeat']:
  rr,ii=h.rows_for(case,mode=mode);report['sensitivity'][mode]=evaluate(h.encode(rr,ii))
 rr,ii=h.rows_for(case,representation='composed');report['sensitivity']['composed']=evaluate(h.encode(rr,ii))
 report['lags']={}
 for lag in [1,2,3]:
  rr,ii=h.rows_for(case,mode='lag',lag=lag);report['lags'][str(lag)]=evaluate(h.encode(rr,ii))
 buckets=collections.defaultdict(list)
 for i,r in enumerate(rows):buckets[r['page'],r['horizontal'],r['vertical']].append(i)
 groups=[np.array(v) for v in buckets.values() if len(v)>1];rng=np.random.default_rng(20261028);null=[]
 for it in range(199):
  xx=e['x'].copy()
  for ix in groups:xx[ix]=rng.permutation(xx[ix])
  null.append(evaluate(e,32,xx,cache)['gain_bits'])
 report['null']={'draws':199,'mean':float(np.mean(null)),'q025':float(np.quantile(null,.025)),'q975':float(np.quantile(null,.975)),'exploratory_upper_tail':(1+sum(v>=primary['gain_bits'] for v in null))/200}
 if name.startswith('Toy_'):report['original_joint_model']=h.evaluate(e)
 h.save(ROOT/'results'/f'{name}_pooled_null_draws.json',null);h.save(ROOT/'results'/f'{name}_pooled_summary.json',report)
 print(name,json.dumps(primary),round(time.time()-t,2),'sec',flush=True);return report

def main():
 toys=[synthetic(True),synthetic(False)];h.save(ROOT/'data/toy_controls.json',toys)
 toy_results=[run(c) for c in toys];h.save(ROOT/'results/toy_summary.json',toy_results)
 reports=[run(c) for c in h.read(ROOT/'data/inputs.json')];h.save(ROOT/'results/pooled_summary.json',reports)
if __name__=='__main__':main()
