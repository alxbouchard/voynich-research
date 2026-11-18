"""Compare des paquets d’inscriptions végétales à la prose de leur cahier."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
import json
from math import factorial, lcm
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, labels, tokens

SEED = 'f89r2'
NO_LABEL = 'f101r'
MODES = [(ed, cut) for ed in ('H', 'ZL') for cut in ('joints', 'separes')]
DATA = HERE.parents[1] / 'voynich_20261028/data'


def eligible(word):
    return re.fullmatch('[a-z]+', word) and len(re.findall(r'c[kptf]h|ch|sh|.', word)) >= 3


def inventory(prose_kinds=('P0',)):
    editions, sections = corpus()
    meta = {}
    for line in (DATA / 'ZL3b-n.txt').read_text().splitlines():
        match = re.match(r'^<(f\w+)>', line)
        if match:
            meta[match[1]] = dict(re.findall(r'\$(\w)=(\w+)', line))

    pages = [p for p, section in sections.items() if section == 'P']
    collections = {}
    for ed, cut in MODES:
        rows = editions[ed]
        table = labels(rows, cut)
        captions, prose = {}, {}
        for page in pages:
            captions[page] = {loc: ws for loc, ws in table.items() if loc.partition('.')[0] == page}
            prose[page] = {loc: tokens(raw, cut) for loc, (p, kind, _, raw) in rows.items()
                           if p == page and kind in prose_kinds}
            assert prose[page]
        assert [p for p in pages if not captions[p]] == [NO_LABEL]
        assert {key.split('.')[0] for key in table} == set(pages) - {NO_LABEL}
        collections[ed, cut] = (captions, prose)

    assert len(pages) == 16
    assert all(meta[p]['H'] == '1' and meta[p]['L'] == 'A' for p in pages)
    return pages, {p: meta[p]['Q'] for p in pages}, collections


def common_words(sources):
    """Une forme doit être présente au même locus dans chaque lecture retenue."""
    per_word = defaultdict(list)
    for loc in set.intersection(*(set(source) for source in sources)):
        shared = set.intersection(*(set(source[loc]) for source in sources))
        for word in shared:
            if eligible(word):
                per_word[word].append(loc)
    return {w: sorted(locs) for w, locs in sorted(per_word.items())}


def cut_prose(table, limit):
    kept = {}
    for loc, words in table.items():
        if limit is None:
            kept[loc] = words
        elif limit:
            kept[loc] = words[:limit]
            limit -= len(kept[loc])
    return kept


def vocabularies(pages, groups, data, modes, equal):
    captions, texts, lengths, limits = {}, {}, {}, {}
    for mode in modes:
        prose = data[mode][1]
        lengths[mode] = {p: sum(map(len, prose[p].values())) for p in pages}
    for group in set(groups.values()):
        limits[group] = (min(lengths[m][p] for m in modes for p in pages if groups[p] == group)
                         if equal else None)
    for p in pages:
        captions[p] = common_words([data[m][0][p] for m in modes])
        texts[p] = common_words([cut_prose(data[m][1][p], limits[groups[p]]) for m in modes])
    return captions, texts, {'longueurs': {'/'.join(m): lengths[m] for m in modes}, 'plafonds': limits}


def permutation_distribution(block, points):
    """Histogramme exact des totaux pour les bijections à l’intérieur du bloc."""
    @cache
    def fill(mask):
        index = mask.bit_count()
        if index == len(block):
            return Counter({0: 1})
        row = block[index]
        dist = Counter()
        for j, col in enumerate(block):
            if not mask & (1 << j):
                for rest, n in fill(mask | (1 << j)).items():
                    dist[rest + points[row][col]] += n
        return dist
    dist = fill(0)
    assert sum(dist.values()) == factorial(len(block))
    return dist


def combine(blocks, points, observed):
    total = Counter({0: 1})
    for block in blocks:
        dist = permutation_distribution(block, points)
        new = Counter()
        for a, count_a in total.items():
            for b, count_b in dist.items():
                new[a+b] += count_a * count_b
        total = new
    tail = sum(n for score, n in total.items() if score >= observed)
    count = sum(total.values())
    return {'blocs': list(blocks), 'au_moins_aussi_bon': tail, 'permutations': count,
            'fraction': str(Fraction(tail, count)), 'p': tail/count}


def evaluate(targets, candidates, groups, captions, texts):
    by_quire = {g: [p for p in candidates if groups[p] == g] for g in sorted(set(groups.values()))}
    scale = lcm(*(2*(len(block)-1) for block in by_quire.values()))
    rows, points = {}, {}
    for p in targets:
        scores, overlaps = {}, {}
        for q in by_quire[groups[p]]:
            words = sorted(captions[p].keys() & texts[q].keys())
            scores[q] = len(words)
            overlaps[q] = words
        best = max(scores.values())
        leaders = [q for q in scores if scores[q] == best]
        points[p] = {}
        for q, score in scores.items():
            # Un concurrent battu vaut 1, une égalité 1/2. On retire le candidat lui-même.
            twice = sum((v < score)*2 + (v == score) for v in scores.values()) - 1
            points[p][q] = twice * (scale // (2*(len(scores)-1)))
        wins = best > 0 and leaders == [p]
        rows[p] = {'scores': scores, 'mots_communs': overlaps, 'seuls_en_tete': leaders if best else [],
                   'score_attendu': scores[p], 'prediction_correcte_unique': wins,
                   'rang_attendu_meilleur': 1+sum(s > scores[p] for s in scores.values()),
                   'rang_attendu_pire': sum(s >= scores[p] for s in scores.values())}
    observed = sum(points[p][p] for p in targets)
    result = {'par_panneau': rows, 'score_moyen': observed/(scale*len(targets)),
              'reussites_uniques': [p for p in targets if rows[p]['prediction_correcte_unique']],
              'fausses_destinations_uniques': [p for p in targets if len(rows[p]['seuls_en_tete']) == 1
                                                and not rows[p]['prediction_correcte_unique']]}
    if set(targets) == set(candidates):
        result['permutations_cahier'] = combine(list(by_quire.values()), points, observed)
        folios = defaultdict(list)
        for p in targets:
            folios[re.match(r'f\d+', p)[0]].append(p)
        result['permutations_feuillet'] = combine(list(folios.values()), points, observed)
    return result


def one(pages, groups, data, modes, with_seed=False, equal=False, negative=False):
    targets = [p for p in pages if p != NO_LABEL and (with_seed or p != SEED)]
    candidates = [p for p in pages if p in targets or (negative and p == NO_LABEL)]
    captions, texts, sizes = vocabularies(candidates, groups, data, modes, equal)
    result = evaluate(targets, candidates, groups, captions, texts)
    details = {'legendes': captions, 'prose': texts, **sizes}
    return result, details


def controls():
    pages = ['f1r', 'f1v', 'f2r', 'f2v']
    groups = dict.fromkeys(pages, 'A')
    caps = {p: {p: ['x']} for p in pages}
    text = {p: {p: ['y']} for p in pages}
    r = evaluate(pages, pages, groups, caps, text)
    assert len(r['reussites_uniques']) == 4 and r['permutations_cahier']['p'] == 1/24
    for i, p in enumerate(pages):
        text[p] = {pages[(i + 1) % 4]: ['y']}
    r = evaluate(pages, pages, groups, caps, text)
    assert len(r['fausses_destinations_uniques']) == 4
    empty = evaluate(pages, pages, groups, {p: {} for p in pages}, text)
    assert empty['score_moyen'] == 0.5 and empty['permutations_cahier']['p'] == 1.0
    assert common_words([{'A':['alpha'], 'B':['beta']},{'A':['beta'], 'B':['alpha']}]) == {}
    assert cut_prose({'a':['?','a'], 'b':['foo']}, 2) == {'a':['?','a']}


def main():
    controls()
    pages, groups, data = inventory()
    primary, vocab = one(pages, groups, data, MODES)
    full, with_seed = one(pages, groups, data, MODES, with_seed=True)
    capped, sample = one(pages, groups, data, MODES, equal=True)
    negative, _ = one(pages, groups, data, MODES, negative=True)
    sans89, _ = one([p for p in pages if not p.startswith('f89')], groups, data, MODES)
    _, _, centered = inventory(('P0', 'Pc'))
    with_centered, _ = one(pages, groups, centered, MODES)
    variants = {'/'.join(m): one(pages, groups, data, [m])[0] for m in MODES}
    winning_words = set()
    for p in primary['reussites_uniques']:
        winning_words.update(primary['par_panneau'][p]['mots_communs'][p])
    masked = {}
    targets = list(primary['par_panneau'])
    for word in sorted(winning_words):
        filtered = {p:{w:locs for w,locs in vocab['legendes'][p].items() if w != word} for p in targets}
        test = evaluate(targets, targets, groups, filtered, vocab['prose'])
        masked[word] = test['reussites_uniques']
    report = {'cahiers':groups, 'principal':primary, 'avec_f89r2':full, 'meme_longueur':capped,
              'plafonds_positions':sample['plafonds'], 'avec_texte_sans_legende_f101r':negative,
              'lectures_separees':variants, 'reussites_apres_retrait_par_mot':masked,
              'diagnostic_sans_feuillet_89':sans89, 'diagnostic_avec_ligne_centree':with_centered}
    for filename, obj in [('RESULTATS.json', report), ('OCCURRENCES.json', with_seed)]:
        (HERE / filename).write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
