"""Situer la légende et les trois blocs de prose sur les deux vues natives de f101v."""
from hashlib import sha256
import json
import math
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
# Boîtes visuelles en pixels des deux vignettes proportionnelles de travail.
VUES = {
    'gauche':{'oid':'1006250', 'largeur':1600,'découpe':(148,24,1458,2140),
              'blocs':[(271,1275,1370,1445),(272,1430,1370,1577),(270,1557,1370,1692),(995,1655,1367,1722)]},
    'droite':{'oid':'1006251','largeur':2200,'découpe':(115,30,776,994),
              'blocs':[(118,617,751,692),(119,694,749,759),(115,742,746,816),(116,797,450,833)]}
}
LEGENDE_NATIVE = (850,820,985,955)  # cadre publié dans photos_okol/produire.py

def fonte(n):
    for f in ('/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf'):
        try:return ImageFont.truetype(f,n)
        except OSError:pass
    return ImageFont.load_default()


def cadre_natif(box,k):
    return [round(v*k) for v in box]


def main(cache):
    reg=json.loads((ICI.parents[3]/'voynich_resources/yale/image_index.json').read_text())
    cols=['#1b6781','#90652f','#704c83','#656565']
    panneau=Image.new('RGB',(1160,919),'#faf9f5')
    d=ImageDraw.Draw(panneau)
    d.text((22,12),'f101v : situer la légende et les paragraphes sur le dépliant',font=fonte(28),fill='#222222')
    d.text((22,60),'Deux clichés distincts, présentés côte à côte. Les bords du pli sont incomplets.',font=fonte(18),fill='#444444')
    données={}
    for i,(nom,v) in enumerate(VUES.items()):
        fiche=next(s for s in reg if f"/{v['oid']}/" in s['url'])
        chemin=cache/(v['oid']+'.jpg')
        assert sha256(chemin.read_bytes()).hexdigest()==fiche['sha256']
        photo=Image.open(chemin).convert('RGB')
        ratio=photo.width/v['largeur']
        raw=cadre_natif(v['découpe'],ratio)
        img=photo.crop(raw)
        scale=min(526/img.width,693/img.height)
        img=img.resize((round(img.width*scale),round(img.height*scale)),Image.Resampling.LANCZOS)
        x=24+i*557+(526-img.width)//2
        y=126
        panneau.paste(img,(x,y))
        def pt(xx,yy):
            return x+(xx-raw[0])*scale,y+(yy-raw[1])*scale
        d.text((24+i*557,96),'Partie '+nom+' de f101v',font=fonte(19),fill='#222222')
        data={'url':fiche['url'],'sha256':fiche['sha256'],'dimensions':list(photo.size),
              'rectangles_nat':{},'découpe_native':raw}
        for j,b in enumerate(v['blocs']):
            b=cadre_natif(b,ratio)
            data['rectangles_nat'][['19–21','22–24','25–27','28'][j]]=b
            left,top=pt(b[0],b[1]);right,bottom=pt(b[2],b[3])
            # Les accolades sont placées au bord extérieur pour laisser le texte libre.
            if not i:
                drawx=left-7-j*3
                d.line([(drawx+4,top),(drawx,top),(drawx,bottom),(drawx+4,bottom)],fill=cols[j],width=3)
            else:
                drawx=right+2+j*2
                d.line([(drawx-4,top),(drawx,top),(drawx,bottom),(drawx-4,bottom)],fill=cols[j],width=3)
        if nom=='gauche':
            data['cadre_légende_natif']=LEGENDE_NATIVE
            cx=(LEGENDE_NATIVE[0]+LEGENDE_NATIVE[2])/2
            cy=(LEGENDE_NATIVE[1]+LEGENDE_NATIVE[3])/2
            data['distance_point_rectangle_native']={}
            for n,b in data['rectangles_nat'].items():
                data['distance_point_rectangle_native'][n]=round(math.hypot(max(0,b[0]-cx,cx-b[2]),max(0,b[1]-cy,cy-b[3])),1)
            xx,yy=pt(cx,cy)
            d.ellipse((xx-10,yy-10,xx+10,yy+10),outline='#a53624',width=3)
        données[nom]=data
    d.text((24,840),'Cercle rouge : f101v.10',font=fonte(19),fill='#a53624')
    for j,t in enumerate(['Lignes 19–21','Lignes 22–24','Lignes 25–27','Ligne décalée 28']):
        d.text((24+j*280,879),t,font=fonte(19),fill=cols[j])
    panneau.save(ICI/'deux-vues.jpg',quality=93,optimize=True)
    (ICI/'GÉOMÉTRIE.json').write_text(json.dumps(données,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__': main(Path(sys.argv[1]))
