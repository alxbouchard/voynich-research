"""Créer les cartes sans lire le texte transcrit ni interpréter les dessins."""
import argparse
import hashlib
import json
import random
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def metadata(path):
    pages = {}
    current = None
    for line in path.read_text().splitlines():
        loc = line.partition('>')[0]
        if re.fullmatch(r'<f\d+[rv]\d*', loc):
            opts = dict(re.findall(r'\$(\w)=(\w+)', line))
            current = None
            if opts.get('Q') in ('B', 'C') and opts.get('I') == 'H' and opts.get('L') == 'A' and opts.get('H') == '1':
                current = loc[1:]
                pages[current] = {'Q':opts['Q'], 'B':opts['B'], 'P0':0}
        elif current and re.fullmatch(r'<f\d+[rv]\d*\.[^,]+,[^!]P0', loc):
            pages[current]['P0'] += 1
    return {f: v for f, v in pages.items() if v['P0']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('depot',type=Path)
    parser.add_argument('photos',type=Path,help='JPEG Yale originaux nommés par face, p. ex. f9r.jpg')
    parser.add_argument('sortie',type=Path)
    args = parser.parse_args()
    output = args.sortie
    private = output/'prive'
    cards = output/'cartes'
    boards = output/'planches'
    for directory in [private, cards, boards]: directory.mkdir(parents=True,exist_ok=True)
    src = args.depot/'voynich_20261028/data'
    h = metadata(src/'IT2a-n.txt')
    z = metadata(src/'ZL3b-n.txt')
    assert h==z
    yale = {'f'+item['label']:item for item in json.loads((args.depot/'voynich_resources/yale/image_index.json').read_text())}
    order = list(h)
    seed = 2026111820
    random.Random(seed).shuffle(order)
    maps = {}
    for i, face in enumerate(order, start=1):
        ident = 'V%02d'%i
        source = args.photos/(face+'.jpg')
        info = yale[face]
        assert digest(source) == info['sha256'], face
        with Image.open(source) as im:
            assert im.size == (info['width'],info['height'])
            card = im.resize((round(1200*im.width/im.height),1200),Image.Resampling.LANCZOS).convert('RGB')
            card.info.clear()
            dest = cards/(ident+'.jpg')
            card.save(dest,quality=94,subsampling=0)
        maps[ident]={'face':face,**h[face],'url':info['url'],'sha256_yale': info['sha256'], 'dimensions_original':[info['width'],info['height']], 'sha256_carte':digest(dest), 'dimensions_carte':list(card.size)}
    (private/'correspondance.json').write_text(json.dumps(maps,indent=2,ensure_ascii=False)+'\n')
    manifest={'graine':seed,'faces':len(order),'dimensions_planches':'3 colonnes × 2 rangées, 5 cartes','hauteur_carte':1200,
              'source_H_sha256':digest(src/'IT2a-n.txt'),'source_ZL_sha256':digest(src/'ZL3b-n.txt'),
              'source_index_sha256':digest(args.depot/'voynich_resources/yale/image_index.json'),'planches':{}}
    fonts = [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    font = next((ImageFont.truetype(str(f),38) for f in fonts if f.exists()),ImageFont.load_default())
    for off in range(0,len(order),5):
        num=off//5+1
        batch = 1 if num<=3 else 2
        batchdir = boards/('lot'+str(batch))
        batchdir.mkdir(exist_ok=True)
        sheet=Image.new('RGB',(2700,2460),'white')
        draw=ImageDraw.Draw(sheet)
        ids=list(maps)[off:off+5]
        for j,id_ in enumerate(ids):
            x,y=j%3*900,j//3*1230
            with Image.open(cards/(id_+'.jpg')) as im:
                im.thumbnail((890,1160),Image.Resampling.LANCZOS)
                sheet.paste(im,(x+(900-im.width)//2,y+60))
            draw.text((x+450,y+27),id_,font=font,fill='black',anchor='mm')
        dest=batchdir/('planche_%02d.jpg'%num)
        sheet.save(dest,quality=90,subsampling=0)
        manifest['planches'][str(dest.relative_to(output))]={'codes':ids,'sha256':digest(dest)}
    (private/'selection.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print('Faces vérifiées',len(maps),'planches',len(manifest['planches']))

if __name__=='__main__': main()
