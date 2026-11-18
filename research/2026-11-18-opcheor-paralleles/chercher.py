"""Recherche exhaustive d'un passage avec réserve du quatrième mot, sans franchir de notice."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '2026-11-18-legendes-et-paragraphes/lecture'))
from deux_mots import sources, tokenize, tables

SHAPES = {'principale': 'IT2a-n', 'ancienne-F': 'F'}


def corpus(name):
    return json.loads((HERE / name / 'corpus.json').read_text())


def triples(chapters, step):
    """La valeur à prédire reste hors de ce tableau, y compris pour le parcours inverse."""
    for chapter, words in chapters.items():
        starts = range(len(words) - 3) if step == 1 else range(3, len(words))
        for i in starts:
            yield chapter, i, tuple(words[i + j * step] for j in range(3))


def shared_length(a, b):
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))


def affixes(a, b):
    return shared_length(a, b), shared_length(a[::-1], b[::-1])


def cases(data):
    for step in (1, -1):
        records = []
        for chapter, pos, words in triples(data, step):
            records.append((chapter, pos, words, affixes(*words[:2]), tuple(map(len, words))))
        yield step, records


def analyze(cipher, records, width, allow_null):
    alphabet = sorted(set().union(*cipher[:3]))
    assert set(cipher[3]) <= set(alphabet)
    pair_sites, triple_sites = set(), set()
    predictions = defaultdict(dict)
    for null in (alphabet if allow_null else [None]):
        pronounced = [tuple(s for s in w if s != null) for w in cipher]
        prefix, suffix = affixes(*pronounced[:2])
        lengths = [len(w) for w in pronounced[:3]]
        @lru_cache(maxsize=8192)
        def first_pair(a, b):
            return [updated for key in tables(pronounced[0], a, width)
                    for updated in tables(pronounced[1], b, width, key)]
        for chapter, pos, words, common, sizes in records:
            if prefix > common[0] or suffix > common[1]:
                continue
            if sizes[0] < lengths[0] or sizes[1] < lengths[1]:
                continue
            if width and (sizes[0] > width * lengths[0] or sizes[1] > width * lengths[1]):
                continue
            pair = first_pair(*words[:2])
            if not pair:
                continue
            site = (chapter, pos)
            pair_sites.add(site)
            if sizes[2] < lengths[2] or (width and sizes[2] > width * lengths[2]):
                continue
            for key in pair:
                for full in tables(pronounced[2], words[2], width, key):
                    if null is not None:
                        full[null] = ''
                    assert [''.join(full[s] for s in w) for w in cipher[:3]] == list(words)
                    pred = ''.join(full[s] for s in cipher[3])
                    entry = predictions[site].setdefault(pred, {'tables': 0, 'exemple': full})
                    entry['tables'] += 1
                    triple_sites.add(site)
    return {
        'nombre_fenetres': len(records),
        'deux_mots': len(pair_sites),
        'deux_mots_par_segment': dict(sorted(Counter(k for k, _ in pair_sites).items())),
        'trois_mots': len(triple_sites),
        'reservations': [{'segment': k, 'rang_physique_historique_depart': i + 1, 'sorties': preds}
                         for (k,i), preds in sorted(predictions.items())],
    }


def save_gz(p, value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    p.write_bytes(gzip.compress(raw, mtime=0))


def learn(lang):
    data = corpus(lang)
    editions = sources()
    out = {}
    for step, records in cases(data):
        for (name, ed), compounds, reverse in product(SHAPES.items(), (True, False), (False, True)):
            cipher = [tokenize(w, compounds, reverse) for w in editions[ed][4:8]]
            for width, mute in product((1, 2, None), (False, True)):
                model = '/'.join([name,'bancs' if compounds else 'separes',
                                  'inverse' if reverse else 'direct',str(step),
                                  str(width or 'libre'),str(int(mute))])
                out[model] = analyze(cipher, records, width, mute)
    save_gz(HERE / lang / 'PREDICTIONS.json.gz', out)
    print(lang, len(out), 'règles, fenêtres-règles produisant une prédiction',
          sum(s['trois_mots'] for s in out.values()))


def judge(lang):
    data = corpus(lang)
    path = HERE / lang / 'PREDICTIONS.json.gz'
    out = {}
    for name, branch in json.loads(gzip.decompress(path.read_bytes())).items():
        shape, mode, direction, step, width, mute = name.split('/')
        step = int(step)
        hits, misses, expected = [], [], 0.0
        n_compared = 0
        # Réaffecter uniformément les quatrièmes mots de toutes les fenêtres de
        # la même notice dans le même sens ; tous les départs restent possibles.
        target_counts = {chapter: Counter(words[3:] if step == 1 else words[:-3])
                         for chapter, words in data.items()}
        for trial in branch['reservations']:
            chapter, i = trial['segment'], trial['rang_physique_historique_depart'] - 1
            words = data[chapter]
            expected_word = words[i + 3*step]
            options = trial['sorties']
            counts = target_counts[chapter]
            expected += sum(counts.get(w, 0) for w in options) / sum(counts.values())
            n_compared += len(options)
            basic = {'segment':chapter,'rang_depart':i+1,'trois_mots':[words[i+j*step] for j in range(3)],
                     'mot_reserve':expected_word}
            if expected_word in options:
                hits.append(basic | {'sortie':options[expected_word]})
            elif len(misses) < 3:
                misses.append(basic | {'nombre_sorties':len(options),'exemples':sorted(options)[:12]})
        out[name] = {k:v for k,v in branch.items() if k!='reservations'}
        out[name].update({'predictions_position_graphie':n_compared,'sites_corrects':hits,
                          'exemples_manques':misses,'esperance_reaffectation_dans_la_notice':round(expected,6)})
    (HERE / lang / 'VERIFICATION.json').write_text(json.dumps(
        {'sha256_predictions':hashlib.sha256(path.read_bytes()).hexdigest(),'branches':out},
        ensure_ascii=False, indent=1, sort_keys=True)+'\n')


if __name__ == '__main__':
    {'apprendre':learn, 'verifier':judge}[sys.argv[1]](sys.argv[2])
