"""Unpack the deliverable, compile independently, and check saved measurements."""
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def main():
 with tempfile.TemporaryDirectory(prefix='portable_',dir=ROOT/'tmp') as tmp:
  with zipfile.ZipFile(ROOT/'output/Voynich_phase13_reproduction.zip') as z:z.extractall(tmp)
  root=Path(tmp)/'voynich_phase13';manifest=json.loads((root/'MANIFEST.json').read_text())
  for d in manifest:assert hashlib.sha256((root/d['path']).read_bytes()).hexdigest()==d['sha256'],d['path']
  env={**os.environ,'OPENBLAS_NUM_THREADS':'1'};outputs=[]
  for script in ['build.py','verify_engine.py','verify_results.py']:
   r=subprocess.run([sys.executable,str(root/'src'/script)],env=env,check=True,capture_output=True,text=True)
   outputs.append({'script':script,'output':r.stdout.strip()})
  original=json.loads((root/'results/control_mono_s13010_k100.json').read_text())
  subprocess.run([sys.executable,str(root/'src/run.py'),'control_mono','--steps','100','--annealers','8'],env=env,check=True,capture_output=True)
  reproduced=json.loads((root/'results/control_mono_s13010_k100.json').read_text())
  for k in ['state','mapping','energy','heldout','heldout_accuracy']:assert original[k]==reproduced[k],k
  result={'archive_files_hash_verified':len(manifest),'fresh_compilation':True,'checks':outputs,'fixed_seed_100_step_control_exactly_reproduced':True}
  (ROOT/'results/portable_verification.json').write_text(json.dumps(result,indent=2))
  print(json.dumps(result))
if __name__=='__main__':main()
