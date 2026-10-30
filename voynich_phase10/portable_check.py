#!/usr/bin/env python3
"""Recompile and rerun every optimizer in a new extracted copy, without caches."""
import datetime,hashlib,json,subprocess,sys,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent;dest=P/'tmp/portable'
assert not dest.exists(),'Use a new destination; do not overwrite an old audit.'
dest.mkdir();archive=P/'output/Voynich_phase10_reproduction_2026-10-28.zip'
with zipfile.ZipFile(archive) as z:
 manifest=json.loads(z.read('SHA256SUMS.json'))
 for n,h in manifest.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
 z.extractall(dest)
copy=dest/'voynich_phase10';(copy/'tmp').mkdir(exist_ok=True)
removed=0
for p in (copy/'results').glob('*.json'):
 x=json.loads(p.read_text())
 if isinstance(x,dict) and 'key_mapping' in x:
  p.unlink();removed+=1
assert removed==200
commands=[]
for name in ['homophonic','context_boundary','context_permutation']:
 commands.append(['g++','-O3','-std=c++17',str(copy/'src'/f'{name}.cpp'),'-o',str(copy/'tmp'/name)])
commands.append([sys.executable,str(copy/'prepare_boundary_lm.py')])
for flag in ['--controls','--boundary-controls','--permutation-controls','--permutation-real']:
 commands.append([sys.executable,str(copy/'run.py'),flag])
for name in ['diagnose.py','verify.py','summarize.py']:commands.append([sys.executable,str(copy/name)])
with open(P/'tmp/portable.log','w') as f:
 for cmd in commands:
  print('RUN',Path(cmd[1]).name if cmd[0]==sys.executable else cmd[0],cmd[-1] if cmd[-1].startswith('--') else '',flush=True)
  subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,cwd=dest)
same=0;maxerr=0.
for p in (P/'results').glob('*.json'):
 x=json.loads(p.read_text())
 if isinstance(x,dict) and 'key_mapping' in x:
  y=json.loads((copy/'results'/p.name).read_text())
  for k in ['key','test_decoded_NOT_TRANSLATION']:assert x[k]==y[k],(p.name,k)
  err=abs(x['training_objective']-y['training_objective']);assert err<1e-7;maxerr=max(maxerr,err);same+=1
for name in ['controls_summary','controls_boundary_summary','controls_permutation_summary','real_permutation_summary','report_summary']:
 assert json.loads((P/'results'/f'{name}.json').read_text())==json.loads((copy/'results'/f'{name}.json').read_text()),name
result={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_hashes_checked':len(manifest),'cached_model_results_removed':removed,'fresh_optimizations':same,'same_keys_and_all_decoded_texts':True,'max_objective_difference':maxerr,'five_aggregate_result_files_identical':True,'verification':json.loads((copy/'results/verification.json').read_text()),'scope':'Fresh extraction and recompilation in same environment; not external independent replication. Final archive adds this audit record.'}
(P/'results/portable_reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
