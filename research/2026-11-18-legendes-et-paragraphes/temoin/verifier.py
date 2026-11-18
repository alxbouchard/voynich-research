"""Classe des faces à partir des intitulés du Liber de coquina et permute leurs destinations."""
import argparse
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
INPUT_SHA = 'c737510eaabc4d0979fa9ae648c4f698d296e1bed1c70ceea8f213a97100eb8a'
FACES = [f"{n}{side}" for n in range(160, 190) for side in 'rv']
BLOCKS = [FACES[i:i + 10] for i in range(0, len(FACES), 10)]


class Edition(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.face = None
        self.markers = []
        self.paragraphs = {}
        self.titles = {}
        self.number = None
        self.record = None
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        if tag in {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}:
            return
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        role = ''
        if attrs.get('id') == 'testo':
            role = 'text'
        if self.inside('text'):
            if 'pagina' in classes:
                role = 'page'
            elif 'ricetta' in classes:
                role = 'recipe'
            elif self.inside('recipe') and (tag == 'p' or 'head' in classes):
                role = 'title' if 'head' in classes else 'paragraph'
                assert self.record is None
                self.record = role
                self.fragments = []
        self.stack.append((tag, role))

    def inside(self, role):
        return any(r == role for _, r in self.stack)

    def handle_startendtag(self, tag, attrs):
        if tag not in {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}:
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not any(t == tag for t, _ in self.stack):
            return
        while self.stack:
            ended, role = self.stack.pop()
            if role and role == self.record:
                self.finish_record()
            if ended == tag:
                break

    def handle_data(self, data):
        if self.inside('page'):
            value = data.strip()
            if value:
                assert value in FACES
                self.face = value
                self.markers.append(value)
        elif self.record:
            if self.fragments and self.fragments[-1][0] == self.face:
                self.fragments[-1][1] += data
            else:
                self.fragments.append([self.face, data])

    def finish_record(self):
        pieces = [(face, text) for face, text in self.fragments if text.strip()]
        if self.record == 'title':
            full = ' '.join(t for _, t in pieces)
            number = re.search(r'\b(\d+)\.?\s*$', full)
            self.number = int(number[1]) if number else None
            if self.number is not None:
                assert self.number not in self.titles
                self.titles[self.number] = (pieces[0][0], TOKEN.findall(full.casefold()))
        else:
            assert self.number is not None and self.number not in self.paragraphs
            self.paragraphs[self.number] = [(face, w) for face, t in pieces for w in TOKEN.findall(t.casefold())]
        self.record = None


def build_index(html):
    assert hashlib.sha256(html).hexdigest() == INPUT_SHA
    parser = Edition()
    parser.feed(html.decode('utf-8'))
    parser.close()
    assert set(parser.markers) == set(FACES) and len(parser.markers) == 60
    assert set(parser.titles) == set(parser.paragraphs) == set(range(1, 169))
    vocabulary = {w for _, words in parser.titles.values() for w in words if len(w) >= 3}
    data = {f: {'titres': [], 'mots_titres': set(), 'nombre_mots': 0, 'occurrences': []} for f in FACES}
    for number, (face, words) in parser.titles.items():
        data[face]['titres'].append(number)
        data[face]['mots_titres'].update(w for w in words if w in vocabulary)
        for pos, (dest, word) in enumerate(parser.paragraphs[number], 1):
            row = data[dest]
            row['nombre_mots'] += 1
            if word in vocabulary:
                row['occurrences'].append([row['nombre_mots'], pos, word])
    for row in data.values():
        row['mots_titres'] = sorted(row['mots_titres'])
    return {'html_sha256': INPUT_SHA, 'faces': data}


@lru_cache(maxsize=None)
def totals(matrix):
    """Distribution exacte des sommes sur toutes les affectations bijectives."""
    states = {0: Counter({0: 1})}
    for row in matrix:
        next_states = {}
        for mask, counts in states.items():
            for j, points in enumerate(row):
                bit = 1 << j
                if not mask & bit:
                    acc = next_states.setdefault(mask | bit, Counter())
                    for level, freq in counts.items():
                        acc[level + points] += freq
        states = next_states
    return next(iter(states.values()))


def combine(dist1, dist2):
    result = Counter()
    for s1, n1 in dist1.items():
        for s2, n2 in dist2.items():
            result[s1 + s2] += n1 * n2
    return result


def null_stats(d, observed):
    total = sum(d.values())
    above = sum(n for score, n in d.items() if score >= observed)
    return {'observé': observed, 'attributions': total, 'au_moins_observe': above,
            'fraction_au_moins_observe': str(Fraction(above, total)),
            'proportion_au_moins_observe': above / total,
            'score_moyen': float(Fraction(sum(s * n for s, n in d.items()), total))}


def evaluate(pages, mode, allowed):
    rows = {}
    null = Counter({0: 1})
    local = Counter({0: 1})
    for block in BLOCKS:
        cap = min(pages[f]['nombre_mots'] for f in block)
        texts = {}
        for f in block:
            texts[f] = {w for facepos, recipepos, w in pages[f]['occurrences']
                        if (mode != 'longueurs_egales' or facepos <= cap)
                        and (mode != 'apres_huit_mots' or recipepos > 8)}
        matrix = []
        for f in block:
            terms = set(pages[f]['mots_titres'])
            if mode == 'ingredients':
                terms &= allowed
            hits = {g: sorted(terms & texts[g]) for g in block}
            scores = [len(hits[g]) for g in block]
            ranks = tuple(2 * sum(other < score for other in scores) + scores.count(score) - 1
                          for score in scores)
            matrix.append(ranks)
            i = block.index(f)
            rows[f] = {'requete': sorted(terms), 'titres': pages[f]['titres'], 'longueur': pages[f]['nombre_mots'],
                       'plafond': cap if mode == 'longueurs_egales' else None,
                       'intersections': hits, 'points_doubles': ranks[i],
                       'seule': ranks[i] == 18 and scores[i] > 0,
                       'premiere_ex_aequo': scores[i] == max(scores) and scores[i] > 0 and scores.count(scores[i]) > 1,
                       'partages_sur_place': hits[f]}
        null = combine(null, totals(tuple(matrix)))
        for j in range(0, 10, 2):
            pair = tuple(tuple(row[j:j+2]) for row in matrix[j:j+2])
            local = combine(local, totals(pair))
    observed = sum(r['points_doubles'] for r in rows.values())
    two = [r for r in rows.values() if len(r['requete']) >= 2]
    stats = {'faces': len(rows), 'seules': sum(r['seule'] for r in rows.values()),
             'premieres_ex_aequo_positives': sum(r['premiere_ex_aequo'] for r in rows.values()),
             'requete_vide': sum(not r['requete'] for r in rows.values()),
             'aucun_mot_commun_sur_place': sum(not r['partages_sur_place'] for r in rows.values()),
             'proportion_moyenne_battue': observed / (18 * len(rows)),
             'deux_termes_ou_plus': len(two), 'seules_parmi_deux_termes_ou_plus': sum(r['seule'] for r in two),
             'blocs': null_stats(null, observed), 'recto_verso': null_stats(local, observed)}
    return {'resume': stats, 'faces': rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--html', type=Path, help='Rebâtir l’index à partir du fichier HTML intégral de O.')
    args = ap.parse_args()
    idx = HERE / 'index.json'
    if args.html:
        index = build_index(args.html.read_bytes())
        idx.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')) + '\n')
    else:
        index = json.loads(idx.read_text())
    assert index['html_sha256'] == INPUT_SHA
    items = (HERE / 'ingredients.txt').read_text().split()
    allowed = set(items)
    pages = index['faces']
    assert allowed <= set.union(*(set(p['mots_titres']) for p in pages.values()))
    out = {mode: evaluate(pages, mode, allowed) for mode in ('tous', 'ingredients', 'apres_huit_mots', 'longueurs_egales')}
    (HERE / 'resultats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for mode, data in out.items():
        print(mode, json.dumps(data['resume'], ensure_ascii=False))


if __name__ == '__main__':
    main()
