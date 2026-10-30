#!/usr/bin/env python3
"""Run the authors' README fixture, never a Voynich decipherment.

CC BY-SA 4.0; see ../README.md for attribution.
"""
import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'vendor/hhk-decipherment'
MODELS = ROOT / 'tmp/authors_models'
OUT = ROOT / 'results'
PLAIN = 'this is a top secret message'
CIPHER = 'ziol ol q zgh ltektz dtllqut'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rerun', action='store_true', help='Recompute and replace both smoke-test results.')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    for row in json.loads((ROOT/'data/vendor_sources.json').read_text())['files']:
        assert hashlib.sha256((VENDOR/row['path']).read_bytes()).hexdigest() == row['sha256']
    for row in json.loads((ROOT/'data/authors_model_sources.json').read_text())['extracted']:
        assert hashlib.sha256((MODELS/row['file']).read_bytes()).hexdigest() == row['sha256']
    rows = []
    for no_spaces in (False, True):
        name = 'authors_readme_' + ('no_spaces' if no_spaces else 'spaces')
        output_path = OUT / (name + '.json')
        if output_path.exists() and not args.rerun:
            print(json.dumps({'cached': name, 'recomputed': False}), flush=True)
            rows.append(json.loads(output_path.read_text()))
            continue
        command = ['perl', '-I', str(VENDOR), str(VENDOR/'masc_solver_mcts.pl'), '-mi', '100']
        if no_spaces:
            command.append('-n')
        ciphertext = CIPHER.replace(' ', '') if no_spaces else CIPHER
        env = dict(os.environ, PERL_HASH_SEED='0', PERL_PERTURB_KEYS='0')
        start = time.monotonic()
        print(json.dumps({'started': name, 'iterations': 100}), flush=True)
        with (OUT/(name+'.stdout.txt')).open('w') as stdout, (OUT/(name+'.stderr.txt')).open('w') as stderr:
            process = subprocess.Popen(command, cwd=MODELS, stdin=subprocess.PIPE,
                                       stdout=stdout, stderr=stderr, text=True, env=env)
            (ROOT/'tmp/current-smoke-process.json').write_text(json.dumps({'pid':process.pid,'case':name}))
            process.communicate(ciphertext+'\n')
        decoded = (OUT/(name+'.stdout.txt')).read_text().strip()
        actual, expected = decoded.replace(' ', ''), PLAIN.replace(' ', '')
        row = {'case': name, 'command': command, 'ciphertext': ciphertext,
               'plaintext': PLAIN, 'output': decoded, 'returncode': process.returncode,
               'seconds': round(time.monotonic()-start, 3),
               'matches_readme_letters': process.returncode == 0 and actual == expected,
               'character_accuracy': sum(a==b for a,b in zip(actual,expected))/len(expected) if len(actual)==len(expected) else None,
               'scope': 'Published example; installation check only, not held-out calibration.'}
        output_path.write_text(json.dumps(row,indent=2)+'\n')
        print(json.dumps(row), flush=True)
        rows.append(row)
    (OUT/'authors_smoke_summary.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__ == '__main__':
    main()
