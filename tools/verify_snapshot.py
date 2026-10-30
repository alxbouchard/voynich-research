#!/usr/bin/env python3
"""Verify archived research bytes, not the scientific validity of their conclusions."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    records = json.loads((ROOT / 'artifacts/file_index.json').read_text())
    paths = set()
    total = compressed = 0
    for record in records:
        assert record['path'] not in paths, record['path']
        paths.add(record['path'])
        stored = (ROOT / record['stored_path']).resolve()
        assert stored.is_relative_to(ROOT)
        payload = stored.read_bytes()
        if record['storage'] == 'gzip':
            payload = gzip.decompress(payload)
            compressed += 1
        assert len(payload) == record['bytes'], record['path']
        assert hashlib.sha256(payload).hexdigest() == record['sha256'], record['path']
        restored = ROOT / record['path']
        if record['storage'] == 'gzip' and restored.exists():
            assert hashlib.sha256(restored.read_bytes()).hexdigest() == record['sha256'], record['path']
        total += len(payload)
    for phase in range(1,18):
        assert (ROOT / f'docs/phases/{phase:02}_rapport_integral.txt').stat().st_size > 100
    print(json.dumps({'status': 'passed', 'logical_files': len(records),
                      'compressed_files': compressed, 'logical_bytes': total,
                      'reports': 17, 'scope': 'Integrity only; experiments not rerun'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
