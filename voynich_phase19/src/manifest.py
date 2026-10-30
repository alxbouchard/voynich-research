#!/usr/bin/env python3
"""Write or verify the phase-19 artifact inventory; does not rerun experiments."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'SHA256SUMS.json'


def inventory():
    entries = {}
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if not path.is_file() or path == MANIFEST or 'tmp' in relative.parts or '__pycache__' in relative.parts:
            continue
        if path.suffix in ('.pyc', '.writing'):
            continue
        data = path.read_bytes()
        entries[str(relative)] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Create/update inventory after deliberate changes.')
    args = parser.parse_args()
    current = inventory()
    if args.write:
        MANIFEST.write_text(json.dumps(current, ensure_ascii=False, indent=2)+'\n')
    else:
        expected = json.loads(MANIFEST.read_text())
        different = [key for key in set(current)|set(expected) if current.get(key) != expected.get(key)]
        if different:
            raise SystemExit('Inventory mismatch: '+', '.join(sorted(different)))
    print(json.dumps({'status': 'written' if args.write else 'passed', 'files': len(current),
                      'scope': 'Phase-19 stored artifacts, excluding regenerated tmp and Python cache.'}))


if __name__ == '__main__':
    main()
