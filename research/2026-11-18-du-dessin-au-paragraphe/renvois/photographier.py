"""Reproduire les couloirs et les extrémités depuis les clichés natifs de Yale."""
import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
DEPOT = ICI.parents[2]
VERT = ICI.parents[1] / '2026-11-18-noms-dans-une-phrase/enumeration/verticale/REPERES.json'
INFOS = {'f99r':('1006246',25,18,8,[15]), 'f102v1':('1006253',3,21,3,[19]),
         'f102v2':('1006252',11,39,2,[30,37]), 'f89v2':('1006234',5,7,2,[7])}
RELEVES_89 = {(5,1):(2570,871,2740,964), (4,1):(2220,878,2454,960),
              (7,2):(858,1143,1007,1210), (7,1):(693,1098,850,1211)}


def fonte(n):
    for nom in ('/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf'):
        try: return ImageFont.truetype(nom,n)
        except OSError: pass
    return ImageFont.load_default()


def centre(b):
    return (b[0]+b[2])/2, (b[1]+b[3])/2


def charger_boites():
    registre=json.loads(VERT.read_text())
    fiches={}
    for page,(oid,lab,lig,slot,incipit) in INFOS.items():
        def boite(i,j):
            if page=='f89v2':
                return list(RELEVES_89[i,j])
            return next(r['boite'] for r in registre[page]['lignes'][str(i)]['repere'] if r['rang']==j)
        cases=[]
        for dec in (0,1):
            cases.append({'type':'témoin' if dec else 'reprise','légende':f'{page}.{lab-dec}',
                          'boîte_légende':boite(lab-dec,1),'prose':f'{page}.{lig}/{slot-dec}',
                          'boîte_prose':boite(lig,slot-dec)})
        fiches[page]={'oid':oid,'paires':cases,'incipit':{str(n):boite(n,1) for n in incipit}}
    return fiches


def corridor(photo,depart,fin):
    ax,ay=centre(depart); bx,by=centre(fin)
    longueur=math.hypot(bx-ax,by-ay)
    ux,uy=(bx-ax)/longueur,(by-ay)/longueur
    largeur=math.ceil(longueur)+160
    # La légende arrive à x=80, le mot de prose à x=80+longueur.
    transform=(ux,-uy,ax-80*ux+80*uy,uy,ux,ay-80*uy-80*ux)
    return photo.transform((largeur,160),Image.Transform.AFFINE,transform,Image.Resampling.BICUBIC)


def copier_reduit(canevas,im,box):
    im=im.copy()
    im.thumbnail((box[2],box[3]),Image.Resampling.LANCZOS)
    x=box[0]+(box[2]-im.width)//2
    y=box[1]+(box[3]-im.height)//2
    canevas.paste(im,(x,y))
    return x,y,im.width,im.height


def vignettes(fiches,photos,sortie):
    output = Image.new('RGB',(1450,1117),'#faf9f5')
    d = ImageDraw.Draw(output)
    d.text((22,12),'Peut-on suivre un repère entre une légende et le texte ?',fill='#252525',font=fonte(30))
    d.text((24,61),'Bleu : légende    ·    Bordeaux : mot repris dans la prose    ·    Les photographies ne portent aucun trait ajouté entre ces points.',fill='#424242',font=fonte(19))
    for i,(page,f) in enumerate(fiches.items()):
        x=18+i*358
        im=photos[page]
        cl=f['paires'][0]
        d.text((x,102),page,fill='#222222',font=fonte(23))
        ax,ay,w,h=copier_reduit(output,im,(x,140,338,472))
        for q,c in [('boîte_légende','#006b95'),('boîte_prose','#af3428')]:
            cx,cy=centre(cl[q])
            X,Y=ax+cx*w/im.width,ay+cy*h/im.height
            d.ellipse((X-6,Y-6,X+6,Y+6),outline=c,width=2)
        for j,(champ,tit) in enumerate([('boîte_légende',cl['légende']),('boîte_prose',cl['prose'])]):
            px,py=centre(cl[champ])
            y=642+j*137
            d.text((x,y-26),tit,fill='#006b95' if j==0 else '#af3428',font=fonte(17))
            vv=im.crop((px-195,py-59,px+195,py+59)).resize((333,101),Image.Resampling.LANCZOS)
            output.paste(vv,(x,y))
        initbox=f['incipit'][next(iter(f['incipit']))]
        px,py=initbox[0],centre(initbox)[1]
        d.text((x,894),f"Début du paragraphe, ligne {next(iter(f['incipit']))}",fill='#333333',font=fonte(17))
        vv=im.crop((px-135,py-75,px+255,py+75)).resize((333,128),Image.Resampling.LANCZOS)
        output.paste(vv,(x,924))
    d.text((22,1070),'Les extrémités sont agrandies à une échelle commune. Le premier cliché et celui de f89v2 appartiennent à deux feuillets distincts du dépliant f102.',fill='#444444',font=fonte(17))
    output.save(sortie/'renvois.jpg',quality=91,optimize=True)


def detail(fiches,photos,out):
    for page,f in fiches.items():
        im=photos[page]
        im.copy().resize((int(1350*im.width/im.height),1350),Image.Resampling.LANCZOS).save(out/(page+'-vue.jpg'),quality=95)
        for i,cas in enumerate(f['paires']):
            a,b=cas['boîte_légende'],cas['boîte_prose']
            corridor(im,a,b).save(out/(page+'-'+str(i)+'-couloir.jpg'),quality=96)
            for n,rect in [('legende',a),('prose',b)]:
                x,y=centre(rect)
                im.crop((x-260,y-130,x+260,y+130)).save(out/(page+'-'+str(i)+'-'+n+'.jpg'),quality=95)
        for n,rect in f['incipit'].items():
            x,y=rect[0],centre(rect)[1]
            im.crop((max(0,x-650),y-145,x+680,y+165)).save(out/(page+'-debut-'+n+'.jpg'),quality=95)
    e=photos['f103v'].copy()
    e.thumbnail((1020,1200))
    e.save(out/'f103v.jpg',quality=93)


def bande(fiches,photos,out):
    plan=Image.new('RGB',(1390,1248),'#faf9f5')
    dr=ImageDraw.Draw(plan)
    dr.text((20,12),'Les huit trajets examinés dans la photographie',font=fonte(29),fill='#222222')
    dr.text((20,57),'Le couloir (largeur native de 160 px) est tourné de la légende, à gauche, vers le mot de prose, à droite. Les 80 px à chaque extrémité gardent le contexte.',font=fonte(17),fill='#444444')
    for i,(page,f) in enumerate(fiches.items()):
        for j,cas in enumerate(f['paires']):
            y=104+(i*2+j)*142
            a,b=cas['boîte_légende'],cas['boîte_prose']
            c=corridor(photos[page],a,b)
            dr.text((22,y),f"{cas['type'].capitalize()}   {cas['légende']}  →  {cas['prose']}",font=fonte(17),fill='#222222')
            # Doubler la lisibilité des deux petites bandes f99 par rapport à une mise à l'échelle globale.
            facteur=min(1.0,1320/c.width,103/c.height)
            c=c.resize((round(c.width*facteur),round(c.height*facteur)),Image.Resampling.LANCZOS)
            plan.paste(c,(22,y+27))
    plan.save(out/'couloirs.jpg',quality=92,optimize=True)


def points_materiels(photos,out):
    plan=Image.new('RGB',(1300,755),'#faf9f5')
    d=ImageDraw.Draw(plan)
    d.text((20,12),'Un contact entre lettres et deux vues de la même tache',font=fonte(28),fill='#222222')
    vues=[('f99r',(1665,1030,1945,1250),(20,109,430,310),'f99r.18 au-dessus de f99r.25'),
          ('f99r',(1790,1105,1860,1160),(492,109,334,302),'Détail du contact'),
          ('f99r',(1785,1155,1905,1240),(864,109,396,302),'Descendantes de la légende inférieure'),
          ('f102v1',(200,748,480,968),(20,463,356,240),'f102v1, marge du pot'),
          ('f103v',(130,788,410,1008),(428,463,356,240),'Même emplacement visible sous f103v'),
          ('f103v',(394,135,674,355),(855,463,356,240),'Étoile dans la marge de f103v')]
    for page,box,(x,y,w,h),nom in vues:
        d.text((x,y-28),nom,font=fonte(18),fill='#333333')
        im=photos[page].crop(box)
        target=min(w/im.width,h/im.height)
        im=im.resize((round(target*im.width),round(target*im.height)),Image.Resampling.NEAREST if nom=='Détail du contact' else Image.Resampling.LANCZOS)
        plan.paste(im,(x,y))
    plan.save(out/'contacts-et-marques.jpg',quality=94,optimize=True)


def interligne_f99(photo,out):
    loci=json.loads(VERT.read_text())['f99r']['lignes']
    plan=Image.new('RGB',(1508,897),'#faf9f5')
    d=ImageDraw.Draw(plan)
    d.text((18,10),'f99r : la ligne 18 au-dessus des huit légendes de la même rangée',font=fonte(29),fill='#222222')
    d.text((18,54),'Deux lignes sont visibles dans chaque détail. La barre en marge inférieure situe la largeur de la légende.',font=fonte(18),fill='#454545')
    for i in range(8):
        row=loci[str(i+20)]['repere'][0]
        b=row['boite'];x,y=centre(b)
        px=14+373*(i%4);py=118+249*(i//4)
        d.text((px,py-24),f"f99r.{i+20}    {row['mot_H']}",font=fonte(17),fill='#252525')
        frame=(round(x-151),round(y-120),round(x+151),round(y+44))
        im=photo.crop(frame).resize((360,196),Image.Resampling.LANCZOS)
        plan.paste(im,(px,py))
        d.line((px+(b[0]-frame[0])*360/302,py+201,px+(b[2]-frame[0])*360/302,py+201),fill='#4d6774',width=3)
    cas = [('Sans signe de jonction : .18/3 et .21', (839,1060,929,1138)),
           ('Groupes différents : .18/6 et .24', (1454,1070,1532,1167)),
           ('Groupes identiques : .18/8 et .25', (1790,1101,1866,1160))]
    for k,(nom,box) in enumerate(cas):
        x=20+k*493
        d.text((x,608),nom,font=fonte(19),fill='#252525')
        im=photo.crop(box)
        im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
        plan.paste(im,(x+68,643))
    plan.save(out/'interligne-f99r.jpg',quality=95,optimize=True)


def main(cache,out,inspection):
    reg=json.loads((DEPOT/'voynich_resources/yale/image_index.json').read_text())
    fiches=charger_boites(); photos={}
    for page,oid in [(s,v['oid']) for s,v in fiches.items()]+[('f103v','1006255')]:
        ent=next(x for x in reg if f'/{oid}/' in x['url'])
        chemin=cache/(oid+'.jpg')
        assert sha256(chemin.read_bytes()).hexdigest()==ent['sha256']
        photos[page]=Image.open(chemin).convert('RGB')
        if page in fiches:
            fiches[page].update({'url':ent['url'],'sha256':ent['sha256'],'dimensions':list(photos[page].size)})
    (out/'REPERES.json').write_text(json.dumps(fiches,indent=2,ensure_ascii=False)+'\n')
    vignettes(fiches,photos,out)
    bande(fiches,photos,out)
    points_materiels(photos,out)
    interligne_f99(photos['f99r'],out)
    if inspection:
        inspection.mkdir(exist_ok=True,parents=True)
        detail(fiches,photos,inspection)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('cache',type=Path)
    p.add_argument('--inspection',type=Path)
    a=p.parse_args()
    main(a.cache,ICI,a.inspection)
