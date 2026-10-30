#!/usr/bin/env python3
"""Verify the stored phase-20 artifacts; does not rerun experiments.

CC BY-SA 4.0; see phase README for attribution.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'SHA256SUMS.json'


def inventory():
    rows=[]
    for path in sorted(ROOT.rglob('*')):
        relative=path.relative_to(ROOT)
        if not path.is_file() or path==MANIFEST or {'tmp','__pycache__'}&set(relative.parts):
            continue
        if path.suffix in ('.pyc','.writing'):
            continue
        data=path.read_bytes()
        rows.append({'path':str(relative),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args();rows=inventory()
    if args.write:
        MANIFEST.write_text(json.dumps({'scope':'Post-experiment integrity inventory, not a preregistration. Excludes local models, temporary files and caches.','files':rows},indent=2)+'\n')
    elif json.loads(MANIFEST.read_text())['files']!=rows:
        raise SystemExit('Phase-20 inventory mismatch')
    print(json.dumps({'status':'written' if args.write else 'passed','files':len(rows)}))


if __name__=='__main__':
    main()
