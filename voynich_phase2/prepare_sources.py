#!/usr/bin/env python3
"""Rebuild the letter stream used by the Latin model from the pinned XML."""
from pathlib import Path
import hashlib, json
from lxml import etree
from search_keys import clean

ROOT = Path(__file__).resolve().parent

def main():
    info = json.loads((ROOT/'SOURCES_AND_LIMITS.json').read_text())
    for source in info['sources']:
        if 'sha256' in source:
            assert hashlib.sha256((ROOT/source['file']).read_bytes()).hexdigest() == source['sha256']
    tree = etree.parse(str(ROOT/'data/caesar.xml'))
    body = tree.xpath('//*[local-name()="body"]')[0]
    for element in body.xpath('.//*[local-name()="note" or local-name()="head"]'):
        element.getparent().remove(element)
    letters = clean(''.join(body.itertext()))
    target = ROOT/'data/latin_train.txt'
    if target.exists():
        assert clean(target.read_text()) == letters, 'Model input changed'
    target.write_text(letters)
    assert len(letters) == 317080
    print(json.dumps({'latin_model_letters': len(letters), 'raw_source_hashes': 'PASS'}))

if __name__ == '__main__':
    main()
