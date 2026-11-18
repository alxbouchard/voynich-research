"""Usage: python3 cadrer.py /chemin/vers/le/1006252.jpg"""
from hashlib import sha256
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
source = Path(sys.argv[1])
assert sha256(source.read_bytes()).hexdigest() == '8cdb1030d805b968932146124915cb0d86f7abf853167ffec028b59599820fad'
photo = Image.open(source).convert('RGB')
assert photo.size == (2981, 3795)
INK, RED, BLUE = '#242424', '#a22835', '#195b77'


def font(size, bold=False):
    names = ('Arial Bold.ttf', 'DejaVuSans-Bold.ttf') if bold else ('Arial.ttf', 'DejaVuSans.ttf')
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


# Coordonnées dans l'original. Les cadres laissent une marge autour de l'encre.
spots = {
    '.11': (879, 975, 1080, 1054),
    '.32': (827, 2485, 982, 2565),
    '.33': (1321, 2564, 1501, 2639),
    '.39': (985, 2987, 1165, 3075)
}
scale = .25
page = photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.Resampling.LANCZOS)
overview = Image.new('RGB', (1130, 1003), 'white')
overview.paste(page, (12, 42))
d = ImageDraw.Draw(overview)
d.text((12, 7), 'f102v2   |   Emplacement des quatre inscriptions', font=font(25, True), fill=INK)
for name, box in spots.items():
    xy = [round(v * scale) + (12 if i % 2 == 0 else 42) for i, v in enumerate(box)]
    d.rectangle(xy, outline=RED, width=2)
    x = xy[0] - 38 if name != '.33' else xy[2] + 3
    d.text((x, xy[1] - 1),name,font=font(15, True),fill=RED,stroke_width=1,stroke_fill='white')
for y0,y1,label,detail in [(1140,1585,'Paragraphe supérieur','7 lignes, f102v2.17 à .23'),
                           (2330,3070,'Paragraphe inférieur','10 lignes, f102v2.30 à .39')]:
    y0,y1 = round(scale*y0)+42, round(scale*y1)+42
    d.line([(762,y0),(773,y0),(773,y1),(762,y1)], fill=BLUE, width=3)
    mid=(y0+y1)//2
    d.text((785,mid-25),label,font=font(22,True), fill=BLUE)
    d.text((785,mid+5),detail,font=font(16), fill=INK)
for raw_y,lines in [(720,['Récipient supérieur','Deux rangées de fragments','214–220 et 221–227']),
                    (1970,['Récipient inférieur','Une rangée de fragments','229–233'])]:
    y=round(raw_y*scale)+42
    for i,t in enumerate(lines):
        d.text((785, y+26*i), t, font=font(19, i==0),fill=INK)
overview.save(OUT/'page-annotee.jpg', quality=90)

# Montrer le même morceau de ligne en une seule vue lorsque la fenêtre le permet.
strips = [
    ('.11   Légende du fragment 222', (825,785,1200,1080), 0.85),
    ('.32   dar   |   cheor   |   sheor / shoar   |   okeol', (700,2477,1410,2570), 1.17),
    ('.33   ?keeeos   |   cheor   |   o · s/r · al   |   début de chos', (1010,2540,1850,2650), 1.12),
    ('.39   yotaiin   |   cheor   |   cheekey   |   orain', (713,2973,1710,3090), .99),
]
plate=Image.new('RGB',(1060,920),'white')
d=ImageDraw.Draw(plate)
d.text((18,12),'f102v2   |   Légende et lignes de prose',font=font(28,True),fill=INK)
y=69
for title,box,factor in strips:
    d.text((20,y),title,font=font(21,True),fill=BLUE)
    cut=photo.crop(box)
    cut=cut.resize((round(cut.width*factor),round(cut.height*factor)),Image.Resampling.LANCZOS)
    plate.paste(cut,(20,y+34))
    y+=cut.height+54
plate.crop((0,0,1060,y)).save(OUT/'quatre-lectures.jpg',quality=94)
