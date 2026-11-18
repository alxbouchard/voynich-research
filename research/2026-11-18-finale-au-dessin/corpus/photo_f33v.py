"""Préparer le détail de la ligne 4 à partir de la vue native de Yale."""
import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
EXPECTED = '41b148c40e9cf73c63044c5415d3c2bbeebffc20153a36762f35e8134da42941'


def panel(page, box):
    x0, y0, x1, y1 = box
    scale = 3
    left, top = 47, 30
    view = page.crop(box).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.Resampling.NEAREST)
    frame = Image.new('RGB', (view.width + left + 17, view.height + top), 'white')
    frame.paste(view, (left, top))
    draw = ImageDraw.Draw(frame)
    for x in range((x0 + 9) // 10 * 10, x1, 10):
        column = left + scale * (x - x0)
        draw.line((column, top - 5, column, top), fill='#435465')
        draw.text((column, top - 20), str(x), anchor='mt', fill='#24384d')
    for y in range((y0 + 9) // 10 * 10, y1, 10):
        row = top + scale * (y - y0)
        draw.line((left - 5, row, left, row), fill='#435465')
        draw.text((left - 9, row), str(y), anchor='rm', fill='#24384d')
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    args = parser.parse_args()
    assert hashlib.sha256(args.original.read_bytes()).hexdigest() == EXPECTED
    page = Image.open(args.original)
    assert page.size == (2871, 3769)
    figure = Image.new('RGB', (1250, 691), 'white')
    draw = ImageDraw.Draw(figure)
    try:
        fonts = [ImageFont.truetype('DejaVuSans.ttf', n) for n in (24, 18)]
    except OSError:
        fonts = [ImageFont.truetype('Arial.ttf', n) for n in (24, 18)]
    title, text = fonts
    draw.text((15, 10), 'f33v, ligne 4 — deux groupes sur la même ligne', font=title, fill='#172a3c')
    context = (590, 895, 1820, 1080)
    figure.paste(page.crop(context), (10, 49))
    for label, (x0, y0, x1, y1) in [('A', (797, 988, 940, 1069)), ('B', (1628, 1012, 1774, 1078))]:
        coords = (x0 - 590 + 10, y0 - 895 + 49, x1 - 590 + 10, y1 - 895 + 49)
        draw.rectangle(coords, outline='#04718a', width=2)
        draw.text((coords[0], coords[1] - 22), label, font=text, fill='#054255', stroke_fill='white', stroke_width=2)
    draw.text((20, 252), 'A   shdy dans le texte', font=title, fill='#172a3c')
    draw.text((650, 252), 'B   shd devant la tige peinte', font=title, fill='#172a3c')
    figure.paste(panel(page, (797, 988, 951, 1098)), (15, 291))
    figure.paste(panel(page, (1628, 1012, 1782, 1122)), (645, 291))
    draw.text((15, 662), 'Axes en pixels de la vue Yale 1006139. Les deux détails ont le même agrandissement.', font=text, fill='#24384d')
    figure.save(HERE / 'f33v-ligne4.jpg', quality=95, subsampling=0)


if __name__ == '__main__':
    main()
