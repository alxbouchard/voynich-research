"""Extract anonymized rubric images from Yale IIIF 1006194, native 4972 by 3738.
Usage: python3 prepare_cards.py original.jpg output_directory
Requires Pillow, NumPy and SciPy. Coordinates in unmirrored native image.
"""
import argparse
import csv
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

CENTER = (3660,1490)
# Clockwise angles from the top of the Yale photo. Negative values are NW.
RUBRICS = [
    ("J6",1,-81,-59),("P4",2,-54,-25),("D8",3,-14,6),
    ("W3",4,11,36),("N9",5,42,64),("G2",6,70,83),
    ("V7",7,92,124),("K3",8,133,149),("T5",9,159,179),
    ("H8",10,191,217),("R2",11,223,251),("B5",12,253,278)]
# Two excerpts of the separate red line beneath the diagram; same folio, ink and hand.
CONTROLS = [("F7",(2717,2779,3162,2878)),("M4",(3491,2779,3955,2878))]

def ring(image,t1,t2,r1,r2):
    from scipy.ndimage import map_coordinates

    width = round(math.radians(t2-t1)*(r1+r2)/2)
    theta, radius = np.meshgrid(np.deg2rad(np.linspace(t1,t2,width)), np.arange(r2,r1-1,-1))
    xx = CENTER[0]+radius*np.sin(theta)
    yy = CENTER[1]-radius*np.cos(theta)
    return Image.fromarray(np.stack([map_coordinates(image[:,:,i],(yy,xx),order=1)
                                     for i in range(3)],axis=2))

def run(source,out):
    out.mkdir(parents=True,exist_ok=True)
    im=Image.open(source).convert("RGB")
    if im.size != (4972,3738):
        raise ValueError(f"Expected Yale's native dimensions, found {im.size}")
    pixels=np.array(im)
    cards={code:ring(pixels,t1,t2,1023,1165) for code,_,t1,t2 in RUBRICS}
    cards.update({code:im.crop(box) for code,box in CONTROLS})
    for code,img in cards.items():
        img.save(out/f"{code}.png")
    for j,group in enumerate((sorted(cards)[:7], sorted(cards)[7:])):
        sheet=Image.new("RGB",(650,7*114),"white")
        draw=ImageDraw.Draw(sheet)
        for row,code in enumerate(group):
            img=cards[code].copy()
            img.thumbnail((570,109))
            y=114*row
            draw.text((10,y+45),code,fill="black")
            sheet.paste(img,(60,y+(114-img.height)//2))
        sheet.save(out/f"planche-{j+1}.jpg",quality=89)
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    run(args.source,args.out)
