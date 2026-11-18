"""Ouvrir l'espace des mains dans un cadrage plus large, sans masquer aucune écriture."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from PIL import Image,ImageDraw
from extraire import CASES,RESERVE

HERE=Path(__file__).resolve().parent
CODES={'L6':'N8','Z2':'R7','F4':'M9','U8':'B4'}
def main(native_a,native_b):
    key=json.loads((HERE/'CLE.json').read_bytes())
    for new,old in CODES.items():
        r=key['cartes'][old]
        in_a=old in CASES
        oid='1006204' if in_a else '1006206'
        path=native_a if in_a else native_b
        assert sha256(path.read_bytes()).hexdigest()==key['photos'][oid]['sha256']
        with Image.open(path) as whole:
            cx,cy=r['centre_boite_figure']
            x0,y0=cx-650,cy-650
            img=whole.crop((x0,y0,cx+650,cy+650)).convert('RGB')
        x,y=r['point_front_natif'];x-=x0;y-=y0
        ImageDraw.Draw(img).ellipse((x-5,y-5,x+5,y+5),fill='#2096ce',outline='#174b6b')
        img=img.rotate(r['rotation_antihoraire_deg'],Image.Resampling.BICUBIC).crop((140,145,1160,1155))
        img.save(HERE/'originaux'/(new+'.jpg'),quality=94,subsampling=0,optimize=True)
if __name__=='__main__': main(*(Path(p) for p in sys.argv[1:]))
