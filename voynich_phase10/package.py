#!/usr/bin/env python3
import hashlib,json,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent;out=P/'output/Voynich_phase10_reproduction_2026-10-28.zip'
files=sorted(p for p in P.rglob('*') if p.is_file() and 'tmp' not in p.relative_to(P).parts and '__pycache__' not in p.parts and p.suffix not in ['.zip','.pyc'])
manifest={p.relative_to(P.parent).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(P.parent).as_posix())
 z.writestr('SHA256SUMS.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for n,h in manifest.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'files':len(files)+1,'manifest':'PASS','sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
