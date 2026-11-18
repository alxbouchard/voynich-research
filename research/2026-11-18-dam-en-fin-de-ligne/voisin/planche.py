"""python3 planche.py DOSSIER ; noms des vues 1006141.jpg et 1006255.jpg."""
from hashlib import sha256
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

images = Path(sys.argv[1])
out = Image.new('RGB',(1180,698),'#f9f8f5')
pen = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype('Arial.ttf',18).path
except OSError:
    font = ImageFont.truetype('DejaVuSans.ttf',18).path

def label(x,y,msg,n):
    pen.text((x,y),msg,font=ImageFont.truetype(font,n),fill='#20272a')

def panel(oid,empreinte,ligne,mots,y,titre):
    p=images/(str(oid)+'.jpg')
    assert sha256(p.read_bytes()).hexdigest()==empreinte
    im=Image.open(p)
    label(24,y,titre,23)
    for boite,largeur,yoff in [(ligne,1110,38),(mots,640,134)]:
        ex=im.crop(boite)
        ex=ex.resize((largeur,round(largeur*ex.height/ex.width)),Image.Resampling.LANCZOS)
        out.paste(ex,(24,y+yoff))

panel(1006141,'2f68183982075a405f7e2cc11ea06b76b263f80f20f01083279e7f03dcb4f78a',
      (716,676,2560,795),(1712,682,2080,797),10,'f34v.5  |  Apprentissage : chedy qokar, suivi de deux autres mots')
panel(1006255,'dd2444928b8dd5d1e60fbd58e04e4be38ed877f9d491058a7c6b779ceb18a75b',
      (646,452,2570,575),(2209,460,2550,566),350,'f103v.6  |  Réserve : chedy qokam à la fin de la ligne')
out.save(Path(__file__).with_name('paire.jpg'), quality=93)
