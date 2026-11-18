"""Relever les interruptions de f40v et montrer où se lit le groupe EVA arol."""
from hashlib import sha256
from pathlib import Path
import json
import re
import sys
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
R = ICI.parents[2]
DEPOT = R.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(R/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite
sys.path.insert(0,str(R/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import sequence

B = '#006581'
O = '#ad472f'


def police(n):
    for f in ['/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf']:
        try:return ImageFont.truetype(f,n)
        except OSError:pass
    return ImageFont.load_default()


def empreinte(p):
    return sha256(p.read_bytes()).hexdigest()


def collationner():
    result={}
    for ed,f in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        text=(DEPOT/'voynich_20261028/data'/f).read_text()
        rows=[(int(n),k,raw.strip()) for n,k,raw in re.findall(r'^<f40v\.(\d+),.(..)>[ \t]*(.*)', text, re.M)]
        r=[]
        for n,k,raw in rows:
            if '<->' in raw:
                gauche,droite=raw.split('<->')
                cuts={}
                for mode in ('joints','separes'):
                    ga=sequence(gauche,mode)
                    dr=sequence(droite,mode)
                    cuts[mode]={'rang_gauche':len(ga),'dernier_gauche':ga[-1][1],'premier_droite':dr[0][1]}
                r.append({'ligne':n,'lectures':cuts})
        lab=re.search(r'^<f99v\.8,.[^>]*>[ \t]*(.*)',text,re.M)[1]
        assert sequence(lab,'joints')==[(0,'arol')]
        result[ed]={'lignes_P0':sum(k=='P0' for _,k,_ in rows),'lignes_Pc':sum(k=='Pc' for _,k,_ in rows),
                    'interruptions':r,'f40v.18':rows[17][2],'f40v.19':rows[18][2],'f99v.8':lab}
    return result


def planche(p,q):
    canvas=Image.new('RGB',(1336,812),'#faf9f5');dr=ImageDraw.Draw(canvas)
    dr.text((18,11),'f40v.18 : la ligne reprend de l’autre côté du dessin',fill='#242424',font=police(30))
    dr.text((20,62),'Les repères colorés sont ajoutés. L’extrait horizontal conserve les deux bords du dessin et la fin de la ligne.',fill='#444444',font=police(18))
    window=(465,1450,2690,1810)
    d=p.crop(window);k=1300/d.width
    canvas.paste(d.resize((1300,round(d.height*k)),Image.Resampling.LANCZOS),(18,103))
    # Segments courts sous les traits des mots aux quatre positions contrôlées.
    for a,b,y,col in [(1380,1551,1662,B),(1570,1690,1667,O),(2213,2370,1667,B),(2409,2564,1649,B)]:
        xx=18+(a-window[0])*k;yy=103+(y-window[1])*k
        dr.line((xx,yy,18+(b-window[0])*k,yy),fill=col,width=2)
    dr.text((20,332),'De gauche à droite : okair, arol, partie peinte, qokey, okary. En dessous, la ligne courte .19.',fill='#333333',font=police(18))
    # Les mots sont agrandis à une même échelle ; leurs voisins donnent le contexte.
    views=[(p,(1355,1565,1745,1725),'f40v.18, sixième groupe'),
           (q,(1930,135,2320,295),'f99v.8, légende du fragment 101')]
    for i,(im,reg,title) in enumerate(views):
        x=18+i*440
        dr.text((x,397),title,fill='#272727',font=police(19))
        canvas.paste(im.crop(reg).resize((415,170),Image.Resampling.LANCZOS),(x,440))
        start,end=(1568,1691) if i==0 else (2132,2243)
        # Barre hors de la fenêtre photographique, sans couvrir les signes.
        dr.line((x+(start-reg[0])*415/390,614,x+(end-reg[0])*415/390,614),fill=O,width=4)
    dr.text((900,397),'Portion du dessin entre les mots',fill='#272727',font=police(19))
    reg=(1481,1290,2424,1860)
    part=p.crop(reg).resize((416,251),Image.Resampling.LANCZOS)
    canvas.paste(part,(900,439))
    dr.text((20,716),'La transcription EVA rend les quatre signes par a-r-o-l. Les barres orange situent leur étendue.',fill='#333333',font=police(19))
    dr.text((20,756),'Beinecke MS 408, Yale. Clichés 1006153 et 1006247.',fill='#585858',font=police(17))
    canvas.save(ICI/'arol-et-interruption.jpg',quality=94,optimize=True)


def main(img40,ref40,layout,img99):
    d,points=json.loads(layout.read_text())
    m,fit=recaler(ref40,img40)
    labels=[d[x[0]][0] for x in points]
    derniers=labels[-12:]
    assert derniers==['saiin','otain','chckhy','okal','okair','arol','qokey','okary','pchedy','chetar','ofair','arody']
    source=R/'2026-11-18-du-dessin-au-paragraphe/cressons/PHOTO.json'
    r99=json.loads(source.read_text())
    assert empreinte(img40)=='bce0c42319b096126ad9fe0558ecfb8a61335867cbd1869e0865eaacf54c1087'
    assert empreinte(img99)==r99['empreinte']
    geom={f'f40v.{18 if i<8 else 19}/{(i if i<8 else i-8)+1}':{'forme':w,'boîte':boite(x,m)}
          for i,(w,x) in enumerate(zip(derniers,points[-12:]))}
    geom['f99v.8']={'forme':'arol','boîte':r99['positions_approximatives_visualiseur']['arol']}
    geom['f99v.8']['cadre_encre_relevé_sur_photo']=[2129,158,2246,242]
    geom['f40v.18/6']['cadre_encre_relevé_sur_photo']=[1567,1606,1694,1667]
    out={'f40v':{'yale':'https://collections.library.yale.edu/iiif/2/1006153/full/full/0/default.jpg',
                 'sha256':empreinte(img40),'reference':'https://www.voynichese.com/2/data/folio/image/glance/color/large/f40v.jpg',
                 'sha256_reference':empreinte(ref40),'carte':'https://www.voynichese.com/2/data/folio/script/f40v.js',
                 'sha256_carte':empreinte(layout),'calage':fit},
         'f99v':{'yale':r99['source'],'sha256':empreinte(img99),'calage':r99['calage']},'emplacements_nat':geom,
         'largeur_entre_boites_apres_arol':geom['f40v.18/7']['boîte'][0]-geom['f40v.18/6']['boîte'][2],
         'transcriptions':collationner()}
    (ICI/'REPERES.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    with Image.open(img40) as p, Image.open(img99) as q:planche(p,q)


if __name__=='__main__':
    main(*[Path(n) for n in sys.argv[1:]])
