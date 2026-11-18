"""Appliquer les équivalents publiés, sans inventer la valeur des signes hors de la table."""
from itertools import product
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE=Path(__file__).resolve().parent
STUDY=HERE.parents[1]
ROOT=STUDY.parents[1]
sys.path.insert(0,str(STUDY.parent/'2026-11-18-formes-souterraines/nom/second'))
from transfert import tokens

def unmarked(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))

def read(word, table, reverse=False):
    units=re.findall(r'c[ptfk]h|ch|sh|iin|in|.',word)
    if reverse:
        units.reverse()
    alphabet=list(dict.fromkeys(units))
    result=set()
    for subset in product(*(table.get(s,['['+s+']']) for s in alphabet)):
        mapping=dict(zip(alphabet,subset))
        result.add(''.join(mapping[s] for s in units))
    return sorted(result)

def main():
    source=json.loads((STUDY/'histoire/table.json').read_text())
    table={s:r['valeurs'] for r in source['lignes_table_p141'] for s in r['eva']}
    examples={}
    for word,forms in [('okcheor',['ātlmaāe']),('otols',['ātlācân']),
                       ('opololaiin',['āguācaācaoll','āhuācaācaoll']),('otoly',['ātlācai'])]:
        options=read(word,table)
        assert all(unmarked(f) in {unmarked(x) for x in options} for f in forms)
        examples[word]={'formes_comparees_2019':forms,'lecture_table_2018':options,
                        'toutes_exactes':all(f in options for f in forms)}
    # Pour 100v n°6, le dessin donné par les auteurs laisse une question
    # d'alignement. La translittération propre à la page 2019 reste dans table.json.
    selected={'f89r2.5','f100v.10','f89r2.22','f100v.16','f96r.1'}
    panels={}
    for edition in ('IT2a-n','ZL3b-n'):
        for text in (ROOT/'voynich_20261028/data'/f'{edition}.txt').read_text().splitlines():
            m=re.fullmatch(r'<([^,>]+),[^>]+>\s*(.*)',text)
            if m and m[1] in selected:
                for split in ('joints','separes'):
                    words=tokens(m[2],split)
                    panels.setdefault(m[1],{})[edition+'/'+split]=[
                        {'eva':word,'sorties':read(word,table)} for word in words]
    assert set(panels)==selected
    out={'controles':examples,'lignes':panels}
    (HERE/'PASSAGES.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
    words=[r['eva'] for r in panels['f100v.16']['IT2a-n/joints']]
    assert words==[r['eva'] for r in panels['f100v.16']['ZL3b-n/joints']]
    planned={mode:[{'eva':word,'formes_sans_diacritiques':sorted({unmarked(o) for o in read(word,table,rev)})}
                   for word in words] for mode,rev in [('lecture_publiee',False),('ordre_des_signes_inverse',True)]}
    (HERE/'MOTS-A-VERIFIER.json').write_text(json.dumps(planned,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
