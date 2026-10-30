"""Package, re-run in isolation, compare full null results, then seal final ZIP."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,zipfile
import numpy,reportlab,threadpoolctl
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def collect():
 files=[ROOT/f for f in ['PROTOCOL.json','ADDENDUM.txt','README.txt','SOURCE_MANIFEST.json','ENVIRONMENT.json']]
 for folder in ['src','data','results']:
  files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
 files.append(ROOT/'output/Voynich_phase15_variantes_et_prediction.pdf')
 return sorted(files)
def pack(out):
 files=collect();hashes={str(p.relative_to(ROOT)):sha(p) for p in files}
 (ROOT/'SHA256SUMS.json').write_text(json.dumps(hashes,indent=2))
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for p in files+[ROOT/'SHA256SUMS.json']:z.write(p,'voynich_phase15/'+str(p.relative_to(ROOT)))
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for path,h in hashes.items():assert hashlib.sha256(z.read('voynich_phase15/'+path)).hexdigest()==h
 return len(hashes)
def comparable(x):
 if isinstance(x,dict):return {k:comparable(v) for k,v in x.items() if k!='elapsed_seconds'}
 if isinstance(x,list):return [comparable(v) for v in x]
 return x
def main():
 pdf=ROOT/'output/Voynich_phase15_variantes_et_prediction.pdf'
 assert len(PdfReader(pdf).pages)==3
 (ROOT/'ENVIRONMENT.json').write_text(json.dumps(dict(python=sys.version,numpy=numpy.__version__,reportlab=reportlab.Version,threadpoolctl=threadpoolctl.__version__),indent=2))
 (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(dict(date='2026-10-29',transcription_source='https://voynich.nu/transcr.html',inherited_from='Phase 14 data, same frozen file bytes',files={p.name:sha(p) for p in sorted((ROOT/'data').iterdir()) if p.is_file()},prior_report_library_id='libfile_91cef371f8e4819181d0b68129c273b5'),indent=2))
 out=ROOT/'output/Voynich_phase15_dossier_reproductible.zip';pack(out)
 with tempfile.TemporaryDirectory(prefix='voynich15_portable_') as td:
  with zipfile.ZipFile(out) as z:z.extractall(td)
  fresh=Path(td)/'voynich_phase15'
  # Remove old result files so each comparison truly relies on fresh output.
  for p in (fresh/'results').glob('*.json'):p.unlink()
  for script in ['controls.py','experiment.py','verify.py']:
   subprocess.run([sys.executable,str(fresh/'src'/script)],cwd=fresh,check=True)
  checked=[]
  for name in ['ZL_strict.json','ZL_lattice.json','IT_strict.json','IT_lattice.json','summary.json','controls.json','verification.json','q_prefix_descriptive.json']:
   original=comparable(json.loads((ROOT/'results'/name).read_text()))
   new=comparable(json.loads((fresh/'results'/name).read_text()))
   assert original==new,name
   checked.append(name)
 result=dict(fresh_extraction=True,full_experiment_reproduced=True,files_compared=checked,
             null_permutations_per_condition=720,conditions=4,null_fold_fits=17280,
             comparison='all JSON content identical except elapsed_seconds',pdf_pages=3)
 (ROOT/'results/portable_verification.json').write_text(json.dumps(result,indent=2))
 n=pack(out)
 print(json.dumps(dict(status='verified',archive_bytes=out.stat().st_size,files_hashed=n,**result),indent=2))

if __name__=='__main__':main()
