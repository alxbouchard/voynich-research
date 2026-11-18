"""Refabriquer les images des 96 entrées, les vues masquées et quatre rubriques."""
from argparse import ArgumentParser
from pathlib import Path
import json
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
SOURCES={718:(3486,[(485,1750),(1817,3100)]),719:(3420,[(476,1735),(1770,3085)])}

def plates(inputs, mask):
    coords=json.loads((HERE/"COORDONNEES.json").read_text())
    for n,(original_width,columns) in SOURCES.items():
        src=Image.open(inputs/f"ordre-gart-{n}.jpg")
        scale=src.width/original_width
        panel=Image.new("RGB",(1730,1580),"white")
        d=ImageDraw.Draw(panel)
        d.text((8,5),f"Gart der Gesundheit, 1485, BSB 2 Inc.c.a. 1601, vue {n}",fill="black")
        for col,(left,right) in enumerate(columns):
            for i,y in enumerate(coords[f"{n}-{col}"]):
                if mask=="impairs" and i%2==1 or mask=="pairs" and i%2==0:
                    continue
                cut=src.crop(tuple(round(v*scale) for v in (left-45,y-40,right,y+40)))
                x=865*col
                py=31+i*64
                d.text((x+3,py+11),str(i+1),fill="black")
                panel.paste(cut,(x+30,py))
        fname=f"registre-{n}.jpg" if mask=="tous" else f"registre-{n}-{mask}.jpg"
        panel.save((HERE if mask=="tous" else inputs)/fname,quality=86)

def headings(inputs):
    rows=[
        (98, "Chapitre XLIIII, Armoniacum", (338,210,1250,330)),
        (99, "Chapitre XLV, Alumen", (195,178,1130,286)),
        (110,"Chapitre LII, Agnus castus", (338,1315,1235,1440)),
        (112,"Chapitre LIII, Betonica", (338,1275,1240,1400)),
    ]
    panel=Image.new("RGB",(1030,643),"white")
    d=ImageDraw.Draw(panel)
    for j,(n,title,rect) in enumerate(rows):
        src=Image.open(inputs/f"ordre-body-{n}.jpg")
        cut=src.crop(rect)
        d.text((20,j*160+4),f"Vue {n} - {title}",fill="black")
        panel.paste(cut,(20,j*160+30))
    panel.save(HERE/"grandes-rubriques.jpg",quality=91)

if __name__=="__main__":
    parser=ArgumentParser()
    parser.add_argument("sources",type=Path)
    parser.add_argument("--masque",choices=["tous","pairs","impairs"],default="tous")
    args=parser.parse_args()
    plates(args.sources,args.masque)
    if args.masque=="tous":headings(args.sources)
