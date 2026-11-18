"""Préparer les lectures fixées puis les comparer aux réponses archivées des lexiques."""
from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
PREV = RESEARCH / '2026-11-18-deux-legendes-botaniques'
INVENTORY = PREV / 'lecture/tucker/prefixe/resultats.json'
DICTIONARY = PREV / 'histoire/table.json'
LATIN = RESEARCH / '2026-11-18-opcheor-paralleles/latin/corpus.json'
KEYS = RESEARCH / '2026-11-18-racine-et-possessif/cle/suite.json'
LATIN_SEG = re.compile(r'c[ptfk]h|ch|sh|.')
TJ_SEG = re.compile(r'c[ptfk]h|ch|sh|iin|in|.')


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n')


def plain(word):
    return ''.join(c for c in unicodedata.normalize('NFD', word) if not unicodedata.combining(c))


def by_code():
    labels = {}
    for kind, record in load(INVENTORY)['par_code'].items():
        words = defaultdict(list)
        for locus, word in sorted(record['mots_par_locus'].items()):
            words[word].append(locus)
        labels[kind] = words
    return labels


def pairs(labels, exclude):
    return {
        w: {'court': list(loci), 'long': list(labels[w + 'y'])}
        for w, loci in labels.items()
        if w + 'y' in labels and w not in exclude and w + 'y' not in exclude
    }


def tucker_tables():
    rows = load(DICTIONARY)['lignes_table_p141']
    return [
        {sign: value for row, value in zip(rows, values) for sign in row['eva']}
        for values in product(*(row['valeurs'] for row in rows))
    ]


def latin_tables():
    return [row['cle'] for row in load(KEYS)['tables']]


def decode(sequence, table):
    if not all(sign in table for sign in sequence):
        return None
    return ''.join(table[sign] for sign in sequence)


def lists():
    labels = by_code()
    seed = pairs(labels['Lf'], set())
    reserved = next(k for k in ('Ls', 'Lz', 'Ln', 'Lc', 'Lt') if pairs(labels[k], labels['Lf']))
    sets = {'plantes': seed, 'reserve': pairs(labels[reserved], labels['Lf'])}
    data = {
        'lieux': sets, 'classe_reserve': reserved,
        'n_retenus': {k: sum(map(len, words.values())) for k, words in labels.items()},
        'lectures': {},
    }
    models = [('Tucker-Janick', tucker_tables(), TJ_SEG), ('latin', latin_tables(), LATIN_SEG)]
    for name, tables, parser in models:
        rows = []
        for index, key in enumerate(tables, start=1):
            records = []
            for group, forms in sets.items():
                for word in forms:
                    words = [parser.findall(form) for form in (word, word + 'y')]
                    for order in ('direct', 'inverse'):
                        sequences = words if order == 'direct' else [signs[::-1] for signs in words]
                        records.append({
                            'série': group, 'X': word, 'ordre': order,
                            'lues': [decode(seq, key) for seq in sequences],
                            'absents': sorted({sign for seq in sequences for sign in seq if sign not in key}),
                        })
            rows.append({'cle': key, 'num': index, 'paires': records})
        data['lectures'][name] = rows
    return data


def latin_extension(lex):
    candidates = [(w, w + 'us') for w in sorted(lex) if w + 'us' in lex]
    assert list(pairs(by_code()['Lf'], set())) == ['otal']
    attempts = []
    for key in latin_tables():
        left, right = key['o'], key['a'] + key['l']
        # Extraire la valeur manquante uniquement si le reste du mot coïncide.
        possible = set()
        for word in lex:
            if word.startswith(left) and word.endswith(right):
                value = word[len(left): len(word) - len(right)]
                if len(value) in (1, 2):
                    possible.add(value)
        solo = sorted((t, decode('otal', key | {'t': t})) for t in possible)
        assert all(w in lex for t, w in solo)
        both = [{'t': t, 'forme': w, 'longue': w + 'us'} for t, w in solo if w + 'us' in lex]
        reference = [(short, long) for short, long in candidates
                     if short.startswith(left) and short.endswith(right)
                     and 1 <= len(short) - len(left) - len(right) <= 2]
        assert sorted((r['forme'], r['longue']) for r in both) == sorted(reference)
        attempts.append({'cle': key, 'court_atteste': solo, 'deux_attestes': both})
    return {'paires_dans_le_macer': candidates, 'essais': attempts}


def evaluate(data, responses):
    lex = Counter(w.replace('j', 'i') for words in load(LATIN).values() for w in words)
    assert lex['radix'] and lex['foliis'] and not lex['zzzxqvzzzz']
    assert all(responses[w].get('entrees', {}).get('xvie') for w in ('atl', 'xochitl'))
    assert responses['zzzxqvzzzz']['etat'] == 'aucune_fiche'
    report = {
        'latin_extension': latin_extension(lex),
        'temoins_latins': {w: lex[w] for w in ('radix', 'foliis', 'zzzxqvzzzz')},
    }
    for model, rows in data['lectures'].items():
        by_pair = defaultdict(set)
        winners = []
        for record in rows:
            successful = {}
            for row in record['paires']:
                pair = row['lues']
                found = []
                for output in pair:
                    if output is None:
                        found.append(None)
                    elif model == 'latin':
                        found.append(bool(lex[plain(output)]))
                    else:
                        response = responses[plain(output)]
                        assert response['etat'] in ('fiches', 'aucune_fiche')
                        found.append(bool(response.get('entrees', {}).get('xvie')))
                label = (row['série'], row['X'], row['ordre'])
                by_pair[label].add(tuple(pair + found))
                if row['ordre'] == 'direct' and all(found):
                    successful.setdefault(row['série'], []).append(row['X'])
            winners.append({'cle': record['num'], 'paires_attestees': successful})
        report[model] = {
            'table_par_table': winners,
            'par_paire': [
                {'série': label[0], 'X': label[1], 'ordre': label[2],
                 'options': [list(option) for option in sorted(options, key=str)]}
                for label, options in sorted(by_pair.items())
            ],
        }
    return report


if __name__ == '__main__':
    data = lists()
    save(HERE / 'PREDICTIONS.json', data)
    print('Catégorie réservée', data['classe_reserve'])
    if (HERE / 'gdn.json').is_file():
        save(HERE / 'resultats.json', evaluate(data, load(HERE / 'gdn.json')))
