"""Ouvrir le mot suivant sur les trois autres feuillets."""
from collections import Counter
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from combiner import segment
from suffixe import metadata

def main():
    # Les sections P0 du dernier cahier sont identifiées via Q=T.
    from corpus_dam import aligned, corpus
    ed,_=corpus()
    meta=metadata()
    result={}
    group={}
    for loc,(page,kind,_,_) in ed['H'].items():
        if meta.get(page,{}).get('Q')!='T' or kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0':
            continue
        rs=list(aligned(ed,loc,page,meta[page].get('I'),page,Counter()))
        for i,r in enumerate(rs):
            if r['mot'] not in ('dshedy','shedy'):continue
            idx=list(map(int,r['rangs_quatre'].split('/')))
            key=f"{loc}/{r['troncon']}/{idx[0]}"
            target=None
            if i+1<len(rs):
                a=rs[i+1]
                inds=list(map(int,a['rangs_quatre'].split('/')))
                if r['troncon']==a['troncon'] and all(x+1==y for x,y in zip(idx,inds)):
                    target=a['mot']
            group[key]=(r['mot'],target)
    for kind in ['dshedy','shedy']:
        cases={k:v for k,(w,v) in group.items() if w==kind}
        vals=[v for v in cases.values() if v is not None]
        result[kind]={'ouvertures':cases,'lisibles':len(vals),'exact':sum(v in ('tedy','qotedy') for v in vals),
                      'fin_tedy':sum(tuple(segment(v))[-4:]==tuple('tedy') for v in vals),
                      'fin_edy':sum(tuple(segment(v))[-3:]==tuple('edy') for v in vals),
                      'qokedy':vals.count('qokedy'),'shedy':vals.count('shedy')}
    (HERE/'RESULTATS.json').write_text(json.dumps(result,indent=1,sort_keys=True)+'\n')
    print({k:{key:v for key,v in r.items() if key!='ouvertures'} for k,r in result.items()})
    print(result['dshedy']['ouvertures'])

if __name__=='__main__':main()
