"""Cherche une même table de signes pour deux noms inscrits sur le Taureau d’al-Ṣūfī."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from essai import SPEC, frozen, project, tables, tokenize, variants


def base_letters(word):
    return ''.join(c for c in unicodedata.normalize('NFC', word)
                   if not unicodedata.category(c).startswith('M') and c != 'ـ')


def compare(signs_a, signs_b, word_a, word_b, mute):
    preset = {mute: ''} if mute else {}
    # Les occurrences muettes ne consomment aucune lettre de la cible.
    audible_a = tuple(sign for sign in signs_a if sign != mute)
    audible_b = tuple(sign for sign in signs_b if sign != mute)
    maps_a = list(tables(audible_a, word_a, None, preset))
    maps_b = list(tables(audible_b, word_b, None, preset))
    joint = {frozen(m) for a in maps_a for m in tables(audible_b, word_b, None, a)}
    reverse = {frozen(m) for b in maps_b for m in tables(audible_a, word_a, None, b)}
    assert joint == reverse
    return {
        'tables_X1_seul': len(maps_a),
        'tables_X3_seul': len(maps_b),
        'lectures_exactes_X3_depuis_X1_sans_ajout': sum(project(signs_b, m) == word_b for m in maps_a),
        'lectures_exactes_X1_depuis_X3_sans_ajout': sum(project(signs_a, m) == word_a for m in maps_b),
        'tables_communes': [dict(m) for m in sorted(joint)],
    }


def calibration(word_a, word_b):
    alphabet = {letter: f'u{i}' for i, letter in enumerate(sorted(set(word_a + word_b)))}
    def encode(word):
        return tuple(alphabet[c] for c in word)

    trained = list(tables(encode(word_a), word_a, 1))
    assert len(trained) == 1 and project(encode('ال'), trained[0]) == 'ال'
    joint = list(tables(encode(word_b), word_b, 1, trained[0]))
    assert len(joint) == 1 and project(encode(word_b), joint[0]) == word_b
    expanded = compare(('K', 'Z', 'K', 'Z'), ('Z', 'K', 'M'), 'الال', 'الب', 'Z')
    assert expanded['tables_communes'] == [{'K': 'ال', 'M': 'ب', 'Z': ''}]
    return {
        'controle_signe_muet': expanded, 'mots': [word_a, word_b],
        'mot2_depuis_mot1': project(encode(word_b), trained[0]),
        'article_depuis_mot1': project(encode('ال'), trained[0]),
        'cle_commune': joint[0],
    }


def run_variant(word_a, word_b, articles):
    counts = Counter(hypotheses_non_vide=0, hypotheses_un_signe_muet=0,
                     tables_non_vide=0, tables_un_signe_muet=0)
    records = []
    for edition, (first, second) in SPEC['lectures'].items():
        for (cut, form), compound, reverse in itertools.product(variants(second), (True, False), (False, True)):
            signs_a = tokenize(first, compound, reverse)
            signs_b = tokenize(form, compound, reverse)
            known = set(signs_a)
            present = sorted((known | set(signs_b)) - {' '})
            for mute in [None, *present]:
                stat = compare(signs_a, signs_b, word_a, word_b, mute)
                category = 'un_signe_muet' if mute else 'non_vide'
                counts['hypotheses_' + category] += 1
                counts['tables_' + category] += len(stat['tables_communes'])
                for key in stat['tables_communes']:
                    # Une table ajustée aux deux cibles peut encore être testée sur le trait X.2.
                    stat.setdefault('transfert_par_table', []).append({
                        'X2': project(tokenize('oalcheol', compound, reverse), key),
                        'lecture_X3_avec_valeurs_communes': project(signs_b, {s:v for s,v in key.items() if s in known or s == mute}),
                        'lettres_de_X3_dont_le_signe_est_dans_X1': sum(len(key[s]) for s in signs_b if s in known and s != ' '),
                    })
                records.append({
                    'articles': articles, 'mots': [word_a, word_b], 'edition': edition,
                    'espaces': cut, 'ch_compose': compound, 'inverse': reverse, 'signe_muet': mute, **stat,
                })
    return counts, records


def main():
    source = HERE.parent.parent / 'medieval'
    reference = json.loads((source / 'NOMS-ARABES.json').read_text())
    image = source / reference['source_file']
    assert hashlib.sha256(image.read_bytes()).hexdigest() == reference['source_sha256']
    names = [reference['names'][k] for k in ('pleiades', 'aldebaran')]
    a, b = [base_letters(n['normalized']) for n in names]
    assert [list(a), list(b)] == [n['base_letters'] for n in names]
    assert a.startswith('ال') and b.startswith('ال')

    totals, details = {}, []
    for articles, left, right in [('deux', a, b), ('aucun', a[2:], b[2:]), ('X1', a, b[2:]), ('X3', a[2:], b)]:
        totals[articles], rows = run_variant(left, right, articles)
        details.extend(rows)
    witness = {'source': reference['witness'], 'image_sha256': reference['source_sha256'],
               'graphies': [a, b], 'source_des_lettres': '../../medieval/NOMS-ARABES.json'}
    result = {'temoin': witness, 'empreinte_protocole': hashlib.sha256((HERE / 'PROTOCOLE.md').read_bytes()).hexdigest(),
              'controle': calibration(a, b), 'totaux': totals, 'detail': details}
    (HERE / 'RESULTATS.json').write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
