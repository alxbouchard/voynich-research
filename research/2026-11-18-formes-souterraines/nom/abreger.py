"""Tester des expansions variables de signes et l’omission de lettres internes."""
from itertools import combinations
from pathlib import Path
import json
import sys

from lire import ALL, units

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-noms-secteurs/herbier'))
from mesurer import macer_source, words


def consistent(seq,parts):
    table=dict(zip(seq,parts))
    return table if all(table[u]==s for u,s in zip(seq,parts)) else None


def expanded(seq,name):
    for cuts in combinations(range(1,len(name)),len(seq)-1):
        borders=(0,*cuts,len(name))
        key=consistent(seq,[name[a:b] for a,b in zip(borders,borders[1:])])
        if key:
            return key
    return None


def contracted(seq,name):
    if len(name)<len(seq):
        return None
    for middle in combinations(range(1,len(name)-1),len(seq)-2):
        positions=(0,*middle,len(name)-1)
        key=consistent(seq,[name[i] for i in positions])
        if key:
            return {'positions':[i+1 for i in positions],'table':key}
    return None


def geometry(seq,name,reverse):
    # Opcheor a une seule répétition. Il suffit de laisser une lettre par signe,
    # puisque les signes extrêmes sont distincts et le signe répété touche un bord.
    n,k=len(name),len(seq)
    if n<k:
        return False
    if reverse:
        assert seq[1]==seq[-1] and len(set(seq))==k-1
        return name[-1] in name[1:n-k+2]
    assert seq[0]==seq[-2] and len(set(seq))==k-1
    return name[0] in name[k-2:-1]


def main():
    source=macer_source()
    titles=[(' '.join(words(title)),''.join(words(title))) for title,_ in source]
    assert len(titles)==77
    # A compound historical heading may contain several words. Preserve the
    # diplomatic normalized title for inspection, even when joining to test the form.
    tables={}
    for mode in ('unites','caracteres'):
        for reverse in (False,True):
            seq=units('opcheor',mode)
            if reverse:
                seq=seq[::-1]
            by_name={}
            for label,name in [(w,w) for w in ALL]+titles:
                full=expanded(seq,name)
                short=contracted(seq,name)
                assert bool(short)==geometry(seq,name,reverse)
                assert not full or short
                by_name[label]={'expansion_integrale':full,'avec_omissions':short}
            tables[mode+('_inverse' if reverse else '_direct')]={
                'unites_eva':seq,'formes_testees':{w:by_name[w] for w in ALL},
                'rubriques_integrales':[n for n,_ in titles if by_name[n]['expansion_integrale']],
                'rubriques_omissions':[n for n,_ in titles if by_name[n]['avec_omissions']],
                'solutions_temoins':{n:by_name[n] for n,_ in titles if by_name[n]['avec_omissions']}}
    (HERE/'contractions.json').write_text(json.dumps({'rubriques':titles,'comparaisons':tables},indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
