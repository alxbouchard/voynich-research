#!/usr/bin/env python3
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
def main():
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or {'tmp','__pycache__'}.intersection(p.relative_to(ROOT).parts) or p.suffix in {'.zip','.pyc','.bin'} or p.name=='homophonic':continue
  files.append(p)
 for name in ['analyse.py','PROTOCOL.json','SOURCES.json','data/ZL3b-n.txt','data/IT2a-n.txt','data/000_README.txt','data/IVTFF_format.pdf','data/IVTFF_format.txt','controls/input/nathist_book16.txt','controls/LICENSE_GRESHKO']:
  files.append(BASE/'voynich_20261028'/name)
 for name in ['data/caesar.xml','data/dante.txt','data/latin_train.txt','prepare_sources.py','SOURCES_AND_LIMITS.json']:
  files.append(BASE/'voynich_phase2'/name)
 for name in ['results/anchor_robustness.json','results/aligned_loci.json','results/image_annotations.json','results/pilot_summary.json']:
  files.append(BASE/'voynich_phase3'/name)
 hashes={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 target=ROOT/'output/Voynich_phase4_sources_2026-10-28.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:z.write(p,str(p.relative_to(BASE)))
  z.writestr('SHA256_MANIFEST.json',json.dumps(hashes,indent=2)+'\n')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  manifest=json.loads(z.read('SHA256_MANIFEST.json'));assert set(z.namelist())==set(manifest)|{'SHA256_MANIFEST.json'}
  for name,sha in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==sha
 print(json.dumps({'archive':str(target),'files':len(files),'bytes':target.stat().st_size,'verification':'PASS'},indent=2))
if __name__=='__main__':main()
