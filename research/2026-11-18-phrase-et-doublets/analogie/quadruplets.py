"""Prédire D par insertion, puis évaluer sur un feuillet ou dans une autre section."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-opcheor-paralleles/variantes'))
from compter import corpus, runs, segment

ANCHOR = ('f89r2.22', 'opcheor', 'opcheol', 'shody')
EXCLUDED = {'f89', 'f100'}
VIEWS = ('H/joints', 'H/separes', 'ZL/joints', 'ZL/separes')
MAIN = 'b_apres_2'
RULES = (MAIN, 'b_avant_2', 'a_apres_2', 'a_avant_2')
BASELINE = 'copier_C'
units = lru_cache(maxsize=None)(segment)


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')


def trigger(a, b, c):
    return len(a) >= 3 and a[:-1] == b[:-1] and a[-1] != b[-1] and len(c) >= 3


def insert(word, position, sign):
    return word[:position] + (sign,) + word[position:]


def predict(site):
    _, a, b, c = site
    A, B, C = map(units, (a, b, c))
    assert trigger(A, B, C)
    return {
        MAIN: insert(C, 2, B[-1]), 'b_avant_2': insert(C, len(C)-2, B[-1]),
        'a_apres_2': insert(C, 2, A[-1]), 'a_avant_2': insert(C, len(C)-2, A[-1]),
        BASELINE: C,
    }


def extract(rows, cut, reverse, reveal):
    sites = defaultdict(list)
    for loc, (page, kind, _, raw) in sorted(rows.items()):
        if kind != 'P0':
            continue
        if re.match(r'f\d+', page)[0] in EXCLUDED and loc != ANCHOR[0]:
            continue
        for span in runs(re.sub(r'\{[^}]*\}', '?', raw), cut):
            if reverse:
                span = list(reversed(span))
            for i in range(len(span)-2):
                a, b, c = [w for _, w in span[i:i+3]]
                if not trigger(units(a), units(b), units(c)):
                    continue
                key = (loc, a, b, c)
                if loc == ANCHOR[0] and (reverse or key != ANCHOR):
                    continue
                rank = span[i][0]
                d = span[i+3][1] if reveal and i+3 < len(span) else None
                sites[key].append((rank, d))
    return sites


def common(views):
    common_keys = set.intersection(*(set(view) for view in views.values()))
    unique = sorted(k for k in common_keys if all(len(v[k]) == 1 for v in views.values()))
    return unique, len(common_keys)-len(unique)


def mask(views):
    unique, ambiguous = common(views)
    return {'triplets_communs_repetes_ecartes': ambiguous,
            'sites': [{'lieu_A_B_C': key,
                       'rangs_A_par_lecture': {v: views[v][key][0][0] for v in VIEWS},
                       'apres_2_b_unites': predict(key)[MAIN]} for key in unique]}


def summarize(entries, sections):
    total = Counter()
    floor = Counter()
    strata = defaultdict(lambda: [Counter(), Counter()])
    successes = defaultdict(list)
    trials = []
    for key, fourth in entries:
        if key == ANCHOR:
            continue
        loc, a, b, c = key
        A, B, C = map(units, (a, b, c))
        total['annonces'] += 1
        if fourth is None:
            total['quart_absent_ou_divergent'] += 1
            continue
        D = units(fourth)
        total['evaluables'] += 1
        if (A[-1], B[-1]) == ('r','l'):
            floor['evaluables'] += 1
        projections = predict(key)
        for rule, target in projections.items():
            if D == target:
                total[rule] += 1
                successes[rule].append((*key, fourth))
                if (A[-1], B[-1]) == ('r','l'):
                    floor[rule] += 1
        possible = {insert(C, k, B[-1]) for k in range(1,len(C))}
        total['nombre_de_lectures_internes'] += len(possible)
        if D in possible:
            total['b_en_position_interne_libre'] += 1
            successes['b_en_position_interne_libre'].append((*key, fourth))
        group = (sections.get(loc.split('.')[0], '?'), len(C))
        incoming, actual = strata[group]
        incoming[B[-1]] += 1
        # Si le signe de D au rang 3 retire exactement la différence, il est déterminé.
        if len(D) == len(C)+1 and D[:2] + D[3:] == C:
            actual[D[2]] += 1
            total['insertion_quelconque_apres_2'] += 1
        trials.append((*key, fourth))
    expected = sum((Fraction(sum(incoming[s]*n for s,n in actual.items()),incoming.total())
                    for incoming, actual in strata.values()), start=Fraction(0))
    return {'comptes': {k:total[k] for k in ('annonces','evaluables','quart_absent_ou_divergent',
                  *RULES, BASELINE,'nombre_de_lectures_internes','b_en_position_interne_libre',
                  'insertion_quelconque_apres_2')},
            'r_vers_l': {k:floor[k] for k in ('evaluables', *RULES, BASELINE)},
            'attente_par_permutation_section_longueur_C': str(expected),
            'lieux_des_reussites': dict(successes),
            'essais_complets': trials}


def evaluate(views, sections):
    unique, _ = common(views)
    definite = []
    discrepancies = []
    for key in unique:
        ds = {name: views[name][key][0][1] for name in VIEWS}
        vals = set(ds.values())
        value = ds[VIEWS[0]] if len(vals) == 1 else None
        if value is None:
            discrepancies.append((key, ds))
        definite.append((key, value))
    main = summarize(definite, sections)
    return {'accord': main, 'voisins_non_evalues': discrepancies,
            'par_traitement': {k: {name: v for name,v in summarize(
              [(key, d) for key, values in view.items() for _, d in values], sections).items()
              if name not in ('essais_complets', 'lieux_des_reussites')}
              for k,view in views.items()}}


def run(phase):
    assert predict(ANCHOR)[MAIN] == units('sholdy')
    assert predict(('ex','daiir','daiil','chody'))[MAIN] == units('choldy')
    assert predict(('ex','daiir','daiil','chyd'))['b_avant_2'] != predict(('ex','daiir','daiil','chyd'))[MAIN]
    toy = [(('f1r.1','dar','dal','sola'), 'solla'), (('f2r.1','dar','day','sola'), 'dara')]
    check = summarize(toy, {'f1r':'H','f2r':'H'})
    assert check['comptes'][MAIN] == 1 and check['comptes']['insertion_quelconque_apres_2'] == 1
    assert check['attente_par_permutation_section_longueur_C'] == '1/2'
    editions, sections = corpus()
    results, masked = {}, {}
    for reverse in (False, True):
        direction = 'inverse' if reverse else 'direct'
        views = {label: extract(editions[label.split('/')[0]], label.split('/')[1], reverse, phase=='verifier')
                 for label in VIEWS}
        masked[direction] = mask(views)
        if phase == 'verifier':
            results[direction] = evaluate(views, sections)
            if not reverse:
                anchor = {k: v[ANCHOR][0][1] for k,v in views.items()}
    if phase == 'predire':
        save('PREDICTIONS.json', masked)
        return
    frozen = json.loads((HERE/'PREDICTIONS.json').read_text())
    assert frozen == json.loads(json.dumps(masked))
    counts = results['direct']['accord']['comptes']
    winners = [name for name in RULES if counts[name] == max(counts[n] for n in RULES)]
    results['retour_au_point_de_depart'] = {
        'gagnantes_sur_la_reserve': winners, 'predictions_f89r2_22': {r:predict(ANCHOR)[r] for r in winners},
        'quart_lu': anchor}
    results['sha256_predictions'] = sha256((HERE/'PREDICTIONS.json').read_bytes()).hexdigest()
    save('RESULTATS.json', results)
    for direction in ('direct','inverse'):
        main = results[direction]['accord']
        print(direction,main['comptes'],main['r_vers_l'],main['attente_par_permutation_section_longueur_C'])
        print(main['lieux_des_reussites'].get(MAIN,[]))
    print(results['retour_au_point_de_depart'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['predire','verifier'])
    run(parser.parse_args().phase)
