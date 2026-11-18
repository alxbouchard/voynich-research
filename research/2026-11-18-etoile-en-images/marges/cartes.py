"""Cartes de lecture anonymes. Seuls les premiers groupes écrits servent au repérage."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SALT = 'q20-marge-18-nov-2026'
CELL = (494,245)
MIST = (219,246,248)
BOUND = (12,111,136)
AXIS = (112,27,119)


def hashfile(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def axis_measure(im, words, body_boxes=None):
    # Extraction uniquement dans les boîtes du texte. Les points utilisés ne traversent
    # pas la marge. Limiter le tracé aux premiers 370 pixels de la ligne.
    x0 = min(p[0] for p in words[0]['quadrilatere_yale'])
    points = []
    for word in words:
        q = np.asarray(word['quadrilatere_yale'])
        l,t = np.floor(q.min(axis=0)).astype(int)
        r,b = np.ceil(q.max(axis=0)).astype(int)
        if l >= x0+370:
            break
        r = min(r, int(x0+370))
        if r-l<25:
            continue
        if body_boxes and word['slot'] in body_boxes:
            # Contrôle géométrique du corps du groupe sur le texte seul.
            t,b=body_boxes[word['slot']]
        ink = im[t:b, l:r]
        smooth = np.convolve(ink.mean(axis=1), np.ones(7)/7, mode='same')
        start = 0 if body_boxes and word['slot'] in body_boxes else int(ink.shape[0]*.40)
        peak = start + np.argmax(smooth[start:])
        for a in range(4, r-l-20, 35):
            tile = ink[max(0,peak-13):min(b-t,peak+16), a:min(a+35,r-l)]
            ys,xs = np.where(tile)
            if len(xs) < 30:
                continue
            # 85e centile de l'encre du corps, afin d'ignorer les hampes et jambages.
            points.append((l+a+float(np.median(xs)), t+max(0,peak-13)+float(np.percentile(ys,85))))
    p = np.asarray(points)
    assert len(p)>=4,(words,points)
    slopes = [(y2-y1)/(x2-x1) for i,(x1,y1) in enumerate(p) for x2,y2 in p[i+1:] if x2-x1>=75]
    slope = float(np.median(slopes))
    intercept = float(np.median(p[:,1]-slope*p[:,0]))
    spans = p[:,1]-slope*p[:,0]-intercept
    return dict(x_premier=float(x0),pente=slope,ordonnee_origine=intercept,
                points=[[round(float(x),2),round(float(y),2)] for x,y in p],
                ecart_p90_interne_px=round(float(np.percentile(np.abs(spans),90)),2))


def pool_slopes(lines, block):
    common=float(np.median([lines[k]['pente'] for k in block]))
    for k in block:
        line=lines[k]
        line['pente_individuelle']=line['pente']
        line['ordonnee_individuelle']=line['ordonnee_origine']
        px,py=np.array(line['points']).T
        line['pente']=common
        line['ordonnee_origine']=float(np.median(py-common*px))
        line['ecart_p90_commun_px']=round(float(np.percentile(np.abs(py-common*px-line['ordonnee_origine']),90)),2)


def at(line, x):
    return line['ordonnee_origine']+line['pente']*x


def getfont(size):
    # Version TrueType de la police embarquée dans Pillow.
    return ImageFont.load_default(size=size)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--photos',type=Path,default=HERE/'cache/yale')
    ap.add_argument('--placement-initial',action='store_true',help='Reproduire la version antérieure au contrôle des résidus.')
    ap.add_argument('--calages',type=Path,default=HERE/'calages.json')
    ap.add_argument('--sortie',type=Path,default=HERE)
    args=ap.parse_args()
    out=args.sortie
    out.mkdir(exist_ok=True,parents=True)
    cal=json.loads(args.calages.read_text())['folios']
    pred=json.loads((HERE.parent/'PREDICTIONS.json').read_text())['paires_marge']
    locs=[(p[k],k) for p in pred for k in ('lieu','temoin')]
    locs.sort(key=lambda z:hashlib.sha256((SALT+'|'+z[0]).encode()).digest())
    codes={l:(f'S{i:02}',role) for i,(l,role) in enumerate(locs,1)}
    assert len(codes)==18
    contact=Image.new('RGB',(3*CELL[0],6*CELL[1]),'white')
    key={}
    for f, finfo in cal.items():
        source=args.photos/(f+'.jpg')
        assert hashfile(source)==finfo['sha256']['yale']
        im=Image.open(source).convert('RGB')
        gray=np.array(im)[:,:,1].copy()
        local_bg=cv2.GaussianBlur(gray,(0,0),10)
        ink=(local_bg.astype(float)-gray)>21
        lines={}
        for ns,data in finfo['lignes'].items():
            # Le grand rectangle du 2e groupe de cette ligne inclut la hampe suivante.
            window={2:(2310,2350)} if (f,ns)==('f105v','31') and not args.placement_initial else None
            lines[int(ns)]=axis_measure(ink,data['mots'],window)
        # Les trois voisines partagent l'inclinaison locale du bloc. Rassembler les
        # pentes réduit l'instabilité d'une extrapolation depuis 1 ou 2 mots seulement.
        block=[]
        for k in sorted(lines):
            if block and k != block[-1]+1:
                pool_slopes(lines,block)
                block=[]
            block.append(k)
        pool_slopes(lines,block)
        for n,line in lines.items():
            loc=f+'.'+str(n)
            if loc not in codes:
                continue
            code,role=codes[loc]
            prev=lines.get(n-1)
            nex=lines[n+1]
            # Inclure une petite amorce écrite. La limite commune aux trois lignes empêche
            # de dévoiler des groupes complets, même en cas de retrait de paragraphe.
            neighbors=[k for k in (n-1,n,n+1) if k in lines]
            end=int(min(lines[k]['x_premier'] for k in neighbors))+40
            left=0
            def y(l,x):
                return at(l,x)
            def upper(x):
                if prev:
                    return (y(line,x)+y(prev,x))/2
                return 0
            def lower(x):
                return (y(line,x)+y(nex,x))/2
            X=[left,end]
            top=0 if prev is None else max(0,math.floor(min(y(prev,x)-.45*(y(line,x)-y(prev,x)) for x in X)))
            bottom=min(im.height,math.ceil(max(y(nex,x)+.45*(y(nex,x)-y(line,x)) for x in X)))
            assert all(lower(x)-y(line,x)>14 and y(line,x)-upper(x)>14 for x in X)
            meta=dict(lieu=loc,statut=role,boite_native=[left,top,end,bottom],
                      quadrilatere_couloir=[[x,round(upper(x),2)] for x in X]+[[x,round(lower(x),2)] for x in reversed(X)],
                      axe=[[x,round(y(line,x),2)] for x in X],
                      voisine_haute=n-1 if prev else None,voisine_basse=n+1,
                      premiere_ligne=prev is None,
                      mesures={str(k):lines[k] for k in neighbors})
            crop=im.crop((left,top,end,bottom))
            # La photo est intégrale à gauche; la bande neutre à droite masque les
            # caractères à plus de 30 pixels du premier mot sur chacune des lignes.
            pix=np.array(crop)
            for k in neighbors:
                if lines[k]['x_premier']+30>=end:
                    continue
                cut=math.floor(lines[k]['x_premier']+30)
                for x in range(max(left,cut),end):
                    ymid=at(lines[k],x)
                    all_y=[at(lines[j],x) for j in neighbors]
                    pos=neighbors.index(k)
                    lo=top if pos==0 else (ymid+all_y[pos-1])/2
                    hi=bottom if pos==len(all_y)-1 else (ymid+all_y[pos+1])/2
                    pix[max(0,int(lo-top)):max(0,math.ceil(hi-top)),x-left]=(240,239,235)
            crop=Image.fromarray(pix)
            # Agrandir/réduire de manière isotrope et laisser deux gouttières pour repères.
            w,h=crop.size
            cw,ch=CELL
            s=min((cw-37)/w,(ch-31)/h)
            rw,rh=round(w*s),round(h*s)
            crop=crop.resize((rw,rh),Image.Resampling.LANCZOS)
            panel=Image.new('RGB',CELL,'#f7f7f4')
            ox,oy=(cw-rw)//2,23+(ch-27-rh)//2
            meta['rectangle_photo_sur_carte']=[ox,oy,ox+rw,oy+rh]
            # Sensibilité des bissectrices si chaque ligne utilise sa propre pente.
            def solo(k,x):
                v=lines[k]
                return v['pente_individuelle']*x+v['ordonnee_individuelle']
            hi=[(solo(n-1,x)+solo(n,x))/2 if prev else 0.0 for x in X]
            lo=[(solo(n+1,x)+solo(n,x))/2 for x in X]
            alt=[[x,round(y,2)] for x,y in zip(X,hi)]+[[x,round(y,2)] for x,y in zip(X[::-1],lo[::-1])]
            meta['couloir_pentes_individuelles_sensibilite']=alt
            meta['deplacement_bords_pentes_individuelles_px']=[round(p[1]-q[1],2) for p,q in zip(alt,meta['quadrilatere_couloir'])]
            panel.paste(crop,(ox,oy))
            dr=ImageDraw.Draw(panel)
            dr.text((8,2),code,font=getfont(18),fill='#141d29')
            for ximg,dx,xpix in [(left,1,ox),(end,-1,ox+rw-1)]:
                for val,col,ln in [(y(line,ximg),AXIS,12),(lower(ximg),BOUND,7)]+([(upper(ximg),BOUND,7)] if prev else []):
                    yy=oy+round((val-top)*rh/h)
                    dr.line((xpix-dx*ln,yy,xpix+dx*3,yy),fill=col,width=2)
            # Pointillés très fins aux deux bissectrices, sans trace sur l'axe cible.
            for fn in [lower]+([upper] if prev else []):
                for xp in range(9,rw-1,17):
                    xx=left+xp*w/rw
                    yy=oy+round((fn(xx)-top)*rh/h)
                    dr.point((ox+xp,yy),fill=BOUND)
                    dr.point((ox+xp+1,yy),fill=MIST)
            dr.rectangle((0,0,cw-1,ch-1),outline='#c4c7c6')
            dest=out/(code+'.png')
            panel.save(dest)
            ix=int(code[1:])-1
            contact.paste(panel,((ix%3)*cw,(ix//3)*ch))
            key[code]={**meta,'carte_sha256':hashfile(dest)}
    contact.save(out/'CONTACT.jpg',quality=92,subsampling=0)
    (out/'cle.json').write_text(json.dumps({k:key[k] for k in sorted(key)},indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
