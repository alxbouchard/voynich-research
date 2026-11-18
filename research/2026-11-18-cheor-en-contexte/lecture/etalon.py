"""Contrôles de lecture à clé cachée. Exécuter avec python3 -B etalon.py."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from random import Random
from string import ascii_lowercase, ascii_uppercase

from lecture import potential, heldout
from corpus_sources import LATIN

HERE = Path(__file__).resolve().parent


def synthetic():
    # Ces deux variantes rendent les deux lectures de la ligne 32 avec la même table.
    truth = dict(d='pi', a='c', r='k', ch='p', e='e', o='a', sh='b',
                 s='t', l='an', y='r', t='c', i='o', n='n', k='l')
    output = []
    for edition, third in [('H', 'beak'), ('ZL', 'back')]:
        for case, right, left, intermediate in [
            ('positif', 'peeler', 'raccoon', 'can'),
            ('droite_deplacee', 'pelere', 'raccoon', 'can'),
            ('gauche_alteree', 'peeler', 'raccogn', 'can'),
            ('milieu_altere', 'peeler', 'raccoon', 'dog'),
        ]:
            row = ['pick', 'peak', third, 'then', 'peak', 'at', intermediate,
                   'and', left, 'peak', right]
            # Ces entrées isolées rendent les lexiques comparables sans créer de voisinage.
            corpus = {'passage': row, **{w: [w] for w in
                      ['peeler', 'pelere', 'raccoon', 'raccogn', 'can', 'dog']}}
            for group in potential(corpus):
                if group['edition'] != edition:
                    continue
                group['records'] = [rec for rec in group['records']
                                    if rec['section'] == 'passage' and rec['center'] == 1]
                predictions = sorted({w for rec in group['records'] for w in rec['predicted']})
                competitor = sorted({w for rec in group['records'] for w in rec['control']})
                assert predictions == ['peeler'] and competitor == ['pelere']
                result = heldout(corpus, group)
                matches = result['local_three_occurrences']
                assert all(m['centers'] == [1, 4, 9] for m in matches)
                labels = {m['test'] for m in matches}
                expected = {'positif': {'predicted'}, 'droite_deplacee': {'control'},
                            'gauche_alteree': set(), 'milieu_altere': set()}[case]
                assert labels == expected, (edition, case, labels)
                if matches:
                    assert any(all(truth[k] == v for k, v in m['key'].items())
                               for m in matches)
                counts = result['counts']
                if case == 'gauche_alteree':
                    assert counts['predicted_forward_right'] and not counts.get('predicted_forward_two_sides_keys')
                if case == 'milieu_altere':
                    assert counts['predicted_forward_two_sides_keys']
                output.append(dict(edition=edition, cas=case, largeur=group['width'],
                                   passage=row, amorce=row[:3], tables_amorce=len(group['records']),
                                   predictions_lexique=predictions, concurrent_lexique=competitor,
                                   verification=result))
    return dict(table_de_construction=truth, essais=output)


def first_three(row):
    for pos, word in enumerate(row):
        if not pos or len(word) < 4:
            continue
        later = [i for i in range(pos + 2, min(len(row)-1, pos + 121)) if row[i] == word]
        for second in later:
            for third in later:
                if third >= second + 2:
                    return pos, second, third
    raise ValueError('Aucun triplet admissible')


def possibilities(cipher, vocabulary, seed_key):
    matches = []
    for word in vocabulary:
        if len(word) != len(cipher):
            continue
        key = dict(seed_key)
        for symbol, letter in zip(cipher, word):
            if symbol in key:
                if key[symbol] != letter:
                    break
            elif letter in key.values():
                break
            else:
                key[symbol] = letter
        else:
            matches.append(word)
    return matches


def predict(ciphertext, seeds, centers, vocabulary, other_vocabulary):
    key = {}
    for encoded, plain in zip(ciphertext[centers[0]-1:centers[0]+2], seeds):
        assert len(encoded) == len(plain)
        for cipher, letter in zip(encoded, plain):
            assert key.get(cipher, letter) == letter
            key[cipher] = letter
    assert len(set(key.values())) == len(key)

    def masked(token):
        return ''.join(key.get(c, '?') for c in token)

    candidates = []
    for center in centers[1:]:
        triple = []
        for i in range(center-1, center+2):
            raw = ciphertext[i]
            mask = masked(raw)
            triple.append(dict(rang=i+1, chiffre=raw, cle_seule=mask,
                               candidats_notice=possibilities(raw, vocabulary, key),
                               candidats_autres_notices=possibilities(raw, other_vocabulary, key)))
        candidates.append(triple)
    exact_elsewhere = Counter(masked(w) for i,w in enumerate(ciphertext)
                              if abs(i-centers[0]) > 1 and '?' not in masked(w))
    return dict(cle_apprise=key, triplets_reserves=candidates,
                lectures_entieres_hors_amorce=dict(sorted(exact_elsewhere.items())))


def macer():
    assert sha256(LATIN.read_bytes()).hexdigest() == 'c251598bbab3f9f93de40a72d4e039c17f52ce079dd95e86c7322f9a2283893b'
    corpus = json.loads(LATIN.read_text())
    title, row = next(iter(corpus.items()))
    background = sorted({w for other, words in corpus.items() if other != title for w in words})
    cipher_alpha = list(ascii_uppercase)
    seed = 102222
    Random(seed).shuffle(cipher_alpha)
    encrypt = str.maketrans(ascii_lowercase, ''.join(cipher_alpha))
    encoded = [w.translate(encrypt) for w in row]
    centers = first_three(row)
    assert centers == (26,34,140) and title == 'Artemisia'
    seeds = row[centers[0]-1:centers[0]+2]
    predictions = predict(encoded, seeds, centers, sorted(set(row)), background)
    # La vérité de lecture des voisins intervient pour la première fois ici.
    for triplet in predictions['triplets_reserves']:
        for record in triplet:
            actual = row[record['rang']-1]
            assert actual in record['candidats_notice']
            mask = record['cle_seule']
            assert all(m in ('?',c) for m,c in zip(mask,actual))
            record['devoile'] = actual
    assert [v['cle_seule'] for vs in predictions['triplets_reserves'] for v in vs] == [
        'in?entri?', 'dicitur', 'e?u?', 'ru?eti?', 'dicitur', 'et']
    radix = row.index('radix')
    visible = ''.join(predictions['cle_apprise'].get(c, '?') for c in encoded[radix])
    assert visible == 'radi?'
    radix_record = dict(rang=radix+1, chiffre=encoded[radix], cle_seule=visible,
        candidats_notice=possibilities(encoded[radix], sorted(set(row)), predictions['cle_apprise']),
        candidats_autres_notices=possibilities(encoded[radix], background, predictions['cle_apprise']))
    assert not possibilities(encoded[141], ['te'], predictions['cle_apprise'])
    return dict(notice=title, longueur=len(row), rangs=[i+1 for i in centers], amorce=seeds,
                vocabulaire_notice=len(set(row)), vocabulaire_autres_notices=len(background),
                radix_illustration_exploratoire=radix_record, rng=seed, sha256_chiffre=sha256(
                    ' '.join(encoded).encode()).hexdigest(),
                contre_exemple_et_inverses=dict(propose='te', compatible=False),
                **predictions)


if __name__ == '__main__':
    content = dict(synthetique=synthetic(), macer=macer())
    (HERE / 'ETALON.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
