#!/usr/bin/env python3
"""Position-key calibration and held-out comparisons; never a translation.

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


def controls(p):
    source = {x['case']: x for x in load(OLD / 'source_inputs.json')}
    cases = []
    for li, (language, source_name) in enumerate(p['control_sources'].items()):
        lines = source[source_name]['lines']
        split = len(capped(lines, p['train_letter_cap']))
        for fi, family in enumerate(p['families']):
            for trial in range(1, p['control_keys_per_language_family']+1):
                seed = p['seed'] + 10000*li + 1000*fi + trial
                encrypted, keys = encrypt(lines, family, seed)
                name = f'control_{language}_{family}_{trial}'
                case = dict(name=name, language=language, family=family,
                            control=True, trial=trial, encryption_seed=seed,
                            train=encrypted[:split], test=encrypted[split:],
                            truth_train=lines[:split], truth_test=lines[split:],
                            true_encryption=keys)
                save(DATA / f'{name}_truth.json', {
                    'encryption_tables': keys, 'seed': seed, 'source_case': source_name,
                    'train_lines': split, 'test_lines': len(lines)-split,
                    'note': 'Evaluation only; not passed to optimizer.',
                })
                cases.append(case)
    return cases


def role(word, i):
    if len(word) == 1:
        return 'singleton'
    if i == 0:
        return 'initial'
    if i == len(word)-1:
        return 'final'
    return 'interior'


def shuffle_letters(lines, seed):
    """Permute within (physical leaf, role), separately within each split.

    Words' lengths, line breaks, unknowns and per-role symbol totals are fixed.
    This destroys local sequences, not the positional marginal distribution.
    """
    rng = random.Random(seed)
    result = copy.deepcopy(lines)
    positions = collections.defaultdict(list)
    for ri, row in enumerate(result):
        row['words'] = [list(w) if w is not None else None for w in row['words']]
        for wi, word in enumerate(row['words']):
            if word is not None:
                for ci in range(len(word)):
                    positions[(row['physical_leaf'], role(word, ci))].append((ri, wi, ci))
    for group in sorted(positions):
        locations = positions[group]
        values = [result[r]['words'][w][c] for r, w, c in locations]
        rng.shuffle(values)
        for (r, w, c), value in zip(locations, values):
            result[r]['words'][w][c] = value
    for row in result:
        row['words'] = [''.join(w) if w is not None else None for w in row['words']]
    return result


def real_cases(p):
    sources = [x for x in load(OLD / 'source_inputs.json') if x['case'] in p['real_cases']]
    leaves = sorted({row['physical_leaf'] for x in sources for row in x['lines']})
    test_leaves = set(leaves[::5])
    split = {'rule': p['real_split'], 'test_physical_leaves': sorted(test_leaves), 'cases': {}}
    result = []
    for ci, source in enumerate(sources):
        train = capped([r for r in source['lines'] if r['physical_leaf'] not in test_leaves], p['train_letter_cap'])
        test = [r for r in source['lines'] if r['physical_leaf'] in test_leaves]
        tr_leaves = sorted({r['physical_leaf'] for r in train})
        te_leaves = sorted({r['physical_leaf'] for r in test})
        assert not set(tr_leaves) & set(te_leaves)
        split['cases'][source['case']] = dict(train_leaves=tr_leaves, test_leaves=te_leaves,
                                              train_lines=len(train), test_lines=len(test))
        for null_index in range(1 + (p['null_replicates'] if source['case'].startswith('ZL') else 0)):
            seed = p['seed'] + 100000 + 1000*ci + null_index*2
            tr = train if not null_index else shuffle_letters(train, seed)
            te = test if not null_index else shuffle_letters(test, seed+1)
            for language in p['languages']:
                result.append(dict(name=f"{source['case']}_{language}_null{null_index:02}",
                                   source_case=source['case'], language=language, control=False,
                                   null_index=null_index, train=tr, test=te))
    save(DATA / 'split.json', split)
    return result


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
                   'runner': sha(Path(__file__)), 'input': sha(inp),
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


def compare(case, model, baseline, result, p):
    row = dict(name=case['name'], family=model, language=case['language'], control=case['control'],
               source_case=case.get('source_case'), null_index=case.get('null_index'),
               single_bits=baseline['test']['bits_per_quadgram'], position_bits=result['test']['bits_per_quadgram'],
               gain_bits=baseline['test']['bits_per_quadgram']-result['test']['bits_per_quadgram'],
               test_letters=result['test_letters'], test_quadgrams=result['test']['quadgrams'],
               coverage=result['test_coverage'])
    if case['control']:
        gate = p['calibration_gate']
        row.update(single_accuracy=baseline['heldout_accuracy'], accuracy=result['heldout_accuracy'],
                   position_accuracy=result['position_accuracy'], position_errors=result['position_errors'],
                   position_characters=result['position_characters'], errors=result['heldout_errors'],
                   gate_passed=result['heldout_accuracy'] >= gate['overall_accuracy'] and
                   result['position_accuracy'] >= gate['position_accuracy'] and
                   result['test_coverage'] >= gate['training_support_coverage'])
    return row


def run_controls(p, workers):
    def run(case):
        baseline = fit(case, 'single', p)
        result = fit(case, case['family'], p)
        return compare(case, case['family'], baseline, result, p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(run, controls(p)))
    gates = {family: all(r['gate_passed'] for r in rows if r['family'] == family) for family in p['families']}
    save(OUT / 'controls_summary.json', dict(rows=rows, family_gates=gates, protocol_sha256=sha(PROTOCOL)))
    print('CALIBRATION', gates, flush=True)


def run_real(p, workers):
    calibration = load(OUT / 'controls_summary.json')
    assert calibration['protocol_sha256'] == sha(PROTOCOL)
    expected = len(p['families'])*len(p['languages'])*p['control_keys_per_language_family']
    assert len(calibration['rows']) == expected
    allowed = [f for f in p['families'] if calibration['family_gates'][f]]
    if not allowed:
        save(OUT / 'real_status.json', {'status': 'not_run', 'reason': 'No family passed calibration.'})
        print('STOP: no calibrated family', flush=True)
        return
    # Check each cached control against the current inputs/code before opening the gate.
    for case in controls(p):
        if case['family'] in allowed:
            fit(case, case['family'], p)
    def run(case):
        baseline = fit(case, 'single', p)
        return [compare(case, model, baseline, fit(case, model, p), p) for model in allowed]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        nested = list(pool.map(run, real_cases(p)))
    rows = [row for group in nested for row in group]
    summary = []
    for row in rows:
        if row['null_index'] != 0:
            continue
        nulls = [r['gain_bits'] for r in rows if r['null_index'] and r['source_case'] == row['source_case']
                 and r['family'] == row['family'] and r['language'] == row['language']]
        summary.append(dict(row, null_count=len(nulls), null_min=min(nulls) if nulls else None,
                            null_max=max(nulls) if nulls else None,
                            null_mean=float(np.mean(nulls)) if nulls else None,
                            null_at_least_observed=sum(n >= row['gain_bits'] for n in nulls) if nulls else None))
    save(OUT / 'real_summary.json', {'observed': summary, 'all_comparisons': rows,
                                    'protocol_sha256': sha(PROTOCOL), 'families': allowed})
    save(OUT / 'real_status.json', {'status': 'completed', 'comparisons': len(rows), 'families': allowed})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'controls', 'real'])
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 4:
        parser.error('workers must be 1..4')
    p = protocol()
    if args.stage == 'prepare':
        prepare(p)
    elif args.stage == 'controls':
        run_controls(p, args.workers)
    else:
        run_real(p, args.workers)


if __name__ == '__main__':
    main()
