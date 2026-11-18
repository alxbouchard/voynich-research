"""Apprentissage sur un bifeuillet, évaluation sur trois bifeuillets réservés."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import json
import re

ICI=Path(__file__).resolve().parent
DEPOT=ICI.parents[2]
BIFEUILLETS={'f75v':'75/84','f84r':'75/84','f77r':'77/82','f77v':'77/82','f82r':'77/82','f82v':'77/82','f83v':'76/83','f80r':'79/80'}
CLASSES=['C','N']


def joindre(lot):
    cotation=json.loads((ICI/'COTATION.json').read_text())['objets']
    objets=[r for r in cotation if r['lot']==lot and r['geste'] in CLASSES]
    debuts={r['objet'].split('+')[0] for r in objets}
    lectures=defaultdict(list)
    for nom in ['IT2a-n','ZL3b-n']:
        for line in (DEPOT/'voynich_20261028/data'/(nom+'.txt')).read_text().splitlines():
            ident,sep,body=line.partition('>')
            locus=ident.removeprefix('<').split(',')[0]
            if locus not in debuts or not sep or ',!' in ident:continue
            propre=re.sub(r'<![^>]*>|<[%$]>|!', '',body.strip()).replace('<->','.').replace('<~>','.')
            for virg in ['','.']:
                champs=[v for v in propre.replace(',',virg).split('.') if v]
                lectures[locus].append(champs[0] if champs else '')
    result=[]
    for r in objets:
        forms=lectures[r['objet'].split('+')[0]]
        assert len(forms)==4
        w=forms[0] if len(set(forms))==1 and re.fullmatch('[a-z]+',forms[0]) else None
        result.append({'objet':r['objet'],'face':r['face'],'bifeuillet':BIFEUILLETS[r['face']],'geste':r['geste'],
                       'quatre_lectures':forms,'mot':w,'unite':re.match(r'c[ktpf]h|[cs]h|.',w)[0] if w else None})
    return result


def ajuster():
    cas=joindre('apprentissage');valid=[r for r in cas if r['mot']]
    totals=Counter(r['geste'] for r in valid)
    methodes={}
    for critere in ['unite','mot']:
        freqs={}
        for val in sorted({r[critere] for r in valid}):
            counts=Counter(r['geste'] for r in valid if r[critere]==val)
            score=Fraction(counts['C'],totals['C'])-Fraction(counts['N'],totals['N']) if all(totals[c] for c in CLASSES) else 0
            freqs[val]={'C':counts['C'],'N':counts['N'],'difference':str(score)}
        candidats=[k for k,v in freqs.items() if min(totals['C'],totals['N'])>=2 and v['C']>=2 and Fraction(v['difference'])>0]
        candidats.sort(key=lambda k:(-Fraction(freqs[k]['difference']),-freqs[k]['C'],k))
        methodes[critere]={'candidat':candidats[0] if candidats else None,'table':freqs}
    return {'cas':cas,'denominateurs':totals,'regles':methodes}


def bilan(cas,critere,cand):
    groupes=sorted({r['face'] for r in cas});tables={}
    distrib={0:Fraction(1)};quantite=0
    for f in groupes:
        rows=[r for r in cas if r['face']==f and r['mot']];q={}
        for c in CLASSES:
            cat=[r for r in rows if r['geste']==c];q[c]={'oui':sum(r[critere]==cand for r in cat),'n':len(cat)}
        tables[f]=q
        nc,nn=q['C']['n'],q['N']['n'];h=q['C']['oui']+q['N']['oui']
        if not (nc and nn):continue
        quantite+=q['C']['oui']
        chances={k:Fraction(comb(nc,k)*comb(nn,h-k),comb(nc+nn,h)) for k in range(max(0,h-nn),min(h,nc)+1)}
        temp=defaultdict(Fraction)
        for a,pa in distrib.items():
            for b,pb in chances.items():temp[a+b]+=pa*pb
        distrib=temp
    tot={c:{k:sum(s[c][k] for s in tables.values()) for k in ['oui','n']} for c in CLASSES}
    diff=Fraction(tot['C']['oui'],tot['C']['n'])-Fraction(tot['N']['oui'],tot['N']['n']) if all(tot[c]['n'] for c in CLASSES) else None
    return {'candidat':cand,'faces':tables,'denominateurs':tot,'difference':str(diff),'faces_deux_gestes':sum(bool(t['C']['n'] and t['N']['n']) for t in tables.values()),
            'distribution':{str(k):str(v) for k,v in sorted(distrib.items())},'p_unilateral':str(sum(v for k,v in distrib.items() if k>=quantite))}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('etape',choices=['apprendre','verifier']);args=p.parse_args()
    if args.etape=='apprendre':
        out=ajuster()
    else:
        f=ICI/'PREDICTION.json'
        formule=json.loads(f.read_text())
        assert formule==ajuster(),'Le calcul de la prédiction a changé.'
        cas=joindre('reserve')
        out={'sha256_prediction':sha256(f.read_bytes()).hexdigest(),'cas':cas,
             'tests':{cr:bilan(cas,cr,o['candidat']) if o['candidat'] else None for cr,o in formule['regles'].items()}}
    print(json.dumps(out,ensure_ascii=False,indent=1))
