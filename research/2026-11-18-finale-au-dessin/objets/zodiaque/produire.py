"""Assembler cinq épreuves et deux exemples depuis quatre vues Yale vérifiées."""
import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCES = {
    'lion': ('1006204', 'full', '2552b2eafb7948d182e52ec49e96a5d92a774917924aea594fb1ac3af3bfcdc5'),
    'scorpion': ('1006206', 'full', '5bc8e07dbd61cc1f218cfc4449cd527be118aa7884878ec4c8e568e9c2d89bad'),
    'bain75': ('1006209', '1840,1250,520,800', '7041ed3166a43eae66fba55e01f1befccbebaf94b4742d8612dbaf154ae9ba3d'),
    'bain84': ('1006226', '1550,190,900,700', 'f6eecc9d330c8f4d2016d56d81a27db991e538302aae5786fc25a0981f9df48f'),
    'conduit': ('1006226', '55,1970,360,645', '7868944304d46c91e635881a60d05ed0a24c152bb23ae7d7477a22236c2c55c0'),
}
# Nom, source, rectangle dans le JPEG, rotation antihoraire, rectangle dans la rotation,
# abscisse du centre du troisième signe dans cette rotation.
CARDS = [
    ('Exemple o', 'bain84', (348, 214, 493, 304), 0, (3, 9, 130, 88), 69),
    ('Exemple a', 'conduit', (65, 210, 205, 321), 0, (1, 7, 139, 110), 65),
    ('A', 'scorpion', (873, 550, 1021, 654), 0, (13, 5, 132, 102), 76),
    ('B', 'bain75', (305, 340, 454, 425), 0, (10, 11, 144, 84), 76),
    ('C', 'lion', (1630, 1320, 1855, 1580), -63, (78, 106, 221, 219), 151),
    ('D', 'scorpion', (822, 1012, 1004, 1152), -25, (41, 46, 181, 139), 120),
    ('E', 'lion', (3250, 1720, 3410, 1860), 90, (12, 8, 139, 138), 78),
]


def font(size):
    try:
        return ImageFont.truetype('DejaVuSans.ttf', size)
    except OSError:
        return ImageFont.truetype('Arial.ttf', size)


def card(name, image, box, angle, crop, target):
    view = image.crop(box).rotate(angle, expand=True, resample=Image.Resampling.BICUBIC, fillcolor='white').crop(crop)
    scale = 2
    view = view.resize((view.width * scale, view.height * scale), Image.Resampling.NEAREST)
    result = Image.new('RGB', (320, 337), 'white')
    draw = ImageDraw.Draw(result)
    draw.text((160, 0), name, font=font(21), fill='#132a40', anchor='mt')
    x = (result.width - view.width) // 2
    y = 32 + (264 - view.height) // 2
    result.paste(view, (x, y))
    aim = x + (target - crop[0]) * scale
    bottom = y + view.height
    draw.polygon([(aim, bottom+2),(aim-6,bottom+11),(aim+6,bottom+11)],fill='#00526d')
    draw.line([(aim,bottom+11),(aim,bottom+19)],fill='#00526d',width=2)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for source in SOURCES:
        parser.add_argument('--'+source, type=Path, required=True)
    args = parser.parse_args()
    opened = {}
    for source, (_, _, expected) in SOURCES.items():
        path = getattr(args, source)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, source
        opened[source] = Image.open(path).convert('RGB')
    board = Image.new('RGB', (974, 1051), 'white')
    draw = ImageDraw.Draw(board)
    for i, (name, src, box, angle, crop, target) in enumerate(CARDS):
        panel = card(name, opened[src], box, angle, crop, target)
        if i < 2:
            position = (157 + i*340, 0)
        else:
            j = i-2
            position = (5 + (j%3)*322, 341 + (j//3)*337)
        board.paste(panel, position)
    draw.line((10,332,964,332), fill='#b5bdc3',width=1)
    draw.text((487,1025),'La flèche indique le signe à lire.',font=font(17),fill='#243c4f',anchor='mm')
    board.save(HERE/'cartes.png', optimize=True)


if __name__ == '__main__':
    main()
