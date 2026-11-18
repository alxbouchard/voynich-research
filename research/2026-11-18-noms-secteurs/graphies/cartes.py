"""Reproduce the glyph cards from the native Yale photograph 1006194."""
import argparse
import hashlib
import math
from pathlib import Path
from PIL import Image, ImageDraw

EXPECT = "0518312a566ee713a46c9887d8b8b9d7141d14095e360661789c1dad9b5c0d1c"
# Angles east of the top. Bounds in the deskewed sector image.
CARDS = {
 "V": (53,(480,173,534,272),"f67r2.27, dernier signe, m dans H et ZL"),
 "P": (110,(392,568,444,663),"f67r2.58, dernier signe, g dans H et ZL"),
 "F": (23,(476,215,525,289),"f67r2.24, dernier signe, r dans H et ZL"),
 "B4": (-8,(375,289,419,360),"f67r2.21, finale du deuxième groupe, m dans H et ZL"),
 "J7": (53,(432,396,480,494),"f67r2.28, finale à vérifier"),
 "N2": (23,(276,297,334,387),"f67r2.25, finale divergente"),
 "T9": (53,(523,96,564,167),"f67r2.26, dernier signe, r dans H et ZL"),
 "L3": (176,(440,266,488,349),"f67r2.40, finale divergente"),
 "H6": (202,(541,260,591,353),"f67r2.43, finale divergente"),
}

def rotated(im,angle):
    a=math.radians(angle)
    sn,cs=math.sin(a),math.cos(a)
    return im.transform((690,940),Image.Transform.AFFINE,
                        (cs,-sn,3660+1070*sn-345*cs,sn,cs,1490-1070*cs-345*sn),
                        resample=Image.Resampling.BICUBIC)


def generate(source,path):
    assert hashlib.sha256(source.read_bytes()).hexdigest()==EXPECT
    path.mkdir(parents=True,exist_ok=True)
    im=Image.open(source)
    sheet=Image.new("RGB",(555,700),"white")
    draw=ImageDraw.Draw(sheet)
    for j,(k,(a,box,_)) in enumerate(CARDS.items()):
        cut=rotated(im,a).crop(box)
        cut=cut.resize((cut.width*2,cut.height*2),Image.Resampling.LANCZOS)
        cut.save(path/(k+".png"))
        x=185*(j%3); y=230*(j//3)
        draw.text((x+8,y+4),k,fill="black")
        sheet.paste(cut,(x+24,y+24))
    sheet.save(path/"planche.png")
    rotated(im,53).crop((121,80,579,566)).save(path/"secteur.jpg",quality=94)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    generate(args.source,args.out)
