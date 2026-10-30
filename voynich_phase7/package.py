#!/usr/bin/env python3
import hashlib,json,platform,sys,zipfile
from pathlib import Path
import numpy,sklearn,matplotlib,reportlab
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
def main():
 (ROOT/'ENVIRONMENT.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'sklearn':sklearn.__version__,'matplotlib':matplotlib.__version__,'reportlab':reportlab.Version},indent=2)+'\n')
 files=[p for p in ROOT.rglob('*') if p.is_file() and not {'tmp','__pycache__'}.intersection(p.relative_to(ROOT).parts) and p.suffix not in {'.zip','.pyc'} and p.name!='bpe']
 deps={'voynich_20261028':['analyse.py','PROTOCOL.json','SOURCES.json','data/ZL3b-n.txt','data/IT2a-n.txt','data/000_README.txt','data/IVTFF_format.txt','controls/LICENSE_GRESHKO'],'voynich_phase6':['data/adjacency_inputs.json','data/LICENSE_TIMM.txt','SOURCES.json','README.txt'],'voynich_phase2':['SOURCES_AND_LIMITS.json']}
 for folder,names in deps.items():files.extend(BASE/folder/n for n in names)
 files=sorted(set(files));assert all(p.is_file() for p in files);manifest={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 target=ROOT/'output/Voynich_phase7_reproduction_2026-10-28.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:z.write(p,str(p.relative_to(BASE)))
  z.writestr('SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None;assert set(z.namelist())==set(manifest)|{'SHA256_MANIFEST.json'}
  for name,sha in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==sha
 print(json.dumps({'status':'PASS','files':len(files),'bytes':target.stat().st_size,'archive':str(target)},indent=2))
if __name__=='__main__':main()
