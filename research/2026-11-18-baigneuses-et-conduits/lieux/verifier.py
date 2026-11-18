"""Vérifier les quatre étiquettes. L'option --images lit les trois JPG Yale locaux."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
DEPOT = ICI.parents[2]
EDITION = {'H':'IT2a-n.txt', 'ZL':'ZL3b-n.txt'}
GROUPE = 'otoly'


def lire_etiquettes(emplacements):
    cibles = {loc['locus']:loc['categorie'] for page in emplacements.values() for loc in page['loci']}
    resultats = {}
    for nom,fichier in EDITION.items():
        chemin = DEPOT/'voynich_20261028'/'data'/fichier
        releve = {}
        for ligne in chemin.read_text().splitlines():
            match = re.match(r'<([^,>]+),.([^>]+)>\s*(.*)', ligne)
            if not match or match[1] not in cibles:
                continue
            locus, typ, brut = match.groups()
            assert locus not in releve
            nettoye = re.sub(r'<![^>]*>', '', brut).replace('!', '').strip()
            joint = nettoye.replace(',', '').split('.')
            separe = re.split(r'[.,]', nettoye)
            releve[locus] = {'categorie':cibles[locus], 'type':typ, 'transcription':brut, 'cible_virgule_jointe':GROUPE in joint,'cible_virgule_separee':GROUPE in separe}
        assert set(releve) == set(cibles)
        resultats[nom] = {'fichier':fichier,'sha256':hashlib.sha256(chemin.read_bytes()).hexdigest(),'releve':releve}
    return resultats


def planche(emplacements, dossier, cacher):
    from PIL import Image, ImageDraw, ImageFont
    largeur = 880
    panneau = Image.new('RGB',(largeur,1060),'white')
    dessin = ImageDraw.Draw(panneau)
    for face_police in ('DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            police = ImageFont.truetype(face_police,21)
            titre = ImageFont.truetype(face_police,25)
            break
        except OSError:
            continue
    else:
        police = ImageFont.load_default(size=21)
        titre = ImageFont.load_default(size=25)
    zones = {'f82v':(0,55,880,566),'f82r':(0,650,425,1033),'f78r':(455,650,880,1033)}
    dessin.text((24,12),'A   f82v.41 et f82v.43, registre du bas', fill='black',font=titre)
    dessin.text((24,590),'B   f82r.44, figures',fill='black',font=police)
    dessin.text((465,590),'B   f78r.44, conduit',fill='black',font=police)
    for face,page in emplacements.items():
        chemin = dossier/(face+'.jpg')
        assert hashlib.sha256(chemin.read_bytes()).hexdigest() == page['yale_sha256']
        with Image.open(chemin) as source:
            im = source.convert('RGB')
        assert list(im.size) == page['dimensions']
        d = ImageDraw.Draw(im)
        for loc in page['loci']:
            for x,y,r,b in loc['boites_mots']:
                d.rectangle((x-9,y-5,r+9,b+5), fill='#e3d5bf' if cacher else None,outline='#ac0056',width=6)
            if cacher:
                d.text(((x+r)/2,(y+b)/2),loc['locus'].split('.')[1],font=police,fill='black',anchor='mm')
        detail=im.crop(page['rectangle_du_detail'])
        l,t,r,b=zones[face]
        detail.thumbnail((r-l,b-t),Image.Resampling.LANCZOS)
        panneau.paste(detail,(l+(r-l-detail.width)//2,t))
    panneau.save(ICI/('lieux-masques.jpg' if cacher else 'lieux-verifies.jpg'),quality=94)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--images',type=Path,help='Dossier contenant f82v.jpg, f82r.jpg et f78r.jpg de Yale')
    options=p.parse_args()
    emplacements=json.loads((ICI/'emplacements.json').read_text())['faces']
    resultats=lire_etiquettes(emplacements)
    print(json.dumps(resultats,ensure_ascii=False,indent=2))
    if options.images:
        for cache in [True,False]:
            planche(emplacements,options.images,cache)
