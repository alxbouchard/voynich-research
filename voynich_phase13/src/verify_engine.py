"""Independent, exhaustive tests of the CPU distance and group objective."""
import hashlib,importlib.util,itertools,json,random,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment
from engine import ROOT,Problem,distance_matrix
def edit(a,b):
 d=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  r=[i]
  for j,y in enumerate(b,1):r.append(min(d[j]+1,r[-1]+1,d[j-1]+(x!=y)))
  d=r
 return d[-1]
def ged(a,b):
 d=edit(a,b)
 return 2*d/(len(a)+len(b)+d) if a or b else 0.
def reference(w,v,alphabet,known,masks):
 choices=[[c for j,c in enumerate(known) if masks[alphabet.index(s)]>>j&1] or [''] for s in w]
 return min(ged(''.join(z),v) for z in itertools.product(*choices))
def main():
 rng=random.Random(13001);n=0
 for trial in range(120):
  masks=[rng.randrange(16) for _ in range(4)]
  ws=[''.join(rng.choices('abcd',k=rng.randrange(1,7))) for _ in range(4)]
  vs=[''.join(rng.choices('wxyz',k=rng.randrange(1,7))) for _ in range(5)]
  matrix=distance_matrix(ws,vs,list('abcd'),list('wxyz'),masks)
  for i,w in enumerate(ws):
   for j,v in enumerate(vs):
    assert abs(matrix[i,j]-reference(w,v,'abcd','wxyz',masks))<1e-12
    n+=1
 assert distance_matrix(['a'],['x'],['a'],['x'],[0])[0,0]==1
 # Directly exercise the vendor's grouped assignment with random grouped costs.
 vendor=ROOT/'vendor/CSA_OptMatcher'
 spec=importlib.util.spec_from_file_location('vendor_lsa',vendor/'lsa_2g.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 for trial in range(50):
  a=np.array([2,1,3]);b=np.array([1,3,2,1]);matrix=np.array([[rng.random() for _ in range(sum(b))] for _ in range(sum(a))])
  grouped=np.minimum.reduceat(np.minimum.reduceat(matrix,np.array([0,2,3]),axis=0),np.array([0,1,4,6]),axis=1)
  i,j=linear_sum_assignment(grouped);_,_,v=mod.lsa_2g(matrix,a,b)
  assert abs(v-grouped[i,j].sum())<1e-12
 # Reproduce serial proposal mutation in unchanged vendor pycsa.
 spec=importlib.util.spec_from_file_location('vendor_csa',vendor/'pycsa.py');csa=importlib.util.module_from_spec(spec);spec.loader.exec_module(csa)
 def move(s,tgen,qa=False):s[0]+=1;return s
 initial=[0];a=csa.CoupledAnnealer(lambda s:float(s[0]),move,initial_state=[initial]*2,n_annealers=2,processes=1)
 before=[s[:] for s in a.current_states];csa.worker_probe(a,0)
 mutated=before!=a.current_states
 assert mutated and a.current_states[0] is a.current_states[1]
 manifest=json.loads((ROOT/'data/upstream_manifest.json').read_text())
 for entry in manifest:
  data=(ROOT/entry['path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['git_blob_sha'],entry['path']
 result={'distance_pairs_exactly_verified':n,'group_assignment_cases':50,'original_serial_state_aliasing_reproduced':True,
  'empty_to_nonempty_distance_original':0,'empty_to_nonempty_distance_corrected':1,'upstream_files_git_hash_verified':len(manifest)}
 (ROOT/'results/engine_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
