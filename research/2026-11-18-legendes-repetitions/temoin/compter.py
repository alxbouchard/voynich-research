"""Compter trois noms d'organes dans l'édition latine du Macer."""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / '2026-11-18-opcheor-paralleles/latin'
FORMS = {
    'radix': 'radix radicis radici radicem radice radices radicum radicibus',
    'folium': 'folium folii foli folio folia foliorum foliis',
    'flos': 'flos floris flori florem flore flores florum floribus',
}
MATCH = {form + suffix: lemma for lemma, forms in FORMS.items()
         for form in forms.split() for suffix in ('', 'que', 've', 'ne')}


def write_table(name, header, records):
    with (HERE / name).open('w') as out:
        tsv = csv.writer(out, delimiter='\t', lineterminator='\n')
        tsv.writerow(header)
        tsv.writerows(records)


def main():
    chapters = json.loads((SOURCE / 'corpus.json').read_bytes())
    hits = []
    chapter_hits = defaultdict(Counter)
    with (SOURCE / 'vers.tsv').open() as src:
        for row in csv.DictReader(src, delimiter='\t'):
            start = int(row['premier_mot_notice'])
            end = int(row['dernier_mot_notice'])
            words = chapters[row['titre']][start - 1:end]
            for rank, word in enumerate(words, start):
                if word in MATCH:
                    lemma = MATCH[word]
                    chapter_hits[row['titre']][lemma] += 1
                    hits.append([row['notice'], row['titre'], row['rang_du_vers'], rank,
                                 word, lemma, row['texte_edite']])
    write_table('occurrences.tsv', ['notice', 'titre', 'vers', 'mot_notice', 'forme', 'lemme', 'texte_edite'], hits)
    overview = []
    for rank, (title, words) in enumerate(chapters.items(), 1):
        heading = [word for word in re.findall(r'[^\W\d_]+', title.lower()) if word in MATCH]
        overview.append([rank, title, len(words), ','.join(heading),
                         *[chapter_hits[title][lemma] for lemma in FORMS]])
    write_table('notices.tsv', ['notice', 'titre', 'mots', 'titre_organes', *FORMS], overview)
    print('titres', len(overview), 'dont avec organe', sum(bool(r[3]) for r in overview))
    for i, lemma in enumerate(FORMS, 4):
        print(lemma, 'occurrences', sum(r[i] for r in overview), 'notices', sum(r[i] > 0 for r in overview))
    print('au moins un', sum(any(r[4:]) for r in overview), 'sur', len(overview))


if __name__ == '__main__':
    main()
