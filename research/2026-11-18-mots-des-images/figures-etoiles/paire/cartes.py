"""Cartes anonymes de f73v. Argument unique : scan Yale 1006207 à 2979 × 3724."""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

source = np.asarray(Image.open(sys.argv[1]).convert("RGB"))
if source.shape[:2] != (3724, 2979):
    raise ValueError("Dimensions inattendues")
# Dérouler la roue avec le haut du feuillet comme origine angulaire.
# Les abscisses du développement suivent la tête, et non la légende.
scale = 2
width = 2200
angles = np.arange(width * scale) * math.tau / (width * scale)
radial = 350 - np.arange(285 * scale)[:, None] / scale
x = np.rint((566 + radial * np.sin(angles)) * 2979 / 1000).astype(int)
y = np.rint((575 - radial * np.cos(angles)) * 3724 / 1251).astype(int)
ring = Image.fromarray(source[y, x])
# (position horizontale de la tête, rayon exprimé comme ordonnée de l'image
# déroulée). Un n° en dehors des deux couronnes complètes n'est pas inclus.
heads = {
    "E": [(41,48),(151,38),(262,46),(357,55),(484,57),(609,56),
          (759,59),(921,56),(1083,65),(1246,63),(1441,68),(1539,67),
          (1682,66),(1823,59),(1968,55),(2135,44)],
    "I": [(148,177),(322,177),(502,179),(719,187),(894,182),(1090,196),
          (1322,190),(1548,181),(1772,174),(2146,177)],
}
# 9 h 30 dans la couronne intérieure est le locus connu f73v.23.
# Le plus près au-dessus du rayon de 9 h ~ 1650 est 1772.
cards = [(band, i, pos) for band, items in heads.items()
         for i, pos in enumerate(items) if (band, i) != ("I", 8)]
random.Random(73023).shuffle(cards)
columns, card_width, card_height = 5, 178, 215
sheet = Image.new("RGB", (columns * card_width, 5 * card_height), "white")
font = ImageFont.load_default(size=18)
painter = ImageDraw.Draw(sheet)
for idx, (band, i, (hx, hy)) in enumerate(cards):
    # Le corps s'incline davantage dans le dépliage du petit rayon.
    if band == "E":
        outline = [(-24,-11),(15,-11),(15,13),(1,30),(-6,49),
                   (-12,61),(-12,76),(-39,79),(-55,57),(-61,45),(-39,20)]
    else:
        outline = [(-37,-12),(29,-12),(23,7),(0,25),(-12,43),
                   (-30,61),(-57,78),(-90,77),(-105,50),(-69,26)]
    # Recadrer autour des tracés du corps, en masquant le reste de la page.
    a, b = min(u for u,v in outline), min(v for u,v in outline)
    c, d = max(u for u,v in outline)+1, max(v for u,v in outline)+1
    sx = ((hx * scale + np.arange(a*scale, c*scale)) % (width*scale))
    sy = hy * scale + np.arange(b*scale, d*scale)
    cut = Image.fromarray(np.asarray(ring)[np.ix_(sy, sx)])
    mask = Image.new("L",cut.size)
    ImageDraw.Draw(mask).polygon([((u-a)*scale,(v-b)*scale) for u,v in outline],fill=255)
    cut = Image.composite(cut, Image.new("RGB",cut.size, "white"), mask)
    cut.thumbnail((card_width-6,card_height-25))
    px,py = (idx%columns)*card_width,(idx//columns)*card_height
    sheet.paste(cut,(px+(card_width-cut.width)//2,py+24))
    painter.text((px+7,py+1), f"{idx+1:02}", font=font,fill="black")
    print(f"{idx+1:02}",band,i+1,hx,hy)
sheet.save(Path(__file__).with_name("f73v-cartes.jpg"), quality=92)
