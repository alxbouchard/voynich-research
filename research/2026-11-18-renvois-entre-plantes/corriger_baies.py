"""Reprendre le calcul des deux panneaux à baies, selon le catalogue et l'alignement."""
from fractions import Fraction
import json
from math import comb
from pathlib import Path
from croiser import CAT, corpus, load, texts

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-11-18-opcheor-suite/f52/fleurs/PANNEAUX.json'
TARGETS = ('f99r', 'f100r')
WORDS = {'ctheor', 'ctheol'}


def placement(n, m, a, b):
    """Probabilité conditionnelle que chacun des deux panneaux soit atteint."""
    all_draws = comb(n, m)
    numerator = all_draws - comb(n-a, m) - comb(n-b, m) + comb(n-a-b, m)
    # Second calcul indépendant par nombres de places choisies sur chacun des deux panneaux.
    direct = sum(comb(a, i)*comb(b, j)*comb(n-a-b, m-i-j)
                 for i in range(1, m) for j in range(1, m-i+1))
    assert numerator == direct
    return Fraction(numerator, all_draws)


def summarize(pages, data):
    pages = sorted(pages)
    sizes = {p: len(data[p]) for p in pages}
    hits = {p: [(word, loc) for word, loc, _, _ in data[p] if word in WORDS] for p in pages}
    observed = [p for p in pages if hits[p]]
    readable = [p for p in pages if sizes[p]]
    m = sum(map(len, hits.values()))
    n = sum(sizes.values())
    probability = placement(n, m, *(sizes[p] for p in TARGETS))
    return dict(positions=n, occurrences=m, positions_par_face=sizes,
                faces_avec_une_forme=observed, faces_avec_au_moins_une_position=readable,
                paires_positives=comb(len(observed), 2), paires_du_catalogue=comb(len(pages), 2),
                paires_sur_faces_lisibles=comb(len(readable), 2),
                probabilite_exacte=[probability.numerator, probability.denominator],
                pourcentage=float(probability)*100)


def original_panels():
    ed, _ = corpus()
    kinds = {}
    for loc, (page, kind, _, _) in ed['H'].items():
        if loc in ed['ZL'] and ed['ZL'][loc][1] == kind:
            kinds.setdefault(page, set()).add(kind)
    return {p for p, types in kinds.items() if {'P0', 'Lf'} <= types}


def main():
    panels = load(CAT)['panneaux']
    original = original_panels()
    assert set(panels) - original == {'f101r'} and not original - set(panels)
    q19 = {p for p, r in panels.items() if r['cahier'] == 19}
    old_record = load(OLD)
    out = {}
    for method, local in [('ruptures_identiques', False), ('alignement_local', True)]:
        data = texts('panneaux', local)
        for criterion, pool in [('prose_et_legende', original), ('catalogue_complet', set(panels))]:
            key = method+'/'+criterion
            out[key] = {label: summarize(pool & subset, data)
                        for label, subset in [('Q19', q19), ('Q15_Q19', set(panels))]}
        if not local:
            for label, bucket in [('Q19', 'comparaison_cahier_19'), ('Q15_Q19', 'comparaison_tous_panneaux')]:
                old = old_record[bucket]
                replay = out[method+'/prose_et_legende'][label]
                assert replay['positions_par_face'] == {p: old_record['positions_par_panneau'].get(p, 0) for p in old['panneaux']}
                assert replay['faces_avec_une_forme'] == old['avec_un_mot']
                assert replay['paires_positives'] == old['paires_atteignant_deux']
                assert replay['paires_du_catalogue'] == old['paires_possibles']
                fields = old['tirage_parmi_places']
                assert (replay['positions'], replay['occurrences'], replay['probabilite_exacte']) == (
                    fields['positions'], fields['occurrences'], fields['proportion_deux_faces'])
                assert sorted(replay['positions_par_face'][p] for p in TARGETS) == fields['places_cibles']
    rows = []
    for page, entries in sorted(data.items()):
        for word, loc, section, ranks in entries:
            if word in WORDS:
                rows.append(dict(face=page, ligne=loc, mot=word, rangs_ligne=ranks))
    result = dict(cibles=TARGETS, comparaisons=out, occurrences_alignement_local=rows)
    (HERE/'CORRECTION-BAIES.json').write_text(json.dumps(result, ensure_ascii=False, indent=1)+'\n')


if __name__ == '__main__':
    main()
