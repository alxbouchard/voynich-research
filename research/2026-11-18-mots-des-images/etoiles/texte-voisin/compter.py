"""Neuf associations entre légendes d'étoiles et texte du dépliant f68r."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[3] / 'voynich_20261028/data'
PAGES = ('f68r1', 'f68r2', 'f68r3')
FILES = {
    'H': ('IT2a-n.txt', '7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5'),
    'ZL': ('ZL3b-n.txt', 'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc'),
}
ROW = re.compile(r'<(f68r[123])\.(\d+),.(Ls|P0|C\w)>\s*(.*)')
UNIT = re.compile(r'ckh|cph|cth|cfh|ch|sh|@[0-9]{3};|[a-z]')
EXPECTED = {'f68r1': {'Ls': 29, 'P0': 4, 'Cc': 1},
            'f68r2': {'Ls': 24, 'P0': 5, 'Cc': 2}, 'f68r3': {'Ls': 11, 'Cc': 2}}


def read_file(name, digest):
    raw = (DATA / name).read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f'Empreinte inattendue de {name}')
    records = {}
    counts = defaultdict(Counter)
    for line in raw.decode().splitlines():
        m = ROW.fullmatch(line)
        if m:
            page, number, kind, content = m.groups()
            key = (page, int(number), kind)
            assert key not in records
            records[key] = content
            counts[page][kind] += 1
    assert counts == EXPECTED
    return records


def words(raw, join):
    clear = re.sub(r'<![^>]*>|<[\$%]>', '', raw).replace('<->', '.')
    clear = clear.translate(str.maketrans('', '', '!{} ')).replace(',', '' if join else '.')
    result = []
    for word in clear.strip('.').split('.'):
        if not word:
            raise ValueError(f'Groupe vide inattendu dans {raw}')
        if '?' in word or '[' in word:
            result.append((None, 0))
            continue
        units = UNIT.findall(word)
        if ''.join(units) != word:
            raise ValueError(f'Encodage inconnu dans {word}')
        result.append((word, len(units)))
    return result


def positions(records, join):
    groups = {}
    for (page, number, kind), raw in records.items():
        for i, token in enumerate(words(raw, join), 1):
            groups[page, number, kind, i] = token
    return groups


def locus(key):
    page, number, kind, index = key
    return f'{page}.{number},{kind}/{index}'


def inventory(tokens, other, agreement):
    labels = {page: defaultdict(list) for page in PAGES}
    for key, (word, size) in tokens.items():
        if key[2] == 'Ls' and size >= 3 and (not agreement or other.get(key) == (word, size)):
            labels[key[0]][word].append(locus(key))
    return labels


def matrix(tokens, labels, register):
    texts = {page: [] for page in PAGES}
    for key, (word, size) in tokens.items():
        if key[2] == 'Ls' or (register != 'tous' and not key[2].startswith(register)):
            continue
        texts[key[0]].append((locus(key), word, size))
    counts = {page: {'positions': len(values), 'lisibles': sum(w is not None for _, w, _ in values),
                     'lisibles_3_unites': sum(size >= 3 for _, _, size in values)}
              for page, values in texts.items()}
    hits = {src: {dst: [{'mot': word, 'legendes': labels[src][word], 'texte': loc}
                        for loc, word, _ in texts[dst] if word in labels[src]]
                  for dst in PAGES} for src in PAGES}
    tests = {}
    for base in ('lisibles', 'lisibles_3_unites'):
        # A missing destination has no defined proportion. For P0 the two extant
        # texts are still assigned in all six possible ways; no 0/0 term is added.
        scores = {}
        for order in permutations(PAGES):
            score = sum((Fraction(len(hits[src][dst]), counts[dst][base])
                         for src, dst in zip(PAGES, order) if counts[dst][base]), Fraction(0))
            scores[tuple(order)] = score
        observed = scores[PAGES]
        tests[base] = {'sommes': {'/'.join(p[-1] for p in order): str(v) for order, v in scores.items()},
                       'superieures': sum(v > observed for v in scores.values()),
                       'ex_aequo': sum(v == observed for v in scores.values()),
                       'au_moins_diagonale_sur_six': sum(v >= observed for v in scores.values())}
    return {'textes': counts, 'rencontres': hits, 'permutations': tests}


def main():
    records = {ed: read_file(*file) for ed, file in FILES.items()}
    assert records['H'].keys() == records['ZL'].keys()
    output = {'prediction_commit': '29a4535', 'sources': FILES, 'variantes': {}}
    for spaces, join in [('separes', False), ('joints', True)]:
        tokens = {ed: positions(rows, join) for ed, rows in records.items()}
        for ed, other in [('H', 'ZL'), ('ZL', 'H')]:
            for agreed in (False, True):
                labels = inventory(tokens[ed], tokens[other], agreed)
                key = f'{ed}_{spaces}_' + ('accord' if agreed else 'tous')
                output['variantes'][key] = {
                    'inventaires': labels,
                    'registres': {r: matrix(tokens[ed], labels, r) for r in ('tous', 'P0', 'C')},
                }
    (HERE / 'MESURES.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
