#!/usr/bin/env python3
"""Fetch source JPEGs named by the official Yale IIIF manifest. No resynthesis."""
import concurrent.futures, hashlib, io, json, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
IDS=['1006076','1006078','1006167','1006196','1006200','1006201','1006208',
     '1006234','1006235','1006238','1006248','1006249','1006254','1006273']

def main():
    manifest=json.loads((ROOT/'data/yale_manifest.json').read_text())
    canvases={c['id'].split('/')[-1]:c for c in manifest['items']}
    def fetch(oid):
        c=canvases[oid];body=c['items'][0]['items'][0]['body'];url=body['id']
        path=ROOT/'images'/(oid+'.jpg')
        for trial in range(3):
            try:
                if path.exists():data=path.read_bytes()
                else:
                    req=urllib.request.Request(url,headers={'User-Agent':'Voynich-study/1.0'})
                    with urllib.request.urlopen(req,timeout=40) as response:data=response.read()
                with Image.open(io.BytesIO(data)) as im:
                    im.load();size=im.size
                assert size==(body['width'],body['height']),(oid,size)
                path.write_bytes(data)
                result={'oid':oid,'canvas':c['id'],'label':sum(c['label'].values(),[])[0],
                    'url':url,'width':size[0],'height':size[1], 'bytes':len(data),
                    'sha256':hashlib.sha256(data).hexdigest(),'file':str(path.relative_to(ROOT))}
                print(json.dumps(result),flush=True);return result
            except Exception as e:
                if trial==2:raise
                print(json.dumps({'retry':oid,'error':str(e)[:120]}),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=list(ex.map(fetch,IDS))
    (ROOT/'data/image_sources.json').write_text(json.dumps(results,indent=2)+'\n')
    print('ALL SOURCE IMAGES VERIFIED',flush=True)

if __name__=='__main__':main()
