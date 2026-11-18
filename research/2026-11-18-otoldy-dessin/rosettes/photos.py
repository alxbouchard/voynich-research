"""Recréer les recadrages et la série de lecture à partir des deux JPEG de Yale."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCES = {'pli': '1006231', 'herbier': '1006169'}
HASHES = {'pli': '4b08afeee514691b0a511099ca299aed544d6fd1782b7dee8df163dfc06354ed',
          'herbier': 'c0ecc85912878c5c27ad64d560dd088e703ea95e68a87aaecb112a4aabcbe516'}
# All boxes in unrotated, full-size Yale JPEGs (origin top left; XYXY).
CARDS = {
    'S12': ('herbier', (1853,1121,2212,1208), 0, 'f48v.9, deux groupes après la seconde interruption'),
    'S23': ('pli', (6957,2650,7219,2768), 180, 'inscription latérale, à droite sur le dépliant orienté par Yale'),
    'S37': ('pli', (6412,2570,6722,2678), 180, 'fRos.45, inscription entre les deux bords'),
    'S48': ('herbier', (2220,1105,2513,1197), 0, 'f48v.9, deux derniers groupes'),
    'S59': ('pli', (6019,2592,6288,2755), 180, 'inscription latérale, à gauche sur le dépliant orienté par Yale'),
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pli', type=Path)
    ap.add_argument('herbier', type=Path)
    ap.add_argument('out', type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cards = args.out/'cartes'
    cards.mkdir(exist_ok=True)
    meta = {'sources':{}, 'cartes':{}}
    images = {}
    for name, oid in SOURCES.items():
        path = getattr(args, name)
        if digest(path) != HASHES[name]:
            raise ValueError('Empreinte différente du fichier source de Yale')
        images[name] = Image.open(path).convert('RGB')
        if images[name].size != ((7925,7268) if name=='pli' else (2950,3769)):
            raise ValueError('Taille différente du JPEG Yale attendu')
        meta['sources'][name] = {'oid':oid,'sha256':digest(path),'url':'https://collections.library.yale.edu/iiif/2/'+oid+'/full/full/0/default.jpg','taille':images[name].size}
    for key, (src,box,rot,site) in CARDS.items():
        crop = images[src].crop(box).rotate(rot)
        # Neutral monochrome; homogeneous canvas. Preserve relative proportions.
        card = ImageOps.autocontrast(ImageOps.grayscale(crop), cutoff=0.4)
        card.thumbnail((390,175))
        card = card.resize((card.width*2,card.height*2), Image.Resampling.LANCZOS)
        canvas = Image.new('L',(820,365),235)
        canvas.paste(card,((820-card.width)//2,(365-card.height)//2))
        out = cards/(key+'.png')
        canvas.save(out)
        meta['cartes'][key] = {'source':src,'boite':box,'rotation':rot,'site':site,'sha256':digest(out)}
    overview = images['pli'].crop((5770,2210,7580,3160)).rotate(180)
    overview.thumbnail((1040,610))
    overview.save(args.out/'passage-du-depliant.jpg', quality=92)
    plant = images['herbier'].crop((1745,1020,2600,1345))
    plant.save(args.out/'trois-lignes-herbier.jpg', quality=92)
    panel = Image.new('RGB',(578,410),'#f8f6f0')
    pen = ImageDraw.Draw(panel)
    font = ImageFont.load_default(size=20)
    for y, title, ident in [(12,'Herbier, f48v, ligne 9','S12'),(207,'Neuf rosettes, inscription 45','S37')]:
        src, box, rot, _ = CARDS[ident]
        cut = images[src].crop(box).rotate(rot)
        cut = cut.resize((round(cut.width*1.45),round(cut.height*1.45)),Image.Resampling.LANCZOS)
        pen.text((25,y),title,fill='#252523',font=font)
        panel.paste(cut,(25,y+28))
    panel.save(args.out/'deux-inscriptions.png')
    (args.out/'COORDONNEES.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    main()
