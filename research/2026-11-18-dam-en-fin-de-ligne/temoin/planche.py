"""Refaire la preuve avec les quatre photos décrites dans SOURCES.json."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

ici = Path(__file__).resolve().parent
dossier = Path(sys.argv[1])
vues = {}
for source in json.loads((ici / 'SOURCES.json').read_text()):
    p = dossier / source['fichier']
    assert sha256(p.read_bytes()).hexdigest() == source['sha256'], p
    vues[source['id']] = Image.open(p)
out = Image.new('RGB', (1180, 1424), '#faf9f5')
dessin = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype('Arial.ttf', 18).path
except OSError:
    font = ImageFont.truetype('DejaVuSans.ttf', 18).path

def titre(y, texte):
    dessin.text((32,y), texte, font=ImageFont.truetype(font, 22), fill='#1f292b')

def extrait(id_, boite, x, y, largeur):
    ex = vues[id_].crop(boite)
    ex = ex.resize((largeur, round(ex.height * largeur / ex.width)), Image.Resampling.LANCZOS)
    out.paste(ex, (x,y))

titre(12, 'Aristologia longa, chapitre XIII  |  Alignement de deux éditions de l’Herbarius')
titre(61, 'Passau, 1485. Recto, huit lignes. La sixième finit par multum.')
extrait('passau-r', (171,1381,1159,1800), 33, 96, 960)
titre(527, 'Mayence, 1484. Recto, neuf lignes. La septième porte multū, avant valet.')
extrait('mayence-r', (261,1432,1147,1850), 32, 567, 910)
titre(1011, 'Passau, verso, lignes 3–4. Après eius, cum entier à droite. Après mente, cū au milieu.')
extrait('passau-v', (303,191,1260,314), 32, 1047, 1000)
titre(1215, 'Mayence, verso, lignes 2–4. La troisième ligne porte cū deux fois, dont une en marge.')
extrait('mayence-v', (548,421,1440,548), 32, 1251, 1000)
out.save(ici / 'comparaison.jpg', quality=92)
