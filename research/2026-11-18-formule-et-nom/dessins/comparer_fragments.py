"""Appariement des quatre notices aux douze légendes et aux deux blocs de prose."""
from collections import Counter
from functools import lru_cache
from itertools import permutations
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-phrase-et-doublets/noms'))
from reprendre import MODES, agreed, corpus, counts, inventory
from comparer import eligible

SRC = 'f89v2'
OBJECTS = {i: f'{SRC}.{n}' for i,n in zip(range(50,62),[2,3,4,5,6,12,13,14,24,25,27,28])}
PAIRS = {50: 'f10v', 54: 'f48v', 56: 'f24r', 61: 'f48r'}


@lru_cache(None)
def glyphs(word):
    return tuple(re.findall('c[kptf]h|ch|sh|.', word))


def similarity(word, candidate, variant):
    if word == candidate:
        return 1 if variant == 'identique' else 2
    if variant == 'identique':
        return 0
    small, big = sorted((glyphs(word), glyphs(candidate)), key=len)
    if len(small) < 4 or len(big)-len(small) not in (1,2):
        return 0
    site = big[-len(small):] if variant == 'debut_mobile' else big[:len(small)]
    return int(small == site)


def locus_order(locus):
    return int(locus.split('.')[1])


def collect(labels, prose, variant, line_limit):
    matrix = {}
    for obj, source in labels.items():
        cells = {}
        for page in PAIRS.values():
            loci = sorted([loc for loc in prose if loc.partition('.')[0] == page],key=locus_order)
            if line_limit:
                loci = loci[:line_limit]
            found = []
            for loc in loci:
                for (candidate,), n in sorted(prose[loc][0].items()):
                    for word in sorted(source):
                        score = similarity(word, candidate, variant)
                        if score:
                            found.append([loc, word, candidate, score, n])
            cells[page] = {'score': max((item[3] for item in found), default=0), 'preuves': found}
        matrix[obj] = cells
    totals = Counter(sum(matrix[obj][p]['score'] for obj,p in zip(PAIRS,assignment))
                     for assignment in permutations(PAIRS.values()))
    actual = sum(matrix[obj][p]['score'] for obj,p in PAIRS.items())
    ranks = {}
    for obj,p in PAIRS.items():
        val = matrix[obj][p]['score']
        rows = {other:cell['score'] for other,cell in matrix[obj].items()}
        cols = {other:matrix[other][p]['score'] for other in matrix}
        ranks[obj] = {'page_designee_seule': val > 0 and sum(x >= val for x in rows.values()) == 1,
                      'fragment_designe_seul': val > 0 and sum(x >= val for x in cols.values()) == 1}
    return {'matrice': matrix, 'classements': ranks, 'total': actual, 'affectations': dict(totals),
            'au_moins_observe_sur_24': sum(n for a,n in totals.items() if a>=actual)}


def row_context(prose):
    def locate(loci):
        return {pair:sorted([loc for loc in loci if pair in prose[loc][1]])
                for loc in loci for pair in prose[loc][1]}
    contexts = {'haut':locate([f'{SRC}.{n}' for n in range(7,11)]),
                'milieu':locate([f'{SRC}.{n}' for n in range(15,23)])}
    result = {}
    for p in PAIRS.values():
        large = locate([loc for loc in prose if loc.partition('.')[0]==p])
        result[p] = {}
        for name, ctx in contexts.items():
            common = sorted(set(ctx) & set(large))
            result[p][name] = {'paires_notice':len(large),'paires_contexte':len(ctx),'accords':len(common),
                               'union':len(set(ctx)|set(large)),
                               'communes':[{'mots':pair,'notice':large[pair],'rangee':ctx[pair]} for pair in common]}
    return result


def main():
    editions,_ = corpus()
    _,_,views = inventory()
    consensus = agreed(editions)
    output = {'appariements': PAIRS, 'loci': OBJECTS, 'lectures': {}, 'contextes':row_context(consensus)}
    for key, modes in [('commun', MODES)] + [('/'.join(m), [m]) for m in MODES]:
        labels = {obj:sorted(filter(eligible,set.intersection(*(set(views[m][0][SRC][loc]) for m in modes))))
                  for obj,loc in OBJECTS.items()}
        if key == 'commun':
            prose = consensus
        else:
            (ed, cut), = modes
            prose = {loc:[counts(raw,cut,1)] for loc,(p,kind,_,raw) in editions[ed].items()
                     if p in PAIRS.values() and kind=='P0'}
        output['lectures'][key] = {
            'legendes':labels,
            'mots_par_page':{p:sum(grams[0].total() for loc,grams in prose.items() if loc.partition('.')[0]==p)
                             for p in PAIRS.values()},
            'mots_deux_lignes':{p:sum(prose[loc][0].total() for loc in sorted(
                [l for l in prose if l.partition('.')[0]==p], key=locus_order)[:2]) for p in PAIRS.values()},
            'analyses':{f'{variant}/{limit or "notice"}':collect(labels,prose,variant,limit)
                        for variant in ['identique','debut_mobile','fin_mobile'] for limit in [None,2]}}
    (HERE/'RESULTATS.json').write_text(json.dumps(output,ensure_ascii=False,sort_keys=True,indent=1)+'\n')


if __name__ == '__main__':
    main()
