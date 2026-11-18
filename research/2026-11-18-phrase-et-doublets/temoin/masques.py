"""Produire les photos masquées et dévoilées des deux pages à partir des régions IIIF."""
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
parser = ArgumentParser()
parser.add_argument("dossier", type=Path, help="Contient 68.jpg et 70.jpg, régions IIIF natives")
args = parser.parse_args()
for view, left, top in [(68,2262,3577),(70,1424,3752)]:
    original = Image.open(args.dossier / f"{view}.jpg").convert("RGB")
    assert original.size == (2600,1150)
    im = original.copy()
    x, y = left - 500, top - 2850
    draw = ImageDraw.Draw(im)
    draw.rectangle((x-7,y-30,im.width,im.height), fill="black")
    draw.rectangle((0,y+110,im.width,im.height), fill="black")
    im.resize((1300,575)).save(HERE / f"masque-{view}.jpg",quality=90)
    original.resize((1450,round(original.height*1450/original.width))).save(HERE / f"devoile-{view}.jpg",quality=90)
