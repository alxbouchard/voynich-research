"""Extraire les six détails et estimer l'écart horizontal des signes à trois seuils."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from PIL import Image

HERE=Path(__file__).resolve().parent
RECTS={
    'f11r':{3:(546,603,885,733),4:(698,685,1145,809),5:(1258,727,2050,883),7:(845,881,1168,1031)},
    'f15r':{3:(1100,699,1645,833),5:(763,831,1642,991)},
}
# Origine de chaque rectangle dans le petit recadrage de la ligne.
# Chaque liste suit la dernière queue du mot précédent, d, y,
# et le bord du premier signe suivant, s'il y a un mot suivant.
BOXES={
    ('f11r',5):[(292,70,325,132),(337,57,382,112),(383,66,421,131),(421,70,461,112)],
    ('f15r',5):[(724,86,768,155),(773,78,813,139),(811,91,844,152)],
    ('f11r',7):[(146,67,188,122),(207,46,249,100),(249,63,290,122)],
    ('f11r',4):[(134,49,166,99),(187,36,226,85),(224,54,256,110),(267,35,311,85)],
}
OIDS={'f11r':('1006096',(2672,3744)),'f15r':('1006102',(2648,3729))}

def ink_extent(green,box,threshold):
    x,y,right,bottom=box
    pixels={(i,j) for i in range(x,right) for j in range(y,bottom) if green[i,j]<threshold}
    retained=set()
    while pixels:
        stack=[pixels.pop()];component=set(stack)
        while stack:
            i,j=stack.pop()
            for di in (-1,0,1):
                for dj in (-1,0,1):
                    point=i+di,j+dj
                    if point in pixels:
                        pixels.remove(point);component.add(point);stack.append(point)
        if len(component)>=35:
            retained.update(component)
    assert retained
    xs=[i for i,j in retained]
    return min(xs),max(xs)

def main(paths):
    report={}
    for (page,boxes),path in zip(RECTS.items(),paths,strict=True):
        oid,size=OIDS[page]
        image=Image.open(path).convert('RGB')
        assert image.size==size
        record={'oid':oid,'dimensions':size,'sha256':sha256(path.read_bytes()).hexdigest(),'rectangles':boxes,'mesures':{}}
        for row,b in boxes.items():
            patch=image.crop(b)
            patch.save(HERE/f'{page}-l{row}.jpg',quality=96)
            if (page,row) not in BOXES:continue
            regions=BOXES[page,row]
            green=patch.getchannel('G').load()
            measurements={}
            for thresh in (130,145,160):
                bounds=[ink_extent(green,region,thresh) for region in regions]
                measurements[thresh]={'limites_x':bounds,'intervalles_x':[r[0]-l[1]-1 for l,r in zip(bounds,bounds[1:])]}
            record['mesures'][row]={'fenetres':regions,'seuils_verts':measurements}
        top=image.crop((0,0,image.width,1600))
        top.resize((1200,round(1200*top.height/top.width)),Image.Resampling.LANCZOS).save(HERE/f'{page}-ensemble.jpg',quality=91)
        report[page]=record
    (HERE/'reperes.json').write_text(json.dumps(report,indent=1)+'\n')
    for page,r in report.items():
        print(page,r['sha256'])
        for row,m in r['mesures'].items():print(row,{t:v['intervalles_x'] for t,v in m['seuils_verts'].items()})
if __name__=='__main__':main(list(map(Path,sys.argv[1:])))
