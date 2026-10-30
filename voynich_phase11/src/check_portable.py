"""Rerun the delivered scripts in a clean extraction using verified pinned inputs."""
import json,subprocess,zipfile,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
tmp=Path(tempfile.mkdtemp(prefix='portable_',dir=ROOT/'tmp'))
archive=ROOT/'output/Voynich_phase11_reproduction.zip'
with zipfile.ZipFile(archive) as z:z.extractall(tmp)
dest=tmp/'voynich_phase11'
manifest=json.loads((dest/'data/source_manifest.json').read_text())
for f in manifest:
 target=dest/f['local_path'];target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ROOT/f['local_path'],target)
commands=[['python','src/fetch_sources.py'],['node','src/audit_scott.mjs'],['python','src/audit_zfd.py'],['python','src/verify_results.py']]
for i,command in enumerate(commands):
 result=subprocess.run(command,cwd=dest,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (tmp/f'command_{i}.txt').write_text(result.stdout)
 assert result.returncode==0,result.stdout
files=['scott_audit.json','zfd_v3_reproduction.json','zfd_v3_semantic.json','zfd_canonical_semantic.json','verification.json']
for f in files:assert json.loads((dest/'results'/f).read_text())==json.loads((ROOT/'results'/f).read_text()),f
report={'status':'PASS','fresh_archive_extraction':True,'source_files_verified':len(manifest),
 'numerical_result_files_identical':files,'commands':commands,
 'network_redownload_tested':False,'input_note':'Verified pinned source bytes copied from initial connector retrieval; no source modification.'}
(ROOT/'results/portable_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
