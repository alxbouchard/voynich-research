"""Vérifier les familles de finales dans les inscriptions attribuées à Grove."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import re

from comparer import FALL, PANELS, benchmark, known, matches, score, show, suffix_map, units

HERE = Path(__file__).resolve().parent
RAW = HERE/'grove-index.json'


def extract(folder):
    entries, sources = {}, {}
    for panel in PANELS:
        file = folder/(panel+'.txt')
        section = 10 if panel.startswith('f70') else 12 if panel.startswith('f73') else 11
        sources[panel] = {'sha256':sha256(file.read_bytes()).hexdigest(),
                          'url':f'https://www.voynich.nu/q{section}/f0{panel[1:]}_tr.txt'}
        table = {}
        for line in file.read_text(encoding='latin-1').splitlines():
            m = re.match(r'^<([^>]+);V>\s*(.*)',line)
            if m:
                loc,raw = m.groups()
                assert loc not in table and loc.startswith(panel+'.')
                raw = re.sub(r'\{[^}]*\}', '', raw.split('=',1)[0]).replace('!','').strip()
                table[loc] = raw
        assert table and all(loc.split('.')[1].startswith('S') or loc=='f70v2.C.1' for loc in table)
        entries[panel] = table
    assert sum(map(len,entries.values())) == 299
    return {'sources':sources,'loci':entries}


def summarize(data, split):
    words = {}
    counts = {}
    for panel,table in data['loci'].items():
        index = {}
        count = Counter(loci=len(table))
        for loc, line in table.items():
            for word in line.replace(',', '.' if split else '').split('.'):
                if known(word):
                    count['groupes_lisibles'] += 1
                    index.setdefault(word, []).append(loc)
                    if len(units(word))>4:
                        count['groupes_admissibles_4'] += 1
        counts[panel] = count
        words[panel] = index
    index = {p:suffix_map(words[p]) for p in PANELS}
    autumn = matches(FALL,index)
    target = score(autumn)
    scores = [score(matches(ps,index)) for ps in combinations(PANELS,4)]
    return {'automne':show(autumn), 'score':target,'lots':benchmark(target,scores),'effectifs':counts,
            'lieux_eody':{p:{w:loc for w,loc in ws.items() if len(units(w))>4 and units(w)[-4:]==tuple('eody')}
                           for p,ws in words.items()}}


def main():
    parser=ArgumentParser()
    parser.add_argument('--sources',type=Path,help='Répertoire des douze pages interlinéaires, de f70v2.txt à f73v.txt.')
    args=parser.parse_args()
    if args.sources:
        raw = extract(args.sources)
        RAW.write_text(json.dumps(raw,sort_keys=True,ensure_ascii=False,indent=1)+'\n')
    else:
        raw = json.loads(RAW.read_text())
    results = {name:summarize(raw, split) for name,split in [('joints',False),('separes',True)]}
    (HERE/'grove-resultats.json').write_text(json.dumps(results,sort_keys=True,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main()
