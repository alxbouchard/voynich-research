"""Régénérer une planche native de f99r à partir du JPEG intégral 1006246."""
from pathlib import Path
from hashlib import sha256
import json,sys
from PIL import Image,ImageDraw,ImageFont

ICI=Path(__file__).resolve().parent
p=Path(sys.argv[1]);reg=json.loads((ICI/'SOURCES.json').read_text())['photo']
assert sha256(p.read_bytes()).hexdigest()==reg['calage']['yale_sha256']
im=Image.open(p).convert('RGB')
def police(n):
    for font in ('DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:return ImageFont.truetype(font,n)
        except OSError:continue
    return ImageFont.load_default(size=n)

bounds=(1310,966,2380,1420)
v=im.crop(bounds)
g=ImageDraw.Draw(v)
for n,item in reg['boites'].items():
    x,y,r,b=item['boite'];bords=(x-bounds[0]-5,y-bounds[1]-4,r-bounds[0]+5,b-bounds[1]+3)
    couleur='#a21d5b' if n.endswith('/10') else ('#0e6980' if n.endswith('/8') or n.endswith('.25') else '#947639')
    g.rectangle(bords,outline=couleur,width=3)

pl=Image.new('RGB',(1110,645),'white');d=ImageDraw.Draw(pl)
d.text((20,14),'f99r   Fin du paragraphe et légendes de la rangée suivante',font=police(24),fill='#172f35')
pl.paste(v,(20,58))
for n,t,c,x in [('7','daiin','#785927',26),('8','okeoly','#0e6980',256),('9','daiin','#785927',482),('10','ckhy','#a21d5b',740)]:
    d.text((x,523),f'Rang {n}   {t}',font=police(23),fill=c)
d.text((24,583),'Sous le rang 8, la légende f99r.25 porte aussi la lecture okeoly.',font=police(22),fill='#172f35')
pl.save(ICI/'rang-10.jpg',quality=95)
