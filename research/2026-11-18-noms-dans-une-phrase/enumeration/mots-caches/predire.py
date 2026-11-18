"""Produire une carte de positions sans graphies et prédire par la seule géométrie."""
import argparse
from collections import Counter
import csv
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
from statistics import median
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0,str(HERE.parents[1]/'contexte'))
from contexte import MODES, corpus, sequence, units
from PIL import Image

PAGES = ('f88r','f88v','f89r1','f89r2')
TABLE = RESEARCH/'2026-11-18-paires-ingredients/rangees/rangees.tsv'


def write(file, obj):
    (HERE/file).write_text(json.dumps(obj, ensure_ascii=False, indent=1)+'\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(source):
    editions,_ = corpus()
    result = {}
    for page in PAGES:
        js, jpg = source/(page+'.json'), source/(page+'.jpg')
        # L'étape aval ne reçoit ni dictionnaire ni identifiant lexical des rectangles.
        rectangles = [entry[1:5] for entry in json.loads(js.read_bytes())[1]]
        with Image.open(jpg) as im:
            width,height = im.size
        lines = {}
        i = 0
        for loc,row in editions['H'].items():
            if row[0] != page: continue
            count = len(sequence(row[3], 'joints'))
            num = int(loc.split('.')[-1])
            item = {'classe': row[1], 'boites': rectangles[i:i+count]}
            entries = [ed[loc] for ed in editions.values() if loc in ed]
            if row[1]=='Lf':
                vs = [tuple(w for _,w in sequence(ed[3],cut)) for ed in entries for cut in MODES]
                item['graphies_legende'] = [list(v) for v in vs]
            elif row[1]=='P0':
                item['debut'] = len(entries)==2 and all('<%>' in ed[3] for ed in entries)
                item['fin'] = len(entries)==2 and all('<$>' in ed[3] for ed in entries)
            lines[num] = item
            i += count
        assert i == len(rectangles), (page,i,len(rectangles))
        result[page] = {'taille':[width,height], 'carte_sha256':digest(js), 'image_sha256':digest(jpg), 'lignes':lines}
    return result


def centre(box):
    x,y,w,h = box
    return x+w/2, y+h/2


def slopes(lines, width):
    values = []
    for line in lines.values():
        if line['classe'] != 'P0' or len(line['boites']) < 4: continue
        pts = [centre(b) for b in line['boites']]
        if max(p[0] for p in pts)-min(p[0] for p in pts)<width/4: continue
        s = [(y2-y1)/(x2-x1) for (x1,y1),(x2,y2) in combinations(pts,2) if abs(x2-x1)>=width/5]
        if s: values.append(median(s))
    assert values
    return median(values)


def closest(box, line, slope):
    a,b = centre(box)
    distances = sorted((abs((x-a)+slope*(y-b)),i) for i,(x,y) in enumerate(map(centre,line['boites']),1))
    return None if len(distances)>1 and distances[1][0]-distances[0][0]<1e-8 else distances[0][1]


def captions(row):
    return [int(n) for group in row['fragments'].split(',') for n in group.split('+')]


def generate(masked):
    assert digest(TABLE)=='584a27515c49c4c2cb4a527c0c54c30c02f7a34893001cdeeb1e047514afc5a4'
    output = []
    for row in csv.DictReader(TABLE.open(),delimiter='\t'):
        page = row['page']
        if page not in PAGES: continue
        geom = masked[page]
        lines = {int(k):v for k,v in geom['lignes'].items()}
        slope = slopes(lines,geom['taille'][0])
        caps = captions(row)
        extent = [int(n) for n in row['pots'].split(',')] + caps
        for side,number,flag in [('haut',min(extent)-1,'fin'),('bas',max(extent)+1,'debut')]:
            target = lines.get(number)
            is_target = bool(target and target['classe']=='P0' and target[flag])
            for num in caps:
                item = lines[num]
                vs = item['graphies_legende']
                predicted = None
                why = None
                if not is_target: why = 'aucune_ligne_contigue'
                elif len(vs)!=4 or len({tuple(v) for v in vs})!=1: why = 'lecture_divergente'
                elif len(vs[0])!=1 or len(item['boites'])!=1: why = 'legende_multiple'
                elif not re.fullmatch('[a-z]+',vs[0][0]) or len(units(vs[0][0],False))<3: why = 'mot_court_ou_incertain'
                elif not all(centre(b)[0]<centre(c)[0] for b,c in zip(target['boites'],target['boites'][1:])): why = 'rangs_non_croissants'
                else:
                    raw = closest(item['boites'][0],target,0)
                    corrected = closest(item['boites'][0],target,slope)
                    if raw is None or corrected is None or raw!=corrected: why = 'axes_divergents_ou_egalite'
                    else: predicted = {'mot':vs[0][0], 'rang':raw}
                output.append({'page':page, 'rangee':int(row['rang']), 'cote':side, 'legende':f'{page}.{num}',
                               'cible':f'{page}.{number}' if is_target else None, 'pente':round(slope,7),
                               'annonce':predicted,'abstention':why})
    return output


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('etape',choices=['masquer','predire'])
    parser.add_argument('--sources',type=Path)
    args = parser.parse_args()
    if args.etape=='masquer': write('GEOMETRIE-MASQUEE.json', mask(args.sources))
    else: write('PREDICTIONS.json',generate(json.loads((HERE/'GEOMETRIE-MASQUEE.json').read_text())))
