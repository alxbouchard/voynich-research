"""Détails des impressions de 1475 et 1482. Les cadres sont dans les vues BSB téléchargées."""
from pathlib import Path
from hashlib import sha256
import json, sys
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
SOURCES={
    '1482-379':('mgn-par-379.jpg','bsb00032393',379,1450,'78e460b89a82c47820068cc7d1f2a16d9152d47e2a650be0a2f44190cb49cfa5'),
    '1482-383':('mgn-par-383.jpg','bsb00032393',383,1450,'6a45bc182a891406f5440037606d245c45771d4c6bb093ef8a76d42c5023235b'),
    '1482-384':('mgn-par-384.jpg','bsb00032393',384,1450,'5bc67ff048e9253f76c6053cac81a822ec4cae27e1f2e7e13182d0d0cb24b2b5'),
    '1475-489':('mgn-1475-par-489.jpg','bsb00029636',489,1300,'4bd2c97df5a6578e6409f1e9145b0987d5107b81a8a43a51e6aa7e177c9237ae'),
    '1475-490':('mgn-1475-par-490.jpg','bsb00029636',490,1300,'a9df00f61206276f2134e5a7cc687093d1d8065eeaa1c205c85ce4aa6ed554ad')}
PLATES={'trois-rubriques.jpg':[
 ('F. 190v. Cresson','1482-383',(220,1248,1285,1456)),
 ('F. 191r. Plante aquatique','1482-384',(141,481,1245,618)),
 ('F. 191r. Nigelle','1482-384',(134,1277,1246,1397)),
 ('F. 190v. Von dans la prose','1482-383',(610,274,1330,347)),
 ('F. 191r. Von dans la prose','1482-384',(560,1128,1108,1199))],
 'deux-editions.jpg':[
 ('1475, f. 243r. Même titre et début de la notice du cresson','1475-489',(110,955,939,1076)),
 ('1482, f. 190v. Le signe du titre reste, celui de la prose disparaît','1482-383',(210,1268,1220,1458)),
 ('1475, f. 243v. La notice de la nigelle commence par un pied-de-mouche','1475-490',(340,1161,1172,1314)),
 ('1482, f. 191r. Un titre précède le mot Nigella','1482-384',(132,1277,1242,1398)),
 ('1475, f. 243r. Deux unités de sens sur une seule ligne','1475-489',(125,463,956,521)),
 ('1482, f. 190v. La même transition après mit dem kraut','1482-383',(226,806,1312,877))]}

def font():
    for name in ('/System/Library/Fonts/Helvetica.ttc','DejaVuSans.ttf'):
        try:return ImageFont.truetype(name,22)
        except OSError:pass
    return ImageFont.load_default()

def main(cache):
    images={}
    for key,(name,book,n,size,digest) in SOURCES.items():
        path=cache/name
        assert sha256(path.read_bytes()).hexdigest()==digest
        images[key]=Image.open(path).convert('RGB')
    for out,items in PLATES.items():
        crops=[]
        for title,src,rect in items:
            crops.append((title,images[src].crop(rect)))
        width=max(im.width for _,im in crops)+24
        height=sum(im.height+52 for _,im in crops)+8
        plate=Image.new('RGB',(width,height),'#f9f6ec'); draw=ImageDraw.Draw(plate); y=8
        for title,im in crops:
            draw.text((12,y),title,font=font(),fill='#27251d')
            plate.paste(im,(12,y+32));y+=52+im.height
        plate.save(HERE/out,quality=91,subsampling=0,optimize=True)
    data={k:{"vue":n,"url":f'https://api.digitale-sammlungen.de/iiif/image/v2/{book}_{n:05}/full/{size},/0/default.jpg',
             "nom_cache":name,"sha256":h} for k,(name,book,n,size,h) in SOURCES.items()}
    (HERE/'SOURCES.json').write_text(json.dumps({'vues':data,'recadrages':PLATES},ensure_ascii=False,indent=1)+'\n')
if __name__=='__main__': main(Path(sys.argv[1]))
