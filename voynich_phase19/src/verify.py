#!/usr/bin/env python3
"""Verify phase-19 scores, generator provenance and retained-role null invariants.

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

import engine as inputs
import study
import gzip
import random
import copy

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
    assert result['fingerprint']['runner'] == inputs.sha(ROOT/'src/engine.py')
    assert result['fingerprint']['study'] == inputs.sha(ROOT/'src/study.py')
    assert result['fingerprint']['generator'] == inputs.sha(ROOT/'src/generators.py')
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


def scored_slots(rows):
    retained = set()
    for ri, row in enumerate(rows):
        start = 0
        for end in range(len(row['words'])+1):
            if end == len(row['words']) or row['words'][end] is None:
                words = row['words'][start:end]
                if len(' '.join(words)) >= 4:
                    retained.update((ri, wi) for wi in range(start, end))
                start = end+1
    return retained


def category(word, i):
    return 'singleton' if len(word) == 1 else 'initial' if i == 0 else 'final' if i+1 == len(word) else 'interior'


def verify_generator(base, template, model, p):
    # Reconstruct the sufficient statistics from independently selected training
    # spans; the template's test symbols are never included.
    expected = collections.defaultdict(collections.Counter)
    global_counts = collections.Counter()
    for ri, wi in sorted(scored_slots(template['train'])):
        word = template['train'][ri]['words'][wi]
        for index, ch in enumerate(word):
            tag = category(word, index)
            global_counts[ch] += 1
            expected[tag, ''][ch] += 1
            if index >= 1:
                expected[tag, word[index-1]][ch] += 1
            if index >= 2:
                expected[tag, word[index-2:index]][ch] += 1
    actual = {(r['role'], r['context']): r['letters'] for r in model['counts']}
    assert actual == dict(expected)
    assert model['global_counts'] == dict(global_counts)
    assert model['order'] == 2 and model['alpha'] == 1.0
    assert base['model_sha256'] == study.digest(model)
    assert model['alphabet'] == sorted(global_counts)
    alphabet = model['alphabet']
    regenerated_letters = 0
    probability_cache = {}
    def draw(tag, prefix, rng):
        history = prefix[-2:]
        if (tag, history) not in probability_cache:
            counts = actual.get((tag, ''), global_counts)
            weights = [counts.get(c, 0)/sum(counts.values()) for c in alphabet]
            for length in range(1, len(history)+1):
                counts = actual.get((tag, history[-length:]), {})
                total = sum(counts.values())
                weights = [(counts.get(c, 0)+w)/(total+1) for c, w in zip(alphabet, weights)]
            probability_cache[tag, history] = weights
        return rng.choices(alphabet, weights=probability_cache[tag, history], k=1)[0]
    for split in ('train', 'test'):
        rng = random.Random(base['generation_seeds'][split])
        output = []
        for row in template[split]:
            words = []
            for source_word in row['words']:
                if source_word is None:
                    words.append(None)
                    continue
                # Source letters are never consulted to choose a character.
                shape = '.'*len(source_word)
                generated = ''
                for i in range(len(shape)):
                    generated += draw(category(shape, i), generated, rng)
                words.append(generated)
                regenerated_letters += len(generated)
            output.append(dict(row, words=words))
        assert output == base[split], (base['name'], split)
    return regenerated_letters


def main():
    p = inputs.protocol()
    calibration = inputs.load(ROOT/'results/calibration.json')
    summary = inputs.load(ROOT/'results/summary.json')
    bases = json.loads(gzip.decompress((ROOT/'data/base_cases.json.gz').read_bytes()))
    assert bases == study.base_cases(p)
    by_name = {b['name']: b for b in bases}
    models = inputs.load(ROOT/'data/markov_models.json')
    generated_letters = sum(verify_generator(b, by_name[b['template']], models[b['template']], p)
                            for b in bases if b['origin'] == 'Markov2')
    source = {c['case']: c for c in inputs.load(inputs.OLD/'source_inputs.json')}
    # Reconstruct the seed-line removal and ensure the full archived sample is used.
    raw = (ROOT.parent/'voynich_phase6/data/timm_generated_text.txt').read_text().splitlines()
    noncomments = [line for line in raw if line.strip() and not line.startswith('#')]
    timm_words = ' '.join(noncomments[1:]).split()
    assert timm_words == [w for r in source['Timm_generated']['lines'] for w in r['words'] if w]
    timm = by_name['Timm_published']
    assert timm['train']+timm['test'] == source['Timm_generated']['lines']
    assert not {r['page'] for r in timm['train']} & {r['page'] for r in timm['test']}
    fits, predictions, null_checks = 0, 0, 0
    for case in study.controls(p):
        results = {m: check_fit(case, m, p) for m in ['single', 'final']}
        fits += 2
        predictions += sum(r['test_letters'] for r in results.values())
        row = next(r for r in calibration['rows'] if r['name'] == case['name'])
        b = results['final']
        near(row['accuracy'], b['heldout_accuracy'])
        near(row['position_accuracy'], b['position_accuracy'])
        gate = p['calibration_gate']
        assert row['passed'] == (b['heldout_accuracy'] >= gate['overall_accuracy'] and
                                b['position_accuracy'] >= gate['position_accuracy'] and
                                b['test_coverage'] >= gate['training_support_coverage'])
        # Same solver path/budget and controls must reproduce phase 18 here.
        for m in ['single', 'final']:
            old = inputs.load(ROOT.parent/'voynich_phase18/results'/f"{case['name']}_{m}.json")
            assert old['key'] == results[m]['key']
            near(old['training_objective'], results[m]['training_objective'])
    assert calibration['passed'] == all(r['passed'] for r in calibration['rows'])
    manifest = {x['name']: x for x in inputs.load(ROOT/'data/case_inputs.json')}
    pairs = {r['name']: r for r in summary['comparisons']}
    for case in study.all_cases(p):
        original = by_name[case['base_name']]
        for split in ['train', 'test']:
            assert study.digest(case[split]) == manifest[case['name']][split+'_sha256']
            if case['null_index']:
                a, b = original[split], case[split]
                assert len(a) == len(b)
                assert role_counts(a, True) == role_counts(b, True)
                active = scored_slots(a)
                for ri, (before, after) in enumerate(zip(a, b)):
                    assert {k:v for k,v in before.items() if k != 'words'} == {k:v for k,v in after.items() if k != 'words'}
                    assert len(before['words']) == len(after['words'])
                    for wi, (x, y) in enumerate(zip(before['words'], after['words'])):
                        assert (None if x is None else len(x)) == (None if y is None else len(y))
                        if (ri, wi) not in active:
                            assert x == y
                null_checks += 1
        results = {m: check_fit(case, m, p) for m in ['single', 'final']}
        fits += 2
        predictions += sum(r['test_letters'] for r in results.values())
        row = pairs[case['name']]
        a, b = results['single'], results['final']
        near(row['single_bits'], a['test']['bits_per_quadgram'])
        near(row['final_bits'], b['test']['bits_per_quadgram'])
        near(row['gain_bits'], row['single_bits']-row['final_bits'])
        near(row['coverage'], b['test_coverage'])
        if case['origin'] == 'Voynich' and not case['null_index']:
            for m in ['single', 'final']:
                old = inputs.load(ROOT.parent/'voynich_phase18/results'/f"{case['base_name']}_latin_null00_{m}.json")
                assert old['key'] == results[m]['key']
                near(old['test']['bits_per_quadgram'], results[m]['test']['bits_per_quadgram'])
    for row in summary['observed']:
        nulls = [r['gain_bits'] for r in summary['comparisons'] if r['base_name'] == row['base_name'] and r['null_index']]
        assert len(nulls) == 19
        near(row['null_min'], min(nulls))
        near(row['null_max'], max(nulls))
        near(row['null_mean'], sum(nulls)/len(nulls))
        near(row['excess_over_null_mean'], row['gain_bits']-row['null_mean'])
        assert row['null_at_least_observed'] == sum(v >= row['gain_bits'] for v in nulls)
        assert row['final_signal'] == (row['gain_bits'] > 0 and row['gain_bits'] > max(nulls) and row['coverage'] >= .995)
    expected_signals = [r['base_name'] for r in summary['observed'] if r['origin'] != 'Voynich' and r['final_signal']]
    assert summary['message_free_signal_cases'] == expected_signals
    assert fits == 368 and null_checks == 342
    result = {'status': 'passed', 'fits_checked': fits, 'heldout_letter_predictions_checked': predictions,
              'null_split_invariants_checked': null_checks, 'max_scored_role_histogram_difference': 0,
              'markov_corpora_independently_regenerated': 6, 'markov_characters_regenerated': generated_letters,
              'timm_source_words_verified': len(timm_words), 'original_zl_and_calibration_match_phase18': True,
              'scope': 'Internal separate decoder/rescorer and generator reconstruction; shared archived input and language model. Not external replication.'}
    inputs.save(ROOT/'results/verification.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
