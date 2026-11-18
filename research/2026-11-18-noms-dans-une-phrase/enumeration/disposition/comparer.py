"""Comparer chaque rangée de légendes à ses deux voisins textuels verticaux."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / 'contexte'))
from contexte import corpus, sequence, sections, units, MODES

REG = RESEARCH / '2026-11-18-paires-ingredients/rangees'
SHA = {'rangees.tsv': '584a27515c49c4c2cb4a527c0c54c30c02f7a34893001cdeeb1e047514afc5a4',
       'pots_elargis.tsv': 'fcb26b2da747c6e41a50ae3071320756ad8734d4052648c4b59bcb510c009b50'}


def rows(file):
    raw = (REG/file).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA[file]
    return {(r['page'], int(r['rang'])): r for r in csv.DictReader(raw.decode().splitlines(), delimiter='\t')}


def inputs(data, loc, kind):
    assert all(d[loc][1] == kind for d in data.values())
    return [sequence(d[loc][3], cut) for d in data.values() for cut in MODES]


def line_set(views):
    return set.intersection(*({w for _, w in view if re.fullmatch('[a-z]+', w)} for view in views))


def tokens_at(data, loc):
    views = inputs(data, loc, 'P0')
    words = [w for span in sections(views) for w in span]
    return [(loc, i, w) for i, w in enumerate(words, 1) if w]


def match(places, dictionary):
    hits = [{'locus': loc, 'rang': i, 'mot': w} for loc, i, w in places if w in dictionary]
    return {'places': len(places), 'occurrences': len(hits), 'mots': sorted({hit['mot'] for hit in hits}), 'reprises': hits}


def lines(row):
    return [row['page']+'.'+n for n in row['prose'].split(',') if n]


def tags(data, locs):
    return {e: {'debuts': [loc for loc in locs if '<%>' in d[loc][3]],
                'fins': [loc for loc in locs if '<$>' in d[loc][3]]} for e, d in data.items()}


def compare(data, row, before, after):
    page = row['page']
    labels = {}
    for group in row['fragments'].split(','):
        for num in group.split('+'):
            loc = f'{page}.{num}'
            labels[loc] = sorted(w for w in line_set(inputs(data, loc, 'Lf')) if len(units(w, False)) >= 3)
    dictionary = set().union(*labels.values())
    pair = [[pos for loc in block for pos in tokens_at(data,loc)] for block in (before, after)]
    k = min(map(len,pair))
    assert k >= 5
    top, bottom = pair
    regions = {'entier': (top, bottom), 'equilibre': (top[-k:], bottom[:k]),
               'cinq': (top[-5:], bottom[:5]),
               'ligne_proche': (tokens_at(data,before[-1]), tokens_at(data,after[0])),
               'ligne_opposee': (tokens_at(data,before[0]), tokens_at(data,after[-1]))}
    relaxed = {}
    for side, block in [('haut',before),('bas',after)]:
        relaxed[side] = {loc: ws for loc in block if (ws := sorted(dictionary & line_set(inputs(data, loc,'P0'))))}
    return {'page': page, 'rang': int(row['rang']), 'legendes': labels, 'formes_rangee': len(dictionary),
            'superieur': before, 'inferieur': after, 'bornes': [tags(data, before),tags(data, after)],
            'mesures': {name: dict(haut=match(a,dictionary),bas=match(b,dictionary)) for name,(a,b) in regions.items()},
            'meme_ligne_rang_libre': relaxed}


def inventory(data, file, strict):
    geometry = rows(file)
    accepted = []
    for (page, rank), row in sorted(geometry.items()):
        previous = geometry.get((page, rank-1))
        if page.startswith('f99') or not previous:
            continue
        before, after = lines(previous), lines(row)
        if not before or not after:
            continue
        for d in data.values():
            p0 = [loc for loc, rec in d.items() if rec[:2] == (page, 'P0')]
            intervening = p0[p0.index(before[0]):p0.index(after[-1])+1]
            assert intervening == before + after, (page, rank, intervening)
        if strict and any(t['debuts'] != block[:1] or t['fins'] != block[-1:]
                          for block in (before,after) for t in tags(data,block).values()):
            continue
        accepted.append(compare(data,row,before,after))
    return accepted


def summarize(examples):
    sums = {}
    for name in examples[0]['mesures']:
        sides = {}
        for side in ('haut','bas'):
            scans = [eg['mesures'][name][side] for eg in examples]
            sides[side] = dict(places=sum(s['places'] for s in scans),
                               occurrences=sum(s['occurrences'] for s in scans),
                               couples_rangee_mot=sum(len(s['mots']) for s in scans),
                               rangees_touchees=sum(bool(s['mots']) for s in scans))
        sums[name] = sides
    for side in ('haut','bas'):
        count = sum(len(set().union(*r['meme_ligne_rang_libre'][side].values())) if r['meme_ligne_rang_libre'][side] else 0 for r in examples)
        sums.setdefault('meme_ligne_rang_libre', {})[side] = {'couples_rangee_mot': count}
    return sums


def reading_controls(data, examples):
    output = {}
    for edition, entries in data.items():
        for cut in MODES:
            def read(loc):
                return [w for _, w in sequence(entries[loc][3], cut) if re.fullmatch('[a-z]+', w)]
            captions = set(read('f99r.25'))
            check = [i for i, (_, w) in enumerate(sequence(entries['f99r.18'][3], cut), 1)
                     if w == 'okeoly' and w in captions]
            assert check == [8]
            rows = []
            for row in examples:
                dictionary = {w for loc in row['legendes'] for w in read(loc) if len(units(w,False)) >= 3}
                scans = {}
                for side, key in [('haut','superieur'),('bas','inferieur')]:
                    scanned = [(loc,w) for loc in row[key] for w in read(loc)]
                    scans[side] = {'places': len(scanned), 'reprises': [[loc,w] for loc,w in scanned if w in dictionary]}
                rows.append({'page':row['page'], 'rang':row['rang'], 'formes':len(dictionary), 'mesures':scans})
            output[edition+'_'+cut] = {'rang_okeoly_f99r_18':check,'rangees':rows}
    return output


if __name__ == '__main__':
    data, _ = corpus()
    results = {}
    for name,file,strict in [('strict','rangees.tsv',True),('elargi','pots_elargis.tsv',False)]:
        examples = inventory(data,file,strict)
        results[name] = {'rangees': examples, 'totaux': summarize(examples)}
    results['controles_apres_calcul'] = reading_controls(data,results['strict']['rangees'])
    (HERE/'RESULTATS.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
