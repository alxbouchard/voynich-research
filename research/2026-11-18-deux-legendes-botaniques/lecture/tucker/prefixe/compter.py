"""Dénombrer les préfixes pouvant émettre ātl dans les légendes, au même locus."""
from collections import Counter
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[3]
sys.path.insert(0,str(RESEARCH/'2026-11-18-opcheor-paralleles/variantes'))
from compter import SIMPLE, corpus, segment
from transfert import labels, tokens

KINDS = {'Lf','Ls','Lz','Lc','Lt','Ln'}
POTS = [tuple('f89r2.'+str(n) for n in (29,30)), tuple('f102r2.'+str(n) for n in (13,14,15)),
        tuple('f102v2.'+str(n) for n in (1,2))]
POT_KEY = {loc: '+'.join(group) for group in POTS for loc in group}

def inventory(rows, cut, regroup):
    fragments=labels(rows,cut)
    out={'Lf':fragments} | {k:{} for k in KINDS-{'Lf'}}
    for locus,(page,kind,_,raw) in rows.items():
        if kind not in KINDS-{'Lf'}:
            continue
        words=tokens(raw,cut)
        if regroup and page=='f75v' and kind=='Ln' and 18<=int(locus.split('.')[1])<=37:
            pos=int(locus.split('.')[1])
            key=f'f75v.{pos-pos%2}+f75v.{pos-pos%2+1}'
            out[kind][key]=out[kind].get(key,())+words
        elif regroup and kind=='Lc' and locus in POT_KEY:
            key=POT_KEY[locus]
            out[kind][key]=out[kind].get(key,())+words
        else:
            out[kind][locus]=words
    return out

def summary(views, kind, allowed=lambda l:True):
    loci=sorted(l for l in set.union(*(set(v[kind]) for v in views)) if allowed(l))
    categories=Counter()
    retained={}
    for loc in loci:
        readings=[v[kind].get(loc) for v in views]
        if readings[0] is None or len(readings[0])!=1 or len(set(readings))!=1:
            continue
        w=readings[0][0]
        if not SIMPLE.fullmatch(w):
            continue
        start=segment(w)[:2]
        group=''.join(start) if start in [('o','k'),('o','t')] else 'autre'
        categories[group]+=1
        retained[loc]=w
    return {'brut':len(loci),'admissibles':len(retained),'ok':categories['ok'],'ot':categories['ot'],
            'ok_ou_ot':categories['ok']+categories['ot'],'mots_par_locus':retained}

def main():
    editions,_=corpus()
    def views(group):
        return [inventory(rows,cut,group) for rows in editions.values() for cut in ('joints','separes')]
    individual=views(False); grouped=views(True)
    out={'par_code':{s:summary(grouped,s) for s in sorted(KINDS)},
         'Ln_un_locus_par_ligne_sans_reunir_les_paires_de_f75v':summary(individual,'Ln'),
         'Lc_un_locus_par_ligne':summary(individual,'Lc'),
         'Ls_sur_les_deux_ciels_f68r1_et_f68r2':summary(grouped,'Ls',lambda l:l.split('.')[0] in ('f68r1','f68r2'))}
    assert out['par_code']['Lz']['brut']==299
    assert all(tuple(segment('ockheor')[:2])!=s for s in [('o','k'),('o','t')])
    for k,s in out['par_code'].items():
        print(k,s['brut'],s['admissibles'],s['ok'],s['ot'],s['ok_ou_ot'])
    (HERE/'resultats.json').write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=1)+'\n')
if __name__=='__main__':
    main()
