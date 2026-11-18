"""Usage : python3 construire.py /chemin/vers/1006252.jpg"""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

ici = Path(__file__).resolve().parent
source = Path(sys.argv[1])
image = Image.open(source)
carte = ici.parent / 'images/B/B06.jpg'
prov = json.loads((ici.parent / 'images/PROVENANCE.json').read_text())['B06']
for chemin, attendu in [(source, prov['sha256_original']), (carte, prov['sha256_carte'])]:
    assert sha256(chemin.read_bytes()).hexdigest() == attendu
assert image.size == (2981, 3795)
cache = Image.open(carte)
coupe = (1590, 420, 2410, 1115)
facteur = 1500 / image.height
x_cadre, y_cadre = [round(v * 1.5) for v in prov['cadre_pour_hauteur_1000'][:2]]
boite_carte = tuple(round(coordonnee * facteur) - origine for coordonnee, origine
                    in zip(coupe, (x_cadre, y_cadre, x_cadre, y_cadre)))
try:
    police = ImageFont.truetype('Arial.ttf', 16).path
except OSError:
    police = ImageFont.truetype('DejaVuSans.ttf', 16).path

# Vue de rangée et numéros éditoriaux dans la marge, sans tracer sur l'image.
rangee = image.crop((230, 355, 2840, 905))
rangee.thumbnail((1305, 275), Image.Resampling.LANCZOS)
encart = Image.new('RGB', (1345, 352), 'white')
dessin = ImageDraw.Draw(encart)
dessin.text((20, 7), 'f102v2  |  Première rangée, de gauche à droite', font=ImageFont.truetype(police, 23), fill='#202020')
encart.paste(rangee, (20, 41))
for x, libelle in [(430,'pot'), (685,'214'), (915,'215'), (1140,'216'), (1345,'217'), (1650,'218'), (2040,'219'), (2510,'220')]:
    dessin.text((20+(x-230)*.5, 323), libelle, anchor='mt', font=ImageFont.truetype(police, 19), fill='#261d15')
encart.save(ici/'rangee.jpg', quality=92)

# Les deux images ont la même fenêtre, exprimée sur les axes de l'original Yale.
for vue, nom, legende in [(image.crop(coupe), 'original.jpg', 'f102v2.8  |  Photographie native de Yale'),
                          (cache.crop(boite_carte), 'masque.jpg', 'f102v2.8  |  Carte B06 donnée aux lecteurs, agrandie')]:
    vue = vue.resize((820, 695), Image.Resampling.LANCZOS)
    cadre = Image.new('RGB', (910, 787), 'white')
    cadre.paste(vue, (66, 65))
    d = ImageDraw.Draw(cadre)
    d.text((18, 10), legende, font=ImageFont.truetype(police, 22), fill='#202020')
    for n in range(1600, 2401, 100):
        x = 66 + n-coupe[0]
        d.line((x, 59, x, 64), fill='#494949')
        d.text((x, 56), str(n), anchor='mb', font=ImageFont.truetype(police, 13), fill='#454545')
    for n in range(500, 1101, 100):
        y = 65 + n-coupe[1]
        d.line((60, y, 65, y), fill='#494949')
        d.text((54, y), str(n), anchor='rm', font=ImageFont.truetype(police, 13), fill='#454545')
    d.text((66, 768), 'Coordonnées en pixels du scan Yale ; origine au coin supérieur gauche.', font=ImageFont.truetype(police, 13), fill='#454545')
    cadre.save(ici/nom, quality=92)
