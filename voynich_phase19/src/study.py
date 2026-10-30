#!/usr/bin/env python3
"""Phase 19: specificity of the word-final gain on message-free surrogates."""
import argparse
import collections
import concurrent.futures
import gzip
import hashlib
import json

import engine as e
import generators as g


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def base_cases(p, persist=False):
    source = {c['case']: c for c in e.load(e.OLD/'source_inputs.json')}
    leaf_sources = [source[name] for name in ['ZL_A', 'ZL_B', 'IT_A', 'IT_B']]
    leaves = sorted({r['physical_leaf'] for c in leaf_sources for r in c['lines']})
    reserved = set(leaves[::5])
    bases, models = [], {}
    for ci, name in enumerate(['ZL_A', 'ZL_B']):
        lines = source[name]['lines']
        train = e.capped([r for r in lines if r['physical_leaf'] not in reserved], p['train_letter_cap'])
        test = [r for r in lines if r['physical_leaf'] in reserved]
        assert not {r['physical_leaf'] for r in train} & {r['physical_leaf'] for r in test}
        original = dict(name=name, origin='Voynich', template=name, replicate=None,
                        control=False, language='latin', train=train, test=test)
        bases.append(original)
        model = g.train_markov(train, **p['markov'])
        models[name] = model
        for replicate in p['generator_replicates']:
            seed = p['generation_seed'] + ci*1000 + replicate*10
            bases.append(dict(name=f'Markov2_{name}_{replicate}', origin='Markov2', template=name,
                              replicate=replicate, control=False, language='latin',
                              train=g.generate(train, model, seed), test=g.generate(test, model, seed+1),
                              generation_seeds={'train': seed, 'test': seed+1},
                              model_sha256=digest(model)))
    # This layout is artificial. Keep whole artificial pages in chronological
    # train/test blocks; the original published generator is not rerun here.
    timm = source['Timm_generated']['lines']
    pages = list(dict.fromkeys(r['page'] for r in timm))
    train = []
    for page in pages:
        block = [r for r in timm if r['page'] == page]
        if sum(len(w) for r in train+block for w in r['words'] if w) > p['train_letter_cap']:
            break
        train.extend(block)
    selected_pages = {r['page'] for r in train}
    test = [r for r in timm if r['page'] not in selected_pages]
    assert selected_pages and test
    bases.append(dict(name='Timm_published', origin='Timm_published', template=None, replicate=None,
                      control=False, language='latin', train=train, test=test))
    if persist:
        e.save(e.DATA/'markov_models.json', models)
        payload = json.dumps(bases, ensure_ascii=False, separators=(',', ':')).encode()
        (e.DATA/'base_cases.json.gz').write_bytes(gzip.compress(payload, mtime=0))
        e.save(e.DATA/'split_and_generation.json', {
            'test_physical_leaves': sorted(reserved),
            'cases': [{k: c[k] for k in ['name', 'origin', 'template', 'replicate']} | {
                'train_lines': len(c['train']), 'test_lines': len(c['test']),
                'train_leaves': sorted({r['physical_leaf'] for r in c['train']}),
                'test_leaves': sorted({r['physical_leaf'] for r in c['test']}),
                'train_sha256': digest(c['train']), 'test_sha256': digest(c['test']),
                'generation_seeds': c.get('generation_seeds'), 'model_sha256': c.get('model_sha256'),
            } for c in bases],
        })
    return bases


def all_cases(p, persist=False):
    result = []
    for base in base_cases(p, persist):
        ci = p['shuffle_case_ids'][base['name']]
        for null_index in range(p['null_replicates']+1):
            seed = p['shuffle_seed'] + 1000*ci + 2*null_index
            case = dict(base, name=f"{base['name']}_null{null_index:02}", base_name=base['name'],
                        null_index=null_index, shuffle_seeds=None if null_index == 0 else {'train': seed, 'test': seed+1})
            if null_index:
                case['train'] = g.shuffle_retained(base['train'], seed)
                case['test'] = g.shuffle_retained(base['test'], seed+1)
            result.append(case)
    if persist:
        e.save(e.DATA/'case_inputs.json', [{k: c[k] for k in ['name', 'base_name', 'null_index', 'shuffle_seeds']} |
                                          {'train_sha256': digest(c['train']), 'test_sha256': digest(c['test'])} for c in result])
    return result


def controls(p):
    source = next(c for c in e.load(e.OLD/'source_inputs.json') if c['case'] == 'Latin_Pliny')
    lines = source['lines']
    cut = len(e.capped(lines, p['train_letter_cap']))
    cases = []
    for trial in range(1, 5):
        seed = 20261030+1000+trial  # Exact phase-18 Latin/final calibration keys.
        cipher, tables = e.encrypt(lines, 'final', seed)
        cases.append(dict(name=f'control_latin_final_{trial}', family='final', control=True,
                          language='latin', train=cipher[:cut], test=cipher[cut:],
                          truth_train=lines[:cut], truth_test=lines[cut:], true_encryption=tables))
    return cases


def comparison(case, single, final):
    return {'name': case['name'], 'base_name': case.get('base_name'), 'origin': case.get('origin'),
            'template': case.get('template'), 'replicate': case.get('replicate'),
            'null_index': case.get('null_index'), 'control': case['control'],
            'single_bits': single['test']['bits_per_quadgram'],
            'final_bits': final['test']['bits_per_quadgram'],
            'gain_bits': single['test']['bits_per_quadgram']-final['test']['bits_per_quadgram'],
            'coverage': final['test_coverage'], 'test_letters': final['test_letters'],
            'test_quadgrams': final['test']['quadgrams']}


def calibrate(p, workers):
    def run(case):
        a, b = e.fit(case, 'single', p), e.fit(case, 'final', p)
        row = comparison(case, a, b)
        gate = p['calibration_gate']
        row.update(accuracy=b['heldout_accuracy'], position_accuracy=b['position_accuracy'],
                   passed=b['heldout_accuracy'] >= gate['overall_accuracy'] and
                   b['position_accuracy'] >= gate['position_accuracy'] and
                   b['test_coverage'] >= gate['training_support_coverage'])
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(run, controls(p)))
    e.save(e.OUT/'calibration.json', {'rows': rows, 'passed': all(r['passed'] for r in rows), 'protocol_sha256': e.sha(e.PROTOCOL)})
    print('CALIBRATION', all(r['passed'] for r in rows), flush=True)


def experiment(p, workers):
    gate = e.load(e.OUT/'calibration.json')
    assert gate['protocol_sha256'] == e.sha(e.PROTOCOL) and len(gate['rows']) == 4 and gate['passed']
    for case in controls(p):
        e.fit(case, 'final', p)  # Revalidate cache hashes, never select on test.
    def run(case):
        return comparison(case, e.fit(case, 'single', p), e.fit(case, 'final', p))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(run, all_cases(p, persist=True)))
    observed = []
    for row in rows:
        if row['null_index']:
            continue
        nulls = [r['gain_bits'] for r in rows if r['base_name'] == row['base_name'] and r['null_index']]
        assert len(nulls) == p['null_replicates']
        mean = sum(nulls)/len(nulls)
        observed.append(dict(row, null_min=min(nulls), null_max=max(nulls), null_mean=mean,
                             null_at_least_observed=sum(v >= row['gain_bits'] for v in nulls),
                             excess_over_null_mean=row['gain_bits']-mean,
                             final_signal=row['gain_bits'] > 0 and row['gain_bits'] > max(nulls) and row['coverage'] >= .995))
    e.save(e.OUT/'summary.json', {'observed': observed, 'comparisons': rows, 'protocol_sha256': e.sha(e.PROTOCOL),
                                'message_free_signal_cases': [r['base_name'] for r in observed if r['origin'] != 'Voynich' and r['final_signal']]})
    print(json.dumps({'complete': True, 'comparisons': len(rows), 'message_free_signal_cases': [r['base_name'] for r in observed if r['origin'] != 'Voynich' and r['final_signal']]}), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stage', choices=['prepare', 'controls', 'run'])
    ap.add_argument('--workers', type=int, default=4)
    args = ap.parse_args()
    if not 1 <= args.workers <= 4:
        ap.error('workers must be 1..4')
    p = e.protocol()
    if args.stage == 'prepare':
        e.prepare(p)
        base_cases(p, persist=True)
    elif args.stage == 'controls':
        calibrate(p, args.workers)
    else:
        experiment(p, args.workers)


if __name__ == '__main__':
    main()
