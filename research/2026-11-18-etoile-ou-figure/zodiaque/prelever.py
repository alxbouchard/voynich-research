"""Localiser quatre formes uniques et les confronter aux positions horaires annoncées."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import json
import math
import re
import sys
import cv2
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite

CASES=[('f70v2','9','otody'),('f70v2','12','okody'),('f72r2','29','otam'),('f72r2','25','okam')]
SOURCE=RESEARCH/'2026-11-17-oteos-anneaux-zodiaque'

def main(cache):
    pos=json.loads((SOURCE/'POSITIONS.json').read_text())
    natives=json.loads((SOURCE/'PHOTOGRAPHIES.json').read_text())
    groves=json.loads((RESEARCH/'2026-11-18-mois-automne/finales/grove-index.json').read_text())['loci']
    zl=(RESEARCH.parent/'voynich_20261028/data/ZL3b-n.txt').read_text().splitlines()
    result={}
    cards=[]
    for page,number,word in CASES:
        row=next(r for r in zl if r.startswith(f'<{page}.{number},'))
        clock=re.search(r'<!(\d\d):(\d\d)>',row)
        assert row.split('>')[-1].strip()==word and clock
        native,ref,layout=[cache/(page+s) for s in ('-n.jpg','-r.jpg','-l.json')]
        center_info=next(v for v in pos if v['locus'].split('.')[0]==page)
        center=center_info['centre_xy']
        oid=str(center_info['oid_yale'])
        grd=[k for k,v in groves[page].items() if v==word]
        assert len(grd)==1
        assert sha256(native.read_bytes()).hexdigest()==natives[oid]['sha256']
        cv2.setRNGSeed(408)
        mat,fit=recaler(ref,native)
        dic,seq=json.loads(layout.read_text());located=[b for b in seq if dic[b[0]][0]==word];assert len(located)==1
        x,y,X,Y=boite(located[0],mat)
        cx,cy=(x+X)//2,(y+Y)//2
        hw,hh=(430,500) if page=='f70v2' else (490,550)
        frame=(cx-hw,cy-hh,cx+hw,cy+hh)
        im=Image.open(native).convert('RGB').crop(frame)
        draw=ImageDraw.Draw(im)
        draw.rectangle((x-frame[0]-5,y-frame[1]-5,X-frame[0]+5,Y-frame[1]+5),outline='#a0432f',width=3)
        im.thumbnail((485,540),Image.Resampling.LANCZOS)
        cards.append((f'{page}.{number}   {word}   ({clock[1]} h {clock[2]})',im))
        geom_angle=math.degrees(math.atan2(cx-center[0],center[1]-cy))%360
        record=dict(lieu=f'{page}.{number}',groupe=word,position_Grove=grd[0],
              horloge_ZL=f'{clock[1]}:{clock[2]}',centre=center,boite=[x,y,X,Y],cadre=frame,
              angle_deg_depuis_midi_sens_horaire=round(geom_angle,2),
              rayon_px=round(math.hypot(cx-center[0],cy-center[1]),2),calage=fit,oid=oid,
              source=natives[oid]['source'],detail=natives[oid]['source'].replace('/full/full/',f'/{frame[0]},{frame[1]},{2*hw},{2*hh}/full/'),
              repere='https://www.voynichese.com/2/data/folio/image/glance/color/large/'+page+'.jpg',
              disposition='https://www.voynichese.com/2/data/folio/script/'+page+'.js',
              empreintes=[sha256(f.read_bytes()).hexdigest() for f in (native,ref,layout)])
        result[record['lieu']]=record
    table=Image.new('RGB',(1000,1180),'#f8f6ef')
    try: font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24)
    except OSError: font=ImageFont.truetype('DejaVuSans.ttf',24)
    draw=ImageDraw.Draw(table)
    for i,(title,im) in enumerate(cards):
        x,y=(i%2)*500,(i//2)*590
        draw.text((x+9,y+5),title,fill='#202f25',font=font)
        table.paste(im,(x+(500-im.width)//2,y+42))
    table.save(HERE/'QUATRE-LEGENDES.jpg',quality=93,optimize=True)
    (HERE/'COORDONNEES.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main(Path(sys.argv[1]))
