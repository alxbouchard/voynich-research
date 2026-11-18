"""Reconstitue les observations anonymisées à partir des JPEG natifs de Yale."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
BACKGROUND = (232, 228, 216)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('originaux', type=Path, help='JPEG nommés par face, p. ex. f22r.jpg')
    parser.add_argument('sortie', type=Path)
    args = parser.parse_args()
    args.sortie.mkdir(exist_ok=True, parents=True)
    records = json.loads((HERE/'CLE-CARTES.json').read_text())
    for code, row in records.items():
        source = args.originaux/(row['face']+'.jpg')
        if sha256(source.read_bytes()).hexdigest() != row['sha256_jpeg']:
            raise ValueError(f'Empreinte du JPEG inattendue : {source.name}')
        with Image.open(source) as original:
            bbox = row['cadre']
            crop = original.convert('RGB').crop(bbox)
        polygon = row['polygone_garde']
        if polygon:
            mask = Image.new('L', crop.size)
            ImageDraw.Draw(mask).polygon([(x-bbox[0], y-bbox[1]) for x,y in polygon],fill=255)
            crop = Image.composite(crop, Image.new('RGB',crop.size,BACKGROUND),mask)
        view = ImageOps.contain(crop,(740,570),Image.Resampling.LANCZOS)
        card = Image.new('RGB',(760,590),BACKGROUND)
        card.paste(view,((card.width-view.width)//2,(card.height-view.height)//2))
        card.save(args.sortie/(code+'.jpg'),quality=93,subsampling=0)


if __name__=='__main__':
    main()
