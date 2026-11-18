"""Recenser les deux formes dans la prose accompagnant des rangées végétales."""
from collections import Counter, defaultdict
from itertools import combinations
from fractions import Fraction
from math import comb
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, parse, MODES, metadata


def main():
    ed, _ = corpus()
    meta = metadata()
    targets = {"ctheor","ctheol"}
    by_page = defaultdict(set)
    for locus,(page,kind,_,_) in ed["H"].items():
        if locus in ed["ZL"] and ed["ZL"][locus][1] == kind:
            by_page[page].add(kind)
    panels = {p for p,kinds in by_page.items() if {"P0","Lf"} <= kinds}
    test = {p for p in panels if not re.match(r'f(99|100)[rv]',p)}
    cov = Counter()
    counts = defaultdict(Counter)
    sizes = Counter()
    events = []
    for loc,(page,kind,_,_) in ed["H"].items():
        if kind != "P0" or page not in panels or loc not in ed["ZL"] or ed["ZL"][loc][1] != kind: continue
        views = [parse(ed[e][loc][3], mode)[1] for e,mode in MODES]
        lengths = [sum(map(len,v)) for v in views]
        for r in aligned(ed,loc,page,'P',page,cov):
            local = list(map(int,r['rangs_quatre'].split('/')))
            ranks = [n+sum(map(len,v[:r['troncon']-1])) for n,v in zip(local,views)]
            sizes[page] += 1
            samples = ["tous"]
            if page in test: samples.append("test_sans_f99_f100")
            for sample in samples:
                for k in ['toutes_longueurs']+(['10_mots_dans_les_4_lectures'] if set(lengths)=={10} else []):
                    bucket=counts[sample+'/'+k]
                    bucket['places_lisibles']+=1
                    for pos in (1,5):bucket[f'places_rang_{pos}']+=int(set(ranks)=={pos})
                    if r['mot'] in targets:
                        bucket[r['mot']]+=1
                        for pos in (1,5):bucket[f'{r["mot"]}_rang_{pos}']+=int(set(ranks)=={pos})
            if r['mot'] in targets:
                events.append({"page":page,"lieu":loc,"mot":r['mot'],"rangs_ligne":ranks,"longueurs_ligne":lengths})
    q = meta['f99r']['Q']
    known = {'f99r','f100r'}
    hit = {r['page'] for r in events}
    def null(pool):
        pairs=list(combinations(sorted(pool),2))
        # Hypothèse descriptive alternative : autant de reprises, déplacées aux places
        # lisibles du même lot. Le nombre de mots lisibles par face reste inchangé.
        total=sum(sizes[p] for p in pool)
        m=sum(r["page"] in pool for r in events)
        a,b=(sizes[p] for p in sorted(known))
        share=1-Fraction(comb(total-a,m)+comb(total-b,m)-comb(total-a-b,m),comb(total,m))
        return {"tirage_parmi_places": {"positions":total,"occurrences":m,"places_cibles":[a,b],
                                         "proportion_deux_faces":[share.numerator,share.denominator]},
                "panneaux":sorted(pool),"avec_un_mot":sorted(pool&hit),"paires_atteignant_deux":sum(a in hit and b in hit for a,b in pairs),"paires_possibles":len(pairs)}
    labels = {}
    for loc in ('f99r.46','f100r.2'):
        labels[loc] = {e:ed[e][loc][3] for e in ed}
    out = dict(positions_par_panneau=sizes,etiquettes=labels,cas=events,mesures=counts,
               panneau_deux_sur_deux=known<=hit,comparaison_tous_panneaux=null(panels),
               comparaison_cahier_19=null({p for p in panels if meta[p]['Q']==q}),
               test_hors_deux_feuillets=sorted(test))
    (HERE/'PANNEAUX.json').write_text(json.dumps(out,indent=1,sort_keys=True,ensure_ascii=False)+'\n')
    for k in ('cas','mesures','comparaison_tous_panneaux','comparaison_cahier_19','test_hors_deux_feuillets'): print(k,out[k])


if __name__=='__main__':
    main()
