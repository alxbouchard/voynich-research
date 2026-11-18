"""Compte toutes les tables pouvant épeler la phrase, aucun maximum sur les signes muets."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from itertools import product

from deux_mots import HERE, TARGETS, sources, tokenize

RULE = '719a054b7106755e8756b921ce67db8f035e814e143414c366a592d85edfb834'


def choose_word(signs, target, key):
    """Partitionne le mot en substrings, y compris vides, sans choisir un signe muet d’avance."""
    if not signs:
        if not target:
            yield key
        return
    head, tail = signs[0], signs[1:]
    if head in key:
        val = key[head]
        if target.startswith(val):
            yield from choose_word(tail, target[len(val):], key)
        return
    for size in range(len(target) + 1):
        yield from choose_word(tail, target[size:], {**key, head: target[:size]})


def solve(equations, key):
    if not equations:
        yield key
        return
    signs, word = equations[0]
    for assigned in choose_word(signs, word, key):
        yield from solve(equations[1:], assigned)


@lru_cache(None)
def tally(equations):
    constraints = sorted(equations, key=lambda eq: (len(eq[1]), -len(eq[0])))
    counts = Counter()
    first = {}
    for key in solve(constraints, {}):
        assert all(''.join(key[s] for s in v) == w for v, w in equations)
        n = list(key.values()).count('')
        counts[n] += 1
        first.setdefault(n, key)
    return {'compte_par_nombre_de_signes_muets': dict(sorted(counts.items())),
            'n_tables': sum(counts.values()), 'minimum': min(counts, default=None),
            'exemple_a_ce_minimum': first[min(counts)] if counts else None}


def known_answer():
    cipher = {c: str(i) for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')}
    outputs = []
    for words, ctx in TARGETS.values():
        plain = words + [s for _, s in ctx]
        for mute in (False, True):
            equations = [(tuple(k for c in word for k in ([cipher[c], 'muet'] if mute else [cipher[c]])), word)
                         for word in plain]
            truth = {k: c for c, k in cipher.items() if any(c in w for w in plain)}
            if mute:
                truth['muet'] = ''
            # Ajouter la vraie table de la paire restitue aussi les voisins encodés.
            assert list(solve(equations, truth)) == [truth]
            # Le moteur doit aussi retrouver cette table sans graine, ni positions en clair.
            candidates = solve(sorted(equations, key=lambda e: (len(e[1]), -len(e[0]))), {})
            assert any(truth == proposed for proposed in candidates)
            outputs.append({'clair': plain, 'avec_marque_muette': mute, 'vraie_table_retrouvee': True})
    return outputs


def main():
    assert sha256((HERE / 'SUITE.md').read_bytes()).hexdigest() == RULE
    previous = json.loads((HERE / 'resultats.json').read_text())['essais']
    counts_pair = {(r['edition'], r['cible'], r['composes'], r['signes_inverses'], r['ordre_inverse']):
                   r['compatibles_par_nombre_muet'] for r in previous}
    witness = sources()
    witness['L+8H'] = [*witness['L'][:7], witness['H'][7]]
    records = []
    for ed, line in witness.items():
        for target, compound, char_rev, row_rev in product(TARGETS, (True, False), (False, True), (False, True)):
            pair, ctx = TARGETS[target]
            start, step = (5, -1) if row_rev else (4, 1)
            positions = [(0, pair[0]), (1, pair[1]), *ctx]
            equations, missing = [], []
            for delta, plain in positions:
                word = line[start + step * delta]
                if word is None or '*' in word:
                    missing.append(start + step * delta + 1)
                else:
                    equations.append((tokenize(word, compound, char_rev), plain))
            stats = tally(tuple(equations))
            # Le contre-calcul autorise TOUT choix muet simultanément. Il doit retrouver
            # les mêmes effectifs de solutions au niveau 0, 1 et au minimum sur la paire.
            original = counts_pair[('L' if ed == 'L+8H' else ed, target, compound, char_rev, row_rev)]
            pair_counts = tally(tuple(equations[:2]))['compte_par_nombre_de_signes_muets']
            assert all(pair_counts.get(int(k), 0) == v for k, v in original.items())
            records.append({'edition': ed, 'cible': target, 'composes': compound, 'signes_inverses': char_rev,
                            'ordre_inverse': row_rev, 'positions_absentes': missing, **stats})
    results = {'protocole_sha256': RULE, 'controle': known_answer(), 'essais': records}
    (HERE / 'tous_signes_muets.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for ed in witness:
        group = [r for r in records if r['edition'] == ed]
        print(ed, 'branches solutions complètes', sum(r['n_tables'] > 0 and not r['positions_absentes'] for r in group),
              'branches solutions observées', sum(r['n_tables'] > 0 for r in group),
              'tables', sum(r['n_tables'] for r in group))


if __name__ == '__main__':
    main()
