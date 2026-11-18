"""Recherche d'une partie commune aux noms sur trois panneaux du même dépliant."""
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[3] / 'voynich_20261028/data'
FILES = {'H': 'IT2a-n.txt', 'ZL': 'ZL3b-n.txt'}
ROW = re.compile(r'^<(f68r[123]|f99r|f100r)\.(\d+),.([A-Za-z0-9]{2})>\s*(.*)')
UNITS = re.compile('ckh|cth|cph|cfh|ch|sh|[a-z]')


def load(path):
    groups = defaultdict(dict)
    for line in path.read_text().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        page, num, typ, raw = m.groups()
        desired = 'Ls' if page.startswith('f68') else 'Lf'
        if typ != desired and (page, typ) != ('f68r3', 'Ri'):
            continue
        group = 'rayons' if typ == 'Ri' else page
        locus = f'{page}.{num}'
        if locus == 'f99r.7':
            groups[group]['f99r.6'] += '.' + raw
        else:
            groups[group][locus] = raw
    expected = {'f68r1': 29, 'f68r2': 24, 'f68r3': 11, 'rayons': 8, 'f99r': 29, 'f100r': 17}
    assert {key: len(rows) for key, rows in groups.items()} == expected
    return groups


def patterns(word, compound):
    seq = UNITS.findall(word) if compound else list(word)
    return {tuple(seq[i:i+n]) for n in (2, 3) for i in range(len(seq) - n + 1)}


def inventories(groups, compound, join):
    entries = defaultdict(dict)
    excluded = defaultdict(list)
    for group, rows in groups.items():
        for loc, raw in rows.items():
            raw = re.sub(r'<![^>]*>|<[%$]>', '', raw)
            raw = raw.translate(str.maketrans('', '', '!{} ')).replace('<->', '.')
            words = raw.replace(',', '' if join else '.').strip('.').split('.')
            if group == 'rayons':
                for j, word in enumerate(words):
                    key = f'{loc}/{j+1}'
                    parts = patterns(word, compound) if re.fullmatch('[a-z]+', word) else None
                    for name in (['rayons_tous', 'rayons_premier'] if j == 0 else ['rayons_tous']):
                        if parts is None:
                            excluded[name].append(key)
                        else:
                            entries[name][key] = parts
            elif all(re.fullmatch('[a-z]+', word) for word in words):
                entries[group][loc] = set().union(*(patterns(w, compound) for w in words))
            else:
                excluded[group].append(loc)
    return entries, excluded


def count(groups, compound, join):
    entries, excluded = inventories(groups, compound, join)
    def coverage(pattern, group):
        labels = entries[group]
        return Fraction(sum(pattern in s for s in labels.values()), len(labels))
    panels = ['f68r1', 'f68r2']
    pool = set().union(*(parts for name in panels for parts in entries[name].values()))
    ranks = {p: min(coverage(p, name) for name in panels) for p in pool}
    high = max(ranks.values())
    results = {}
    for p in sorted(p for p in pool if ranks[p] == high):
        counts = {}
        for name, locations in entries.items():
            hits = [loc for loc, s in locations.items() if p in s]
            counts[name] = {'nombre':len(hits), 'dénominateur':len(locations), 'lieux':hits}
        target = entries['f68r3']
        counts['amas_sept'] = p in target['f68r3.11']
        counts['pour_suivre'] = (min(coverage(p, name) for name in panels + ['f68r3']) > Fraction(1, 2)
                                  and all(coverage(p, 'f68r3') > coverage(p, name) for name in ('rayons_premier','rayons_tous')))
        results[' '.join(p)] = counts
    return {'motifs_essayés':len(pool), 'meilleur_minimum':str(high), 'retenus':results, 'exclusions':excluded}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sortie', type=Path, default=HERE/'MESURES.json')
    out = ap.parse_args().sortie
    result = {}
    for ed, name in FILES.items():
        path = DATA/name
        groups = load(path)
        scores = {}
        for compound in (True, False):
            for join in (False, True):
                key = ('unités' if compound else 'caractères') + ('_joints' if join else '_séparés')
                scores[key] = count(groups, compound, join)
        result[ed] = {'source_sha256':sha256(path.read_bytes()).hexdigest(), 'essais':scores}
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()
