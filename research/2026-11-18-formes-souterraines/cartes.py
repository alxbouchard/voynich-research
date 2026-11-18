"""Produire des planches anonymisées dans l'ordre déterminé avant les lectures."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'voynich_20261028/data'


def eligible():
    editions = {}
    metadata = {}
    for ed in ('ZL3b', 'IT2a'):
        current = None
        faces = set()
        for line in (DATA / (ed+'-n.txt')).read_text().splitlines():
            header = re.match(r'^<(f[^,.>]+)>', line)
            if header:
                current = header[1]
                if ed == 'ZL3b':
                    metadata[current] = dict(re.findall(r'\$(\w)=(\w+)',line))
            elif re.match(r'^<f[^,]+,[^!]P0>',line):
                faces.add(current)
        editions[ed] = faces
    return {face:m['Q'] for face,m in metadata.items() if face in editions['ZL3b'] & editions['IT2a']
            and m.get('I')=='H' and m.get('L')=='A' and m.get('H')=='1' and m.get('Q') in tuple('ABCDEFG')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('photos',type=Path)
    parser.add_argument('lot', choices=['apprentissage','reserve'])
    parser.add_argument('planches',type=Path)
    args = parser.parse_args()
    args.planches.mkdir(exist_ok=True, parents=True)
    registry = {'f'+r['label']:r for r in json.loads((ROOT/'voynich_resources/yale/image_index.json').read_text())}
    train = args.lot=='apprentissage'
    faces = eligible()
    names = sorted(f for f,q in faces.items() if (q in 'ABC')==train)
    random.Random(377 if train else 634).shuffle(names)
    key = {}
    prefix = 'M' if train else 'R'
    for i,face in enumerate(names):
        photo = args.photos / (face+'.jpg')
        rec = registry[face]
        assert hashlib.sha256(photo.read_bytes()).hexdigest()==rec['sha256'],face
        code = f'{prefix}{i+1:02}'
        key[code] = {'face':face,'cahier':faces[face], 'url':rec['url'],'sha256_original':rec['sha256']}
        with Image.open(photo) as im:
            w,h = im.size
            bbox = (round(w*.035),round(h*.35),round(w*.965),round(h*.97))
            crop = ImageOps.contain(im.crop(bbox).convert('RGB'), (475,380), Image.Resampling.LANCZOS)
        if i%6==0:
            board = Image.new('RGB',(1488,836),'#ece7dc')
            draw = ImageDraw.Draw(board)
        col,row = i%3, (i%6)//3
        x,y = col*496,row*418
        board.paste(crop,(x+(496-crop.width)//2,y+29+(380-crop.height)//2))
        draw.text((x+15,y+3),code,fill='black',font=ImageFont.load_default(size=23))
        if i%6==5 or i+1==len(names):
            board.save(args.planches/f'{prefix}-{i//6+1:02}.jpg',quality=91)
    (HERE/f'cle-{args.lot}.json').write_text(json.dumps(key,indent=1,ensure_ascii=False)+'\n')
    print(args.lot,len(key))


if __name__ == '__main__':
    main()
