"""Download a connector-provided URL privately and verify image integrity."""
import sys, json, hashlib
from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image

payload=json.load(sys.stdin)
f=payload['file']
p=Path(payload['destination'])
p.parent.mkdir(parents=True,exist_ok=True)
if not p.exists() or p.stat().st_size!=int(f['size']):
    with urlopen(Request(payload['download_url']),timeout=180) as r,open(str(p)+'.part','wb') as out:
        while chunk:=r.read(1024*1024): out.write(chunk)
    Path(str(p)+'.part').replace(p)
assert p.stat().st_size==int(f['size']), 'Size mismatch'
record={k:f[k] for k in ['id','title','mime_type','size','url','group','folio'] if k in f}
record.update(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
if f['mime_type'].startswith('image/'):
    with Image.open(p) as im:
        im.load()
        record.update(width=im.width,height=im.height,mode=im.mode,format=im.format,exif_orientation=im.getexif().get(274,1))
        if im.format=='TIFF':
            record['bits_per_sample']=im.tag_v2.get(258)
            record['description']=im.tag_v2.get(270)
Path(str(p)+'.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({'title':f['title'],'bytes':p.stat().st_size,'verified':True}),flush=True)
