"""Vérifier les fins de paragraphe et les variantes initiales enregistrées."""
from collections import Counter, defaultdict
from pathlib import Path
import json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'deux-lignes'))
from prolonger import line,corpus,metadata
SOURCE={'f82v.36','f103v.36','f108r.20','f116r.17'}
ANCIENS={17,76,82,103,108,116}

def main():
    ed,_=corpus();meta=metadata()
    sig={};st=defaultdict(Counter);allcases={}; backgrounds=defaultdict(Counter)
    ordres={key:defaultdict(list) for key in ed}
    for key,table in ed.items():
        for loc,(page,kind,_,_) in table.items():ordres[key][page].append(loc)
    for loc,(page,kind,_,_) in ed['H'].items():
        if kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0':continue
        leaf=int(re.match(r'f(\d+)',page)[1])
        words=line(ed,meta,loc)
        flags={key:'<$>' in table[loc][3] for key,table in ed.items()}
        if loc in SOURCE:
            then={}
            for key,table in ed.items():
                order=ordres[key][page]
                later=order[order.index(loc)+1:]
                onward=next((k for k in later if table[k][1]=='P0'),None)
                then[key]={'fin':flags[key],'prochaine_P0':onward,
                           'prochaine_debut':None if not onward else '<%>' in table[onward][3],
                           'loci_interposes':later[:later.index(onward)] if onward else later}
            sig[loc]=then
        if len(words)>=3:
            st[page]['lignes']+=1
            st[page]['fin_accord']+=all(flags.values())
            st[page]['divergence']+=len(set(flags.values()))>1
            v=backgrounds[page];v['n']+=1;v['cibles']+=words[2] in ('qokeedy','qokeey')
        if len(words)>=2 and words[0] in ('dain','daiin','sain','saiin') and words[1] in ('chey','shey'):
            allcases[loc]={'mots':words[:3],'neuf':leaf not in ANCIENS,'fin':flags}
    affected={k.split('.')[0] for k,x in allcases.items() if x['neuf']}
    affected_leaves={re.match(r'f\d+',p)[0] for p in affected}
    def total(keys):return dict(sum((backgrounds[k] for k in keys),Counter()))
    results={'quatre_lignes':sig,'fonds_sur_les_quatre_faces':{k.split('.')[0]:st[k.split('.')[0]] for k in SOURCE},
             'familles':allcases,'fond_faces_de_reserve_avec_candidat':total(affected),
             'fond_feuillets_de_reserve_avec_candidat':total(k for k in backgrounds if re.match(r'f\d+',k)[0] in affected_leaves)}
    (HERE/'RESULTATS.json').write_text(json.dumps(results,sort_keys=True,ensure_ascii=False,indent=1)+'\n')
    print(sig);print(allcases);print(results['fond_feuillets_de_reserve_avec_candidat'])
if __name__=='__main__':main()
