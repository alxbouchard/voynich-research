"""Assemble quatre extraits rectangulaires des originaux Yale. Arguments : vues 1006233 et 1006247."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

SOURCES = ['3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e',
           '111f6dfc34b8ecb9230cb5a0d144afef4cbd788048ddda2f440108941c91d5e5']
sources = []
for filename, checksum in zip(sys.argv[1:3], SOURCES, strict=True):
    path = Path(filename)
    assert sha256(path.read_bytes()).hexdigest() == checksum, path
    sources.append(Image.open(path).convert('RGB'))
cases = [
    (0, (3282,137,3864,910), 'oldam', 'Premier exemple', 'f89r1.3  ·  fragment 24'),
    (0, (3150,2532,3798,3643), 'saldam', 'Deuxième exemple', 'f89r1.25  ·  fragment 30'),
    (1, (2223,1535,2685,2302), 'doldam', 'Dessin prédit', 'f99v.31  ·  fragment 113'),
    (1, (1362,1647,1912,2184), 'okeodor', 'Autre dessin à deux bras', 'f99v.29  ·  fragment 111'),
]
def font(size, bold=False):
    for name in ['/System/Library/Fonts/Helvetica.ttc', 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf']:
        try:
            return ImageFont.truetype(name, size, index=1 if bold and name.endswith('.ttc') else 0)
        except OSError:
            pass
    return ImageFont.load_default(size=size)

sheet = Image.new('RGB', (1232, 1264), '#faf8f2')
draw = ImageDraw.Draw(sheet)
def label(pos, value, size, color='#242921', bold=False):
    draw.text(pos,value,font=font(size,bold),fill=color)
label((36,17),'Quatre dessins et leurs légendes',46,bold=True)
label((38,75),'Deux exemples relevés sur le même panneau, puis une prédiction sur un autre feuillet.',23)
for i, (source, box, word, heading, location) in enumerate(cases):
    x, y = 36+(i%2)*602, 138+(i//2)*533
    draw.rectangle((x, y, x+560, y+2),fill='#7c897b')
    label((x,y+10),heading,22,'#475b4c')
    label((x,y+42),word,36,bold=True)
    label((x,y+93),location,22)
    crop = sources[source].crop(box)
    crop.thumbnail((558, 379),Image.Resampling.LANCZOS)
    sheet.paste(crop,(x+(560-crop.width)//2, y+131+(379-crop.height)//2))
label((37,1218),'Beinecke MS 408, Yale University Library  ·  Agrandissements propres à chaque vignette',21,'#465247')
sheet.save(Path(__file__).with_name('quatre-dessins.jpg'),quality=94,optimize=True)
