#!/usr/bin/env python3
"""Retrieve pinned upstream models locally; never add them to the repository.

CC BY-SA 4.0; attribution and corpus restrictions in ../README.md.
"""
import hashlib
import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT/'tmp/authors_models'


def valid(path, row):
    if not path.is_file() or path.stat().st_size != row['bytes']:
        return False
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest() == row['sha256']


def verified_write(source, destination, row):
    with tempfile.NamedTemporaryFile(dir=MODELS, delete=False) as target:
        temporary = Path(target.name)
        try:
            shutil.copyfileobj(source, target, length=1024*1024)
            target.flush()
            if not valid(temporary, row):
                raise ValueError(f'Integrity mismatch: {destination.name}')
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)


def main():
    manifest = json.loads((ROOT/'data/authors_model_sources.json').read_text())
    expected = {r['file']: r for r in manifest['extracted']}
    MODELS.mkdir(parents=True, exist_ok=True)
    for row in manifest['archives']:
        archive = MODELS/row['file']
        if not valid(archive, row):
            with urllib.request.urlopen(row['source_url'], timeout=120) as source:
                verified_write(source, archive, row)
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                if not member.isfile() or member.name not in expected:
                    raise ValueError(f'Unexpected archive member: {member.name}')
                destination = MODELS/member.name
                if not valid(destination, expected[member.name]):
                    with tar.extractfile(member) as source:
                        verified_write(source, destination, expected[member.name])
    if not all(valid(MODELS/name, row) for name, row in expected.items()):
        raise ValueError('Incomplete model set')
    print(json.dumps({'verified_archives': len(manifest['archives']),
                      'verified_models': len(expected), 'redistributed_models': False}))


if __name__ == '__main__':
    main()
