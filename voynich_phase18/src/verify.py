#!/usr/bin/env python3
"""Rescore all saved fits without the optimizer or its encoder/scoring functions.

Input/case preparation and frozen LMs are shared; decoding, position masks,
quadgram scoring and accuracies are recomputed separately in this program.
This is an internal cross-check, not an independent scholarly replication.
"""
import collections
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import experiment as inputs

ROOT = Path(__file__).resolve().parents[1]


def decode(rows, key, family):
    output, codes, positions = [], [], []
    anchor = len(key)-1
    for row in rows:
        runs = [[]]
        for word in row['words']:
            if word is None:
                runs.append([])
            else:
                runs[-1].append(word)
        for words in runs:
            if sum(map(len, words)) + max(0, len(words)-1) < 4:
                continue
            text, ids, marks = [], [], []
            for wi, word in enumerate(words):
                if wi:
                    text.append(' ')
                    ids.append(anchor)
                    marks.append(False)
                for i, ch in enumerate(word):
                    at_position = (i == 0) if family == 'initial' else (i+1 == len(word)) if family == 'final' else False
                    code = ord(ch)-ord('a') + (26 if at_position else 0)
                    ids.append(code)
                    text.append(key[code])
                    marks.append(at_position)
            output.append(''.join(text))
            codes.append(ids)
            positions.append(marks)
    return output, codes, positions


def rescore(texts, lm, q, weight):
    grams = collections.Counter()
    chars = collections.Counter()
    for text in texts:
        chars.update(text)
        grams.update(text[i:i+4] for i in range(len(text)-3))
    ll = 0.
    for word, n in grams.items():
        index = 0
        for c in word:
            index = index*27 + (26 if c == ' ' else ord(c)-97)
        ll += n*float(lm[index])
    n = chars.total()
    penalty = sum(v*math.log2(v/(n*q[26 if c == ' ' else ord(c)-97])) for c, v in chars.items())
    return {'characters': n, 'quadgrams': grams.total(),
            'bits_per_quadgram': -ll/grams.total(), 'objective': ll-weight*penalty}


def near(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-7), (a, b)


def role_counts(rows, retained_only=False):
    """Independent histogram, with optional exclusion of short barrier spans."""
    counts = collections.Counter()
    for row in rows:
        runs = [[]]
        for word in row['words']:
            if word is None:
                runs.append([])
            else:
                runs[-1].append(word)
        for words in runs:
            if retained_only and len(' '.join(words)) < 4:
                continue
            for word in words:
                for i, ch in enumerate(word):
                    tag = 'singleton' if len(word) == 1 else 'initial' if i == 0 else 'final' if i == len(word)-1 else 'interior'
                    counts[(row['physical_leaf'], tag, ch)] += 1
    return counts


def check_fit(case, model, p):
    result = inputs.load(ROOT/'results'/f"{case['name']}_{model}.json")
    key = result['key']
    assert len(key) == (27 if model == 'single' else 53)
    assert key[-1] == ' '
    for offset in range(0, len(key)-1, 26):
        assert sorted(key[offset:offset+26]) == list(inputs.ALPHABET)
    assert result['fingerprint']['protocol'] == inputs.sha(ROOT/'PROTOCOL.json')
    assert result['fingerprint']['runner'] == inputs.sha(ROOT/'src/experiment.py')
    assert result['fingerprint']['solver'] == inputs.sha(ROOT/'src/position_permutation.cpp')
    train, training_codes, _ = decode(case['train'], key, model)
    test, test_codes, _ = decode(case['test'], key, model)
    encoded = '\n'.join(' '.join(map(str, seq)) for seq in training_codes)+'\n'
    assert result['fingerprint']['input'] == hashlib.sha256(encoded.encode()).hexdigest()
    assert result['fingerprint']['test'] == hashlib.sha256(json.dumps(test_codes).encode()).hexdigest()
    assert test == result['test_decoded_NOT_TRANSLATION']
    lm, q = inputs.models(case['language'])
    assert result['fingerprint']['lm'] == inputs.sha(ROOT/'tmp'/f"{case['language']}_lm.bin")
    assert result['fingerprint']['frequency'] == inputs.sha(ROOT/'tmp'/f"{case['language']}_freq.txt")
    tr = rescore(train, lm, q, p['optimizer']['lambda'])
    te = rescore(test, lm, q, 0)
    for field in tr:
        near(tr[field], result['train'][field])
        near(te[field], result['test'][field])
    near(tr['objective'], result['training_objective'])
    near(max(result['restart_objectives']), result['training_objective'])
    counts = collections.Counter(c for seq in training_codes for c in seq)
    assert [counts[i] for i in range(len(key))] == result['training_symbol_counts']
    letters = sum(c != len(key)-1 for seq in test_codes for c in seq)
    unseen = sum(c != len(key)-1 and counts[c] == 0 for seq in test_codes for c in seq)
    assert letters == result['test_letters'] and unseen == result['test_unseen_training']
    near(1-unseen/letters, result['test_coverage'])
    if case['control']:
        family = case['family']
        identity = inputs.ALPHABET*2+' '
        truth, _, position_mask = decode(case['truth_test'], identity, family)
        assert [len(s) for s in truth] == [len(s) for s in test]
        errors = sum(a != b for s, t in zip(truth, test) for a, b in zip(s, t) if a != ' ')
        pos = [(a, b) for s, t, m in zip(truth, test, position_mask) for a, b, marked in zip(s, t, m) if marked]
        pos_errors = sum(a != b for a, b in pos)
        assert errors == result['heldout_errors'] and pos_errors == result['position_errors']
        assert len(pos) == result['position_characters']
        near(1-errors/letters, result['heldout_accuracy'])
        near(1-pos_errors/len(pos), result['position_accuracy'])
        # Independent inverse-key round trip from the saved synthetic cipher.
        true_key = ''.join(''.join(chr(97+t.index(c)) for c in inputs.ALPHABET) for t in case['true_encryption'])+' '
        assert decode(case['test'], true_key, family)[0] == truth
        if model != 'single':
            true_train = decode(case['truth_train'], identity, family)[0]
            for field, value in rescore(true_train, lm, q, p['optimizer']['lambda']).items():
                near(value, result['true_key_train'][field])
            for field, value in rescore(truth, lm, q, 0).items():
                near(value, result['true_key_test'][field])
    return result


def main():
    p = inputs.protocol()
    summary = inputs.load(ROOT/'results/controls_summary.json')
    checked, letters = 0, 0
    for case in inputs.controls(p):
        results = {model: check_fit(case, model, p) for model in ('single', case['family'])}
        checked += 2
        letters += sum(r['test_letters'] for r in results.values())
        row = next(r for r in summary['rows'] if r['name'] == case['name'])
        a, b = results['single'], results[case['family']]
        near(row['gain_bits'], a['test']['bits_per_quadgram']-b['test']['bits_per_quadgram'])
        gate = p['calibration_gate']
        passed = b['heldout_accuracy'] >= gate['overall_accuracy'] and b['position_accuracy'] >= gate['position_accuracy'] and b['test_coverage'] >= gate['training_support_coverage']
        assert row['gate_passed'] == passed
        near(row['accuracy'], b['heldout_accuracy'])
        near(row['position_accuracy'], b['position_accuracy'])
    for family in p['families']:
        assert summary['family_gates'][family] == all(r['gate_passed'] for r in summary['rows'] if r['family'] == family)
    path = ROOT/'results/real_summary.json'
    null_checks, effective_marginal_max_l1 = 0, 0
    if path.exists():
        real = inputs.load(path)
        cases = inputs.real_cases(p)
        originals = {c['source_case']: c for c in cases if c['null_index'] == 0}
        for case in cases:
            if case['null_index'] and case['language'] == 'latin':
                original = originals[case['source_case']]
                for split in ['train', 'test']:
                    before, after = original[split], case[split]
                    assert [(r['page'], r['locus'], [len(w) if w is not None else None for w in r['words']]) for r in before] == [(r['page'], r['locus'], [len(w) if w is not None else None for w in r['words']]) for r in after]
                    assert role_counts(before) == role_counts(after)
                    a, b = role_counts(before, True), role_counts(after, True)
                    l1 = sum(abs(a[k]-b[k]) for k in set(a)|set(b))
                    effective_marginal_max_l1 = max(effective_marginal_max_l1, l1)
                    null_checks += 1
            results = {model: check_fit(case, model, p) for model in ['single']+real['families']}
            checked += len(results)
            letters += sum(r['test_letters'] for r in results.values())
            for family in real['families']:
                row = next(r for r in real['all_comparisons'] if r['name'] == case['name'] and r['family'] == family)
                near(row['gain_bits'], results['single']['test']['bits_per_quadgram']-results[family]['test']['bits_per_quadgram'])
                assert summary['family_gates'][family]
        for row in real['observed']:
            nulls = [r['gain_bits'] for r in real['all_comparisons'] if r['source_case'] == row['source_case'] and
                     r['family'] == row['family'] and r['language'] == row['language'] and r['null_index']]
            assert len(nulls) == (p['null_replicates'] if row['source_case'].startswith('ZL') else 0)
            assert row['null_count'] == len(nulls)
            if nulls:
                near(min(nulls), row['null_min'])
                near(max(nulls), row['null_max'])
                near(sum(nulls)/len(nulls), row['null_mean'])
                assert sum(x >= row['gain_bits'] for x in nulls) == row['null_at_least_observed']
    result = {'status': 'passed', 'fits_checked': checked, 'heldout_letter_predictions_checked': letters,
              'null_split_invariants_checked': null_checks,
              'max_retained_role_histogram_l1_after_short_span_filter': effective_marginal_max_l1,
              'null_filter_caveat': 'Role counts are preserved before short spans are excluded. Shuffling can exchange a letter with an excluded short span, so retained-only counts can differ slightly.',
              'real_results_checked': path.exists(), 'scope': __doc__}
    inputs.save(ROOT/'results/verification.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
