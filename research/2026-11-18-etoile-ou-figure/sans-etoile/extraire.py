"""Présenter trois figures presque à la verticale, sans effacer la moindre encre proche des mains."""
from pathlib import Path
from hashlib import sha256
import json, sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
# Les centres/cadres sont donnés dans le cliché Yale natif. Le point est placé sur le front.
CASES={
 'R7':('f72v2.25','S2.5', 'okeeom', (5160,1505), (5213,1453), 73, (5038,1551,5127,1687)),
 'B4':('f72v2.23','S2.3', 'oeedy', (4743,1253), (4783,1129), 18, (4765,1246,4851,1311)),
 'M9':('f72v2.24','S2.4', 'opalg', (4928,1320), (5018,1210), 35, (4967,1306,5076,1422))}
# Masques suivant les traits des cinq étiquettes de la couronne. Tous les sommets sont en pixels Yale.
POLYGONES=[[(4516,1285),(4575,1255),(4601,1256),(4605,1294),(4653,1288),(4655,1319),(4516,1329)],
           [(4760,1244),(4805,1242),(4850,1275),(4853,1311),(4823,1314),(4759,1276)],
           [(4965,1309),(5003,1306),(5074,1385),(5075,1425),(5031,1405),(4969,1351)],
           [(5038,1550),(5064,1544),(5128,1633),(5127,1687),(5098,1690),(5036,1591)],
           [(5041,1863),(5101,1871),(5166,1970),(5168,2023),(5115,2007),(5045,1915)]]
RESERVE={
 'H3':('f73r.18','S1.14','dalshey',(615,2176),(544,2277),-112,(596,1996,687,2146)),
 'N8':('f73r.19','S1.15','opaiin',(484,1915),(379,1911),-86,(495,1740,576,1890)),
 'K5':('f73r.20','S1.16','okeos',(462,1577),(377,1520),-66,(542,1424,613,1534))}
POLYGONES_RESERVE=[[(783,2280),(808,2277),(861,2320),(863,2354),(841,2356),(788,2316)],
                   [(595,1994),(627,1994),(689,2116),(689,2149),(654,2137),(598,2068)],
                   [(491,1738),(579,1738),(579,1893),(491,1893)],
                   [(539,1421),(616,1421),(616,1537),(539,1537)],
                   [(638,1223),(665,1223),(731,1291),(732,1319),(692,1319),(636,1268)]]

def main(cache):
    known=json.loads((HERE.parents[1]/'2026-11-17-oteos-anneaux-zodiaque/PHOTOGRAPHIES.json').read_text())
    groups=[(CASES,'f72v2','1006204',POLYGONES),(RESERVE,'f73r','1006206',POLYGONES_RESERVE)]
    font=None
    for path in ('/System/Library/Fonts/Helvetica.ttc','DejaVuSans.ttf'):
        try: font=ImageFont.truetype(path,25);break
        except OSError: pass
    key={}
    for cases,panel,oid,masks in groups:
        source=cache/(panel+'-n.jpg')
        assert sha256(source.read_bytes()).hexdigest()==known[oid]['sha256']
        full=Image.open(source).convert('RGB')
        photo=known[oid]['source']
        for code,(locus,rank,word,(cx,cy),(hx,hy),angle,box) in cases.items():
            half=550
            raw=(cx-half,cy-half,cx+half,cy+half)
            im=full.crop(raw)
            draw=ImageDraw.Draw(im)
            for poly in masks:
                draw.polygon([(x-raw[0],y-raw[1]) for x,y in poly],fill='#c9c3b3')
            x=hx-raw[0];y=hy-raw[1];draw.ellipse((x-5,y-5,x+5,y+5),fill='#2096ce',outline='#174b6b',width=1)
            im=im.rotate(angle,Image.Resampling.BICUBIC).crop((195,210,905,890))
            card=Image.new('RGB',(710,721),'#f8f6ed')
            card.paste(im,(0,41));ImageDraw.Draw(card).text((10,5),code,fill='#1c2b24',font=font)
            card.save(HERE/'cartes'/(code+'.jpg'), quality=95,optimize=True,subsampling=0)
            x0,y0=max(0,raw[0]),max(0,raw[1])
            x1,y1=min(full.width,raw[2]),min(full.height,raw[3])
            key[code]={'locus':locus,'rang_Grove':rank,'mot_H_ZL':word,'rotation_antihoraire_deg':angle,'natif_avant_rotation':raw,'rognage_apres_rotation':[195,210,905,890],'centre_boite_figure':[cx,cy],'point_front_natif':[hx,hy],'boite_du_mot':box,'region_nue_Yale':photo.replace('/full/full/', f'/{x0},{y0},{x1-x0},{y1-y0}/full/')}
    (HERE/'CLE.json').write_text(json.dumps({'photos':{oid:known[oid] for oid in ('1006204','1006206')},'centres':{'f72v2':[4603,1790],'f73r':[1260,1745]},'masques_natifs':{'f72v2':POLYGONES,'f73r':POLYGONES_RESERVE},'cartes':key},ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__': main(Path(sys.argv[1]))
