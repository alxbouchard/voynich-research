"""Contrôles de l'alignement et reproduction du test principal depuis la table publiée."""
import csv
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import json

from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
forced = runpy.run_path(str(HERE / 'mesurer.py'))['forced']


def exhaustive_align(a, b):
    for k in range(min(len(a), len(b)), -1, -1):
        solutions = []
        for ii in combinations(range(len(a)), k):
            words = tuple(a[i] for i in ii)
            if '?' in words:
                continue
            for jj in combinations(range(len(b)), k):
                if words == tuple(b[j] for j in jj):
                    solutions.append(set(zip(ii, jj)))
        if solutions:
            return dict(set.intersection(*solutions))


def check_alignments():
    seqs = [seq for length in range(5) for seq in product(('a', 'b', '?'), repeat=length)]
    for left, right in product(seqs, repeat=2):
        assert forced(left, right) == exhaustive_align(left, right), (left, right)
    return len(seqs) ** 2


def check_published():
    summary = json.loads((HERE / 'resultats.json').read_text())
    with (HERE / 'occurrences.tsv').open() as file:
        rows = list(csv.DictReader(file, delimiter='\t'))
    assert len(rows) == sum(summary[subset]['jetons_de_familles'] for subset in ('H', 'autres'))
    ids = [(r['lieu'], r['troncon'], r['rang_troncon_IT']) for r in rows]
    assert len(set(ids)) == len(ids)
    herbal = [r for r in rows if r['section'] == 'H']
    assert len({r['famille'] for r in herbal}) == summary['H']['familles']
    assert all(int(r['feuillet']) not in (10, 11, 15, 96) and r['famille'] != 'cth' for r in rows)
    grouped = defaultdict(list)
    for row in herbal:
        roles = row['positions'].split('+')
        if 'avant' in roles or roles == ['interieur']:
            grouped[row['page'], row['famille']].append(('avant' in roles, row['forme'] == 'courte'))
    observed = 0
    mean = Fraction()
    distribution = {0: Fraction(1)}
    count = 0
    for pairs in grouped.values():
        n = len(pairs)
        k = sum(edge for edge, short in pairs)
        m = sum(short for edge, short in pairs)
        if k in (0, n) or m in (0, n):
            continue
        count += 1
        observed += sum(edge and short for edge, short in pairs)
        mean += Fraction(k * m, n)
        assignments = Counter(sum(pairs[i][1] for i in sampled) for sampled in combinations(range(n), k))
        weights = Counter()
        for cumulative, current_p in distribution.items():
            for extra, freq in assignments.items():
                weights[cumulative + extra] += current_p * Fraction(freq, sum(assignments.values()))
        distribution = weights
    tail = sum(weight for shorts, weight in distribution.items() if shorts >= observed)
    published = summary['H']['tests']['avant']
    assert count == published['strates_informatives']
    assert observed == published['courts_bord_observes']
    assert float(mean) == published['courts_bord_attendus']
    assert float(tail) == published['p_superieur_ou_egal']
    print(f'{len(rows)} occurrences uniques, {count} strates, {observed} courts pour E={mean}, p={tail}.')


if __name__ == '__main__':
    print(f'{check_alignments()} couples de séquences contrôlés par énumération.')
    check_published()
