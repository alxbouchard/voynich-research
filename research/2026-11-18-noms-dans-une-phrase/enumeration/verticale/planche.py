"""Placer les centres, les rangées et les témoins sur trois clichés de Yale."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import sys

ICI = Path(__file__).resolve().parent
BLEU = '#005c99'
ROUGE = '#a53321'
GRIS = '#47494a'


def fonte(taille):
    for nom in ('/System/Library/Fonts/Supplemental/Arial.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(nom, taille)
        except OSError:
            pass
    return ImageFont.load_default()


def enveloppe(reperes):
    boites = [r['boite'] for r in reperes]
    return (min(b[0] for b in boites), min(b[1] for b in boites),
            max(b[2] for b in boites), max(b[3] for b in boites))


def vignette(canvas, photo, x0, y0, repertoire, annonce, prose, centre, dp):
    """Agrandissement à la même échelle pour les deux traits d'un panneau."""
    w, h = 451, 78
    f = .86
    b = (round(centre[0] - w/(2*f)), round(centre[1] - h/(2*f)),
         round(centre[0] + w/(2*f)), round(centre[1] + h/(2*f)))
    canvas.paste(photo.crop(b).resize((w,h),Image.Resampling.LANCZOS), (x0,y0))
    draw = ImageDraw.Draw(canvas)
    for n, box in repertoire.items():
        col = ROUGE if n == 'prose' else BLEU
        if (n == 'prose') != prose:
            continue
        clip = [max(x0, min(x0+w, x0+(box[i]-b[0])*f)) if i in (0,2)
                else max(y0, min(y0+h, y0+(box[i]-b[1])*f)) for i in range(4)]
        if clip[2] > clip[0] and clip[3] > clip[1]:
            draw.line((clip[0],clip[3]-2,clip[2],clip[3]-2),fill=col,width=3)
    draw.text((x0,y0-23),annonce,font=dp,fill=ROUGE if prose else BLEU)


def main(cache, fichier):
    refs = json.loads((ICI / 'REPERES.json').read_text())
    result = json.loads((ICI / 'RESULTATS.json').read_text())
    plan = Image.new('RGB',(1454,978),'#faf9f5')
    draw = ImageDraw.Draw(plan)
    f1,f2,f3,f4 = [fonte(n) for n in (32,22,19,16)]
    draw.text((22,12),'Les mots de la prose et la colonne de leur étiquette',font=f1,fill='#202020')
    draw.text((22,58),'Trait pointillé : verticale corrigée passant par le centre du mot.  Chaque cercle gris situe une légende concurrente.',font=f3,fill=GRIS)
    for i, (page, f) in enumerate(refs.items()):
        r = result[page]
        photo = Image.open(cache/'yale'/(page+'.jpg')).convert('RGB')
        X,Y = 22+i*480, 141
        wx,hy = photo.size
        k = min(451/wx, 526/hy)
        im = photo.resize((round(wx*k),round(hy*k)),Image.Resampling.LANCZOS)
        xbase = X + (451-im.width)//2
        plan.paste(im,(xbase,Y))
        def pt(x,y):
            return (xbase+x*k,Y+y*k)
        p = r['prose']
        t = r['etiquettes'][str(f['cible'])]
        lo,hi = sorted([p[1],t[1]])
        for gy in range(int(lo), int(hi)+1, 58):
            ey = min(hi, gy+30)
            draw.line([pt(p[0]-r['pente']*(gy-p[1]),gy),pt(p[0]-r['pente']*(ey-p[1]),ey)], fill=ROUGE,width=2)
        for n,cen in r['etiquettes'].items():
            x,y=pt(*cen)
            col = BLEU if int(n)==f['cible'] else GRIS
            rad = 6 if int(n)==f['cible'] else 3.5
            draw.ellipse((x-rad,y-rad,x+rad,y+rad),outline=col,width=2)
        px,py = pt(*p)
        draw.line((px-5,py,px+5,py),fill=ROUGE,width=3)
        draw.line((px,py-5,px,py+5),fill=ROUGE,width=3)
        titre = page + ('   |   découverte' if i==0 else '   |   prédiction')
        draw.text((X,105),titre,fill='#222222',font=f2)
        lig = f['lignes'][str(f['ligne_prose'])]
        boite_prose = next(t['boite'] for t in lig['repere'] if t['rang']==f['rang_prose'])
        boite_nom = enveloppe(f['lignes'][str(f['cible'])]['repere'])
        bs = {'prose':boite_prose,'cible':boite_nom}
        vignette(plan,photo,X,706,bs,
                 f"Prose {page}.{f['ligne_prose']}  ·  groupe {f['rang_prose']}",True,p,f4)
        vignette(plan,photo,X,822,bs,
                 f"Étiquette {page}.{f['cible']}  ·  {r['mot']}",False,t,f4)
        a,b = r['classements']['redresse'][:2]
        draw.text((X,919),f"Écart   {a['distance']:.0f} px     |     suivante   {b['distance']:.0f} px",fill=GRIS,font=f3)
    plan.save(fichier,quality=91,optimize=True)

if __name__ == '__main__':
    main(Path(sys.argv[1]), ICI/'alignements.jpg')
