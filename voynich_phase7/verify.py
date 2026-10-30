#!/usr/bin/env python3
import collections,json,math,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import research as h
def read(p):return json.loads(p.read_text())
def py_bpe(lines,base,steps):
 seq=[list(x) for x in lines];out=[]
 for step in range(steps):
  c=collections.Counter((a,b) for s in seq for a,b in zip(s,s[1:]))
  if not c:break
  pair=min(c,key=lambda p:(-c[p],p))
  if c[pair]<2:break
  new=base+step;out.append([*pair,new,c[pair]]);nextseq=[]
  for s in seq:
   v=[];i=0
   while i<len(s):
    if tuple(s[i:i+2])==pair:v.append(new);i+=2
    else:v.append(s[i]);i+=1
   nextseq.append(v)
  seq=nextseq
 return out
def main():
 data=read(ROOT/'data/inputs.json');summaries=read(ROOT/'results/summary.json');checked=0;predcount=0;annotations=[];examples=[]
 for summary in summaries:
  name=summary['case'];records=data[name];pred=read(ROOT/'results'/f'{name}_predictions.json');models=read(ROOT/'results'/f'{name}_models.json');bp=read(ROOT/'results'/f'{name}_bpe.json')
  assert len(pred)==len(records)
  for group in summary['groups']:
   train=[r for r in records if r['group']!=group];test=[r for r in pred if r['group']==group]
   fit=h.fit(train)
   for r in test:
    a,b=h.predict(r,fit);assert np.allclose(a,r['pair'],atol=1e-14) and np.allclose(b,r['four'],atol=1e-14);predcount+=len(a)
   for rep in ['raw','composed']:
    model=models[group+'_'+rep];assert group not in model['train_groups'];assert set(model['train_groups'])==set(summary['groups'])-{group}
    for a,b,n,c in model['merges']:assert model['vocabulary'][n]==model['vocabulary'][a]+model['vocabulary'][b]
  # Independent frequent-pair counting implementation on the first held-out fold, first 8 merges.
  g=summary['groups'][0]
  for rep in ['raw','composed']:
   seq=[[u[0] for u in h.init_units(r['text'],rep)[0]] for r in records if r['group']!=g]
   expected=py_bpe(seq,len(models[g+'_'+rep]['base']),8);assert expected==models[g+'_'+rep]['merges'][:8];checked+=len(expected)
  for r in bp:
   if 'units' in r:
    assert ''.join(r['units'])==r['text']
    pos=0;flag=[1]*(len(r['text'])-1)
    for unit in r['units'][:-1]:pos+=len(unit);flag[pos-1]=0
    assert flag==r['flags'];assert len(r['labels'])==len(flag)
    for k in [0,1,2]:assert [sum(f for f,y in zip(flag,r['labels']) if y==k),r['labels'].count(k)]==r['counts'][str(k)]
  for kind in ['pair','four']:
   known=[(y,p) for r in pred for y,p in zip(r['labels'],r[kind]) if y!=2];tp=sum(y==1 and p>=.5 for y,p in known);proposed=sum(p>=.5 for y,p in known);actual=sum(y for y,p in known)
   m=summary['boundary_prediction']['all'][kind];assert abs(tp/proposed-m['precision'])<1e-12 and abs(tp/actual-m['recall'])<1e-12
  for r in summary['bpe']:
   selected=[x for x in bp if x['representation']==r['representation'] and x['merges']==r['merges'] and (r['stratum']=='all' or r['stratum']==x['currier'])]
   for k in ['0','1','2']:assert r['counts'][k]==[sum(x['counts'][k][i] for x in selected) for i in [0,1]]
  if name=='ZL':
   bmap={(r['locus'],r['span']):r for r in bp if r['representation']=='raw' and r['merges']==64}
   for r in pred:
    for i,(y,p) in enumerate(zip(r['labels'],r['four'])):
     if y==2:annotations.append({'page':r['page'],'locus':r['locus'],'span':r['span'],'offset_in_retained_stream':i+1,'original_separator':',','predicted_dot_probability':p,'crossed_by_space_blind_BPE64':bool(bmap[(r['locus'],r['span'])]['flags'][i]),'context':r['text'][max(0,i-12):i+1]+' | '+r['text'][i+1:i+14],'status':'UNCERTAIN_ORIGINAL_PRESERVED_NOT_A_CORRECTION'})
   # Predeclared pages; first eligible unambiguous span in original line-number order, not best F1.
   for page in ['f1r','f2r','f75r','f103r']:
    pool=sorted([r for r in pred if r['page']==page and 2 not in r['labels'] and 30<=len(r['text'])<=80],key=lambda x:(int(x['locus'].split('.')[1].split(',')[0]),x['span']))
    if pool:
     r=pool[0];examples.append({'locus':r['locus'],'group_held_out':r['group'],'span':r['span'],'text':r['text'],'labels':r['labels'],'probabilities':[round(x,6) for x in r['four']]})
 h.save(ROOT/'results/annotated_uncertain_boundaries.json',{'warning':'All original comma labels retained. Probabilities model conventions, not physical width or linguistic truth.','count':len(annotations),'items':annotations})
 h.save(ROOT/'results/examples.json',{'selection':'First 30-80-character span without uncertain gaps on each of f1r/f2r/f75r/f103r, original line-number order. Illustrative, not performance-selected. A span can be a line fragment after exclusion.','items':examples})
 h.save(ROOT/'results/verification.json',{'status':'PASS','prediction_positions_recomputed':predcount,'independent_BPE_merge_checks':checked,'all_primary_heldout_unit_roundtrips':True,'reported_boundary_counts_recomputed':True,'annotation_count':len(annotations),'limitations':['No original image remeasurement','No semantic validation','Bootstrap intervals conditional on overlapping cross-fit models']})
 print('PASS',predcount,'predicted positions,',checked,'independent merge checks,',len(annotations),'uncertain boundaries');print(json.dumps(examples,ensure_ascii=False))
if __name__=='__main__':main()
