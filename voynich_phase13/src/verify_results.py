import hashlib,json,random,sys
from pathlib import Path
import numpy as np
from engine import ROOT,Problem,distance_matrix
def main():
 cases=json.loads((ROOT/'data/cases.json').read_text())+json.loads((ROOT/'data/default_cases.json').read_text())+[json.loads((ROOT/'data/polyphonic_control.json').read_text())]
 byname={c['name']:c for c in cases};checks=[]
 for file in sorted((ROOT/'results').glob('*_s*_k*.json')):
  d=json.loads(file.read_text());name=d['name'];isnull=d['null'];base=name[:-5] if isnull else name
  c=json.loads(json.dumps(byname[base]))
  if isnull:
   rng=random.Random(7919);perm={}
   for w in sorted({w for g in c['source'] for w in g}|set(c['test'])):
    chars=list(w);rng.shuffle(chars);perm[w]=''.join(chars)
   c['source']=[[perm[w] for w in g] for g in c['source']];c['test']=[perm[w] for w in c['test']]
  p=Problem(c['source'],c['target'],c['N'],c['M'],alphabet=c.get('alphabet'))
  assert p.assignment(d['state'])==d['mapping']
  value=p.evaluate(d['state']);assert abs(value-d['energy'])<1e-8
  if c['kind']=='voynich':
   assert not set(c['train_leaf_ids'])&set(c['test_leaf_ids'])
   if not isnull:assert not set(c['test'])&{w for g in c['source'] for w in g}
  words=[w for w in c['test'] if set(w)<=set(p.lC)]
  if words:
   targets=[w for g in c['target'] for w in g]
   matrix=distance_matrix(words,targets,p.lC,p.kC,p.masks(d['state']))
   assert abs(matrix.min(axis=1).mean()-d['heldout_mean_distance'])<1e-12
   for i,r in enumerate(d['heldout']):
    assert r['source']==words[i]
    assert abs(r['distance']-matrix[i].min())<1e-12
    assert r['candidates']==[targets[j] for j in np.flatnonzero(abs(matrix[i]-matrix[i].min())<1e-12)]
  checks.append({'file':file.name,'energy':value,'heldout_count':len(words)})
 # Confirm the primary source files and pre-run program versions were unchanged.
 pinned=json.loads((ROOT/'data/prerun_hashes.json').read_text())
 for entry in pinned:assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
 result={'result_files_verified':len(checks),'all_objectives_recomputed':True,'all_heldout_candidates_recomputed':True,
  'frozen_files_sha256_verified':len(pinned),'checks':checks}
 (ROOT/'results/results_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
if __name__=='__main__':main()
