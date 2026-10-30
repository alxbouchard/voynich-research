"""A second fixed random seed tests key stability, without heldout tuning."""
import concurrent.futures,json,os,time
from engine import ROOT
from run import run
def worker(case):
 path=ROOT/'tmp'/f"{case['name']}_seed13011.log"
 with path.open('w') as f:
  os.dup2(f.fileno(),1);os.dup2(f.fileno(),2)
  d=run(case,13011,5000,8)
 return {'case':case['name'],'energy':d['energy']}
if __name__=='__main__':
 cases=[c for c in json.loads((ROOT/'data/default_cases.json').read_text()) if c['kind']=='voynich']
 (ROOT/'data/repeat_protocol.json').write_text(json.dumps({'seed':13011,'steps':5000,'annealers':8,'cases':[c['name'] for c in cases],
  'selection':'all eight default Voynich cases; not selected by score','evaluation':'key Jaccard and heldout distance stability'},indent=2))
 results=[];start=time.time()
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
  for f in concurrent.futures.as_completed([pool.submit(worker,c) for c in cases]):
   r=f.result();results.append(r);print(json.dumps({'finished':len(results),'total':len(cases),'elapsed':time.time()-start,**r}),flush=True)
 (ROOT/'results/batch_repeats.json').write_text(json.dumps(results,indent=2))
