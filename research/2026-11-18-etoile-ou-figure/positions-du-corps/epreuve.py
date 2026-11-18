"""Tester l'inversion manu / unam dans les groupes matériellement adjacents."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
import json
import re
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-dam-en-fin-de-ligne'))
from corpus_dam import MODES, WORD, corpus, parse, segment
from dechiffrer import PANELS

ORDERS = tuple(permutations(range(4)))
REVERSE = (3, 2, 1, 0)
VIEWS = {'accord': MODES, 'H': (MODES[0],), 'ZL': (MODES[2],)}


def save(path, value):
    (HERE / path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1) + '\n')


def panels():
    editions, _ = corpus()
    rows = {}
    for edition, mode in MODES:
        for loc, (page, kind, _, raw) in editions[edition].items():
            if page in PANELS:
                # Les angles des étiquettes décrivent leur place et ne portent aucun signe.
                # Garder une séparation aux notes mentionnant un trou ou un espace large.
                raw = re.sub(r'<![^>]*>', lambda m: '<->' if re.search(r'gap|hole', m[0], re.I) else '', raw)
                rows.setdefault(loc, {})[(edition, mode)] = (kind, *parse(raw, mode))
    return rows


def same(words):
    return len(set(words)) == 1 and bool(WORD.fullmatch(words[0]))


def full_key(cipher):
    table = {}
    for latin, eva in zip(('in', 'ipsa', 'manu'), cipher):
        code = segment(eva)
        if len(latin) != len(code):
            return False
        for clear, sign in zip(latin, code):
            if table.setdefault(clear, sign) != sign:
                return False
    return len(set(table.values())) == len(table)


def four(units):
    return len(units) == 4 and len(set(units)) == 4


def read_slots(scope):
    hist = defaultdict(Counter)
    data = []
    for loc, sources in panels().items():
        keys = VIEWS[scope]
        if not all(k in sources for k in keys):
            continue
        members = [sources[k] for k in keys]
        kind, marks, blocks = members[0]
        hist[kind]['lieux'] += 1
        if not all(k == kind and m == marks and list(map(len,b)) == list(map(len,blocks))
                   for k,m,b in members):
            hist[kind]['structure_divergente'] += 1
            continue
        by_word = [[tuple(m[2][j][i] for m in members) for i in range(len(block))]
                   for j,block in enumerate(blocks)]
        if all(same(v) for block in by_word for v in block):
            hist[kind]['mots_par_ligne_'+str(sum(map(len,blocks)))] += 1
        else:
            hist[kind]['ligne_partiellement_lisible'] += 1
        for j,block in enumerate(by_word,1):
            for i,v in enumerate(block):
                if not all(WORD.fullmatch(g) for g in v):
                    continue
                units = segment(v[0])
                if same(v) and four(units) and i+1 < len(block):
                    tests = ['deux_mots']
                    if i >= 2 and all(same(g) for g in block[i-2:i]) and full_key([g[0] for g in block[i-2:i+1]]):
                        tests.append('phrase_quatre_mots')
                    for test in tests:
                        data.append((kind,loc,j,i+1,test,units,block[i+1]))
                # Le mot fusionné doit comporter huit unités dans chaque lecture.
                # Masquer la seconde moitié, la comparer à l'ouverture.
                encoded = [segment(g) for g in v]
                if all(len(g)==8 and g[:4]==units[:4] for g in encoded) and four(units[:4]):
                    data.append((kind,loc,j,i+1,'fusion',units[:4],tuple(''.join(segment(g)[4:]) for g in v)))
    return hist, data


def make():
    forecasts, coverage = [], {}
    for scope in VIEWS:
        hist, rows = read_slots(scope)
        coverage[scope] = hist
        for kind,loc,j,i,test,stem,_ in rows:
            forecasts.append({'vue':scope,'type':kind,'lieu':loc,'troncon':j,'rang':i,'essai':test,
                              'base':list(stem),'annonce':''.join(reversed(stem))})
    return coverage, forecasts


def calibration():
    key = dict(zip('inpsamu', ('ch','o','k','y','d','sh','t')))
    cipher = [''.join(key[c] for c in word) for word in ('in','ipsa','manu','unam')]
    given = cipher[:3]
    assert full_key(given)
    stem = segment(given[-1])
    assert four(stem)
    predictions = {order: ''.join(stem[i] for i in order) for order in ORDERS}
    assert predictions[REVERSE] == cipher[-1]
    assert sum(v == cipher[-1] for v in predictions.values()) == 1
    return dict(expose=given,annonce=predictions[REVERSE],vrai=cipher[-1],ordres_exacts=1,ordres_testes=24)


def verify():
    _, forecasts = make()
    assert forecasts == json.loads((HERE/'ANNONCES.json').read_text())
    coverage, results, details = {}, {}, []
    for scope in VIEWS:
        hist, rows = read_slots(scope)
        coverage[scope] = hist
        for kind in sorted(hist):
            for test in ('deux_mots','phrase_quatre_mots','fusion'):
                group = [r for r in rows if r[0] == kind and r[4] == test]
                scores = [0] * len(ORDERS)
                n = 0
                for _,loc,j,i,_,stem,answers in group:
                    if not same(answers):
                        continue
                    n += 1
                    observed = segment(answers[0])
                    right = [k for k,order in enumerate(ORDERS) if tuple(stem[u] for u in order)==observed]
                    for k in right:
                        scores[k] += 1
                    details.append([scope,kind,test,loc,j,i,''.join(stem),''.join(reversed(stem)),answers[0],
                                    [''.join(str(v+1) for v in ORDERS[k]) for k in right]])
                results['/'.join((scope,kind,test))] = dict(annonces=len(group),juges=n,justes=scores[ORDERS.index(REVERSE)],
                        esperance=sum(scores)/24,ordres_ex_aequo=scores.count(scores[ORDERS.index(REVERSE)]),
                        meilleurs=sum(v>scores[ORDERS.index(REVERSE)] for v in scores),scores=scores)
    save('RESULTATS.json',dict(couverture=coverage,ordres=[''.join(str(v+1) for v in o) for o in ORDERS],resultats=results,
                               controle=calibration(),lectures=details,
                               empreinte_annonces=sha256((HERE/'ANNONCES.json').read_bytes()).hexdigest()))


if __name__ == '__main__':
    if sys.argv[1] == 'annoncer':
        _, forecasts = make()
        save('ANNONCES.json', forecasts)
    elif sys.argv[1] == 'verifier':
        verify()
    else:
        raise ValueError(sys.argv[1])
