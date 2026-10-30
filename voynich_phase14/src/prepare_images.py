import concurrent.futures,hashlib,io,json,shutil,urllib.request
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent;BASE=ROOT.parent
SELECTION=[('f1r','1006076'),('f1v','1006077'),('f2r','1006078'),('f57v','1006187'),('f67r2','1006194'),('f68r1','1006196'),('f70v2','1006200'),('f72r2','1006203'),('f73v','1006207'),('f75v','1006209'),('f78r','1006214'),('f82v','1006223'),('f88r','1037112'),('f89r1','1006233'),('f89r2','1006233'),('f99r','1006246'),('f99v','1006247'),('f100r','1006248'),('f102r2','1006251'),('f116v','1006277')]
def main():
 for d in ['data','images','results','tmp','output']:(ROOT/d).mkdir(parents=True,exist_ok=True)
 manifest_path=ROOT/'data/yale_manifest.json'
 if not manifest_path.exists():
  cache=BASE/'voynich_phase3/data/yale_manifest.json'
  if cache.exists():shutil.copy2(cache,manifest_path)
  else:
   with urllib.request.urlopen('https://collections.library.yale.edu/manifests/2002046',timeout=45) as response:manifest_path.write_bytes(response.read())
 manifest=json.loads(manifest_path.read_text());cs={c['id'].split('/')[-1]:c for c in manifest['items']}
 (ROOT/'data/yale_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False))
 (ROOT/'PROTOCOL.json').write_text(json.dumps({'date':'2026-10-29 America/Toronto','scope':'Image and repeated-label pilot; no semantic key assumed',
  'selected_folios':[f for f,o in SELECTION],'selection_reason':'purposive coverage of prose, herbs, circular diagrams, zodiac, bath diagrams, plant-fragment labels and marginalia; not a random representative sample',
  'transcriptions':['ZL3b-n','IT2a-n'],'candidate_rule':'single clean alphabetic labels of at least 3 EVA characters, exact agreement at the same locus between ZL and IT, repeated on at least two pages; sort by occurrence count then alphabetical; first 10',
  'independence_warning':'transcriptions share a physical source and can share conventions; their agreement is not ground truth',
  'label_prose_test':'plant-fragment and container labels versus prose on same pharmaceutical page, compared with 10000 permutations of whole label-page blocks; replicate in ZL and IT',
  'meaning_rule':'No meanings inferred from diagram identity alone. Observed categories are spatial relations, not translations.',
  'images':'Exact crops only. No synthetic restoration. Coordinates in full-resolution Yale canvas pixels.',
  'new_software_scope':'No full TranscriptTool installation, no joint phonetic decoder in this phase.'},ensure_ascii=False,indent=2))
 for f in ['ZL3b-n.txt','IT2a-n.txt','IVTFF_format.txt']:
  if not (ROOT/'data'/f).exists():shutil.copy2(BASE/'voynich_phase8/data'/f,ROOT/'data'/f)
 def fetch(oid):
  c=cs[oid];body=c['items'][0]['items'][0]['body'];url=body['id'];p=ROOT/'images'/f'{oid}.jpg';cache=BASE/'voynich_phase3/images'/p.name
  if p.exists():b=p.read_bytes()
  elif cache.exists():b=cache.read_bytes()
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Voynich-research/1.0'}),timeout=45) as r:b=r.read()
  with Image.open(io.BytesIO(b)) as im:im.load();size=im.size
  assert size==(body['width'],body['height']);p.write_bytes(b)
  out={'oid':oid,'folios':[f for f,o in SELECTION if o==oid],'yale_label':sum(c['label'].values(),[])[0],'url':url,'canvas':c['id'],'width':size[0],'height':size[1],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'path':str(p.relative_to(ROOT))}
  print(json.dumps({'downloaded':oid,'folios':out['folios'],'size':size}),flush=True);return out
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetch,dict.fromkeys(o for f,o in SELECTION)))
 (ROOT/'data/image_sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
 for k in range(0,len(rows),4):
  sheet=Image.new('RGB',(1600,1900),'#ececec');draw=ImageDraw.Draw(sheet)
  for j,row in enumerate(rows[k:k+4]):
   im=Image.open(ROOT/row['path']);im.thumbnail((780,880));x=(j%2)*800+10;y=(j//2)*950+45;sheet.paste(im,(x,y));draw.text((x,y-32),', '.join(row['folios'])+' / '+row['oid'],fill='black',font=font)
  sheet.save(ROOT/'tmp'/f'contact_{k//4+1:02}.jpg',quality=92)
 print('SOURCES',len(rows),'FOLIOS',len(SELECTION),flush=True)
if __name__=='__main__':main()
