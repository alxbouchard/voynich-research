"""Vérification sur toutes les légendes des registres illustrés, par rangée."""
import collections
import json
import re
import sys
from pathlib import Path
from compter import words

BANDS = {
    'f99r': [(2,14),(20,27),(33,40)],
    'f99v': [(2,9),(15,20),(26,31)],
    'f102v2': [(3,16)],
}

def score(name, path, split):
    per_face={};coverage={};details={}
    lines=path.read_text().splitlines()
    index={}
    for line in lines:
        m=re.match(r'^<([^.]+)\.(\d+),([@+])Lf>(.*)$',line)
        if m:
            index[m[1],int(m[2])] = m[3],re.sub(r'<![^>]*>','',m[4]).strip()
    for face, ranges in BANDS.items():
        labels={}
        for lo,hi in ranges:
            current=None
            for n in range(lo,hi+1):
                pos,raw=index[(face,n)]
                if pos=='@':
                    current=f'{face}.{n}'
                    labels[current]=set()
                assert current
                labels[current].update(words(raw,split))
        details[face]={n:sorted(v) for n,v in labels.items()}
        coverage[face]={'etiquettes':len(labels),'avec_mot_lisible':sum(bool(v) for v in labels.values())}
        per_face[face]=collections.Counter(w for group in labels.values() for w in group)
    return {'couverture':coverage,'texte':details,'candidats':{w:{f:c[w] for f,c in per_face.items()} for w,v in per_face['f99r'].items() if v>=2},'intersection_recto_verso':{w:{f:c[w] for f,c in per_face.items()} for w in sorted(per_face['f99r'].keys()&per_face['f99v'].keys())},'maxima':{f:max(c.values()) for f,c in per_face.items()}}

def main():
    root=Path(sys.argv[1])/'voynich_20261028/data'
    d={n+('_separe' if split else '_joint'):score(n,root/f,split) for n,f in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')] for split in [False,True]}
    print(json.dumps(d,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
