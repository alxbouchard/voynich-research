"""Recadrer le document Yale original avec les trois lieux vérifiés sur la carte."""
from pathlib import Path
from PIL import Image,ImageDraw
from hashlib import sha256
import json,sys
p=Path(__file__).resolve().parent
d=json.loads((p/'COORDONNEES.json').read_text());source=Path(sys.argv[1])
assert sha256(source.read_bytes()).hexdigest()==d['yale_sha256']
for masquer in [True,False]:
 im=Image.open(source).convert('RGB');art=ImageDraw.Draw(im)
 for locus,item in d['lieux'].items():
  x,y,r,b=item['boite_yale'];teinte='#a80f56' if locus=='f78r.2' else '#18527a'
  art.rectangle((x-10,y-6,r+14,b+7),fill='#dccdb4' if masquer else None,outline=teinte,width=7)
 im=im.crop(d['recadrage']);im.thumbnail((1200,820),Image.Resampling.LANCZOS)
 im.save(p/('f78r-masque.jpg' if masquer else 'f78r-verifie.jpg'),quality=93)
