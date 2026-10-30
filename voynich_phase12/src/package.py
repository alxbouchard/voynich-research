import zipfile,hashlib,json,platform,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
(ROOT/'data/runtime.json').write_text(json.dumps({'python':platform.python_version(),'node':subprocess.check_output(['node','--version'],text=True).strip()},indent=2)+'\n')
paths=[ROOT/'LISEZ_MOI.txt',ROOT/'protocol.txt']
for folder,patterns in [('src',['*.py','*.mjs']),('data',['*.json']),('results',['*.json'])]:
 for pattern in patterns:paths+=sorted((ROOT/folder).glob(pattern))
paths+=[ROOT/'output/pdf/Voynich_phase12_regles_et_langue.pdf']
out=ROOT/'output/Voynich_phase12_reproduction.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in paths:z.write(p,'voynich_phase12/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps({'file':str(out),'files':len(paths),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
