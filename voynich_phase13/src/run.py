import argparse,json,math,random,time
import numpy as np
from engine import ROOT,Problem,anneal,distance_matrix
def run(case,seed,steps,annealers,null=False):
 case=json.loads(json.dumps(case));name=case['name']
 if null:
  rng=random.Random(7919);permuted={}
  for w in sorted({w for g in case['source'] for w in g}|set(case['test'])):
   chars=list(w);rng.shuffle(chars);permuted[w]=''.join(chars)
  case['source']=[[permuted[w] for w in g] for g in case['source']];case['test']=[permuted[w] for w in case['test']]
  name+='_null'
 p=Problem(case['source'],case['target'],case['N'],case['M'],alphabet=case.get('alphabet'))
 print(json.dumps({'start':name,'seed':seed,'steps':steps,'source_symbols':p.llC,'target_symbols':p.lkC}),flush=True)
 result=anneal(p,seed,steps,annealers,lambda point:print(json.dumps({'case':name,**point}),flush=True))
 result.update(name=name,kind=case['kind'],null=null,N=p.N,M=p.M,source_types=len(case['source']),target_types=len(case['target']))
 words=[w for w in case['test'] if set(w)<=set(p.lC)]
 result['test_total_types']=len(case['test']);result['test_scored_types']=len(words)
 if words:
  target=[w for g in case['target'] for w in g]
  matrix=distance_matrix(words,target,p.lC,p.kC,p.masks(result['state']))
  best=matrix.min(axis=1);result['heldout_mean_distance']=float(best.mean());result['heldout_exact_fraction']=float(np.mean(best==0))
  result['heldout']=[{'source':w,'distance':float(best[i]),'candidates':[target[j] for j in np.flatnonzero(abs(matrix[i]-best[i])<1e-12)]} for i,w in enumerate(words)]
  if case.get('truth'):
   correct=sum(case['truth'][w] in r['candidates'] and len(r['candidates'])==1 for w,r in zip(words,result['heldout']))
   result['heldout_unique_correct']=correct;result['heldout_accuracy']=correct/len(words)
 if case.get('gold_pairs'):
  found=0
  for aa,bb in case['gold_pairs']:
   if any(set(m['source'])&set(aa) and set(m['target'])&set(bb) for m in result['matches']):found+=1
  result['benchmark_cognate_correct']=found;result['benchmark_cognate_total']=len(case['gold_pairs']);result['benchmark_accuracy']=found/len(case['gold_pairs'])
 path=ROOT/'results'/f'{name}_s{seed}_k{steps}.json';path.write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({'complete':name,'path':str(path),'energy':result['energy'],'seconds':result['seconds'],
  'heldout_accuracy':result.get('heldout_accuracy'),'benchmark_accuracy':result.get('benchmark_accuracy'),'heldout_mean_distance':result.get('heldout_mean_distance')}),flush=True)
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('--steps',type=int,default=5000);ap.add_argument('--seed',type=int,default=13010);ap.add_argument('--annealers',type=int,default=8);ap.add_argument('--null',action='store_true');a=ap.parse_args()
 cases=json.loads((ROOT/'data/cases.json').read_text());case=next(c for c in cases if c['name']==a.name)
 run(case,a.seed,a.steps,a.annealers,a.null)
