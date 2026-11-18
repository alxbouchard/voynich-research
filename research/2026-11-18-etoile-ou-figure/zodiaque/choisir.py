"""Retenir la première paire de la même couronne sans consulter les dessins."""
from collections import defaultdict
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
REPO=RESEARCH.parent
ORDER='f70v1 f71r f71v f72r1 f72r2 f72r3 f72v3 f72v2 f72v1 f73r f73v'.split()


def pairs():
    inventory=json.loads((RESEARCH/'2026-11-18-mois-automne/cle/INVENTAIRE.json').read_text())['panneaux']
    grove=json.loads((RESEARCH/'2026-11-18-mois-automne/finales/grove-index.json').read_text())['loci']
    lines=(REPO/'voynich_20261028/data/IT2a-n.txt').read_text().splitlines()
    result=[]
    for page in ORDER:
        h=defaultdict(list)
        for line in lines:
            m=re.match(r'^<('+page+r'\.\d+),.Lz>\s*(.*)',line)
            if m:
                h[re.sub(r'<[^>]*>|!','',m[2]).strip()].append(m[1])
        loc=inventory[page]['Lz']['loci']
        eligible={}
        for word,positions in h.items():
            if len(positions)!=1 or loc.get(positions[0],{}).get('utilisables')!=[word]: continue
            g=[k for k,v in grove[page].items() if v==word and '.S' in k]
            if len(g)==1:
                eligible[word]={'locus':positions[0],'grove':g[0],'mot':word}
        cases=[]
        for t,v in eligible.items():
            if not t.startswith('ot') or len(t)<3: continue
            k='ok'+t[2:]
            if k not in eligible: continue
            other=eligible[k]
            if v['grove'].split('.')[1]!=other['grove'].split('.')[1]: continue
            key=sorted(int(x['locus'].split('.')[1]) for x in (v,other))
            cases.append((key,{'t':v,'k':other}))
        result.extend(case for _,case in sorted(cases,key=lambda r:r[0]))
    return result

if __name__=='__main__':
    p=pairs()
    print(p[:1],len(p))
    (HERE/'CIBLE.json').write_text(json.dumps({'paire_retenue':p[:1], 'toutes':p},ensure_ascii=False,indent=1)+'\n')
