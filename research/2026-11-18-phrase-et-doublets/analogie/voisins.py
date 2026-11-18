"""Taux d'insertion général et voisins des formes exactes du cas de départ."""
from collections import Counter, defaultdict
from fractions import Fraction
import json
import re

from quadruplets import EXCLUDED, HERE, corpus, runs, save, units

WORDS = {'shody','sholdy','shordy'}


def read(rows, cut):
    lines = {}
    for loc, (page, kind, _, raw) in rows.items():
        if kind != 'P0' or re.match(r'f\d+',page)[0] in EXCLUDED:
            continue
        pairs, singles = Counter(), Counter()
        for segment in runs(re.sub(r'\{[^}]*\}', '?', raw),cut):
            ws = [w for _,w in segment]
            pairs.update(zip(ws,ws[1:]))
            singles.update(w for w in ws if w in WORDS)
        lines[loc] = (pairs,singles)
    return lines


def insert_kind(left, right):
    if len(right) != len(left)+1:
        return None, False
    positions = [i for i in range(1,len(left)) if right[:i]+right[i+1:] == left]
    return right[2] if 2 in positions else None, bool(positions)


def main():
    assert insert_kind(('a','b','c'),('a','b','d','c')) == ('d',True)
    editions, sections = corpus()
    views = [read(rows, cut) for rows in editions.values() for cut in ('joints','separes')]
    strata = defaultdict(Counter)
    solo = defaultdict(dict)
    selected = defaultdict(dict)
    successors = Counter()
    for loc in sorted(set.intersection(*(set(v) for v in views))):
        pairs, singles = [counter.copy() for counter in views[0][loc]]
        for view in views[1:]:
            pairs &= view[loc][0]
            singles &= view[loc][1]
        for w,n in singles.items():
            solo[w][loc] = n
        for (c,d),n in pairs.items():
            if c in WORDS and d in WORDS and (d=='shody') != (c=='shody'):
                selected[c+' '+d][loc] = n
            if c == 'shody':
                successors[d] += n
            C, D = units(c), units(d)
            if len(C) >= 3:
                count = strata[sections.get(loc.split('.')[0], '?'),len(C)]
                sign, possible = insert_kind(C,D)
                count['paires'] += n
                count['insertion_apres_2'] += n*bool(sign)
                count['insertion_interne'] += n*possible
    rows = json.loads((HERE/'RESULTATS.json').read_text())['direct']['accord']['essais_complets']
    expected = Counter()
    for loc, _, _, c, _ in rows:
        counts = strata[sections.get(loc.split('.')[0], '?'), len(units(c))]
        for test in ('insertion_apres_2','insertion_interne'):
            expected[test] += Fraction(counts[test],counts['paires'])
    combined = sum(strata.values(),Counter())
    report = {'base':dict(combined), 'par_strate':{str(k):dict(v) for k,v in sorted(strata.items())},
              'attente_sur_les_essais': {k:float(v) for k,v in expected.items()},
              'nombre_essais':len(rows),
              'mots_seuls':{k:{'total':sum(v.values()),'lieux':v} for k,v in solo.items()},
              'paires_ciblees': {key:selected[key] for key in
                ('shody sholdy','sholdy shody','shody shordy','shordy shody')},
              'voisins_droits_shody': dict(successors)}
    save('VOISINS.json',report)
    print(combined, report['attente_sur_les_essais'])
    print({k:v['total'] for k,v in report['mots_seuls'].items()}, report['paires_ciblees'])
    print('Voisins',len(successors),sum(successors.values()),successors.most_common(15))


if __name__=='__main__':
    main()
