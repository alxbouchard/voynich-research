from pathlib import Path
import json,hashlib,zipfile,tempfile,subprocess,sys,platform
import PIL,reportlab
R=Path(__file__).resolve().parent.parent
Z=R/'output/Voynich_phase16_dossier_reproductible.zip'

sources={
 'consulted_on':'2026-10-29',
 'transliterations':{'ZL3b-n.txt':'Zandbergen-Landini v3b 2025-05-13; copied byte-for-byte from phase15',
                    'IT2a-n.txt':'Takahashi IT2a, 2023-02-02, modified 2025-06-25; copied byte-for-byte from phase15',
                    'landing_page':'https://www.voynich.nu/transcr.html'},
 'f104r_Yale.jpg':'https://collections.library.yale.edu/iiif/2/1006256/full/full/0/default.jpg',
 'drive_images':json.loads((R/'data/drive_sources.json').read_text()),
 'published_figures':{n:'https://manuscriptroadtrip.wordpress.com/wp-content/uploads/2024/09/'+n for n in ['screenshot-696.png','screenshot-691.png']},
 'glyph_references':{p.name:'https://voynich.nu/img/eva/'+p.stem[4:]+'.gif' for p in sorted((R/'data').glob('eva_*.gif'))},
 'primary_readings':[
 'https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/',
 'https://www.voynich.ninja/printthread.php?page=7&tid=437',
 'https://voynich.ninja/printthread.php?tid=2017',
 'https://herculeaf.wordpress.com/2023/08/28/f116v-most-likely-readings-based-on-glyph-shapes/'],
 'image_status':'Only crops listed in results/image_audit.json enter archive. No generative image alteration.'}
for row in sources['drive_images']:row['path']='data/'+Path(row['path']).name
(R/'SOURCE_MANIFEST.json').write_text(json.dumps(sources,indent=2)+'\n')
(R/'ENVIRONMENT.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform(),Pillow=PIL.__version__,reportlab=reportlab.Version),indent=2)+'\n')

def files():
 fs=[R/n for n in ['README.txt','PROTOCOL.json','ADDENDUM.txt','SOURCE_MANIFEST.json','ENVIRONMENT.json']]
 for folder in ['src','data','results']:
  fs.extend(p for p in (R/folder).glob('*') if p.is_file())
 fs.extend(R/a['crop'] for a in json.loads((R/'results/image_audit.json').read_text()))
 fs.append(R/'output/Voynich_phase16_points_appui_historiques.pdf')
 return sorted(set(fs))
def package():
 fs=files();manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in fs}
 (R/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n');fs.append(R/'SHA256SUMS.json')
 with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in fs:z.write(p,'voynich_phase16/'+str(p.relative_to(R)))
 with zipfile.ZipFile(Z) as z:assert z.testzip() is None
 return fs

package()
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='portable_') as t:
 with zipfile.ZipFile(Z) as z:z.extractall(t)
 q=Path(t)/'voynich_phase16'
 saved={n:(q/'results'/n).read_bytes() for n in ['analysis.json','summary.json','image_audit.json','verification.json']}
 for n in ['analyse.py','audit_images.py','verify.py']:
  subprocess.run([sys.executable,str(q/'src'/n)],cwd=q,check=True,stdout=subprocess.DEVNULL)
 for n,b in saved.items():assert (q/'results'/n).read_bytes()==b,n
 result=dict(status='passed',fresh_zip_extraction=True,recomputed_identical=list(saved),archive_integrity='passed',
             scope='Analysis and crop regeneration; PDF rendering inspected separately.')
 (R/'results/portable_verification.json').write_text(json.dumps(result,indent=2)+'\n')
fs=package();print(json.dumps(dict(zip=str(Z),size=Z.stat().st_size,members=len(fs),verification=result),indent=2))
