"""Le mot de la page concurrente et les fins de ligne dans les autres pages de plantes."""
import json
import re
from collections import Counter
from comparer_fragments import HERE, MODES, PAIRS, corpus
from transfert import tokens


def main():
    eds,sections = corpus()
    output={}
    site_sets=[]
    for ed,cut in MODES:
        counts=Counter()
        occ=[]
        for loc,(page,kind,_,raw) in eds[ed].items():
            if sections.get(page)!='H' or page in PAIRS.values() or kind!='P0':
                continue
            ws=tokens(re.sub(r'\{[^}]*\}','?',raw),cut)
            counts['lignes']+=1
            for i,w in enumerate(ws):
                if not re.fullmatch('[a-z]+',w):
                    continue
                final=i==len(ws)-1
                groups=['tous']
                if w=='okam':
                    groups.append('okam')
                    occ.append({'lieu':loc,'rang':i+1,'emplacements':len(ws),'final':final})
                elif w.endswith('m'):
                    groups.append('autres_m')
                for g in groups:
                    counts[g+('_fin' if final else '_interne')]+=1
        site_sets.append({(r['lieu'],r['final']) for r in occ})
        output['/'.join((ed,cut))]={'comptes':counts,'occurrences':occ}
    output['concordance_lieu_et_position']=sorted(set.intersection(*site_sets))
    (HERE/'POSITION-OKAM.json').write_text(json.dumps(output,ensure_ascii=False,sort_keys=True,indent=1)+'\n')


if __name__=='__main__':
    main()
