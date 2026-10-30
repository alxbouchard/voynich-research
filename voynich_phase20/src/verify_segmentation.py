#!/usr/bin/env python3
"""Check the fixed-key diagnostic against unchanged upstream Perl modules.

CC BY-SA 4.0; attribution and limitations in ../README.md.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    vendor = json.loads((ROOT/'data/vendor_sources.json').read_text())
    for row in vendor['files']:
        path = ROOT/'vendor/hhk-decipherment'/row['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    models = json.loads((ROOT/'data/authors_model_sources.json').read_text())
    for row in models['extracted']:
        path = ROOT/'tmp/authors_models'/row['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    audit = json.loads((ROOT/'results/authors_exact_segmentation_audit.json').read_text())
    process = subprocess.run([
        'perl', str(ROOT/'src/verify_with_authors.pl'),
        str(ROOT/'tmp/reduced_model_tables.json'),
        str(ROOT/'tmp/authors_models/lmtrain_nyt_word.patlst'),
        str(ROOT/'results/authors_exact_segmentation_audit.json'),
    ], capture_output=True, text=True, check=True)
    if process.stderr:
        raise RuntimeError(process.stderr)
    actual = json.loads(process.stdout)
    assert actual['vocabulary_size'] == audit['vocabulary_size']
    errors = []
    assert len(actual['rows']) == len(audit['rows']) == 2
    for perl, python in zip(actual['rows'], audit['rows']):
        assert perl['candidate'] == python['candidate']
        assert perl['greedy_segmentation'] == python['greedy_segmentation']
        assert perl['exact_segmentation'] == python['exact']['segmentation']
        errors.extend([
            abs(perl['greedy_score_ln']-python['greedy_scores']['combined_score_ln']),
            abs(perl['exact_score_ln']-python['exact']['score_ln']),
            abs(python['exact']['score_ln']-python['exhaustive_check']['best_score_ln']),
        ])
        assert python['exact']['segmentation'] == python['exhaustive_check']['best_segmentation']
    assert max(errors) < 1e-9
    actual.update({
        'passed': True, 'maximum_score_difference': max(errors),
        'exhaustive_paths_checked': sum(x['exhaustive_check']['paths_enumerated'] for x in audit['rows']),
        'vendor_revision': vendor['revision'],
        'input_sha256': {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT/'results/authors_exact_segmentation_audit.json',
                      ROOT/'tmp/reduced_model_tables.json',
                      ROOT/'data/authors_model_sources.json']
        },
        'NOT_TRANSLATION': True,
    })
    (ROOT/'results/segmentation_verification.json').write_text(json.dumps(actual, indent=2)+'\n')
    print(json.dumps(actual, indent=2))


if __name__ == '__main__':
    main()
