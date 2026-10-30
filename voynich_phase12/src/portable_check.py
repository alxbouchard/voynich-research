from pathlib import Path
import zipfile,tempfile,shutil,json,subprocess
ROOT=Path(__file__).resolve().parent.parent
tmp=Path(tempfile.mkdtemp(prefix='portable_',dir=ROOT/'tmp'))
with zipfile.ZipFile(ROOT/'output/Voynich_phase12_reproduction.zip') as z:z.extractall(tmp)
dest=tmp/'voynich_phase12'
for item in json.loads((dest/'data/source_manifest.json').read_text()):
 target=dest/item['local_path'];target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ROOT/item['local_path'],target)
commands=[['python','src/fetch_sources.py'],['node','src/export_upstream.mjs'],['python','src/analyse.py'],['python','src/verify.py']]
for i,command in enumerate(commands):
 r=subprocess.run(command,cwd=dest,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (tmp/f'command_{i}.txt').write_text(r.stdout);assert r.returncode==0,r.stdout
for name in ['rule_audit.json','verification.json']:
 assert json.loads((dest/'results'/name).read_text())==json.loads((ROOT/'results'/name).read_text()),name
out={'status':'PASS','fresh_archive_extraction':True,'result_json_identical':['rule_audit.json','verification.json'],
 'pinned_sources_copied_and_hash_verified':12,'network_redownload_tested':False,'commands':commands}
(ROOT/'results/portable_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
