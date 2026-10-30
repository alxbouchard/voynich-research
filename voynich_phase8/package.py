#!/usr/bin/env python3
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
out=ROOT/'output/Voynich_phase8_reproduction_2026-10-28.zip'
files=[p for p in ROOT.rglob('*') if p.is_file() and 'tmp' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts and p.suffix not in ['.zip','.pyc']]
files.sort()
manifest={p.relative_to(BASE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(BASE).as_posix())
 z.writestr('SHA256SUMS.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for name,h in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
print(json.dumps({'archive':str(out),'bytes':out.stat().st_size,'files':len(files)+1,'manifest_verified':True,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
