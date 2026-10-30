"""Paper's inventory-size defaults: N=2,M=1 when target inventory is larger.
The earlier N=2,M=2 runs are retained as exploratory flexibility checks.
Added before inspecting or selecting Voynich outputs. No heldout selection.
"""
import concurrent.futures,json,os,subprocess,sys,time
from engine import ROOT
from run import run
def worker(case,null):
 path=ROOT/'tmp'/f"{case['name']}_{null}.log"
 with path.open('w') as f:
  # File descriptor replacement also captures imported function progress.
  os.dup2(f.fileno(),1);os.dup2(f.fileno(),2)
  result=run(case,13010,5000,8,null)
 return {'case':case['name'],'null':null,'energy':result['energy']}
if __name__=='__main__':
 cases=json.loads((ROOT/'data/cases.json').read_text())
 cases=[c for c in cases if c['kind']=='voynich']+[json.loads((ROOT/'data/polyphonic_control.json').read_text())]
 for c in cases:c['M']=1;c['name']+='_DEFAULT'
 (ROOT/'data/default_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
 tasks=[(c,n) for c in cases for n in ([False,True] if c['kind']=='voynich' else [False])]
 results=[];start=time.time()
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
  for f in concurrent.futures.as_completed([pool.submit(worker,*t) for t in tasks]):
   r=f.result();results.append(r);print(json.dumps({'finished':len(results),'total':len(tasks),'elapsed':time.time()-start,**r}),flush=True)
 (ROOT/'results/batch_defaults.json').write_text(json.dumps(results,indent=2))
