"""Épreuve de la position de sheol, avec comptage des ouvertures renseignées."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from comparer import MODES, corpus, tokens

WORD = 'sheol'


def corresponding(readings):
    return [s[0] if len(set(s)) == 1 and re.fullmatch('[a-z]+', s[0]) else None
            for s in zip(*readings)]


def tail(hits_per_line, observed):
    dist = {0: Fraction(1)}
    for hits in hits_per_line:
        if hits:
            chance = Fraction(hits, 4)
            dist = {k: dist.get(k, 0)*(1-chance) + dist.get(k-1, 0)*chance
                    for k in range(max(dist)+2)}
    value = sum((prob for k, prob in dist.items() if k >= observed), Fraction(0))
    return {'proportion_exacte': str(value), 'p': float(value)}


def summarize(rows, clean):
    test = [r for r in rows if r['debut_commun'] and r['longueur_commune'] >= 4]
    if clean:
        test = [r for r in test if r['lisibles'] == 4]
    by_rank = [sum(i in r['positions'] for r in test) for i in range(1, 5)]
    by_rank_denom = [sum(r['accord_quatre'][i] is not None for r in test) for i in range(4)]
    predicted = [r['locus'] for r in test if 2 in r['positions']]
    return {
        'lignes_P0_deux_editions': len(rows),
        'ouvertures_communes_avant_longueur': sum(r['debut_commun'] for r in rows),
        'ouvertures_marquees_dans_une_seule_edition_sur_P0_communs':
            [r['locus'] for r in rows if r['debut_partiel']],
        'ouvertures_communes_trop_courtes':
            [r['locus'] for r in rows if r['debut_commun'] and r['longueur_commune'] < 4],
        'ouvertures_retenues': len(test), 'positions_lisibles': by_rank_denom,
        'sheol_par_rang': by_rank, 'lieux_en_deuxieme_position': predicted,
        'feuillets_distincts_en_deuxieme_position': sorted({re.match(r'f\d+', loc)[0] for loc in predicted}),
        'loi_conditionnelle': tail([sum(pos <= 4 for pos in r['positions']) for r in test], by_rank[1]),
        'occurrences_apres_position_4_sur_ouvertures_retenues': sum(sum(pos > 4 for pos in r['positions']) for r in test),
        'occurrences_sur_toutes_les_lignes_P0_alignees': sum(len(r['positions']) for r in rows),
    }


def main():
    assert tail([1, 1], 2)['proportion_exacte'] == '1/16'
    assert tail([2, 0], 1)['proportion_exacte'] == '1/2'
    assert tail([], 0)['p'] == 1
    editions, sections = corpus()
    rows, omitted = [], []
    for loc in dict.fromkeys((*editions['H'], *editions['ZL'])):
        aligned = [editions[e].get(loc) for e in ('H', 'ZL')]
        flags = [a is not None and a[1] == 'P0' for a in aligned]
        if not all(flags):
            if any(a and a[1]=='P0' and '<%>' in a[3] for a in aligned):
                omitted.append(loc)
            continue
        a, b = aligned
        readings = [tokens(editions[e][loc][3], cut) for e, cut in MODES]
        common = corresponding(readings)
        starts = ['<%>' in a[3], '<%>' in b[3]]
        rows.append({'locus': loc, 'folio': re.match(r'f\d+',loc)[0], 'page': a[0],
                     'section': sections[a[0]], 'debut_commun': all(starts), 'debut_partiel': starts[0]!=starts[1],
                     'longueur_commune': len(common), 'accord_quatre': common[:4],
                     'lisibles': sum(w is not None for w in common[:4]),
                     'positions': [i for i,w in enumerate(common, 1) if w == WORD]})
    affected = [r for r in rows if r['folio'] == 'f89']
    assert {r['locus'] for r in affected if r['debut_commun'] and 2 in r['positions']} >= {'f89r2.22','f89v2.7'}
    rest = [r for r in rows if r['folio'] != 'f89']
    summary = {}
    for name, subset in [('pharmaceutique', [r for r in rest if r['section']=='P']),
                         ('autres_sections', [r for r in rest if r['section']!='P']),
                         ('tous_hors_f89', rest), ('source_f89', affected)]:
        summary[name] = {key:summarize(subset, clean) for key,clean in [('principal',False),('tous_lisibles',True)]}
    result = {'bilan': summary, 'ouvertures_absentes_du_corpus_P0_aligne': sorted(omitted),
              'lignes_avec_sheol': [r for r in rows if r['positions']]}
    (HERE/'POSITIONS.json').write_text(json.dumps(result, ensure_ascii=False, indent=1)+'\n')


if __name__ == '__main__':
    main()
