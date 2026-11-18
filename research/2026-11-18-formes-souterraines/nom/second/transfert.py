"""Transférer toutes les subdivisions exactes de opcheor, puis chercher ses répétitions."""
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent))
from abreger import consistent, macer_source, units, words
import langage

SOURCE = 'f89r2.5'
WORD = 'opcheor'
SIGNS = units(WORD, 'unites')
TARGETS = ['f6r', 'f52r', 'f56v', 'f66v', 'f96r', 'f38r']
ROW = re.compile(r'^<([^,>]+)\.([0-9]+),(.)([^>]+)>\s*(.*)$')


def all_tables(name):
    for cuts in combinations(range(1, len(name)), len(SIGNS) - 1):
        bounds = (0, *cuts, len(name))
        parts = [name[a:b] for a, b in zip(bounds, bounds[1:])]
        table = consistent(SIGNS, parts)
        if table:
            yield cuts, table


def spellings(name, table):
    """Toutes les séquences d'unités, bornées car les sorties sont non vides."""
    @lru_cache(maxsize=None)
    def visit(start):
        if start == len(name):
            return [()]
        return [(sign, *suffix) for sign, output in table.items()
                if name.startswith(output, start)
                for suffix in visit(start + len(output))]
    return visit(0)


def corpus():
    editions = {}
    sections = {}
    for edition, stem in langage.EDITIONS.items():
        data = (langage.DATA / (stem + '-n.txt')).read_bytes()
        assert hashlib.sha256(data).hexdigest() == langage.HASH[edition]
        rows = {}
        for line in data.decode().splitlines():
            head = re.match(r'^<([^.,>]+)>', line)
            if head and edition == 'ZL':
                meta = dict(re.findall(r'\$(\w)=(\w+)', line))
                sections[head[1]] = meta.get('I', '')
            row = ROW.match(line)
            if row and row[3] != '!':
                page, number, position, kind, raw = row.groups()
                locus = f'{page}.{number}'
                assert locus not in rows
                rows[locus] = (page, kind, position, raw.strip())
            elif line.startswith('<') and ',' in line.partition('>')[0]:
                assert row and row[3] == '!', line
        editions[edition] = rows
    return editions, sections


def tokens(raw, split):
    # Une lecture alternative, un signe spécial ou douteux reste illisible.
    raw = re.sub(r'<![^>]*>|<[%$]>|!', '', raw)
    raw = re.sub(r'\[[^\]]*\]', '?', raw)
    raw = raw.replace('{', '').replace('}', '')
    raw = re.sub(r'<[-~]>', '.', raw)
    return tuple(filter(None, raw.replace(',', '.' if split == 'separes' else '').split('.')))


def labels(rows, split):
    objects = {}
    last = None
    for loc, (page, kind, pos, raw) in rows.items():
        if kind != 'Lf':
            last = None
            continue
        if pos == '+':
            assert last == 'f99r.6' and loc == 'f99r.7'
            objects[last + '+' + loc] = objects.pop(last) + tokens(raw, split)
        else:
            assert pos == '@'
            objects[loc] = tokens(raw, split)
        last = loc
    return objects


def decode(seq, table):
    signs = [s for word in seq for s in units(word, 'unites')]
    if any(not re.fullmatch('[a-z]+', w) for w in seq) or any(s not in table for s in signs):
        return None
    return ''.join(table[s] for s in signs)


def audit_labels(by_edition, split, tables, titles):
    lh, lz = (labels(rows, split) for rows in by_edition.values())
    assert lh.keys() == lz.keys() and lh[SOURCE] == lz[SOURCE] == (WORD,)
    totals = Counter()
    covered = []
    forms = {}
    for loc in sorted(lh.keys() - {SOURCE}):
        h, z = lh[loc], lz[loc]
        totals['etiquettes_hors_apprentissage'] += 1
        certain = all(re.fullmatch('[a-z]+', w) for w in h + z)
        if certain:
            totals['deux_editions_sans_ambiguite_de_signe'] += 1
            totals['eva_et_blancs_identiques_sans_ambiguite'] += int(h == z)
        else:
            totals['lecture_IVTFF_incertaine'] += 1
        if not certain:
            category = 'lecture_IVTFF_incertaine'
        elif all(decode(s, tables[0]['table']) is not None for s in (h, z)):
            category = 'deux_lectures_couvertes'
            totals[category] += 1
            covered.append((loc, h, z))
        else:
            category = 'signe_sans_correspondance_dans_au_moins_une_edition'
            totals[category] += 1
        forms[loc] = {'H': h, 'ZL': z, 'categorie': category}
    for t in tables:
        readings = []
        counts = Counter()
        for loc, h, z in covered:
            a, b = (decode(seq, t['table']) for seq in (h, z))
            if a != b:
                status = 'lectures_divergentes'
            elif a == ''.join(t['rubrique'].split()):
                status = 'nom_apprentissage'
            elif a in titles:
                status = 'autre_rubrique'
            else:
                status = 'hors_repertoire'
            counts[status] += 1
            readings.append([loc, a, b, status])
        t.setdefault('transfert', {})[split] = {'comptes': dict(counts), 'lectures': readings}
    return {'loci_Lf': len(lh) + 1, 'etiquettes_Lf': len(lh), 'effectifs': totals,
            'etiquettes': forms}


def occurrence_counts(editions, sections, split):
    scopes = {p: {p} for p in TARGETS}
    scopes['herbier_H_IVTFF'] = {p for p, category in sections.items() if category == 'H'}
    scopes['herbier_H_hors_six_cibles'] = scopes['herbier_H_IVTFF'] - set(TARGETS)
    scopes['corpus_controle_85'] = set(langage.eligible())
    scopes['manuscrit'] = None
    result = {}
    all_hits = {}
    for ed, rows in editions.items():
        counts = {group: {} for group in scopes}
        hits = []
        for locus, (page, kind, _, raw) in rows.items():
            seq = tokens(raw, split)
            positions = [i for i, w in enumerate(seq, 1) if w == WORD]
            if positions:
                hits.append({'locus': locus, 'classe': kind, 'positions': positions, 'ligne': raw})
            for group, pages in scopes.items():
                if pages is not None and page not in pages:
                    continue
                part = counts[group].setdefault('P0' if kind == 'P0' else 'autres', Counter())
                part['loci'] += 1
                part['positions'] += len(seq)
                part['positions_lisibles'] += sum(re.fullmatch('[a-z]+', w) is not None for w in seq)
                part['occurrences'] += len(positions)
        result[ed] = counts
        all_hits[ed] = hits
    result['occurrences'] = all_hits
    result['communes_meme_locus_et_meme_position'] = sorted(set.intersection(*(
        {(r['locus'], r['classe'], i) for r in rows for i in r['positions']}
        for rows in all_hits.values())))
    result['faces_herbier_H'] = sorted(scopes['herbier_H_IVTFF'])
    return result


def main():
    titles = {' '.join(words(title)): ''.join(words(title)) for title, _ in macer_source()}
    assert len(titles) == len(set(titles.values())) == 77
    tables = []
    by_name = {}
    for label, name in titles.items():
        all_source_spellings = set()
        for cuts, table in all_tables(name):
            writable = {title: spellings(text, table) for title, text in titles.items()}
            assert SIGNS in writable[label]
            all_source_spellings.update(writable[label])
            tables.append({'id': len(tables) + 1, 'rubrique': label, 'coupes': cuts, 'table': table,
                           'graphies_du_nom': writable[label],
                           'nombre_autres_rubriques_ecrivables': sum(bool(v) for k, v in writable.items() if k != label),
                           'autres_rubriques_ecrivables': {k: v for k, v in writable.items() if k != label and v}})
        if all_source_spellings:
            by_name[label] = {'tables': sum(t['rubrique'] == label for t in tables),
                              'toutes_les_graphies_du_nom': sorted(all_source_spellings)}
    assert len({tuple(t['table'].items()) for t in tables}) == len(tables)
    eds, sections = corpus()
    out = {'protocole_commit': '33464a2', 'unites': SIGNS, 'empreintes_IVTFF': langage.HASH,
           'rubriques': titles, 'par_nom': by_name, 'tables': tables,
           'legendes': {split: audit_labels(eds, split, tables, set(titles.values())) for split in langage.SPLITS},
           'occurrences': {split: occurrence_counts(eds, sections, split) for split in langage.SPLITS}}
    (HERE / 'resultats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
