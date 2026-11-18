"""Produire la planche à partir des trois JPEG natifs de la Beinecke Library."""
from pathlib import Path
from hashlib import sha256
import json,sys
from PIL import Image,ImageDraw,ImageFont

ICI=Path(__file__).resolve().parent
DEPOT=ICI.parents[2]
JETONS=[
    ('1006233','f89r2.21','Fragment 44, troisième rangée',(6610,1790,8890,2600),(7338,2100,7675,2240),(7280,2040,7755,2280)),
    ('1006249','f100v.13','Fragment 143, troisième rangée',(1830,1380,2940,2530),(2550,2160,2858,2280),(2410,2100,2915,2370)),
    ('1006252','f102v2.29','Fragment 233, bord du parchemin',(1660,1500,2870,2420),(2540,2130,2710,2250),(2370,1970,2850,2290))]


def police(size):
    for nom in ('DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:return ImageFont.truetype(nom,size)
        except OSError:continue
    return ImageFont.load_default(size=size)


def dessiner(originaux):
    fiches=json.loads((DEPOT/'voynich_resources/yale/image_index.json').read_text())
    board=Image.new('RGB',(1170,990),'#fff');d=ImageDraw.Draw(board)
    for i,(oid,loc,titre,bounds,cadre,zoom) in enumerate(JETONS):
        f=next(r for r in fiches if ('/'+oid+'/') in r['url'])
        path=originaux/(oid+'.jpg');assert sha256(path.read_bytes()).hexdigest()==f['sha256']
        with Image.open(path) as src:
            im=src.convert('RGB')
        y=330*i
        d.text((12,y+12),loc+'   '+titre,font=police(25),fill='#183140')
        a=im.crop(bounds);b=im.crop(zoom)
        g=ImageDraw.Draw(a);g.rectangle(tuple(v-bounds[j%2] for j,v in enumerate(cadre)),outline='#9e1450',width=8)
        a.thumbnail((698,269),Image.Resampling.LANCZOS);b.thumbnail((423,269),Image.Resampling.LANCZOS)
        board.paste(a,((700-a.width)//2,y+55));board.paste(b,(728+(416-b.width)//2,y+55+(270-b.height)//2))
        if i<2:d.line((12,y+325,1158,y+325),fill='#dedede')
    board.save(ICI/'trois-inscriptions.jpg',quality=93)

if __name__=='__main__':dessiner(Path(sys.argv[1]))
