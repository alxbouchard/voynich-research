"""Reproduce independent black sector views and the labelled overview.
Usage: python3 prepare_sectors.py original.jpg public_photos_folder blind_folder
"""
import argparse
import csv
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from prepare_cards import CENTER, RUBRICS, ring

# An independently inspected set of approximate radial dividers on the native photo.
DIVIDERS = [-89,-58,-23,6,39,67,90,130,158,186,219,248,271]
BLACK_CODES = ["Q8","A3","L7","S4","C6","X9","I2","Z5","U4","E6","O3","Y7"]
# Tangential center of the drawn face, read from the unwrapped image.
FACES = [-72,-39,-8,22,52,82,109,147,175,202,235,263]
def run(source,archive,blind):
    image=Image.open(source).convert("RGB")
    if image.size!=(4972,3738):
        raise ValueError(f"Unexpected source size {image.size}")
    archive.mkdir(parents=True,exist_ok=True)
    blind.mkdir(parents=True,exist_ok=True)
    pixels=np.array(image)
    for i,code in enumerate(BLACK_CODES):
        card=ring(pixels,DIVIDERS[i]+1,DIVIDERS[i+1]-1,490,1020)
        # Width at mean radius; no clipping of original radial extent.
        card.save(blind/f"{code}.jpg",quality=91)
    for j in range(4):
        low=-94+90*j
        cropped=ring(pixels,low,low+100,345,1120)
        cropped=cropped.resize((1000,640),Image.Resampling.LANCZOS)
        draw=ImageDraw.Draw(cropped)
        for angle in range(0,100,5):
            draw.text((10*angle,0),str(low+angle),fill="blue")
        cropped.save(archive/f"secteurs-{j+1}.jpg",quality=83)
    # An unwarped overview, with locations referenced to the Yale original.
    overview=image.crop((2390,290,4890,2770)).resize((680,675),Image.Resampling.LANCZOS)
    draw=ImageDraw.Draw(overview)
    for _,i,left,right in RUBRICS:
        angle=math.radians((left+right)/2)
        x=(CENTER[0]+1197*math.sin(angle)-2390)*680/2500
        y=(CENTER[1]-1197*math.cos(angle)-290)*675/2480
        draw.rounded_rectangle((x-10,y-8,x+10,y+8),radius=2,fill="white")
        draw.text((x,y),str(i),anchor="mm",fill="black")
    overview.save(archive/"vue-native-annotee.jpg",quality=87)
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("source","archive","blind"):
        parser.add_argument(name,type=Path)
    args=parser.parse_args()
    run(args.source,args.archive,args.blind)
