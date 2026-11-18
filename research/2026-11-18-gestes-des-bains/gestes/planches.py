"""Produire les détails annotés à partir des JPEG Yale dont l'empreinte figure au registre."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image,ImageDraw,ImageFont

ICI=Path(__file__).resolve().parent
D=json.loads((ICI/'COTATION.json').read_text())
def police(sz):
    for nom in ['DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
        try:return ImageFont.truetype(nom,sz)
        except OSError:continue
    return ImageFont.load_default(size=sz)

def faire(dossier):
    panneau=Image.new('RGB',(1080,910),'white')
    d=ImageDraw.Draw(panneau)
    specs=[('f80r',[.077,.015,.368,.146],['f80r.2','f80r.3','f80r.4'],(12,54,1068,397)),
           ('f83v',[.690,.539,.859,.703],['f83v.34'],(12,459,526,873)),
           ('f77r',[.045,.397,.348,.56],['f77r.49'],(545,459,1068,873))]
    textes=[(16,12,'f80r   .2   avec objet       .3 et .4   sans objet'),(16,411,'f83v.34   contact'),(550,411,'f77r.49   contact, apprentissage')]
    for x,y,s in textes:d.text((x,y),s,font=police(24),fill='#132e37')
    for f,zone,ids,espace in specs:
        path=dossier/(f+'.jpg')
        assert sha256(path.read_bytes()).hexdigest()==D['source_images'][f]['yale_sha256']
        im=Image.open(path).convert('RGB');g=ImageDraw.Draw(im)
        for r in D['objets']:
            if r['objet'] not in ids:continue
            for _,x,y,l,b in r['boites']:g.rectangle([x-8,y-6,l+8,b+6],outline='#9b1955',width=5)
        q=tuple(round(z*(im.width if i%2==0 else im.height)) for i,z in enumerate(zone));im=im.crop(q)
        x,y,l,b=espace;im.thumbnail((l-x,b-y),Image.Resampling.LANCZOS);panneau.paste(im,(x+(l-x-im.width)//2,y))
    panneau.save(ICI/'gestes-verifies.jpg',quality=93)

if __name__=='__main__':faire(Path(sys.argv[1]))
