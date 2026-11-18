"""Mots entiers communs à des paragraphes associés à des rangs d'illustrations."""
import argparse
import json
import re
from pathlib import Path
from compter import words

BLOCKS = {
    'f99r': [(15,18),(28,31),(41,44),(47,52)],
    'f99v': [(10,13),(21,24),(32,35),(37,43)],
    'f102v2': [(17,23)],
}

def parse(path,split):
    loci={}
    for line in path.read_text().splitlines():
        m=re.match(r'^<([^.]+)\.(\d+),[@+]P0>(.*)$',line)
        if m:
            raw=re.sub(r'<![^>]*>','',m[3]).strip()
            # Preserve occurrence counts for transparent denominators.
            normalized=raw.replace('!', '').replace('<$>','').replace('<%>','').replace('<->','.').replace('<~>','.')
            tokens=[w for w in normalized.replace(',', '.' if split else '').split('.') if re.fullmatch('[a-z]+',w)]
            assert set(tokens)==set(words(raw,split))
            loci[m[1],int(m[2])]=tokens
    result={}
    for face,ranges in BLOCKS.items():
        for i,(lo,hi) in enumerate(ranges,1):
            tokens=[w for n in range(lo,hi+1) for w in loci[(face,n)]]
            result[f'{face}_{i}']=tokens
    return result

def evaluate(blocks):
    train=[set(blocks[f'f99r_{i}']) for i in [1,2,3]]
    test=[set(blocks[f'f99v_{i}']) for i in [1,2,3]]
    controls={x:set(blocks[x]) for x in ['f99r_4','f99v_4','f102v2_1']}
    candidates=sorted(set.intersection(*train))
    return {
        'mots_lisibles_par_bloc':{f:len(v) for f,v in blocks.items()},
        'candidats':{w:{'nombre_blocs_verso':sum(w in v for v in test),
                         'blocs_comparaison':[k for k,v in controls.items() if w in v]}
                     for w in candidates},
        'six_blocs':sorted(set.intersection(*train,*test)),
        'six_blocs_aucun_comparateur':sorted(set.intersection(*train,*test)-set.union(*controls.values()))
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('depot',type=Path)
    d=parser.parse_args().depot/'voynich_20261028/data'
    print(json.dumps({k+('_separe' if split else '_joint'):evaluate(parse(d/f,split)) for k,f in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')] for split in [False,True]},ensure_ascii=False,indent=2))
