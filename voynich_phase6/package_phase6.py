#!/usr/bin/env python3
import hashlib,json,platform,subprocess,sys,zipfile
from pathlib import Path
import numpy,matplotlib,reportlab
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
def main():
    env={'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'matplotlib':matplotlib.__version__,'reportlab':reportlab.Version,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]}
    (ROOT/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
    files=[]
    for folder in [ROOT,BASE/'voynich_phase5']:
        for p in sorted(folder.rglob('*')):
            rel=p.relative_to(folder)
            if not p.is_file() or {'tmp','__pycache__'}.intersection(rel.parts) or p.suffix in {'.zip','.pyc','.bin'} or p.name in {'constrained','constrained_warm','syllabic'}:continue
            if folder.name=='voynich_phase5' and 'output' in rel.parts:continue
            files.append(p)
    dependencies={
      'voynich_20261028':['analyse.py','PROTOCOL.json','SOURCES.json','data/ZL3b-n.txt','data/IT2a-n.txt','data/000_README.txt','data/IVTFF_format.pdf','data/IVTFF_format.txt','controls/input/nathist_book16.txt','controls/generated/naibbe_ciphertext.txt','controls/LICENSE_GRESHKO'],
      'voynich_phase2':['data/caesar.xml','data/dante.txt','data/latin_train.txt','prepare_sources.py','SOURCES_AND_LIMITS.json'],
      'voynich_phase3':['results/anchor_robustness.json','results/pilot_summary.json'],
      'voynich_phase4':['run_homophonic.py','PROTOCOL.json','SOURCES.json','data/latin_train.txt','data/italian_train.txt','data/latin_target.txt','data/italian_target.txt']}
    for folder,names in dependencies.items():files.extend(BASE/folder/name for name in names)
    files=sorted(set(files));assert all(p.is_file() for p in files)
    hashes={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    target=ROOT/'output/Voynich_phase6_reproduction_2026-10-28.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,str(p.relative_to(BASE)))
        z.writestr('SHA256_MANIFEST.json',json.dumps(hashes,indent=2)+'\n')
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        manifest=json.loads(z.read('SHA256_MANIFEST.json'));assert set(z.namelist())==set(manifest)|{'SHA256_MANIFEST.json'}
        for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
    print(json.dumps({'archive':str(target),'files':len(files),'bytes':target.stat().st_size,'verification':'PASS'},indent=2))
if __name__=='__main__':main()
