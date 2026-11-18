"""Substitutions d’une unité p/k dans les étiquettes entières concordantes."""
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'2026-11-18-opcheor-paralleles/variantes/panneaux'))
from verifier import MODES, admissible_labels, corpus, labels, segment

def rank(loc):
    m=re.fullmatch(r'f(\d+)([rv])(\d*)\.(\d+)(?:\+.+)?',loc)
    return (int(m[1]),m[2]=='v',int(m[3] or 0),int(m[4]))

def pair_order(row):
    return (-len(segment(row['mot_p'])),*sorted([rank(row['lieu_p']),rank(row['lieu_k'])]))

def main():
    editions,_=corpus()
    books=[labels(editions[e],c) for e,c in MODES]
    all_locs=set.union(*(set(b) for b in books))
    reserve=sorted({l.split('.')[0] for l in all_locs if rank(l)[0] not in (89,100)})
    items={l:w for page in reserve for l,w in admissible_labels(books,page).items()}
    by_word=defaultdict(list)
    for l,w in sorted(items.items(),key=lambda kv:rank(kv[0])):
        by_word[segment(w)].append(l)
    out=[]
    for a,locs in by_word.items():
        if len(a)<3:
            continue
        for i,s in enumerate(a):
            if s!='p':continue
            b=(*a[:i],'k',*a[i+1:])
            for l,m in product(locs,by_word.get(b,[])):
                out.append({'mot_p':''.join(a),'lieu_p':l,'mot_k':''.join(b),'lieu_k':m,'position_changee':i+1})
    eligible=sorted((r for r in out if rank(r['lieu_p'])[0]!=rank(r['lieu_k'])[0]),key=pair_order)
    within=sorted((r for r in out if rank(r['lieu_p'])[0]==rank(r['lieu_k'])[0]),key=pair_order)
    eligible_locs={l for r in eligible for l in (r['lieu_p'],r['lieu_k'])}
    cross_count=0
    equal_length=0
    direct_matches=[]
    for (l,a),(m,b) in combinations(items.items(),2):
        if rank(l)[0]==rank(m)[0]:
            continue
        cross_count+=1
        x,y=segment(a),segment(b)
        if len(x)!=len(y) or len(x)<3:
            continue
        equal_length+=1
        differences=[{u,v} for u,v in zip(x,y) if u!=v]
        if differences==[{'p','k'}]:
            direct_matches.append(frozenset((l,m)))
    assert set(direct_matches)=={frozenset((r['lieu_p'],r['lieu_k'])) for r in eligible}
    result={'comparaisons_inter_feuillets':cross_count,'comparaisons_inter_de_meme_longueur_admissible':equal_length,
            'panneaux':reserve,'tous_lieux_lf_en_reserve':len([l for l in all_locs if rank(l)[0] not in (89,100)]),
            'loci_accord':len(items),'formes_distinctes':len(by_word),'formes_k_et_p':{
                s:{''.join(w):locs for w,locs in by_word.items() if s in w and len(w)>=3} for s in ('k','p')},
            'couples_inter_feuillets':eligible,'couples_meme_feuillet':within,'lieux_impliques':len(eligible_locs),
            'nombre_couples_de_formes':len({(r['mot_p'],r['mot_k']) for r in eligible}),
            'selection':eligible[0] if eligible else None,'inventaire':items}
    (HERE/'resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')
    print('loci',len(items),'formes',len(by_word),'couples',len(eligible),'memes',len(within),'p',len(result['formes_k_et_p']['p']),'k',len(result['formes_k_et_p']['k']),'choix',result['selection'])
if __name__=='__main__':
    main()
