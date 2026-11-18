from pathlib import Path
import json, random, hashlib
from urllib.request import urlopen
from PIL import Image, ImageDraw
import numpy as np
p=Path(__file__).resolve().parent
for folder in ('prive', 'originaux', 'aveugle'):
 (p/folder).mkdir(exist_ok=True)
manifest=p/'prive/manifest-vat.json'
if not manifest.exists():
 manifest.write_bytes(urlopen('https://digi.vatlib.it/iiif/MSS_Ross.379/manifest.json',timeout=40).read())
m=json.loads(manifest.read_text())
numbers=list(range(75,98,2))
random.Random(413693).shuffle(numbers)
key={}
for k,n in enumerate(numbers):
 c=m['sequences'][0]['canvases'][n-1]
 original=p/'originaux'/f'p{n:04}.jpg'
 url=c['images'][0]['resource']['service']['@id']+'/full/600,/0/default.jpg'
 if not original.exists():
  original.write_bytes(urlopen(url,timeout=40).read())
 im=Image.open(original).convert('RGB'); a=np.array(im).astype(float)
 red=(a[:,:,0]>a[:,:,1]*1.3)&(a[:,:,0]>a[:,:,2]*1.6)&(a[:,:,0]>95)
 xs=(red[70:690,:].sum(axis=0)>30).nonzero()[0]
 ys=(red[:,:].sum(axis=1)>160).nonzero()[0]
 x=xs[(xs>55)&(xs<500)];y=ys[(ys>65)&(ys<710)]
 if len(y)==0 or len(x)==0:box=(65,107,480,660)
 else:box=(max(55,int(x.min())-4),int(y.min()),min(530,int(x.max())+4),min(740,int(y.max())+4))
 if box[3]-box[1]<300:box=(70,110,480,660)
 tag=f'P{k+1:02}'
 url=c['images'][0]['resource']['service']['@id']+'/full/600,/0/default.jpg'
 key[tag]=dict(canvas=n,folio=c['label'],image=url,frame=list(box),sha256_original=hashlib.sha256((p/'originaux'/f'p{n:04}.jpg').read_bytes()).hexdigest())
 img=im.crop(box)
 # Coordonnées relatives au cadre, couvrant les légendes internes et les notes de marge.
 masks={
  'P01':[(.13,.197,.36,.247),(.52,.196,.92,.245)],
  'P02':[(.15,.022,.84,.084),(.39,.338,.65,.385)],
  'P04':[(.54,.337,.92,.387),(.31,.505,.58,.614)],
  'P05':[(.39,.313,.63,.375)],
  'P06':[(.33,.147,.51,.194),(.973,.48,1,.62)],
  'P07':[(0,.369,.061,.635),(.941,.38,1,.64),(.94,.79,1,.92)],
  'P09':[(.36,.213,.59,.271)],
  'P10':[(.22,.224,.42,.274)]}
 draw=ImageDraw.Draw(img)
 for x1,y1,x2,y2 in masks.get(tag,[]):
  draw.rectangle((int(x1*img.width),int(y1*img.height),int(x2*img.width),int(y2*img.height)),fill='#999999')
 key[tag]['masques_rel']=masks.get(tag,[])
 img.save(p/'aveugle'/(tag+'.jpg'),quality=97)
for lot in range(2):
 out=Image.new('RGB',(900,2*395),'white');draw=ImageDraw.Draw(out)
 for t in range(6):
  tag=f'P{lot*6+t+1:02}'; im=Image.open(p/'aveugle'/(tag+'.jpg'));im.thumbnail((290,368));x=t%3*300;y=t//3*395;out.paste(im,(x+(300-im.width)//2,y));draw.text((x+135,y+370),tag,fill='black')
 out.save(p/'aveugle'/f'Planche{lot+1}.jpg',quality=94)
for tag,record in key.items():
 record['sha256_carte']=hashlib.sha256((p/'aveugle'/(tag+'.jpg')).read_bytes()).hexdigest()
(p/'prive/cle.json').write_text(json.dumps(key,ensure_ascii=False,indent=2)+'\n')
