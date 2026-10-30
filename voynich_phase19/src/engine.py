#!/usr/bin/env python3
"""Phase-19 adapter of the frozen phase-18 fitting engine; never a translation.

No network access. Frozen phase-10 inputs are read only. The C++ optimizer
receives cipher integers, a language model and a budget, never control truth.
"""
import argparse
import collections
import concurrent.futures
import copy
import hashlib
import json
import math
import platform
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OLD = REPO / 'voynich_phase10/data'
DATA, OUT, TMP = (ROOT / x for x in ('data', 'results', 'tmp'))
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
PROTOCOL = ROOT / 'PROTOCOL.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.writing')
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def load(path):
    return json.loads(path.read_text())


def protocol():
    p = load(PROTOCOL)
    for name, digest in p['input_sha256'].items():
        if sha(REPO / name) != digest:
            raise ValueError(f'Input changed: {name}')
    return p


def prepare(p):
    for folder in (DATA, OUT, TMP):
        folder.mkdir(parents=True, exist_ok=True)
    for language in p['languages']:
        text = (OLD / f'{language}_train_boundary.txt').read_text().strip()
        a = np.array([26 if c == ' ' else ALPHABET.index(c) for c in text], dtype=np.int32)
        ids = ((a[:-3]*27+a[1:-2])*27+a[2:-1])*27+a[3:]
        counts = np.bincount(ids, minlength=27**4)
        lm = np.log2((counts + p['lm_smoothing']) / (counts.sum() + p['lm_smoothing']*27**4))
        lm.astype('float64').tofile(TMP / f'{language}_lm.bin')
        q = np.bincount(a, minlength=27) + p['frequency_smoothing']
        q = q / q.sum()
        np.savetxt(TMP / f'{language}_freq.txt', q, fmt='%.18g')
    binary = TMP / 'position_permutation'
    source = ROOT / 'src/position_permutation.cpp'
    subprocess.run(['g++', '-O3', '-std=c++17', str(source), '-o', str(binary)], check=True)
    save(DATA / 'environment.json', {
        'python': sys.version, 'numpy': np.__version__, 'platform': platform.platform(),
        'compiler': subprocess.check_output(['g++', '--version'], text=True).splitlines()[0],
        'binary_sha256': sha(binary), 'solver_sha256': sha(source),
        'protocol_sha256': sha(PROTOCOL),
        'models': {x.name: sha(x) for x in sorted(TMP.glob('*_lm.bin'))},
    })


def capped(lines, maximum):
    result, count = [], 0
    for row in lines:
        n = sum(len(w) for w in row['words'] if w is not None)
        if count + n > maximum:
            break
        result.append(row)
        count += n
    return result


def selected(index, word, family):
    if family == 'initial':
        return index == 0
    if family == 'final':
        return index == len(word)-1
    if family == 'single':
        return False
    raise ValueError(family)


def segments(lines):
    """Break at each None and line. Retain only segments with a quadgram."""
    for row in lines:
        words = []
        for word in row['words'] + [None]:
            if word is None:
                if len(' '.join(words)) >= 4:
                    yield words
                words = []
            else:
                if not word or any(c not in ALPHABET for c in word):
                    raise ValueError(f'Invalid literal word: {word!r}')
                words.append(word)


def encode(lines, model):
    anchor = 26 if model == 'single' else 52
    encoded = []
    for words in segments(lines):
        seq = []
        for j, word in enumerate(words):
            if j:
                seq.append(anchor)
            seq.extend(ALPHABET.index(c) + 26*selected(i, word, model) for i, c in enumerate(word))
        encoded.append(seq)
    return encoded


def plain_segments(lines):
    return [' '.join(words) for words in segments(lines)]


def encrypt(lines, family, seed):
    rng = random.Random(seed)
    tables = []
    for _ in range(2):
        values = list(ALPHABET)
        rng.shuffle(values)
        tables.append(''.join(values))
    result = []
    for row in lines:
        words = [None if w is None else ''.join(tables[selected(i, w, family)][ALPHABET.index(c)]
                 for i, c in enumerate(w)) for w in row['words']]
        result.append(dict(row, words=words))
    return result, tables


def models(language):
    return np.fromfile(TMP / f'{language}_lm.bin'), np.loadtxt(TMP / f'{language}_freq.txt')


def score(texts, lm, q=None, weight=0):
    ll, grams, frequencies = 0., 0, np.zeros(27, dtype=np.int64)
    for text in texts:
        a = np.array([26 if c == ' ' else ALPHABET.index(c) for c in text], dtype=np.int32)
        ids = ((a[:-3]*27+a[1:-2])*27+a[2:-1])*27+a[3:]
        ll += float(lm[ids].sum())
        grams += len(ids)
        frequencies += np.bincount(a, minlength=27)
    n = int(frequencies.sum())
    penalty = 0.
    if q is not None:
        valid = frequencies > 0
        penalty = float((frequencies[valid]*np.log2(frequencies[valid]/(n*q[valid]))).sum())
    return dict(characters=n, quadgrams=grams, bits_per_quadgram=-ll/grams,
                objective=ll-weight*penalty)


def fit(case, model, p):
    path = OUT / f"{case['name']}_{model}.json"
    seqs, test = encode(case['train'], model), encode(case['test'], model)
    anchor = 26 if model == 'single' else 52
    inp = TMP / f"{case['name']}_{model}_train.txt"
    inp.write_text('\n'.join(' '.join(map(str, s)) for s in seqs)+'\n')
    fingerprint = {'protocol': sha(PROTOCOL), 'solver': sha(ROOT / 'src/position_permutation.cpp'),
                   'runner': sha(Path(__file__)), 'study': sha(ROOT / 'src/study.py'),
                   'generator': sha(ROOT / 'src/generators.py'), 'input': sha(inp),
                   'lm': sha(TMP / f"{case['language']}_lm.bin"),
                   'frequency': sha(TMP / f"{case['language']}_freq.txt"),
                   'test': hashlib.sha256(json.dumps(test).encode()).hexdigest()}
    if path.exists():
        cached = load(path)
        if cached['fingerprint'] != fingerprint:
            raise ValueError(f'Stale result: {path}; archive it before rerunning.')
        return cached
    opt = p['optimizer']
    cmd = [str(TMP / 'position_permutation'), str(TMP / f"{case['language']}_lm.bin"),
           str(TMP / f"{case['language']}_freq.txt"), str(inp), str(opt['restarts']),
           str(opt['steps']), str(p['seed']), str(opt['lambda']), str(opt['temperature']), str(anchor)]
    start = time.monotonic()
    result = json.loads(subprocess.check_output(cmd, text=True))
    result['key'] = result['key'].replace('{', ' ')
    key = result['key']
    assert len(key) == anchor+1 and key[anchor] == ' '
    assert all(sorted(key[i:i+26]) == list(ALPHABET) for i in range(0, anchor, 26))
    decoded = [''.join(key[i] for i in s) for s in test]
    counts = collections.Counter(i for seq in seqs for i in seq)
    letters = sum(i != anchor for seq in test for i in seq)
    unseen = sum(i != anchor and not counts[i] for seq in test for i in seq)
    lm, q = models(case['language'])
    train_score = score([''.join(key[i] for i in s) for s in seqs], lm, q, opt['lambda'])
    assert abs(train_score['objective']-result['training_objective']) < 1e-6*train_score['characters']
    result.update(name=case['name'], model=model, language=case['language'],
                  control=case['control'], seconds=round(time.monotonic()-start, 3),
                  fingerprint=fingerprint, train=train_score, test=score(decoded, lm),
                  test_letters=letters, test_unseen_training=unseen,
                  test_coverage=1-unseen/letters, training_symbol_counts=[counts[i] for i in range(anchor+1)],
                  test_decoded_NOT_TRANSLATION=decoded)
    if case['control']:
        truth = plain_segments(case['truth_test'])
        assert len(truth) == len(decoded) and all(len(a) == len(b) for a, b in zip(truth, decoded))
        err = sum(a != b for s, t in zip(truth, decoded) for a, b in zip(s, t) if a != ' ')
        marked = encode(case['test'], case['family'])
        pairs = [(a, b) for s, t, ids in zip(truth, decoded, marked)
                 for a, b, i in zip(s, t, ids) if 26 <= i < 52]
        positional_errors = sum(a != b for a, b in pairs)
        result.update(heldout_accuracy=1-err/letters, heldout_errors=err,
                      position_characters=len(pairs), position_errors=positional_errors,
                      position_accuracy=1-positional_errors/len(pairs))
        # True-key scores diagnose a misleading objective; truth never chooses a fitted key.
        if model != 'single':
            result['true_key_train'] = score(plain_segments(case['truth_train']), lm, q, opt['lambda'])
            result['true_key_test'] = score(truth, lm)
    save(path, result)
    print(json.dumps(dict(name=case['name'], model=model, seconds=result['seconds'],
                          accuracy=result.get('heldout_accuracy'), position_accuracy=result.get('position_accuracy'))), flush=True)
    return result
