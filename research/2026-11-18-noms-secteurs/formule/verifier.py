"""Relit littéralement chaque table-exemple et contrôle le témoin de transfert."""
import csv
import itertools
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]


def read(codes, words):
    return [tuple(v for c in w for v in codes[c]) for w in words]


def variants(fragment, alphabet, deferred):
    if deferred == 'omit' and '[' in fragment:
        return []
    m = re.search(r'\[([^\[\]:]+):([^\[\]:]+)\]',fragment)
    if m:
        return [v for alternative in m.groups() for v in variants(
            fragment[:m.start()]+alternative+fragment[m.end():],alphabet,deferred)]
    assert re.fullmatch('[a-z]+',fragment)
    return [re.findall(r'c[kptf]h|[cs]h|.' if alphabet=='EVA' else '.',fragment)]


def main():
    result = json.loads((HERE/'manuscrit.json').read_text())
    with (R/'2026-11-18-secteurs-rouges/photos/secteurs.csv').open() as f:
        sectors = {int(row['secteur']):row for row in csv.DictReader(f)}
    verified = 0
    for variant, analyses in result['variants'].items():
        ed,alphabet,spaces,deferred = variant.split('/')
        file = {'H':'IT2a-n.txt','ZL':'ZL3b-n.txt'}[ed]
        rawrows = {}
        source = R.parent/'voynich_20261028/data'/file
        for ln in source.read_text().splitlines():
            m = re.match(r'^<f67r2\.(\d+),[^>]+>\s+(\S+)',ln)
            if m:
                rawrows[int(m[1])] = re.sub('<[^>]*>','',m[2])
        for a in analyses:
            assert sum(a['distribution_maximum_5040_permutations'].values()) == 5040
            for diagnostic in a['assignments']:
                for subset in diagnostic['maximal_subsets']:
                    assert len(subset['sectors']) == diagnostic['maximum']
                    model = a['model']
                    key = subset['example_key']
                    if model == 'bijection':
                        assert len(key) == len({v[0] for v in key.values()})
                    assert all(1 <= len(v) <= (1 if model=='bijection' else 3) for v in key.values())
                    for item in subset['example']:
                        sector = sectors[item['sector']]
                        start,end = map(int,sector['loci_paragraphe'].split('–'))
                        all_locs = []
                        all_words = {}
                        for n in range(start,end+1):
                            raw = rawrows[n].replace(',','.' if spaces=='split' else '')
                            for j,part in enumerate(raw.split('.'),start=1):
                                loc = f'.{n}/{j}'
                                all_locs.append(loc)
                                all_words[loc] = part
                        for locs, words in item['readable_at']:
                            if len(locs)==2:
                                assert all_locs.index(locs[1]) == all_locs.index(locs[0])+1
                            seq = [next(units for units in variants(all_words[loc],alphabet,deferred)
                                        if ''.join(units)==word) for loc,word in zip(locs,words)]
                            name = item['ablative_normalized']
                            plain = ['sub',name] if a['layout']=='separate' else ['sub'+name]
                            if model == 'letter_to_glyphs':
                                assert read(key,plain) == [tuple(w) for w in seq]
                            else:
                                assert read(key,seq) == [tuple(w) for w in plain]
                            verified += 1
    controls = json.loads((HERE/'etalonnage.json').read_text())
    key = controls['frozen_key']
    assert all(all(len(v)==1 for v in mapping) for mapping in key.values())
    for i,row in enumerate(controls['masked_16_word_passages'][4:]):
        prediction = controls['held_predictions_scored'][i]
        begin = prediction['first_word_position']-1
        assert read(key,[row[begin]]) == [tuple('sub')]
        decoded = ''.join(key.get(c,'?')[0] for c in row[begin+1])
        assert decoded == prediction['reading']
    assert controls['correct_letters'] == 17 and controls['total_letters'] == 18
    print(verified, 'occurrences de tables-exemples contrôlées dans les IVTFF ; trois réserves relues avec la table figée.')


if __name__ == '__main__':
    main()
