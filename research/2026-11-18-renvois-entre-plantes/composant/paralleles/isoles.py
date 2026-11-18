"""Conserver les possibilités où l'on ajuste un seul côté sans imposer l'autre."""
from collections import Counter, defaultdict
from paralleles import LANG, FORMS, HERE, MODES, candidates, code, load, save


def main():
    source=load(HERE/'TABLES.json.gz')
    patterns=source['candidats']
    all_sites=defaultdict(lambda:defaultdict(set))
    fits={}
    cross_check=Counter(couples_de_tables_evalues=0,affectations_fonctionnelles=0,solutions_injectives=0)
    for mode in MODES:
        shapes=[code(w,mode) for w in FORMS]
        for mute in [None,*sorted(set(sum(shapes,())))]:
            sides={}
            for side,sh in [('gauche',shapes[:2]),('droite',shapes[2:])]:
                tables=candidates(sh,patterns,mute)
                sides[side]=tables
                for i,_ in tables:
                    all_sites[patterns[i]['ouvrage']][side].add(i)
            fits[mode+'/'+(mute or 'aucun')]=sides
            # Vérification par produit cartésien direct, sans la table d'index des clés partagées.
            for i,left in sides['gauche']:
                a=patterns[i]['ouvrage']
                for j,right in sides['droite']:
                    b=patterns[j]['ouvrage']
                    if i==j or LANG[a]!=LANG[b]:continue
                    cross_check['couples_de_tables_evalues']+=1
                    assignments=set(left.items()) | set(right.items())
                    if len({k for k,v in assignments})!=len(assignments):continue
                    cross_check['affectations_fonctionnelles']+=1
                    if len({v for k,v in assignments})==len(assignments):
                        cross_check['solutions_injectives']+=1
    distinct={b:{s:sorted(all_sites[b][s]) for s in ('gauche','droite')} for b in source['effectifs']}
    assert cross_check['solutions_injectives']==len(source['solutions'])
    save(HERE/'ISOLES.json.gz',dict(lieux_distincts=distinct,toutes_les_tables=fits,
                                    verification_exhaustive=dict(cross_check)))


if __name__=='__main__':
    main()
