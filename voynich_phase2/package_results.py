#!/usr/bin/env python3
"""Bundle both phases without caches, render previews, or nested archives."""
from pathlib import Path
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
DEST=ROOT/'output/Voynich_dossier_complet_2026-10-28.zip'

def main():
    files=[]
    for directory in (BASE/'voynich_20261028',ROOT):
        for p in sorted(directory.rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(directory)
            if {'__pycache__','tmp'}.intersection(rel.parts):continue
            if p.suffix in {'.zip','.pyc'}:continue
            if p==ROOT/'src/solve':continue
            files.append(p)
    manifest={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,str(p.relative_to(BASE)))
        z.writestr('SHA256_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(DEST) as z:
        assert z.testzip() is None
        check=json.loads(z.read('SHA256_MANIFEST.json'))
        assert set(z.namelist())==set(check)|{'SHA256_MANIFEST.json'}
        for name,digest in check.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
    print(json.dumps({'archive':str(DEST),'files':len(files),'bytes':DEST.stat().st_size,'hash_checks':'PASS'},indent=2))

if __name__=='__main__':main()
