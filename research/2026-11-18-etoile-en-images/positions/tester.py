"""Distribution exacte si les occurrences d'une ligne changent de place entre positions admissibles."""
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from predire import corpus, tokens, langage, certain


def tests(rows, pages, cut):
    by_group = defaultdict(list)
    for loc,(page,kind,_,raw) in rows.items():
        if kind != 'P0' or page not in pages:
            continue
        seq = tokens(raw,cut)
        hits = [i for i,w in enumerate(seq) if w == 'otor']
        if not hits:
            continue
        q,subject = pages[page]
        group = 'decouverte' if q=='T' else 'ancre' if q=='I' else 'reserve'
        for mode in ('lisibles','motif'):
            eligible = []
            for i,w in enumerate(seq):
                if not certain(w):
                    continue
                s = langage.UNIT.findall(w)
                if mode=='lisibles' or (len(s)==4 and s[0]==s[2]=='o'):
                    eligible.append(i)
            for ensemble in (group,group+'_'+subject):
                by_group[ensemble,mode].append({'lieu':loc,'n':len(eligible),'k':len(hits),
                            'derniere':int(seq[-1]=='otor'),'taille_ligne':len(seq),
                            'deux_finales':sum(i>=len(seq)-2 for i in eligible),
                            'succes':sum(i>=len(seq)-2 for i in hits),'rangs':[i+1 for i in hits]})
    return {g:{mode:summarize(by_group[g,mode]) for mode in ('lisibles','motif')}
            for g in sorted({g for g,mode in by_group})}


def summarize(lines):
    dist = {0:Fraction(1)}
    for line in lines:
        n,t,k = line['n'],line['deux_finales'],line['k']
        assert k <= n
        new = defaultdict(Fraction)
        for j in range(max(0,k-n+t),min(k,t)+1):
            prob = Fraction(comb(t,j)*comb(n-t,k-j),comb(n,k))
            for total,p in dist.items():
                new[total+j] += p*prob
        dist = new
    assert sum(dist.values())==1
    obs = sum(row['succes'] for row in lines)
    return {'nombre_lignes':len(lines),'occurrences':sum(l['k'] for l in lines),'observe':obs,
            'derniere':sum(l['derniere'] for l in lines),'lignes_unique_emplacement':sum(l['n']==1 for l in lines),
            'attendu':float(sum(i*p for i,p in dist.items())),
            'p_superieure':float(sum(p for i,p in dist.items() if i>=obs)),'lignes':lines}


def main():
    ed,subjects = corpus()
    tags={}
    for raw in (langage.DATA/'ZL3b-n.txt').read_text().splitlines():
        m=re.match(r'^<([^.,>]+)>.*\$Q=(\w+)\b',raw)
        if m:
            tags[m[1]]=m[2],subjects[m[1]]
    result={edn:{cut:tests(rows,tags,cut) for cut in ('joints','separes')} for edn,rows in ed.items()}
    (HERE/'resultats.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
