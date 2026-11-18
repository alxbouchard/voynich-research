"""Reconstruire les vues de comparaison à partir des JPEG natifs de Yale."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REGIONS = [
    ('f48v','f48v.9 · mot de S12','herbier',(1856,1127,2027,1208),0,None),
    ('fRos','Dépliant · premier mot de S37','pli',(6568,2593,6709,2672),180,None),
    ('31-3','Même passage · 31:3','pli',(6019,2592,6288,2755),180,(12,26,253,142)),
    ('14-28','Anneau · 14:28','pli',(6487,4395,6703,4495),180,None),
    ('11-19','Anneau voisin · 11:19','pli',(6078,1846,6338,2106),-144.4,(47,78,215,186)),
    ('11-21','Anneau voisin · 11:21','pli',(5866,1606,6126,1866),-122.7,(30,85,210,182)),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('pli','herbier','sortie'):
        parser.add_argument(name,type=Path)
    parser.add_argument('--police', help='Police TTF, Arial pour reproduire les légendes à l’identique')
    args = parser.parse_args()
    args.sortie.mkdir(exist_ok=True,parents=True)
    registry = json.loads((HERE.parent/'COORDONNEES.json').read_text())['sources']
    originals = {}
    for name, data in registry.items():
        path = getattr(args,name)
        if sha256(path.read_bytes()).hexdigest() != data['sha256']:
            raise ValueError(f'Source différente pour {name}')
        originals[name] = Image.open(path)
    board = Image.new('RGB',(1130,870),'#f9f7f0')
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(args.police,23) if args.police else ImageFont.load_default(size=23)
    for i,(key,label,source,box,angle,detail) in enumerate(REGIONS):
        view = originals[source].crop(box)
        path = args.sortie/(key+'-natif.png')
        if angle == 180:
            view = view.transpose(Image.Transpose.ROTATE_180)
        elif angle:
            view.save(path)
            view = view.rotate(angle,resample=Image.Resampling.BICUBIC)
        if detail:
            view = view.crop(detail)
        if angle in (0,180):
            view.save(path)
        x,y = i%2*565,i//2*290
        draw.text((x+20,y+10),label,fill='#27281f',font=font)
        view = view.resize((view.width*2,view.height*2),Image.Resampling.NEAREST)
        board.paste(view,(x+(565-view.width)//2,y+43+(290-46-view.height)//2))
    board.save(args.sortie/'comparaison-couleur.png')
    ring = originals['pli'].crop((5650,1320,6520,2190))
    ring.rotate(-135,resample=Image.Resampling.BICUBIC).crop((30,290,833,540)).save(args.sortie/'sequence-anneau.png')


if __name__ == '__main__':
    main()
