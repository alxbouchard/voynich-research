"""Compare les légendes aux paragraphes de leur propre page et énumère les permutations."""
from collections import Counter
import csv
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RESEARCH / '2026-11-18-formes-souterraines' / 'nom' / 'second'))
from transfert import corpus, tokens

SHA_PROTOCOL = 'd53defa792ba402ec82d73b5b015c95554e856f4a9a92eafdfc7ba728104346a'
SHA_GEOMETRY = '584a27515c49c4c2cb4a527c0c54c30c02f7a34893001cdeeb1e047514afc5a4'
TABLE = RESEARCH / '2026-11-18-paires-ingredients' / 'rangees' / 'rangees.tsv'


def geometry(editions):
    assert hashlib.sha256(TABLE.read_bytes()).hexdigest() == SHA_GEOMETRY
    pages = {}
    inventory = []
    seen_lines = set()
    with TABLE.open() as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    for row in rows:
        page = row['page']
        rank = int(row['rang'])
        lines = [f'{page}.{n}' for n in row['prose'].split(',') if n]
        fragments = [[f'{page}.{n}' for n in group.split('+')] for group in row['fragments'].split(',')]
        boundaries = {}
        for edition, entries in editions.items():
            assert all(entries[locus][1] == 'Lf' for item in fragments for locus in item)
            assert all(entries[locus][1] == 'P0' for locus in lines)
            starts = [n for n in lines if '<%>' in entries[n][3]]
            ends = [n for n in lines if '<$>' in entries[n][3]]
            boundaries[edition] = [starts, ends]
        admitted = bool(lines) and all(b == [lines[:1], lines[-1:]] for b in boundaries.values())
        inventory.append({'page': page, 'rang': rank, 'lignes': lines, 'limites': boundaries, 'admis': admitted})
        if admitted:
            assert seen_lines.isdisjoint(lines)
            seen_lines.update(lines)
            pages.setdefault(page, []).append((rank, fragments, lines))
    return pages, inventory


def words(entries, locus, spacing, minimum):
    # Les groupes modifiés par des signes entre accolades ne sont pas traités comme des mots EVA ordinaires.
    raw = re.sub(r'\{[^}]*\}', '?', entries[locus][3])
    return {w for w in tokens(raw, spacing) if re.fullmatch('[a-z]+', w)
            and len(re.findall(r'c[kptf]h|ch|sh|.', w)) >= minimum}


def independent_words(editions, locus, spacing, minimum):
    return set.intersection(*(words(e, locus, spacing, minimum) for e in editions.values()))


def locate(editions, pages, spacing, minimum):
    panels = {}
    for page, geometry_rows in pages.items():
        text = {}
        for locus, (p, kind, _, _) in editions['H'].items():
            if p == page and kind in ('P0', 'Pc') and locus in editions['ZL'] and editions['ZL'][locus][1] == kind:
                for word in independent_words(editions, locus, spacing, minimum):
                    text.setdefault(word, []).append(locus)
        labels = []
        bodies = []
        rows = []
        for rank, fragments, lines in geometry_rows:
            objects = []
            row_words = set()
            for item in fragments:
                variants = {name: set.union(*(words(e, locus, spacing, minimum) for locus in item))
                            for name, e in editions.items()}
                common = set.intersection(*variants.values())
                row_words.update(common)
                objects.append({'loci': item, 'mots_communs': sorted(common),
                                'lectures': {e: sorted(ws) for e, ws in variants.items()}})
            labels.append(row_words)
            bodies.append({w for w, positions in text.items() if not set(lines).isdisjoint(positions)})
            rows.append({'rang': rank, 'lignes': lines, 'fragments': objects})
        matrix = intersections(labels, bodies)
        localization = []
        for i, lexicon in enumerate(labels):
            for word in sorted(lexicon):
                targets = [r['rang'] for j, r in enumerate(rows) if word in matrix[i][j]]
                localization.append({'rang': rows[i]['rang'], 'mot': word, 'rangs_cibles': targets,
                                     'lignes_sur_page': text.get(word, [])})
        panels[page] = {'lignes_et_fragments': rows, 'localisation': localization,
                        'matrice_mots': [[sorted(cell) for cell in row] for row in matrix]}
    return panels


def intersections(labels, bodies):
    return [[set(lexicon) & set(paragraph) for paragraph in bodies] for lexicon in labels]


def rank_scores(matrix):
    n = len(matrix)
    counts = [[len(cell) for cell in row] for row in matrix]
    observed = sum(counts[i][i] for i in range(n))
    dist = Counter(sum(counts[i][j] for i, j in enumerate(p)) for p in itertools.permutations(range(n)))
    return observed, dist


def combine(matrices):
    overall = Counter({0: 1})
    observed = 0
    for matrix in matrices:
        score, dist = rank_scores(matrix)
        observed += score
        tmp = Counter()
        for i, a in overall.items():
            for j, b in dist.items():
                tmp[i + j] += a * b
        overall = tmp
    return {'score': observed, 'histogramme': dict(sorted(overall.items())),
            'au_moins_observe': sum(n for k, n in overall.items() if k >= observed),
            'permutations': sum(overall.values())}


def summarize(panels, include_discovery):
    subset = {p: data for p, data in panels.items() if len(data['lignes_et_fragments']) > 1
              and (include_discovery or p != 'f89r2')}
    result = combine([x['matrice_mots'] for x in subset.values()])
    census = Counter()
    for data in subset.values():
        for rec in data['localisation']:
            census['couples_rangee_mot'] += 1
            census['presents_sur_page'] += bool(rec['lignes_sur_page'])
            targets = rec['rangs_cibles']
            if not targets:
                census['aucun_paragraphe_admis'] += 1
            elif len(targets) > 1:
                census['plusieurs_paragraphes'] += 1
            elif targets == [rec['rang']]:
                census['seulement_le_bon'] += 1
            else:
                census['seulement_un_autre'] += 1
    return dict(result, panneaux=list(subset), localisation=dict(census))


def manuscript_frequencies(editions, words_of_interest):
    # Contexte descriptif pour les deux reprises découvertes sur f89r2.
    result = {}
    for edition, entries in editions.items():
        totals = {word: Counter() for word in words_of_interest}
        local = []
        for locus, (page, kind, _, raw) in entries.items():
            if kind not in ('P0', 'Lf'):
                continue
            sequence = tokens(re.sub(r'\{[^}]*\}', '?', raw), 'joints')
            for index, word in enumerate(sequence, 1):
                if word in totals:
                    totals[word][kind] += 1
                    if page == 'f89r2':
                        local.append({'mot': word, 'locus': locus, 'classe': kind, 'rang': index})
        result[edition] = {'manuscrit': totals, 'sur_f89r2': local}
    return result


def controls():
    pages = []
    for i in range(3):
        labels = [{'commun', f'a{i}'}, {'commun', f'b{i}'}]
        bodies = [['commun', f'a{i}', f'a{i}'], ['commun', f'b{i}', f'b{i}']]
        pages.append(intersections(labels, bodies))
    proper = combine(pages)
    assert proper['score'] == 12 and proper['au_moins_observe'] == 1 and proper['permutations'] == 8
    swapped = [[list(reversed(row)) for row in pages[0]], *pages[1:]]
    other = combine(swapped)
    assert other['score'] == 10 and other['au_moins_observe'] == 4
    null = combine([intersections([{'commun'}, {'commun'}], [['commun'], ['commun']])] * 3)
    assert null['score'] == 6 and null['au_moins_observe'] == null['permutations'] == 8
    return {'positif': proper, 'premiere_page_echangee': other, 'uniforme': null}


def main():
    assert hashlib.sha256((HERE / 'PROTOCOLE.md').read_bytes()).hexdigest() == SHA_PROTOCOL
    editions, _ = corpus()
    pages, inventory = geometry(editions)
    result = {'protocole_sha256': SHA_PROTOCOL, 'table_sha256': SHA_GEOMETRY, 'inventaire': inventory,
              'controles': controls(), 'variantes': {}}
    for spacing, minimum in itertools.product(('joints', 'separes'), (3, 1)):
        panels = locate(editions, pages, spacing, minimum)
        principal = summarize(panels, False)
        plus = summarize(panels, True)
        result['variantes'][f'{spacing}_{minimum}'] = {'hors_f89r2': principal, 'avec_f89r2': plus,
                                                       'detail_panneaux': panels}
        print(spacing, minimum, principal, plus)
    pairs = result['variantes']['joints_3']['detail_panneaux']['f89r2']['localisation']
    found = {rec['mot'] for rec in pairs if rec['lignes_sur_page']}
    result['contexte_des_reprises_de_f89r2'] = manuscript_frequencies(editions, sorted(found))
    (HERE / 'RESULTATS.json').write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
