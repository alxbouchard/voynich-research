"""Construire le matériel aveugle de la lecture des tracés de f73v.4."""
from hashlib import sha256
import json
from pathlib import Path
from random import Random
import sys

from PIL import Image, ImageDraw

from verifier import HERE, MONTHS, font, read_labels

# Les deux dernières boîtes sont dans l'image tournée à résolution native.
CASES = {
    'f73v.4': ((2000,562,2160,663),20,(10,43,175,111),(11,48,65,88),'début'),
    'f73r.2': ((1150,535,1327,632),0,(9,9,168,88),(8,44,50,84),'début'),
    'f73r.17': ((635,2080,1100,2490),220,(283,225,365,284),(281,231,319,270),'début'),
    'f73r.4': ((1650,621,1830,774),25,(36,65,205,154),(89,86,121,126),'intérieur'),
    'f72v1.31': ((1294,1960,1482,2114),210,(32,92,178,146),(53,87,95,130),'intérieur'),
}
def run(sources, editions):
    source_rows={w['folio']:w for w in MONTHS}
    editions_data={n:read_labels(editions/(n+'.txt')) for n in ('IT2a-n','ZL3b-n','GC2a-n','RF1b-e','RF1b-er')}
    indices=list(CASES)
    Random(731804).shuffle(indices)
    tile=Image.new('RGB',(765,705),'white')
    draw=ImageDraw.Draw(tile)
    draw.text((16,11),'Inscription entière',font=font(20),fill='black')
    draw.text((504,11),'Détail à examiner',font=font(20),fill='black')
    key={}
    for i,lid in enumerate(indices):
        code=chr(65+i)
        p=source_rows[lid.split('.')[0]]
        src=sources/(p['oid_yale']+'.jpg')
        assert sha256(src.read_bytes()).hexdigest()==p['sha256_jpeg']
        native_box,angle,word_box,pair_box,place=CASES[lid]
        versions={n:rows[lid] for n,rows in editions_data.items()}
        if lid!='f73v.4':
            assert versions['IT2a-n']==versions['ZL3b-n']
        with Image.open(src) as im:
            native=im.crop(native_box)
            if lid=='f73v.4':
                native.save(HERE/'f73v.4.png')
            straight=native.rotate(angle,Image.Resampling.BICUBIC,expand=True,fillcolor='white')
            y=44+132*i
            for region,scale,(x,x1) in ((word_box,2,(72,407)),(pair_box,3,(444,748))):
                cut=straight.crop(region)
                big=cut.resize((cut.width*scale,cut.height*scale),Image.Resampling.NEAREST)
                # Garder le rapport de forme de chaque prélèvement.
                big.thumbnail((x1-x,119),Image.Resampling.LANCZOS)
                tile.paste(big,(x+(x1-x-big.width)//2,y+(119-big.height)//2))
            draw.text((21,y+40),code,font=font(29),fill='black')
            draw.line((12,y+124,752,y+124),fill='#d0d0d0')
        key[code]={'locus':lid,'place':place,'editions':versions,'oid_yale':p['oid_yale'],
                   'sha256_source':p['sha256_jpeg'],'region_native_xyxy_fin_exclue':native_box,
                   'rotation_deg_antihoraire':angle,'boite_mot_apres_rotation':word_box,
                   'boite_detail_apres_rotation':pair_box}
    tile.save(HERE/'groupes-anonymes.png')
    (HERE/'cle-groupes.json').write_text(json.dumps(key,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    run(*(Path(s) for s in sys.argv[1:]))
