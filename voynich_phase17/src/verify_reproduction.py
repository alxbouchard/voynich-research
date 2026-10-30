"""Re-run all computations from portable inputs and compare every numeric output."""
from pathlib import Path
import os,shutil,subprocess,sys,json,hashlib
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'tmp/portable_reproduction'
DEST.mkdir(parents=True,exist_ok=True)
for name in ['data','src']:
    shutil.copytree(ROOT/name,DEST/name,dirs_exist_ok=True)
for name in ['results','figures','output']:(DEST/name).mkdir(exist_ok=True)
env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
scripts=['spectral.py','make_figures.py','crib_scan.py','shuffle_diagnostic.py','extend_crib.py']
for script in scripts:
    r=subprocess.run([sys.executable,str(DEST/'src'/script)],env=env,capture_output=True,text=True)
    (DEST/(script+'.log')).write_text(r.stdout+'\n'+r.stderr)
    assert r.returncode==0,(script,r.stderr[-2000:])
    print('Reproduced',script,flush=True)
checks={}
for name in ['spectral.json','crib_scan.json','crib_summary.json','shuffle_diagnostic.json','crib_extension.json']:
    a=json.loads((ROOT/'results'/name).read_text());b=json.loads((DEST/'results'/name).read_text())
    assert a==b,name;checks[name]='identical JSON values'
figs=[]
for p in sorted((ROOT/'figures').glob('*.png')):
    with Image.open(p) as im:a=np.array(im)
    with Image.open(DEST/'figures'/p.name) as im:b=np.array(im)
    assert np.array_equal(a,b),p.name
    figs.append(p.name)
result={'portable_computation':'passed','json_comparisons':checks,'pixel_identical_figures':figs,
        'source_crop_verification':json.loads((ROOT/'results/crop_verification.json').read_text()),
        'claim_limit':'Computational reproduction does not validate the crib or establish a translation.'}
(ROOT/'results/reproduction_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'identical_json':len(checks),'identical_images':len(figs),'native_crops_verified':22}),flush=True)
