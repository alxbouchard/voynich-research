#!/usr/bin/env python3
"""Independent Counter-based reconstruction of primary probabilities."""
import collections,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;LETTERS='abcdefghijklmnopqrstuvwxyz';K=26;A=32

def rd(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def make_rows(case):
 rows=[]
 for line in case['lines']:
  words=line['words']
  for j in range(2,len(words)-1):
   if words[j] is None or words[j-1] is None:continue
   rows.append({'locus':line['locus'],'slot':j,'group':line['group'],'page':line['page'],'leaf':line['physical_leaf'],'s':(line['section'],line['hand']),'pos':(line['section'],line['hand'],min(3,4*j//len(words)),line['vertical']),'x':words[j-1][-1],'y':words[j][0]})
 return rows

def slow_predict(rows,expected_original=None,expected_pool=None):
 gains1=[];gains2=[];maxerr=0.;verified=0
 for group in sorted({r['group'] for r in rows}):
  train=[r for r in rows if r['group']!=group];test=[r for r in rows if r['group']==group]
  assert not {r['leaf'] for r in train}&{r['leaf'] for r in test}
  cy=collections.Counter(r['y'] for r in train);cs=collections.Counter(r['s'] for r in train);cp=collections.Counter(r['pos'] for r in train);ce=collections.Counter(r['x'] for r in train);cc=collections.Counter((r['pos'],r['x']) for r in train)
  csy=collections.Counter((r['s'],r['y']) for r in train);cpy=collections.Counter((r['pos'],r['y']) for r in train);cey=collections.Counter((r['x'],r['y']) for r in train);ccy=collections.Counter((r['pos'],r['x'],r['y']) for r in train)
  p0={c:(cy[c]+.5)/(len(train)+K*.5) for c in LETTERS}
  cache={}
  for r in test:
   key=(r['pos'],r['x'])
   if key not in cache:
    b={};p1={};u={}
    for c in LETTERS:
     ps=(csy[r['s'],c]+A*p0[c])/(cs[r['s']]+A)
     b[c]=(cpy[r['pos'],c]+A*ps)/(cp[r['pos']]+A)
     p1[c]=(ccy[r['pos'],r['x'],c]+A*b[c])/(cc[r['pos'],r['x']]+A)
     pe=(cey[r['x'],c]+A*p0[c])/(ce[r['x']]+A)
     u[c]=b[c]*pe/p0[c]
    total=sum(u.values());p2={c:u[c]/total for c in LETTERS};assert abs(sum(b.values())-1)<1e-12 and abs(sum(p1.values())-1)<1e-12 and abs(sum(p2.values())-1)<1e-12
    cache[key]=(b,p1,p2)
   b,p1,p2=cache[key];y=r['y'];g1=math.log2(p1[y]/b[y]);g2=math.log2(p2[y]/b[y]);gains1.append(g1);gains2.append(g2)
   for expect,p,gain in [(expected_original,p1,g1),(expected_pool,p2,g2)]:
    if expect is None:continue
    v=expect[r['locus'],r['slot']]
    assert (v['target_initial'],v['source_end'])==(y,r['x'])
    for calculated,stored in [(b[y],v['p_base']),(p[y],v['p_neighbor']),(gain,v['gain']),(b['q'],v['base_q']),(p['q'],v['neighbor_q'])]:maxerr=max(maxerr,abs(calculated-stored));assert abs(calculated-stored)<1e-10
    assert max(LETTERS,key=b.get)==v['base_prediction'] and max(LETTERS,key=p.get)==v['neighbor_prediction']
    verified+=1
 return {'positions_models_verified':verified,'max_abs_error':maxerr,'joint_gain':sum(gains1)/len(rows),'pooled_gain':sum(gains2)/len(rows)}

def main():
 results=[];cases=rd(ROOT/'data/inputs.json')+rd(ROOT/'data/toy_controls.json')
 for case in cases:
  name=case['case'];rows=make_rows(case);pool={(r['locus'],r['slot']):r for r in rd(ROOT/'results'/f'{name}_pooled_predictions.json')}
  p=ROOT/'results'/f'{name}_predictions.json';orig={(r['locus'],r['slot']):r for r in rd(p)} if p.exists() else None
  assert len(pool)==len(rows) and set(pool)=={(r['locus'],r['slot']) for r in rows}
  r=slow_predict(rows,orig,pool);r['case']=name
  report=rd(ROOT/'results'/f'{name}_pooled_summary.json');assert abs(r['pooled_gain']-report['primary']['gain_bits'])<1e-11
  if orig:
   report1=rd(ROOT/'results'/f'{name}_summary.json');assert abs(r['joint_gain']-report1['primary']['gain_bits'])<1e-11
  else:assert abs(r['joint_gain']-report['original_joint_model']['gain_bits'])<1e-11
  # Independently recompute first conditional-null draw for two differently sized corpora.
  if name in ['ZL_A','Naibbe_Pliny']:
   buckets=collections.defaultdict(list)
   for i,row in enumerate(rows):buckets[row['page'],row['pos'][2],row['pos'][3]].append(i)
   xx=[r['x'] for r in rows];rng=np.random.default_rng(20261028)
   for ix in buckets.values():
    if len(ix)>1:
     vals=[xx[i] for i in ix];new=rng.permutation(vals);assert sorted(vals)==sorted(new)
     for i,c in zip(ix,new):xx[i]=str(c)
   perm=[dict(row,x=xx[i]) for i,row in enumerate(rows)];n=slow_predict(perm)
   assert abs(n['joint_gain']-rd(ROOT/'results'/f'{name}_null_draws.json')[0])<1e-11
   assert abs(n['pooled_gain']-rd(ROOT/'results'/f'{name}_pooled_null_draws.json')[0])<1e-11
   r['first_permutation_independent']='PASS'
  results.append(r);print(name,'verified',r['positions_models_verified'],flush=True)
 for name in ['Toy_dependent','Toy_independent']:
  r=next(r for r in results if r['case']==name);assert abs(r['joint_gain'])<1e-13
 dep=rd(ROOT/'results/Toy_dependent_pooled_summary.json');ind=rd(ROOT/'results/Toy_independent_pooled_summary.json')
 assert dep['primary']['neighbor_accuracy']==1 and dep['primary']['gain_bits']>1.9
 assert abs(ind['primary']['gain_bits'])<.01
 out={'status':'PASS','total_positions_models_verified':sum(r['positions_models_verified'] for r in results),'max_probability_or_gain_error':max(r['max_abs_error'] for r in results),'all_test_leaves_disjoint_from_training':True,'independent_null_draws':4,'cases':results,'scope':'Primary raw alpha32 models only fully recomputed. Sensitivity models use the tested vector implementation. Manual metadata and linguistic interpretation are not validated by arithmetic checks.'}
 write(ROOT/'results/verification.json',out);print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
