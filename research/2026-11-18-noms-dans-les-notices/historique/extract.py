"""Extract the prespecified excerpts in source order, using only Python's standard library."""

import argparse
import gzip
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_SHA256 = '41ca63622e4fbcc4f52c40d7c9261541c5b6d24ee59ebb2964ece69cee480e26'
HEADING = re.compile(r'^==\s*([IVXLCDM]+)\.\s*(.*?)\.\s*==\s*$', re.MULTILINE | re.IGNORECASE)
WORDS = re.compile(r'[^\W\d_]+', re.UNICODE)


def tokens(text):
    normalized = unicodedata.normalize('NFD', text.lower())
    plain = ''.join(char for char in normalized if not unicodedata.combining(char))
    return WORDS.findall(plain)


def extract(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Unexpected source bytes. Retrieve the pinned action=raw revision.')
    source = raw.decode('utf-8')
    headings = list(HEADING.finditer(source))
    if len(headings) != 77:
        raise ValueError('Expected 77 headings')
    for position, (current, following) in enumerate(zip(headings[:40], headings[1:41]), start=1):
        block = source[current.end():following.start()].strip()
        body = re.fullmatch(r'<poem>\s*(.*?)\s*</poem>', block, re.DOTALL)
        if not body:
            raise ValueError(f'Unrecognized chapter format at position {position}')
        clean = re.sub(r'\{\{Versus\|\d+\}\}', ' ', body.group(1))
        if any(char in clean for char in '<>{}[]'):
            raise ValueError(f'Unrecognized markup in chapter {position}')
        all_tokens = tokens(clean)
        heading_tokens = tokens(current.group(2))
        yield {'id':f'macer-{position:02d}', 'position':position,
               'source_numeral':current.group(1), 'source_title':current.group(2),
               'split':'train' if position <= 20 else 'validation', 'label':heading_tokens[0],
               'full_body_token_count':len(all_tokens), 'tokens':all_tokens[:100]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'source.wiki.gz')
    parser.add_argument('--output', type=Path, default=ROOT/'corpus.jsonl')
    args = parser.parse_args()
    raw = args.source.read_bytes()
    if args.source.suffix == '.gz':
        raw = gzip.decompress(raw)
    rows = list(extract(raw))
    args.output.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
