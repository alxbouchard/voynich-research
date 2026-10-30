from pathlib import Path
import zipfile,json,hashlib,platform,subprocess
ROOT=Path(__file__).resolve().parent.parent
runtime={'python':platform.python_version(),'node':subprocess.check_output(['node','--version'],text=True).strip()}
(ROOT/'data/runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
paths=[ROOT/'LISEZ_MOI.txt',ROOT/'protocol.txt',ROOT/'protocol_addendum_01.txt']
paths+=sorted((ROOT/'src').glob('*.py'))+sorted((ROOT/'src').glob('*.mjs'))
paths+=sorted((ROOT/'data').glob('*.json'))+sorted((ROOT/'results').glob('*.json'))
paths+=[ROOT/'output/pdf/Voynich_phase11_audit_des_decodeurs.pdf']
out=ROOT/'output/Voynich_phase11_reproduction.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in paths:z.write(p,'voynich_phase11/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps({'file':str(out),'files':len(paths),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
