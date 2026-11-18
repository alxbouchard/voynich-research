"""Fige les tables des quatre mots historiques avant les deux positions suivantes."""
from collections import Counter
from hashlib import sha256
import json
from deux_mots import HERE, project, sources, tokenize
from voisinage import solve

RULE = '105007ec73b90b7cf5d7855c26181dc4a60c5e60543cea227afe2ead0b2992ff'
TRAIN = ['aristologie', 'longue', 'est', 'ainsi']
TEST = ['appellee', 'pour']


def positive():
    all_words = TRAIN + TEST
    encode = {c: f'g{i}' for i, c in enumerate(sorted(set(''.join(all_words))))}
    encrypted = [tuple(encode[c] for c in w) for w in all_words]
    key = {encode[c]: c for c in ''.join(TRAIN)}
    unseen = {c for w in TEST for c in w if encode[c] not in key}
    known_outputs = [project(v, key) for v in encrypted[4:]]
    assert unseen == {'p'} and list(solve(list(zip(encrypted[:4], TRAIN)), key)) == [key]
    extensions = list(solve(list(zip(encrypted[4:], TEST)), key))
    assert extensions == [{**key, encode['p']: 'p'}]
    # Cette troisième forme réservée n’apporte aucune nouvelle lettre.
    assert project(tuple(encode[c] for c in 'longue'), key) == 'longue'
    return {'mots': all_words, 'chiffre': encrypted, 'sorties': known_outputs,
            'nouvelles_lettres': sorted(unseen), 'extension_unique': extensions[0]}


def evaluate(row, line, identities, projections):
    def token(position):
        return tokenize(line[position - 1], row['composes'], row['signes_inverses'])
    observed = [(token(i), w) for i, w in zip((6, 5, 4, 3), TRAIN)]
    holdout = [(token(i), w) for i, w in zip((2, 1), TEST)]
    counts = Counter(n_tables=0, premier_lisible=0, second_lisible=0, premier_exact=0,
                     second_exact=0, paire_exacte=0, premier_prolongeable=0,
                     second_prolongeable=0, deux_prolongeables=0)
    examples = []
    for key in solve(sorted(observed, key=lambda eq: (len(eq[1]), -len(eq[0]))), {}):
        outputs = [project(seq, key) for seq, _ in holdout]
        identities.add(tuple(sorted(key.items())))
        projections[outputs[0]] += 1
        possible = [next(solve([eq], key), None) is not None for eq in holdout]
        counts.update(n_tables=1, premier_lisible='[' not in outputs[0], second_lisible='[' not in outputs[1],
                      premier_exact=outputs[0] == TEST[0], second_exact=outputs[1] == TEST[1], paire_exacte=outputs == TEST,
                      premier_prolongeable=possible[0], second_prolongeable=possible[1],
                      deux_prolongeables=all(possible) and next(solve(holdout, key), None) is not None)
        if not examples:
            examples.append({'table': key, 'lectures_des_deux_mots': outputs})
    assert counts['n_tables'] == row['n_tables']
    return {'edition': row['edition'], 'composes': row['composes'], 'signes_inverses': row['signes_inverses'],
            'ordre_inverse': row['ordre_inverse'], **counts, 'exemple': examples[0]}


def main():
    assert sha256((HERE / 'TRANSFERT.md').read_bytes()).hexdigest() == RULE
    previous = json.loads((HERE / 'tous_signes_muets.json').read_text())['essais']
    lines = sources()
    lines['L+8H'] = [*lines['L'][:7], lines['H'][7]]
    accepted = [r for r in previous if r['n_tables'] and not r['positions_absentes']]
    assert all(r['cible'] == 'plante' and r['ordre_inverse'] for r in accepted)
    rows, summaries = [], {}
    for edition, line in lines.items():
        keys, readings = set(), Counter()
        rows.extend(evaluate(r, line, keys, readings) for r in accepted if r['edition'] == edition)
        summaries[edition] = {'tables_distinctes': len(keys), 'configurations_avec_table': sum(readings.values()),
                              'sorties_distinctes_cinquieme_mot': len(readings),
                              'lectures_du_cinquieme_et_effectifs': dict(sorted(readings.items()))}
    out = {'protocole_sha256': RULE, 'controle': positive(), 'cibles': TEST, 'bilan_par_edition': summaries, 'essais': rows}
    (HERE / 'transfert.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for ed in lines:
        fields = ('n_tables','premier_lisible','second_lisible','premier_exact','second_exact',
                  'paire_exacte','premier_prolongeable','second_prolongeable','deux_prolongeables')
        print(ed, {k: sum(r[k] for r in rows if r['edition'] == ed) for k in fields})


if __name__ == '__main__':
    main()
