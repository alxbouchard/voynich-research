#!/usr/bin/env python3
"""Restore large texts from the lossless committed blobs; never overwrite edits."""
import gzip
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    records = json.loads((ROOT / 'artifacts/file_index.json').read_text())
    restored = skipped = 0
    for record in records:
        if record['storage'] != 'gzip':
            continue
        target = (ROOT / record['path']).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError('Path outside repository')
        expected = record['sha256']
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise RuntimeError(f'Refusing to overwrite modified file: {record["path"]}')
            skipped += 1
            continue
        payload = gzip.decompress((ROOT / record['stored_path']).read_bytes())
        assert len(payload) == record['bytes']
        assert hashlib.sha256(payload).hexdigest() == expected
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + '.writing')
        with temporary.open('xb') as out:
            out.write(payload)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, target)
        restored += 1
    print(json.dumps({'restored': restored, 'already_identical': skipped}))

if __name__ == '__main__':
    main()
