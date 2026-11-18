"""Apparier les coordonnées du visualiseur aux clichés natifs, sans exposer les mots."""
from collections import defaultdict
from difflib import SequenceMatcher
from hashlib import sha256
from pathlib import Path
from random import Random
import json
import re
import sys

from PIL import Image, ImageDraw, ImageFont
import cv2

BASE = Path(__file__).resolve().parent
RESEARCH = BASE.parents[1]
REPO = RESEARCH.parent
sys.path.insert(0, str(RESEARCH / '2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite

PANELS = {'f68r1': ('Ls', '68r'), 'f68r2': ('Ls', '68r'),
          'f80r': ('Ln', '80r'), 'f84r': ('Ln', '84r')}
REFERENCE = 'https://www.voynichese.com/2/data/folio/'


def fingerprint(path):
    return sha256(path.read_bytes()).hexdigest()


def align(page, viewer):
    dictionary, coordinates = viewer
    words = [dictionary[row[0]][0] for row in coordinates]
    text, places, genres = [], [], {}
    for line in (REPO / 'voynich_20261028/data/IT2a-n.txt').read_text().splitlines():
        match = re.match(r'^<' + page + r'\.(\d+),(.)(..)>(.*)', line)
        if not match or match[2] == '!':
            continue
        place = int(match[1])
        genres[place] = match[3]
        clean = re.sub(r'<[^>]*>|!','',match[4].replace('<->','.').replace('<~>','.')).strip()
        for word in filter(None,clean.split('.')):
            text.append(word)
            places.append(place)
    mapping = {}
    for block in SequenceMatcher(None,text,words,autojunk=False).get_matching_blocks():
        for i in range(block.size):
            mapping[block.a+i] = block.b+i
    grouped = defaultdict(list)
    for j, line_number in enumerate(places):
        grouped[line_number].append(j)
    return genres, grouped, mapping, coordinates, words, text


def main(cache):
    official = {row['label']:row for row in json.loads((REPO/'voynich_resources/yale/image_index.json').read_text())}
    faces, cards, photos = {}, {}, {}
    for page, (typ, label) in PANELS.items():
        files = [cache/(page+s) for s in ('-n.jpg','-r.jpg','-l.json')]
        native, reference, layout = files
        assert fingerprint(native) == official[label]['sha256']
        cv2.setRNGSeed(408)
        mat, goodness = recaler(reference, native)
        faces[page] = dict(photo=official[label]['url'],reperage=REFERENCE+'image/glance/color/large/'+page+'.jpg',
                           carte=REFERENCE+'script/'+page+'.js',empreintes=[fingerprint(p) for p in files],
                           ajustement=goodness)
        genres, grouped, mapping, coords, words, text = align(page,json.loads(layout.read_text()))
        labels = sorted(k for k,v in genres.items() if v == typ)
        im = Image.open(native).convert('RGB')
        for n in [labels[0],labels[len(labels)//2],labels[-1]]:
            indices = grouped[n]
            js = [mapping.get(i) for i in indices]
            if any(k is None for k in js):
                # N'inférer un emplacement que si les voisins concordent et enferment exactement un mot.
                left, right = mapping.get(indices[0]-1), mapping.get(indices[-1]+1)
                candidate = text[indices[0]] if len(indices)==1 else None
                zl_rows=(REPO/'voynich_20261028/data/ZL3b-n.txt').read_text().splitlines()
                zl_raw=next(line.split('>',1)[1] for line in zl_rows if line.startswith(f'<{page}.{n},'))
                zl_word=re.sub(r'<[^>]*>|!', '', zl_raw).replace(',','').strip()
                if candidate == zl_word and words.count(candidate) == 1:
                    js=[words.index(candidate)]
                    mode='mot unique du panneau identique dans les deux éditions'
                elif len(indices)==1 and left is not None and right == left+2:
                    js=[left+1]
                    mode='voisins concordants'
                else:
                    print(page,n,'sans alignement',js,left,right)
                    cards[f'{page}.{n}']={'lieu':f'{page}.{n}','statut':'sans alignement'}
                    continue
            else: mode='alignement de la transcription'
            boxes=[boite(coords[k],mat) for k in js]
            x,y = min(b[0] for b in boxes), min(b[1] for b in boxes)
            X,Y = max(b[2] for b in boxes), max(b[3] for b in boxes)
            cx,cy=(x+X)//2,(y+Y)//2
            frame=(cx-260,cy-210,cx+260,cy+210)
            crop=im.crop(frame)
            draw=ImageDraw.Draw(crop)
            masked=[]
            for k,row in enumerate(coords):
                box=boite(row,mat)
                if box[2]<frame[0] or box[0]>frame[2] or box[3]<frame[1] or box[1]>frame[3]: continue
                local=(box[0]-frame[0]-3,box[1]-frame[1]-3,box[2]-frame[0]+3,box[3]-frame[1]+3)
                draw.rectangle(local, fill='#cec9bc',outline=('#a23a23' if k in js else None),width=3)
                masked.append(box)
            locus=f'{page}.{n}'
            cards[locus] = dict(lieu=locus, mode=mode,serie=typ,cadre=frame,boites=boxes,masques=masked)
            photos[locus]=crop
    ids=list(cards)
    Random(408).shuffle(ids)
    plate=Image.new('RGB',(3*420,4*370),'#f6f3ea')
    draw=ImageDraw.Draw(plate)
    try: font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',29)
    except OSError: font=ImageFont.truetype('DejaVuSans.ttf',29)
    for i,locus in enumerate(ids):
        code=f'C{i+1:02}';cards[locus]['carte']=code
        x,y=(i%3)*420,(i//3)*370
        draw.text((x+8,y+3),code,fill='#273729',font=font)
        if locus in photos: plate.paste(photos[locus].resize((413,334),Image.Resampling.LANCZOS),(x+3,y+34))
    plate.save(BASE/'DETAILS.jpg',quality=93,optimize=True)
    (BASE/'CADRAGES.json').write_text(json.dumps(dict(faces=faces,cartes=cards),ensure_ascii=False,indent=1)+'\n')
    print('Cartes localisées',len(photos),'/',len(cards))

if __name__ == '__main__':
    main(Path(sys.argv[1]))
