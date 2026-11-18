"""Extraire les quatre annotations de mois du JPEG natif Yale de chaque panneau."""
from hashlib import sha256
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'releve.json'


def font(size):
    for family in ('DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def photographies(directory):
    data = json.loads(MANIFEST.read_text())
    w, h = 1024, 278
    plate = Image.new('RGB', (w, h * len(data['observations']) + 26), 'white')
    draw = ImageDraw.Draw(plate)
    for i, row in enumerate(data['observations']):
        raw = directory / (row['oid_yale'] + '.jpg')
        assert sha256(raw.read_bytes()).hexdigest() == row['sha256_jpeg']
        origin = row['boite_contexte']
        bounds = row['boite_mot']
        y = i*h
        with Image.open(raw) as im:
            assert list(im.size) == row['dimensions_natives']
            assert origin[0] <= bounds[0] < bounds[2] <= origin[2]
            assert origin[1] <= bounds[1] < bounds[3] <= origin[3]
            crop = im.crop(bounds)
            crop.save(HERE / row['extrait'])
            assert sha256(crop.convert('RGB').tobytes()).hexdigest() == row['sha256_pixels_extrait_rvb']
            context = im.crop(origin).convert('RGB')
            frame = tuple(n-origin[j % 2] for j,n in enumerate(bounds))
            ImageDraw.Draw(context).rectangle(frame, outline=(185,42,31), width=5)
            context.thumbnail((258,258), Image.Resampling.LANCZOS)
            plate.paste(context, (12+(258-context.width)//2, y+8))
            enlarged = crop.resize((crop.width*2,crop.height*2), Image.Resampling.NEAREST)
            plate.paste(enlarged,(385+(600-enlarged.width)//2,y+(h-enlarged.height)//2))
        draw.text((275,y+83),row['folio'],fill='black',font=font(22))
        draw.text((275,y+119),row['mois_fr'],fill='black',font=font(16))
        draw.line((12,y+h-2,w-12,y+h-2),fill='#bbbbbb',width=1)
    draw.text((12, h*len(data['observations'])+2),
              'Beinecke MS 408, Yale University Library  |  À droite, agrandissement × 2 sans interpolation.',
              fill='black', font=font(15))
    plate.save(HERE/'quatre-annotations.jpg', quality=94, subsampling=0)


if __name__ == '__main__':
    photographies(Path(sys.argv[1]))
