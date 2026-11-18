"""Deux vues ouvertes après la préparation du lot de lecture."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image,ImageDraw,ImageFont

from localiser import HERE,H_PATH,align_words,transformed,sha

W=1460
teal='#075a65'
ink='#19282e'
gray='#46585c'


def label(draw,xy,txt,n,color=ink):
    for face in ('/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(face).is_file():
            draw.text(xy,txt,font=ImageFont.truetype(face,n),fill=color)
            return
    raise FileNotFoundError("Police latine requise pour les légendes.")


def rect_bounds(q,pad):
    return [math.floor(q[:,0].min())-pad,math.floor(q[:,1].min())-pad,
            math.ceil(q[:,0].max())+pad,math.ceil(q[:,1].max())+pad]


def place(board,im,box,target):
    crop=im.crop(box)
    l,t,r,b=target
    sc=min((r-l)/crop.width,(b-t)/crop.height)
    w,h=round(crop.width*sc),round(crop.height*sc)
    board.paste(crop.resize((w,h),Image.Resampling.LANCZOS),(l,t))
    return lambda x,y:(l+(x-box[0])*w/crop.width,t+(y-box[1])*h/crop.height)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--photos',type=Path,default=HERE/'cache/yale')
    p.add_argument('--cache',type=Path,default=HERE/'cache')
    p.add_argument('--h',type=Path,default=H_PATH)
    p.add_argument('--sortie',type=Path,default=HERE)
    args=p.parse_args()
    src=json.loads((HERE/'calages.json').read_text())
    assert sha(args.h)==src['transcription_sha256']
    archive=args.cache/'voynichese_data.zip'
    assert sha(archive)==src['archive_xml']['sha256']
    key=json.loads((HERE/'cle.json').read_text())
    board=Image.new('RGB',(W,950),'#f7f6f0')
    dr=ImageDraw.Draw(board)
    label(dr,(21,12),'Le groupe transcrit otor et la marge de la même ligne',33)
    label(dr,(23,58),'Manuscrit Beinecke 408, Yale University Library. Le cadre vert repère le groupe dans la bande continue.',20,gray)
    details={}
    for i,(f,n,slot) in enumerate([('f107r',1,5),('f104r',19,10)]):
        d=src['folios'][f]
        yale=args.photos/(f+'.jpg')
        layout=args.cache/(f+'.json')
        assert sha(yale)==d['sha256']['yale'] and sha(layout)==d['sha256']['layout']
        im=Image.open(yale).convert('RGB')
        words=align_words(f,archive,layout,args.h)[n]
        m=np.array(d['affine_v2_vers_yale'])
        def quad(w):
            x,y,r,b=w['boite_v2']
            return transformed([[x,y],[x+r,y],[x+r,y+b],[x,y+b]],m)
        target=next(w for w in words if w['slot']==slot)
        assert target['mot']=='otor'
        q=quad(target)
        union=np.concatenate([quad(w) for w in words])
        bb=rect_bounds(union,21); bb[0]=0
        code,card=next((k,v) for k,v in key.items() if v['lieu']==f+'.'+str(n))
        left=card['boite_native'].copy()
        # Cette vue ouverte conserve entièrement l'emplacement de la carte de marge.
        # Rogner le haut vide de la première ligne seulement dans l'agrandissement.
        if n==1:
            left[1]=max(left[1],math.floor(min(y for _,y in card['axe'])-100))
        bb[1]=max(0,min(bb[1],left[1]));bb[3]=max(bb[3],left[3])
        if n==1:
            bb[3]=min(bb[3],math.ceil(max(y for _,y in card['axe'])+48))
        if n==19:
            bb[3]=min(bb[3],math.ceil(union[:,1].max())+21)
        bword=rect_bounds(q,12)
        y=106+423*i
        label(dr,(23,y),f'{f}  ·  Ligne {n}  ·  Groupe {slot} dans IT2a',26)
        cy=y+40
        project=place(board,im,bb,(23,cy,W-23,cy+142))
        poly=[project(*p) for p in np.vstack([q,q[0]])]
        dr.line(poly,fill=teal,width=2)
        label(dr,(23,cy+154),'Marge au départ de la ligne',19,gray)
        label(dr,(681,cy+154),'Groupe encadré',19,gray)
        leftmap=place(board,im,left,(23,cy+182,643,cy+355))
        place(board,im,bword,(681,cy+182,1100,cy+355))
        # Deux tirets extérieurs marquent le niveau choisi sur le détail de marge.
        for x,yn in card['axe']:
            px,py=leftmap(x,yn)
            side=1 if x==0 else -1
            dr.line([(px-3*side,py),(px+6*side,py)],fill='#702577',width=3)
        details[f+'.'+str(n)]={'rang_IT2a':slot,'groupe':target['mot'],'indice_voynichese':target['indice'],
                  'quadrilatere_groupe_yale':q.round(2).tolist(),'bande_yale':bb,'detail_marge_yale':left,
                  'detail_groupe_yale':bword,'carte_associee':code,'yale_url':d['urls']['yale'],'yale_sha256':sha(yale)}
        if i==0:
            dr.line((23,y+409,W-23,y+409),fill='#bfcbc6',width=1)
    dest=args.sortie/'CONTEXTE.jpg'
    board.save(dest,quality=94,subsampling=0)
    (args.sortie/'contexte.json').write_text(json.dumps(dict(image_sha256=sha(dest),lieux=details),ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
