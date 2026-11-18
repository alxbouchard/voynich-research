"""python3 planche.py 1006182.jpg"""
from pathlib import Path
from hashlib import sha256
import sys
from PIL import Image, ImageDraw, ImageFont

p = Path(sys.argv[1])
assert sha256(p.read_bytes()).hexdigest() == '24e4b496a7e198a6bcd8d98044112d45418c157f2f2a54fdf997e01de6d53126'
im = Image.open(p)
assert im.size == (2793, 3738)
out = Image.new('RGB', (1250, 818), '#fbfaf7')
ink = '#1e2d33'
draw = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype('Arial.ttf', 15).path
except OSError:
    font = ImageFont.truetype('DejaVuSans.ttf', 15).path

def label(x, y, value, size):
    draw.text((x, y), value, font=ImageFont.truetype(font, size), fill=ink)

def photo(box, xy, scale):
    tile = im.crop(box)
    tile = tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.LANCZOS)
    out.paste(tile, xy)

label(26, 14, 'Beinecke MS 408, f. 55r  |  Le dernier groupe de la septième ligne', 31)
label(27, 65, 'Lignes 6, 7 et 8. La première ligne du second paragraphe traverse toute la colonne.', 21)
photo((258, 789, 2070, 1018), (27, 107), .655)
label(27, 275, 'Fin de la ligne 7, après le groupe transcrit qokchdy', 22)
photo((1719, 855, 2034, 965), (28, 328), 3)
for x, ch in [(1741,'o'), (1775,'l'), (1820,'k'), (1856,'a'), (1892,'r'), (1922,'d'), (1958,'a'), (1994,'m')]:
    draw.text((28+(x-1719)*3, 315), ch, anchor='ms', font=ImageFont.truetype(font, 18), fill=ink)
label(26, 680, 'Ligne 5, fin de olkam', 20)
label(597, 680, 'Ligne 9, fin de kam', 20)
photo((1777, 722, 1975, 802), (27, 717), 1.13)
photo((1828, 1002, 1972, 1087), (597, 717), 1.13)
out.save(Path(__file__).with_name('graphie.jpg'), quality=93)
