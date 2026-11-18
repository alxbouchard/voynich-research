"""Éprouver le motif d'étoiles sur deux roues au moyen des cotations sans texte."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
PREV=HERE.parents[1]/'2026-11-18-etoile-en-images'
sys.path.insert(0,str(PREV))
from predire import corpus,tokens
from evaluer_rayons import radial


def read(p):return json.loads((PREV/p).read_text())


def solo(words):return [w if re.fullmatch('[a-z]+',w) else None for w in words]


def concordant(views):
    if len({len(v) for v in views})!=1:return None
    return [r[0] if len(set(r))==1 else None for r in zip(*views)]


def rates(words,stars):
    counts={s:[0,0] for s in (1,2)}; literal=constant=known=0
    for seq,s in zip(words,stars):
        if seq is None:continue
        x=sum('ot' in w for w in seq if w); n=sum(w is not None for w in seq)
        counts[s][0]+=x; counts[s][1]+=n
        if all(seq):known+=1;constant+=s==2;literal+=x==s
    diff=Fraction(*counts[2])-Fraction(*counts[1]) if all(c[1] for c in counts.values()) else None
    return counts,diff,dict(inscriptions_entierement_lisibles=known,compte_ot_exact=literal,toujours_deux=constant)


def main():
    ed,_=corpus()
    forms={(e,cut):{loc:solo(tokens(row[3],cut)) for loc,row in rows.items() if row[:2]==('f67r1','Ri')}
           for e,rows in ed.items() for cut in ('joints','separes')}
    locs=sorted(next(iter(forms.values())),key=lambda s:int(s.partition('.')[2]));assert len(locs)==12
    src={name+'_'+cut:table for (name,cut),table in forms.items()}
    src['accord']={loc:concordant([d[loc] for d in forms.values()]) for loc in locs}
    key=read('reperes/cle.json')['cards']; votes=[read(f'vote-radial-{v}.json') for v in ('I','II')]
    groups={}
    for relation in ('locus','alternative_locus'):
        gold={}
        for label,r in key.items():
            if not label.startswith('A'):continue
            v={v['A'][label] for v in votes};assert len(v)==1
            gold[r[relation]]=v.pop()
        assert set(gold)==set(locs)
        stars=[gold[l] for l in locs]; groups[relation]={}
        for view,rows in src.items():
            words=[rows[l] for l in locs];counts,diff,checks=rates(words,stars)
            rotation=[rates(words,stars[i:]+stars[:i])[1] for i in range(12)]
            groups[relation][view]=dict(mots_par_astre=counts,difference=str(diff),
               rotations_au_moins=sum(x>=diff for x in rotation if x is not None),rotations=len(rotation),**checks,
               lignes=[dict(lieu=l,etoiles=gold[l],mots=rows[l]) for l in locs])
    # Recalcul par les votes et les lectures brutes du test ancien sur f68v2.
    former=radial();stored=read('RESULTATS-RAYONS.json');assert json.loads(json.dumps(former))==stored
    result=dict(f67r1=groups,f68v2=former['B_exposition_tous_les_groupes'],
                empreintes={k:sha256((PREV/k).read_bytes()).hexdigest() for k in ['vote-radial-I.json','vote-radial-II.json','reperes/cle.json']})
    (HERE/'RESULTATS.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':main()
