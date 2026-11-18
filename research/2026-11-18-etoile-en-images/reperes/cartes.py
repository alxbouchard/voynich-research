"""Reproduce the anonymous diagram cards from two original Yale JPEG images."""
import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parent
SOURCES = {
    'f67r1': {'oid': '1006194', 'sha256': '0518312a566ee713a46c9887d8b8b9d7141d14095e360661789c1dad9b5c0d1c', 'size': [4972, 3738], 'center': [1302, 1850]},
    'f68v2': {'oid': '1006197', 'sha256': '06d33798cd4f901771b9869078d3f29f7e7ef5a490a9abc6dd09f3a3adec867f', 'size': [8135, 3843], 'center': [4550, 1693]},
}

# Coordinates transcribed from the photograph, clockwise from North.
# f67r1: midpoint of the written compartment; center line, inner and outer
# selected radii of the next illustrated compartment. Units are native pixels.
F67 = [
    (0, 12, 653, 837), (26, 38, 665, 857), (52, 66, 634, 864),
    (82, 96, 653, 894), (112, 126.5, 657, 922), (143, 159.2, 666, 953),
    (177, 192.4, 670, 956), (206, 220.2, 672, 956), (236, 250.0, 648, 950),
    (265, 279.1, 627, 920), (296, 309.6, 619, 901), (327, 342.0, 614, 867),
]
# Entire sample at a common radius, without assigning reference labels.
F68 = [20.5, 44.85, 68.7, 106.6, 123.0, 141.9, 184.9, 206.6, 225.7, 284.5, 311.7, 339.3]


def original(path, meta):
    path = Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != meta['sha256']:
        raise ValueError(f'Unexpected pixels for Yale {meta["oid"]}')
    return Image.open(path).convert('RGB')


def radial_crop(im, center, angle, low, high, width):
    angle = math.radians(angle)
    sin, cos = math.sin(angle), math.cos(angle)
    # Output x goes clockwise across the radial direction, output y inward.
    x0 = center[0] + high * sin - width / 2 * cos
    y0 = center[1] - high * cos - width / 2 * sin
    return im.transform((width, high-low), Image.Transform.AFFINE,
                        (cos, -sin, x0, sin, cos, y0), Image.Resampling.NEAREST)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('yale_1006194')
    parser.add_argument('yale_1006197')
    args = parser.parse_args()
    ims = {p: original(path, SOURCES[p]) for p, path in zip(SOURCES, vars(args).values())}
    rng = random.Random(18671168)
    keys = {}
    for panel, specs in [('f67r1', F67), ('f68v2', F68)]:
        ids = list(range(1, 13))
        rng.shuffle(ids)
        cards = []
        for i, (spec, ident) in enumerate(zip(specs, ids)):
            if panel == 'f67r1':
                axis, ang, low, high = spec
                locus = f'f67r1.{8+i}'
                alternative = f'f67r1.{8+(i+1)%12}'
                label = 'A'
                width = 170
            else:
                axis = ang = spec
                low, high, width = 505, 685, 160
                locus = f'f68v2.{7+i}'
                alternative = None
                label = 'B'
            name = f'{label}{ident:02d}'
            crop = radial_crop(ims[panel], SOURCES[panel]['center'], ang, low, high, width)
            keys[name] = {'locus': locus, 'alternative_locus': alternative, 'axis_written_degrees': axis,
                          'card_axis_degrees': ang, 'radii_native': [low, high], 'width_native': width}
            cards.append((name, crop))
        cards.sort(key=lambda item: item[0])
        sheet = Image.new('RGB', (800, 960), 'white')
        draw = ImageDraw.Draw(sheet)
        for j, (name, crop) in enumerate(cards):
            x, y = (j%4)*200, (j//4)*320
            sheet.paste(crop, (x+(200-crop.width)//2, y+28+(284-crop.height)//2))
            draw.text((x+8, y+6), name, fill='black')
        sheet.save(BASE / f'cartes-{label}.png')
    result = {'angle_zero': 'north', 'angle_positive': 'clockwise', 'origin': 'top left native image',
              'sources': SOURCES, 'cards': dict(sorted(keys.items()))}
    (BASE/'cle.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()
