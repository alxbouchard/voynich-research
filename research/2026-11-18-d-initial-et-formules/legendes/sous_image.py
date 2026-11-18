"""Annoncer un ou deux mots après shedy sur f84r.15, à partir des autres faces."""
from collections import Counter
import argparse
import json
from comparer import HERE, metadata, prose, save

KEY='f84r.15/1/3'


def training():
    groups=prose()
    meta=metadata()
    held=groups['sous_image']
    matched=[(run,i) for run in held for i,(key,_,_) in enumerate(run) if key==KEY]
    assert len(matched)==1
    run,i=matched[0]
    # L'annonce n'a accès qu'au contexte à gauche, et le reste de 84 r/v est exclu.
    masks=run[:i+1]
    subsets={'autres_bains':[],'autres_H2_B':[],'autres_P0':[]}
    for runs in groups.values():
        for row in runs:
            page=row[0][0].split('.')[0]
            if page in ('f84r','f84v'):continue
            info=meta.get(page,{})
            subsets['autres_P0'].append(row)
            if info.get('I')=='B':subsets['autres_bains'].append(row)
            if info.get('H')=='2' and info.get('L')=='B':subsets['autres_H2_B'].append(row)
    return masks,subsets


def words(run,mode):
    return [ 'shedy' if mode=='d_initial' and w=='dshedy' and first else w for k,w,first in run]


def guess(context,src,size):
    counts=Counter()
    for seq in src:
        for j in range(len(context),len(seq)-size+1):
            if not context or seq[j-len(context):j]==context:
                counts[tuple(seq[j:j+size])]+=1
    if not counts:return None
    n=max(counts.values())
    winners=sorted(s for s,c in counts.items() if c==n)
    return {'contexte':context, 'observations':sum(counts.values()),'votes_premier':n,'premier':list(winners[0]),
            'ex_aequo':[list(w) for w in winners]}


def announce():
    masked,subset=training()
    res={}
    for mode in ('exact','d_initial'):
        ctx=words(masked,mode)[-3:]
        for group,runs in subset.items():
            src=[words(run,mode) for run in runs]
            for n in (1,2):
                choices=[guess(ctx[len(ctx)-length:],src,n) for length in range(len(ctx),0,-1)]
                res[f'{group}/{mode}/{n}']={'longueur_maximale':len(ctx),'principal':next((r for r in choices if r),None),
                                           'ancre_seule':choices[-1], 'sans_contexte':guess([],src,n)}
    save('VOISIN-ANNONCES.json',res)


def verify():
    data=json.loads((HERE/'VOISIN-ANNONCES.json').read_bytes())
    _,groups=training()
    for run in prose()['sous_image']:
        for i,(k,word,_) in enumerate(run):
            if k==KEY:
                right=run[i+1:i+3]
                score={}
                for key,methods in data.items():
                    n=int(key.rsplit('/',1)[1])
                    out=words(right,key.split('/')[1])[:n]
                    score[key]={m:r['premier']==out if len(out)==n and r else None
                                for m,r in methods.items() if m!='longueur_maximale'}
                save('VOISIN-RESULTATS.json',{'ancre':k,'ouverture':right,'scores':score})
                return
    raise ValueError(KEY)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('annoncer','verifier'))
    if p.parse_args().mode=='annoncer':announce()
    else:verify()
