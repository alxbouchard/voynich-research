"""Dépouillement de la terminaison retenue après la comparaison des douze panneaux."""
from collections import Counter, defaultdict
from itertools import combinations
import importlib.util
from pathlib import Path
import json
from comparer import FALL, MODES, PANELS, corpus, known, matches, run, suffix_map, tokens, units

HERE = Path(__file__).resolve().parent
TAIL = tuple('eody')


def category(page, kind):
    if page in PANELS:
        if kind in ('Lz', 'Cc'):
            return kind+('_automne' if page in FALL else '_autres_panneaux')
        return 'autre_locus_du_zodiaque'
    if kind.startswith('L'):
        return 'legendes_hors_zodiaque'
    return 'prose_P0' if kind == 'P0' else 'autres_hors_zodiaque'


def retrieve(editions, modes):
    loci = set.intersection(*(set(editions[e]) for e,_ in modes))
    counts, words = defaultdict(Counter), defaultdict(lambda:defaultdict(list))
    for loc in sorted(loci):
        lines = [editions[e][loc] for e,_ in modes]
        p, kind = lines[0][:2]
        if any(line[:2] != (p,kind) for line in lines):
            continue
        key = category(p,kind)
        counts[key]['loci'] += 1
        shared = None
        for ed, cut in modes:
            seq = tokens(editions[ed][loc][3],cut)
            freq = Counter(w for w in seq if known(w) and len(units(w)) > len(TAIL))
            shared = freq if shared is None else shared & freq
        for word, n in shared.items():
            counts[key]['groupes'] += n
            if units(word)[-len(TAIL):] == TAIL:
                counts[key]['avec_finale'] += n
                words[key][word].append([loc,kind,n])
    return {k:dict(inventaire=dict(v), formes=words[k]) for k,v in sorted(counts.items())}


def endings_only():
    """Un désaccord dans le début du mot n'invalide pas une finale lisible."""
    parser_path = HERE.parents[1]/'2026-11-18-nombres-et-reperes/vocabulaire/comparer.py'
    spec = importlib.util.spec_from_file_location('parse_zodiac_ivtff',parser_path)
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    versions = {}
    for ed,cut in MODES:
        name = 'IT2a-n.txt' if ed=='H' else 'ZL3b-n.txt'
        rows = parser.parse(parser.DATA/name,cut=='separes')
        versions[ed,cut] = {loc:variants for series in rows.values() for loc,variants in series}
    all_loci = set.intersection(*(set(v) for v in versions.values()))
    assert len(all_loci)==299
    robust, partial = {}, {}
    for loc in sorted(all_loci):
        evidence = {}
        tests = []
        for m, variant_map in versions.items():
            readings = []
            for seq in sorted(variant_map[loc]):
                matches_here = [''.join(w) for w in seq if len(w)>len(TAIL) and w[-len(TAIL):]==TAIL]
                readings.append(matches_here)
            evidence['/'.join(m)] = readings
            tests.extend(bool(ws) for ws in readings)
        if all(tests):
            robust[loc] = evidence
        elif any(tests):
            partial[loc] = evidence
    return {'meme_finale_toutes_lectures_et_alternatives':robust,
            'au_moins_une_lecture_mais_des_desaccords':partial}


def audit_primary(results):
    """Théorème de Hall, contrôle indépendant des affectations quatre à quatre."""
    for kind in ('Lz','Cc'):
        prim = results[kind]['principal']
        index = {p:suffix_map(prim['occurrences'][p]) for p in PANELS}
        for row in prim['tous_les_lots']:
            panels = row['panneaux']
            expected = Counter()
            for t in set.intersection(*(set(index[p]) for p in panels)):
                ok = all(len(set.union(*(index[p][t] for p in subset)))>=n
                         for n in range(1,5) for subset in combinations(panels,n))
                if ok:
                    expected[str(len(t))] += 1
            assert dict(expected)==row['par_longueur']
    return True


def main():
    source = json.loads((HERE/'resultats.json').read_text())
    assert audit_primary(source)
    editions,_ = corpus()
    primary = retrieve(editions, MODES)
    readings = {}
    single_edition_lots = {}
    for m in MODES:
        obs = retrieve(editions,[m])
        result = run(editions,[m],'Lz',extended=True)
        single_edition_lots['/'.join(m)] = result['lots_temoin']['douze_panneaux']
        readings['/'.join(m)] = {k:v for k,v in obs.items() if k.startswith('Lz')}
    idx={p:suffix_map(words) for p,words in source['Lz']['principal']['occurrences'].items()}
    train = matches(FALL[:3],idx)
    out = {'accord':primary,'lectures_individuelles':readings, 'lots_par_edition':single_edition_lots,
           'transfer_longueur_quatre_apres_examen':{
               'finales_apprentissage':sorted(''.join(k) for k in train if len(k)>=4),
               'destination':{p:sorted(''.join(k) for k in matches(FALL[:3]+(p,),idx) if len(k)>=4)
                              for p in PANELS if p not in FALL[:3]}},
           'controle_495_quadruplets_par_theoreme_de_Hall':True,
           'finale_sans_exiger_egalite_du_mot_entier':endings_only()}
    (HERE/'ailleurs.json').write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main()
