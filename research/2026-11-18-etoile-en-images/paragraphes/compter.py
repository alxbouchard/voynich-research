"""Positions dans les lignes d'ouverture, avec un tirage conditionné par face."""
from collections import Counter, defaultdict
from fractions import Fraction
import csv
import hashlib
import json
from math import comb
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent))
from predire import corpus, tokens, certain, langage

UNITS = re.compile('c[ktpf]h|[cs]h|[a-z]')


def shape(word):
    u = UNITS.findall(word)
    return len(u)==4 and u[0]==u[2]=='o' and len(set(u))==3


def hyper(initial, other, n):
    denom = comb(initial+other,n)
    return {k:Fraction(comb(initial,k)*comb(other,n-k),denom)
            for k in range(max(0,n-other), min(n,initial)+1)}


def pooled(rows, word, subset):
    dist = {0:Fraction(1)}
    expected = Fraction(0)
    observed = 0
    counts = {}
    for face,rec in rows.items():
        opening,inside = rec[subset][True], rec[subset][False]
        a,b = opening.total(), inside.total()
        hits,remaining = opening[word],inside[word]
        n=hits+remaining
        counts[face]=[a,b,hits,remaining]
        if not n:
            continue
        observed+=hits
        expected+=Fraction(n*a,a+b)
        new=defaultdict(Fraction)
        for count,prob in hyper(a,b,n).items():
            for prior,mass in dist.items():
                new[count+prior]+=prob*mass
        dist=dict(new)
    assert sum(dist.values())==1
    p=sum(v for k,v in dist.items() if k>=observed)
    return {'par_face':counts,'total':[sum(x[j] for x in counts.values()) for j in range(4)],
            'esperance':str(expected),'esperance_decimale':float(expected),'p_exact':str(p),'p':float(p),
            'distribution':{k:str(p) for k,p in dist.items()}}


def census(data, faces, cut):
    rows = {f:{g:{b:Counter() for b in [True,False]} for g in ['tous','silhouette']} for f in faces}
    rejected = {f:0 for f in faces}
    hits=[]
    lines={f:Counter() for f in faces}
    for loc,(f,typ,_,raw) in data.items():
        if f not in rows or typ!='P0':
            continue
        leading=re.sub(r'<![^>]*>|!|\s+','',raw)
        opening=leading.startswith('<%>')
        assert ('<%>' in leading)==opening,(loc,leading)
        lines[f]['ouvertures' if opening else 'autres']+=1
        for i,w in enumerate(tokens(raw,cut),1):
            if not certain(w):
                rejected[f]+=1
                continue
            rows[f]['tous'][opening][w]+=1
            if shape(w):
                rows[f]['silhouette'][opening][w]+=1
            if w=='otor':
                hits.append({'lieu':loc,'mot':i,'ouverture':opening})
    score={g:pooled(rows,'otor',g) for g in ('tous','silhouette')}
    freqs=Counter()
    for face in rows.values():
        for counts in face['silhouette'].values():
            freqs.update(counts)
    comparators={}
    for w,n in sorted(freqs.items()):
        if freqs['otor'] <= 2*n and n <= 2*freqs['otor']:
            out=pooled(rows,w,'silhouette')
            comparators[w]={k:out[k] for k in ('total','p_exact','p')}
    return {'positions_otor':hits,'lignes_par_face':lines,'positions_illisibles':rejected,**score,
            'comparateurs':comparators, 'au_moins_aussi_rare':sum(Fraction(r['p_exact']) <= Fraction(score['silhouette']['p_exact']) for r in comparators.values())}


def main():
    editions,_=corpus()
    zl=(langage.DATA/'ZL3b-n.txt').read_text()
    faces=[m[1] for m in re.finditer(r'^<(f(?:10[3-9]|11[0-9])[rv])>[^\n]*\$Q=T\b',zl,re.M)]
    assert 'f103r' in faces and 'f116r' in faces and len(faces)==len(set(faces))
    result={'description_colonnes':['positions sur lignes initiales','positions sur autres lignes',
                                     'occurrences sur lignes initiales','occurrences sur autres lignes'],
            'sha256_protocole':hashlib.sha256((HERE/'PROTOCOLE.md').read_bytes()).hexdigest(),
            'sha256_sources':langage.HASH,'faces':faces,'mesures':{}}
    for ed,data in editions.items():
        for cut in ('joints','separes'):
            result['mesures'][ed+'_'+cut]=census(data,faces,cut)
    with (HERE/'PAR_FACE.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t',lineterminator='\n')
        writer.writerow(['edition_espaces','population','face','positions_ouverture','positions_autres',
                         'part_positions_ouverture','otor_ouverture','otor_autres'])
        for variant,measures in result['mesures'].items():
            for population in ('tous','silhouette'):
                for f,(a,b,c,d) in measures[population]['par_face'].items():
                    writer.writerow([variant,population,f,a,b,str(Fraction(a,a+b)) if a+b else '',c,d])
    (HERE/'RESULTATS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
