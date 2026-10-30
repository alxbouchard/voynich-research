import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
from engine import ROOT
def worker(task):
 name,seed,steps,null=task
 path=ROOT/'tmp'/f'{name}_{seed}_{steps}_{null}.log'
 cmd=[sys.executable,str(ROOT/'src/run.py'),name,'--seed',str(seed),'--steps',str(steps),'--annealers','8']+(['--null'] if null else [])
 with path.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
 return {'task':task,'returncode':r.returncode,'log':str(path)}
if __name__=='__main__':
 cases=json.loads((ROOT/'data/cases.json').read_text());stage=sys.argv[1]
 if stage=='calibration':tasks=[(n,13010,5000,False) for n in ['control_null','control_homophonic','benchmark_Phoenician_Ugaritic']]
 else:tasks=[(c['name'],13010,5000,null) for c in cases if c['kind']=='voynich' for null in [False,True]]
 start=time.time();results=[]
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:
  for f in concurrent.futures.as_completed([ex.submit(worker,t) for t in tasks]):
   r=f.result();results.append(r);print(json.dumps({'finished':len(results),'total':len(tasks),'elapsed':time.time()-start,**r}),flush=True)
 (ROOT/'results'/f'batch_{stage}.json').write_text(json.dumps(results,indent=2))
 assert all(r['returncode']==0 for r in results)
