"""Faire des recadrages documentaires des cas 125 et 209, d’après les clichés de Yale."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OBJECTS={'125':('1006248','B01'),'209':('1006251','B02')}
BOXES={
 '125':{'situation':(1579,248,2440,1269),'f100r.11':(2122,483,2389,627),
        'f100r.9':(1390,977,1604,1100),'f100r.27':(1092,2697,1369,2856)},
 '209':{'rang':(5250,1125,8095,1880),'troisieme_fragment':(6480,1290,7040,1655)}}


def font(size):
    for name in ['/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf']:
        try:return ImageFont.truetype(name,size)
        except OSError:pass
    return ImageFont.load_default()


def paste(im,source,xywh):
    x,y,w,h=xywh;thumb=source.copy();thumb.thumbnail((w,h),Image.Resampling.LANCZOS)
    im.paste(thumb,(x+(w-thumb.width)//2,y))


def main(cache):
    provenance=json.loads((ROOT/'images/PROVENANCE.json').read_text());catalog={}
    for item,(oid,ref) in OBJECTS.items():
        path=cache/(oid+'.jpg');sha=sha256(path.read_bytes()).hexdigest();assert sha==provenance[ref]['sha256_original']
        original=Image.open(path).convert('RGB');regions=BOXES[item]
        catalog[item]=dict(oid=oid,sha256=sha,dimensions=original.size,rectangles_xyxy=regions)
        if item=='125':
            out=Image.new('RGB',(1090,594),'#f8f4ec');d=ImageDraw.Draw(out)
            d.text((18,10),'Folio 100r  ·  La légende du fragment 125 et deux comparaisons',fill='#28251f',font=font(25))
            paste(out,original.crop(regions['situation']),(8,54,425,506));d.text((18,563),'125 sous l’inscription, à droite du deuxième rang',font=font(16),fill='#40392e')
            for i,(key,title) in enumerate([('f100r.11','Fragment 125, f100r.11  ·  sofal / sofam'),('f100r.9','Fragment 123, f100r.9  ·  sosam'),('f100r.27','Prose, f100r.27  ·  otolchey')]):
                y=58+i*174;d.text((461,y),title,font=font(20),fill='#362f26');paste(out,original.crop(regions[key]),(461,y+28,590,132))
        else:
            out=Image.new('RGB',(1330,655),'#f8f4ec');d=ImageDraw.Draw(out)
            d.text((18,12),'Folio 102r2  ·  Registre des fragments 207 à 211',fill='#28251f',font=font(27))
            paste(out,original.crop(regions['rang']),(15,57,1300,344));
            d.text((22,433),'209  ·  Troisième fragment',font=font(24),fill='#28251f');d.multiline_text((22,481),'Une ligne de prose passe au-dessus.\nLe paragraphe suivant commence sous les dessins.',font=font(22),spacing=9,fill='#393329')
            paste(out,original.crop(regions['troisieme_fragment']),(577,405,680,243))
        out.save(HERE/('fragment-'+item+'.jpg'),quality=92,optimize=True)
    (HERE/'REPERES.json').write_text(json.dumps(catalog,indent=1)+'\n')


if __name__=='__main__':main(Path(sys.argv[1]))
