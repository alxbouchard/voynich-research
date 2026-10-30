#!/usr/bin/env python3
import json, collections, hashlib
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score, brier_score_loss
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent

def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def measures(rows):
 y=np.array([r['IT_label'] for r in rows]);p=np.array([r['p4'] for r in rows]);pred=p>=.5
 keep=(p<=.1)|(p>=.9)
 counts={f'{a}->{b}':int(((pred==a)&(y==b)).sum()) for a in [0,1] for b in [0,1]}
 return {'n':len(y),'IT_spaces':int(y.sum()),'agreement':float((y==pred).mean()),'majority_always_split_agreement':float(y.mean()),'confusion_predicted_to_IT':counts,'auc':float(roc_auc_score(y,p)) if len(set(y))==2 else None,'brier':float(brier_score_loss(y,p)), 'extreme_n':int(keep.sum()),'extreme_coverage':float(keep.mean()),'extreme_agreement':float((y[keep]==pred[keep]).mean()) if keep.any() else None,'extreme_errors':int((y[keep]!=pred[keep]).sum()),'pair_agreement':float(((np.array([r['p2'] for r in rows])>=.5)==y).mean()),'BPE_agreement':float((np.array([not r['BPE_crossed'] for r in rows])==y).mean())}

def main():
 data=read(ROOT/'data/source_inputs.json');pred=read(ROOT/'data/source_predictions.json')
 bb={(r['locus'],r['span']):r for r in read(ROOT/'data/source_bpe64.json') if r['representation']=='raw' and r['merges']==64}
 z=collections.defaultdict(list);it=collections.defaultdict(list)
 for r in pred:z[r['locus']].append(r)
 for r in data['IT']:it[r['locus']].append(r)
 matched=[];lines=0
 for loc,rr in z.items():
  if len(rr)!=1 or len(it.get(loc,[]))!=1:continue
  a,b=rr[0],it[loc][0]
  if a['text']!=b['text']:continue
  lines+=1
  for i,label in enumerate(a['labels']):
   if label!=2:continue
   matched.append({'locus':loc,'page':a['page'],'group':a['group'],'currier':a['currier'],'span':a['span'],'offset':i+1,'text':a['text'],'context':a['text'][max(0,i-11):i+1]+' | '+a['text'][i+1:i+13], 'IT_label':b['labels'][i],'p4':a['four'][i],'p2':a['pair'][i],'BPE_crossed':bool(bb[loc,a['span']]['flags'][i])})
 assert lines==1913 and len(matched)==1089 and sum(r['IT_label'] for r in matched)==700
 save(ROOT/'data/paired_uncertain.json',matched)
 out={'matching_loci':lines,'all':measures(matched),'currier':{c:measures([r for r in matched if r['currier']==c]) for c in ['A','B']},'by_quire':{q:measures([r for r in matched if r['group']==q]) for q in sorted({r['group'] for r in matched})}}
 dec=[]
 for i in range(10):
  rows=[r for r in matched if min(int(r['p4']*10),9)==i]
  dec.append({'lower':i/10,'upper':(i+1)/10,'n':len(rows),'mean_p':float(np.mean([r['p4'] for r in rows])) if rows else None,'IT_split_fraction':float(np.mean([r['IT_label'] for r in rows])) if rows else None})
 out['deciles']=dec
 groups=sorted({r['group'] for r in matched});rng=np.random.default_rng(20261028);draw=[]
 grouped={g:[r for r in matched if r['group']==g] for g in groups}
 for _ in range(2000):
  m=measures([r for g in rng.choice(groups,len(groups),replace=True) for r in grouped[g]])
  draw.append([m['agreement'],m['extreme_agreement'],m['agreement']-m['majority_always_split_agreement']])
 out['bootstrap']={'clusters':len(groups),'draws':2000,'intervals':dict(zip(['agreement','extreme_agreement','gain_over_always_split'],np.quantile(np.array(draw),[.025,.975],axis=0).T.tolist())),'warning':'Descriptive clustered resampling of fixed predictions; overlapping fitted training folds, common physical source and transcription conventions.'}
 save(ROOT/'results/transfer_summary.json',out)
 selected=[]
 for page in ['f1r','f75r','f103r']:
  rows=[]
  for r in pred:
   if r['page']!=page:continue
   for i,y in enumerate(r['labels']):
    if y==2:rows.append({'page':page,'locus':r['locus'],'span':r['span'],'offset':i+1,'p4':r['four'][i],'text':r['text'],'context':r['text'][max(0,i-11):i+1]+' | '+r['text'][i+1:i+13]})
  rows.sort(key=lambda r:(r['p4'],r['locus'],r['span'],r['offset']))
  selected.extend([dict(rows[0],selection='minimum'),dict(rows[-1],selection='maximum')])
 save(ROOT/'data/image_targets.json',selected)
 save(ROOT/'data/dependency_hashes.json',{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/source_inputs.json',ROOT/'data/source_predictions.json',ROOT/'data/source_bpe64.json',ROOT/'PROTOCOL.json']})
 print(json.dumps({'all':out['all'],'intervals':out['bootstrap'],'deciles':dec,'image_targets':selected},indent=2))
if __name__=='__main__':main()
