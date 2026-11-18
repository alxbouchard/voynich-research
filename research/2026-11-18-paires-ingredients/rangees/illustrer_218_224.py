"""Extrait deux fragments du scan Yale natif. Usage : python3 illustrer_218_224.py 1006252.jpg"""
from pathlib import Path
from hashlib import sha256
import sys
from PIL import Image, ImageDraw, ImageFont

chemin = Path(sys.argv[1])
assert sha256(chemin.read_bytes()).hexdigest() == '8cdb1030d805b968932146124915cb0d86f7abf853167ffec028b59599820fad'
im = Image.open(chemin)
assert im.size == (2981, 3795)
boites = {
    'ensemble': (205, 310, 2900, 1450),
    'fragment218': (1390, 385, 1790, 750),
    'locus7': (1777, 445, 1930, 575),
    'fragment224': (1500, 615, 1828, 1070),
    'locus13': (1623, 945, 1788, 1110),
}
blanc = '#fcfbf8'
encre = '#202c2b'
out = Image.new('RGB', (1500, 1200), blanc)
d = ImageDraw.Draw(out)
try:
    police = ImageFont.truetype('Arial.ttf', 24).path
except OSError:
    police = ImageFont.truetype('DejaVuSans.ttf', 24).path

def ecrire(x, y, txt, taille, couleur=encre):
    d.text((x, y), txt, fill=couleur, font=ImageFont.truetype(police, taille))
def inserer(nom, boite):
    x, y, w, h = boite
    extrait = im.crop(boites[nom]); facteur = min(w / extrait.width, h / extrait.height)
    extrait = extrait.resize((round(extrait.width*facteur), round(extrait.height*facteur)), Image.Resampling.LANCZOS)
    out.paste(extrait, (x, y))

ecrire(28, 15, 'f102v2  ·  Deux fragments auprès du premier pot', 40)
ecrire(30, 69, 'Beinecke MS 408   /   pot à gauche, deux rangées de sept motifs', 25)
inserer('ensemble', (30, 111, 1440, 610))
for x, n, locus, position in [(30, '218', '7', 'Premier étage, cinquième motif'), (774, '224', '13', 'Second étage, quatrième motif')]:
    ecrire(x, 740, position, 29)
    ecrire(x, 790, 'Dessin '+n, 24, '#76401f')
    ecrire(x+354, 790, 'Inscription f102v2.'+locus, 24, '#215875')
    inserer('fragment'+n, (x, 830, 327, 329))
    inserer('locus'+locus, (x+354, 830, 307, 217))
out.save(Path(__file__).with_name('f102v2-218-224.jpg'), quality=92, optimize=True)
