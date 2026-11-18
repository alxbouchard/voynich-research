"""Essaie deux passages datés sur les deux groupes centraux et leurs voisins."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MODULE = ROOT / 'research/2026-11-18-carte-sept-etoiles/lecture'
sys.dont_write_bytecode = True
sys.path.insert(0, str(MODULE))
from essai import frozen, project, tables

TARGETS = {
    'organe': (['racine', 'longue'], [(-1, 'la'), (2, 'et'), (3, 'deliee')]),
    'plante': (['aristologie', 'longue'], [(2, 'est'), (3, 'ainsi')]),
}
EXPECTED = {
    'IT2a-n': '7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5',
    'ZL3b-n': 'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc',
}
RULE = '673ff44f64faf8c9087b7fa57ce3c255c78f0382518c5b33af98d1565d516634'


def sources():
    lines = {}
    for edition, digest in EXPECTED.items():
        path = ROOT / f'voynich_20261028/data/{edition}.txt'
        assert sha256(path.read_bytes()).hexdigest() == digest
        line = next(s for s in path.read_text().splitlines() if s.startswith('<f89r2.22,@P0>'))
        raw = line.split('<%>')[1]
        lines[edition] = raw.split('<')[0].strip('.').split('.')[:8]
    archive = (HERE / 'sources-1998.txt').read_text().splitlines()
    for header, raw in zip(archive[::2], archive[1::2]):
        edition = re.fullmatch(r'<f89r2\.P3\.8;([HFLU])>', header)[1]
        words = raw.removeprefix('{plant}').removesuffix('-').replace('!', '').split('.')
        assert len(words) in (7, 8)
        # La ligne L finit plus tôt avant le pli. Aucune supposition sur le signe * de U.
        lines[edition] = words + [None] * (8 - len(words))
    assert lines['IT2a-n'] == lines['ZL3b-n'] == lines['H']
    return lines


def tokenize(word, compound, reverse):
    tokens = re.findall(r'ch|sh|.' if compound else '.', word)
    return tuple(reversed(tokens) if reverse else tokens)


def extend(keys, source, target, mute):
    pronounced = tuple(t for t in source if t not in mute)
    return [key for base in keys for key in tables(pronounced, target, None, base)]


def test_context(key, neighbors, mute):
    frozen_readings, covered, extended = {}, {}, [key]
    for offset, signs, target in neighbors:
        if signs is None:
            frozen_readings[offset] = None
            covered[offset] = None
            continue
        frozen_readings[offset] = project(signs, key)
        covered[offset] = frozen_readings[offset] == target
        extended = extend(extended, signs, target, mute)
    return {
        'readings': frozen_readings,
        'covered': covered,
        'all_known_readings_correct': all(v is True for v in covered.values()),
        'n_joint_extensions_observed_context': len(extended),
        'n_joint_extensions_full_context': len(extended) if None not in covered.values() else None,
    }


def fit_pair(words, sources, mute):
    keys = [{s: '' for s in mute}]
    for cipher, word in zip(sources, words):
        keys = extend(keys, cipher, word, mute)
    return keys


def levels(line, key_name, compound, reverse_chars, reverse_order):
    plain, offsets = TARGETS[key_name]
    start, step = (5, -1) if reverse_order else (4, 1)
    def signs_at(delta):
        word = line[start + step * delta]
        if word is None or '*' in word:
            return None
        return tokenize(word, compound, reverse_chars)

    src = [signs_at(i) for i in (0, 1)]
    alphabet = sorted(set(src[0]) | set(src[1]))
    neighbors = [(delta, signs_at(delta), tgt) for delta, tgt in offsets]
    counts, successes = {}, []
    for k in range(len(alphabet) + 1):
        keys = []
        for mute in combinations(alphabet, k):
            for key in fit_pair(plain, src, mute):
                assert [project(s, key) for s in src] == plain
                keys.append((mute, key))
        counts[k] = len(keys)
        if keys and (not successes or k <= 1):
            for mute, key in keys:
                successes.append({'mute': mute, 'table': key, **test_context(key, neighbors, mute)})
        if successes and k >= 1:
            break
    return {'compatibles_par_nombre_muet': counts, 'niveau_minimal': min((k for k in counts if counts[k]), default=None),
            'tables_au_minimum_et_aux_niveaux_zero_un': successes}


def calibration():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    cipher = {letter: f'v{idx:02d}' for idx, letter in enumerate(alphabet)}
    def encode(word, mute):
        return tuple(val for letter in word for val in ([cipher[letter], 'Z'] if mute else [cipher[letter]]))

    tests = []
    for anchor, (words, ctx) in TARGETS.items():
        for mute in ((), ('Z',)):
            src = [encode(w, mute) for w in words]
            known = fit_pair(words, src, mute)
            assert len(known) == 1
            key = known[0]
            check = test_context(key, [(i, encode(w, mute), w) for i, w in ctx], mute)
            # L'altération 'e' -> 'x' du deuxième nom contredit le e fixé sur le premier.
            assert not fit_pair([words[0], 'longux'], src, mute)
            if anchor == 'organe':
                assert check['readings'][-1] == 'la' and check['n_joint_extensions_full_context'] == 1
            else:
                assert check['all_known_readings_correct'] and check['n_joint_extensions_full_context'] == 1
            if mute:
                assert not fit_pair(words, src, ())
            tests.append({'cible': anchor, 'signe_muet': list(mute), **check, 'fausse_finale_rejetee': True})
    return tests


def main():
    assert sha256((HERE / 'PROTOCOLE.md').read_bytes()).hexdigest() == RULE
    rows = []
    for ed, line in sources().items():
        for name, compound, reverse_chars, reverse_order in product(TARGETS, (True, False), (False, True), (False, True)):
            result = levels(line, name, compound, reverse_chars, reverse_order)
            rows.append({'edition': ed, 'cible': name, 'composes': compound, 'signes_inverses': reverse_chars,
                         'ordre_inverse': reverse_order, **result})
    out = {'protocole_sha256': RULE, 'lignes': sources(), 'calibration': calibration(), 'essais': rows}
    (HERE / 'resultats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('Branches', len(rows), 'niveaux minimaux', Counter(r['niveau_minimal'] for r in rows))
    for ed in sources():
        subset = [r for r in rows if r['edition'] == ed]
        print(ed, Counter(r['niveau_minimal'] for r in subset),
              'contexte complet', sum((v['n_joint_extensions_full_context'] or 0) for r in subset
                                      for v in r['tables_au_minimum_et_aux_niveaux_zero_un']))


if __name__ == '__main__':
    main()
