from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]
v=json.loads((ROOT/'results/reproduction_verification.json').read_text())
assert v['portable_computation']=='passed' and len(v['pixel_identical_figures'])==34
files=[ROOT/name for name in ['README.txt','PROTOCOL.json','ADDENDUM.txt','SOURCE_MANIFEST.json','ENVIRONMENT.json']]
for folder,pattern in [('src','*.py'),('data','*'),('results','*.json'),('figures','*.png')]:
    files.extend(p for p in (ROOT/folder).glob(pattern) if p.is_file() and not p.name.startswith('.'))
files.append(ROOT/'output/Voynich_phase17_spectral_et_cryptanalyse.pdf')
checks={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(ROOT/'SHA256SUMS.json').write_text(json.dumps(checks,indent=2))
files.append(ROOT/'SHA256SUMS.json')
dest=ROOT/'output/Voynich_phase17_reproduction.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as z:
    for p in sorted(files):z.write(p,'Voynich_phase17/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for name,h in checks.items():assert hashlib.sha256(z.read('Voynich_phase17/'+name)).hexdigest()==h,name
print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'members':len(files),'crc':'passed','sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
