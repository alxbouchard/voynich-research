"""Download unmodified public Yale images, with a provenance and integrity index."""
import concurrent.futures as cf
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'yale'
DATA.mkdir(parents=True, exist_ok=True)

def download(url, path):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Voynich manuscript research; public facsimile download'}), timeout=90) as r, open(str(path)+'.part', 'wb') as w:
                while chunk := r.read(1024*1024):
                    w.write(chunk)
            Path(str(path)+'.part').replace(path)
            return
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2*(attempt+1))

download('https://collections.library.yale.edu/manifests/2002046', DATA/'yale_manifest.json')
manifest = json.loads((DATA/'yale_manifest.json').read_text())
rows=[]
for i, c in enumerate(manifest['items'],1):
    body=c['items'][0]['items'][0]['body']
    label='; '.join(next(iter(c['label'].values())))
    slug=re.sub(r'[^A-Za-z0-9_-]+','_',label).strip('_')
    rows.append({'order':i,'label':label,'url':body['id'],
        'path':f'yale/images/{i:03d}_{slug}.jpg',
        'expected_width':body['width'],'expected_height':body['height'],
        'original_tiff_url':next((r['id'] for r in c.get('rendering',[]) if r.get('format')=='image/tiff'),None)})
(DATA/'images').mkdir(exist_ok=True)

def one(row):
    p=ROOT/row['path']
    if not p.exists(): download(row['url'],p)
    with Image.open(p) as im:
        im.load()
        assert im.size==(row['expected_width'],row['expected_height']), (row['label'],im.size)
        row['width'],row['height']=im.size
    row['size_bytes']=p.stat().st_size
    row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    return row

results=[]
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    for f in cf.as_completed([pool.submit(one,r) for r in rows]):
        results.append(f.result())
        if len(results)%20==0 or len(results)==len(rows): print(f'Yale images validated: {len(results)}/{len(rows)}',flush=True)
results.sort(key=lambda r:r['order'])
(DATA/'image_index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
pdf=ROOT/'Voynich_Yale_facsimile_complet.pdf'
download(manifest['rendering'][0]['id'],pdf)
from pypdf import PdfReader
pdf_pages=len(PdfReader(pdf).pages)
summary={'images':len(results),'image_bytes':sum(r['size_bytes'] for r in results),
    'pdf_pages':pdf_pages,'pdf_bytes':pdf.stat().st_size,
    'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
    'source':'https://collections.library.yale.edu/catalog/2002046',
    'retrieved_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
(DATA/'download_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary),flush=True)
