"""Refaire les huit cartes utilisées pour coter les gestes, avec les rectangles du visualiseur."""
from argparse import ArgumentParser
from hashlib import sha256
from math import floor, ceil
from pathlib import Path
import json
from PIL import Image, ImageDraw
from planches import police

ICI=Path(__file__).resolve().parent
FACES=['f77r','f77v','f82r','f82v','f75v','f80r','f83v','f84r']


def bloc(w,mat):
    x,y,larg,haut=w
    coins=[(i,j) for i in (x,x+larg) for j in (y,y+haut)]
    a,b=mat[:2]
    xx=[a[0]*i+a[1]*j+a[2] for i,j in coins];yy=[b[0]*i+b[1]*j+b[2] for i,j in coins]
    return floor(min(xx)),floor(min(yy)),ceil(max(xx)),ceil(max(yy))


def generer(yale,layout,dossier):
    cot=json.loads((ICI/'COTATION.json').read_text());cal=json.loads((ICI/'CALAGE.json').read_text())
    board=Image.new('RGB',(1600,1130),'white');leg=ImageDraw.Draw(board)
    for i,f in enumerate(FACES):
        j=layout/(f+'.json');imfile=yale/(f+'.jpg')
        assert sha256(j.read_bytes()).hexdigest()==cal[f]['repere_sha256']
        assert sha256(imfile.read_bytes()).hexdigest()==cot['source_images'][f]['yale_sha256']
        im=Image.open(imfile).convert('RGB');g=ImageDraw.Draw(im);mat=cal[f]['matrice_vers_Yale']
        for entree in json.loads(j.read_text())[1]:
            x,y,r,b=bloc(entree[1:5],mat);g.rectangle((x-8,y-5,r+8,b+6),fill='#dccdb4')
        for o in cot['objets']:
            if f!=o['face']:continue
            for n,x,y,r,b in o['boites']:
                g.rectangle((x-5,y-2,r+5,b+2),outline='#a2116a',width=5)
                g.text(((x+r)//2,(y+b)//2),n.split('.')[1],anchor='mm',font=police(32),fill='#730744')
        if dossier:
            dossier.mkdir(parents=True,exist_ok=True)
            im.save(dossier/(f+'-masque.jpg'),quality=95)
        im.thumbnail((392,516),Image.Resampling.LANCZOS)
        x=i%4*400;y=i//4*565;board.paste(im,(x+(400-im.width)//2,y+39))
        leg.text((x+200,y+18),f,anchor='mm',font=police(24),fill='black')
    board.save(ICI/'cartes-masquees.jpg',quality=93)


if __name__=='__main__':
    a=ArgumentParser(description=__doc__);a.add_argument('yale',type=Path);a.add_argument('layout',type=Path)
    a.add_argument('--individuelles',type=Path);q=a.parse_args()
    generer(q.yale,q.layout,q.individuelles)
