"""Chercher des finales propres identiques dans des mots distincts sur quatre panneaux."""
from collections import Counter, defaultdict
from functools import cache
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]/'2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, tokens

MONTHS = {
    'mars': ['f70v2'], 'avril': ['f70v1', 'f71r'], 'mai': ['f71v','f72r1'],
    'juin': ['f72r2'], 'juillet': ['f72r3'], 'août': ['f72v3'],
    'septembre': ['f72v2'], 'octobre': ['f72v1'], 'novembre': ['f73r'], 'décembre': ['f73v'],
}
PANELS = tuple(p for pages in MONTHS.values() for p in pages)
FALL = PANELS[-4:]
MODES = tuple(product(('H','ZL'), ('joints','separes')))
KINDS = ('Lz', 'Cc')


@cache
def units(word):
    return tuple(re.findall(r'c[kptf]h|ch|sh|.', word))


def known(word):
    return re.fullmatch(r'[a-z]+', word) is not None


def harvest(editions, modes, kind, align):
    forms = {p: defaultdict(list) for p in PANELS}
    counts = {p: Counter() for p in PANELS}
    loci = {ed: [loc for loc, (p, k, _, _) in data.items() if p in PANELS and k == kind]
            for ed, data in editions.items()}
    assert loci['H'] == loci['ZL']
    for loc in loci['H']:
        p = loc.split('.')[0]
        seqs = [tokens(editions[ed][loc][3], cut) for ed,cut in modes]
        freqs = [Counter(w for w in s if known(w)) for s in seqs]
        shared = freqs[0].copy()
        for f in freqs[1:]:
            shared &= f
        fixed = Counter()
        for group in zip(*seqs):
            if len(set(group)) == 1 and known(group[0]):
                fixed[group[0]] += 1
        assert not (fixed - shared)
        chosen = fixed if align else shared
        counts[p].update(loci=1, occurrences_min_locus=sum(shared.values()),
                         occurrences_fixes=sum(fixed.values()),
                         couples_locus_mot_sans_un_seul_rang_commun=len(shared.keys()-fixed.keys()),
                         occurrences_analysees=sum(chosen.values()))
        for word in chosen:
            forms[p][word].append({'locus':loc, 'occurrences_min':chosen[word],
                                   'rangs':{'/'.join(m):[j for j,x in enumerate(seq,1) if x==word]
                                            for m,seq in zip(modes,seqs)}})
    return forms, counts


def suffix_map(words):
    index = defaultdict(set)
    for w in words:
        seq = units(w)
        for start in range(1,len(seq)):
            index[seq[start:]].add(w)
    return index


def pick_distinct(choices, selected=()):
    if len(selected) == len(choices):
        return selected
    for word in sorted(choices[len(selected)] - set(selected)):
        witness = pick_distinct(choices, (*selected, word))
        if witness is not None:
            return witness
    return None


def matches(groups, indices):
    found = {}
    for tail in set.intersection(*(set(indices[p]) for p in groups)):
        alternatives = [indices[p][tail] for p in groups]
        witness = pick_distinct(alternatives)
        if witness:
            found[tail] = {'attribution':dict(zip(groups,witness)),
                           'formes_par_panneau':{p: sorted(ws) for p,ws in zip(groups,alternatives)}}
    return found


def score(matches_):
    sizes = Counter(len(t) for t in matches_)
    return {'longueur_max':max(sizes,default=0), 'n_finales_3':sizes[3], 'par_longueur':dict(sorted(sizes.items()))}


def show(found):
    return [{'unites': list(tail), **val} for tail,val in sorted(found.items(), key=lambda p:(-len(p[0]),p[0]))]


def benchmark(target, trials):
    maximum = Counter(t['longueur_max'] for t in trials)
    three = Counter(t['n_finales_3'] for t in trials)
    return {'n_lots':len(trials), 'au_moins_aussi_long':sum(n for x,n in maximum.items() if x >= target['longueur_max']),
            'au_moins_autant_de_finales_3':sum(n for x,n in three.items() if x >= target['n_finales_3']),
            'histogramme_longueur_max':dict(sorted(maximum.items())), 'histogramme_nombre_de_finales_3':dict(sorted(three.items()))}


def run(editions, modes, kind, align=False, extended=False):
    forms, counts = harvest(editions,modes,kind,align)
    index = {p:suffix_map(forms[p]) for p in PANELS}
    autumn = matches(FALL, index)
    result = {'inventaire':{p:dict(counts[p],formes_distinctes=len(forms[p])) for p in PANELS},
              'automne':{'scores':score(autumn),'finales':show(autumn)}}
    if not extended:
        return result
    scores = {ps:score(matches(ps,index)) for ps in combinations(PANELS,4)}
    full_panels = {ps[0] for ps in MONTHS.values() if len(ps) == 1}
    trios = [tail for tail in matches(FALL[:3],index) if len(tail)==3]
    result.update({
        'occurrences':forms,
        'lots_temoin':{name:benchmark(score(autumn), [s for ps,s in scores.items() if population.issuperset(ps)])
                       for name,population in [('douze_panneaux',set(PANELS)),('huit_mois_non_doubles',full_panels)]},
        'tous_les_lots':[dict(panneaux=ps,**s) for ps,s in scores.items()],
        'neuf_fenetres_panneaux':[dict(panneaux=PANELS[i:i+4],**scores[PANELS[i:i+4]]) for i in range(len(PANELS)-3)],
        'trois_puis_un':{'finales_sur_trois':[list(x) for x in sorted(trios)], 'par_quatrieme':{
            p: [list(t) for t in sorted(matches(FALL[:3]+(p,),index)) if len(t)==3]
            for p in PANELS if p not in FALL[:3]}},
    })
    monthly = {m:suffix_map(set.intersection(*(set(forms[p]) for p in panels))) for m,panels in MONTHS.items()}
    months = tuple(MONTHS)
    result['sept_fenetres_mois'] = [dict(mois=months[i:i+4], **score(matches(months[i:i+4],monthly)))
                                      for i in range(len(months)-3)]
    return result


def controls():
    assert units('chshckhcthcphcfh') == ('ch','sh','ckh','cth','cph','cfh')
    panels = ('A','B','C','D')
    idx = {p:suffix_map([prefix+'chyoy']) for p,prefix in zip(panels,'abcd')}
    assert score(matches(panels,idx))['longueur_max']==4
    identical = {p:suffix_map(['okeey']) for p in panels}
    assert not matches(panels,identical)
    assert pick_distinct([{'a'},{'a'},{'b','c'},{'c','d'}]) is None
    assert 'c' not in suffix_map(['ch'])
    assert ('ch',) not in suffix_map(['ch'])
    assert pick_distinct([{'a','b'},{'a'},{'c','d'},{'c'}]) == ('b','a','d','c')


def main():
    controls()
    editions, sections = corpus()
    assert {p for p,s in sections.items() if s=='Z'} == set(PANELS)
    results = {}
    for kind in KINDS:
        strict = run(editions, MODES, kind, extended=True)
        assert strict['lots_temoin']['douze_panneaux']['n_lots'] == 495
        assert strict['lots_temoin']['huit_mois_non_doubles']['n_lots'] == 70
        results[kind] = {'principal':strict, 'meme_rang':run(editions,MODES,kind,True,True),
                         'editions_et_blancs':{'/'.join(m):run(editions,[m],kind) for m in MODES}}
    (HERE/'resultats.json').write_text(json.dumps(results,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')


if __name__=='__main__':
    main()
