"""Reproduit les deux vues depuis le JPEG complet de Yale 1006233."""
from pathlib import Path
from hashlib import sha256
import sys
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
data=Path(sys.argv[1])
assert sha256(data.read_bytes()).hexdigest()=='3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e'
im=Image.open(data).convert('RGB')
spec=[
    ('f88v, première rangée', (719,125,2549,855), [(1046,370,1284,466),(1472,362,1670,474),(1920,397,2251,516)],['.2','.3','.4']),
    ('f89r2, troisième rangée', (5480,1870,7380,2455), [(5890,2055,6079,2151),(6286,2088,6443,2173),(6614,2113,6798,2198)],['.17','.18','.19'])
]
def font(size):
    for face in ('Arial.ttf','DejaVuSans.ttf'):
        try:return ImageFont.truetype(face,size)
        except OSError:pass
    return ImageFont.load_default()
panels=[]
for title,bounds,boxes,names in spec:
    pic=im.crop(bounds)
    scale=1200/pic.width
    pic=pic.resize((1200,round(pic.height*scale)),Image.Resampling.LANCZOS)
    sheet=Image.new('RGB',(1220,pic.height+48),'white')
    sheet.paste(pic,(10,42))
    d=ImageDraw.Draw(sheet)
    d.text((12,6),title,font=font(25),fill='#242c2b')
    for box,name in zip(boxes,names):
        x0,y0,x1,y1=[round((v-bounds[i%2])*scale)+(10 if i%2==0 else 42) for i,v in enumerate(box)]
        d.rectangle((x0,y0,x1,y1),outline='#842936',width=2)
        d.rectangle((x0,y1,x0+42,y1+23),fill='white')
        d.text((x0+2,y1+1),name,font=font(18),fill='#842936')
    panels.append(sheet)
plate=Image.new('RGB',(1220,sum(x.height for x in panels)),'white')
h=0
for panel in panels:
    plate.paste(panel,(0,h));h+=panel.height
plate.save(HERE/'deux-troisiemes.jpg',quality=93)
