"""Audit the frozen input, manually annotated plant-name forms and corpus readback."""

import gzip
import csv
import hashlib
import json
from pathlib import Path

from extract import extract


ROOT = Path(__file__).resolve().parent
EXPECTED = 'ab401a75ae802158f96fa5d9daa4b2ff09958f1dc9e6a1ad79bccef82fdf5e43'
EXPECTED_PREDICTION = 'b77ee3c01939586e79d18262e167551af6a9dfc24bc904e5655a49803de12a0f'


def main():
    data = (ROOT / 'corpus.jsonl').read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED
    assert hashlib.sha256((ROOT / 'PREDICTION_MS458.md').read_bytes()).hexdigest() == EXPECTED_PREDICTION
    stored = [json.loads(line) for line in data.decode().splitlines()]
    assert list(extract(gzip.decompress((ROOT / 'source.wiki.gz').read_bytes()))) == stored
    assert len({row['label'] for row in stored}) == 40
    with (ROOT / 'premieres_formes.tsv').open(encoding='utf-8') as file:
        annotated = list(csv.DictReader(file, delimiter='\t'))
    assert len(annotated) == len(stored) == 40
    for row, note in zip(stored, annotated):
        assert row['position'] == int(note['position'])
        row['premiere_reprise'] = 1 + row['tokens'].index(note['forme_relevee'])
        row['identique_en_premiere_reprise'] = row['label'] == note['forme_relevee']
    report = {}
    for group in ['train', 'validation']:
        rows = [r for r in stored if r['split'] == group]
        report[group] = {
            'notices': len(rows), 'mots': sum(len(r['tokens']) for r in rows),
            'notices_courtes': sum(len(r['tokens']) < 100 for r in rows),
            'rubrique_exacte_presente': sum(r['label'] in r['tokens'] for r in rows),
            'premiere_reprise_identique': sum(r['identique_en_premiere_reprise'] for r in rows),
            'rang_maximal_premiere_reprise': max(r['premiere_reprise'] for r in rows)
        }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
