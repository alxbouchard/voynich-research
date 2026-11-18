"""Isoler la première autre légende op de réserve, sans ouvrir d’image."""
from pathlib import Path
import json
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from combiner import DATA, FILES, ROW, HERE

def order(loc):
    m=re.fullmatch(r'f(\d+)([rv])(\d*)\.(\d+)',loc)
    return int(m[1]),m[2],int(m[3] or 0),int(m[4])

def main():
    rows={}
    for ed,filename in FILES.items():
        for line in (DATA/filename).read_text().splitlines():
            m=ROW.match(line)
            if not m:continue
            loc,page,leaf,kind,raw=m.groups()
            if kind!='Lz' or not 70<=int(leaf)<=73:continue
            raw=re.sub(r'<![^>]*>|<[%$]>|!','',raw).strip('.')
            rows.setdefault(loc,{})[ed]=raw
    def common(v):
        if len(v)!=2 or len(set(v.values()))!=1:return None
        word=next(iter(v.values()))
        return word if re.fullmatch(r'[a-z]+',word) else None
    collective={k:common(v) for k,v in rows.items()}
    panel=[f'f72v2.{i}' for i in range(21,33)]
    others=sorted([k for k in rows if order(k)[0]!=72],key=order)
    local=[k for k in panel if k!='f72v2.24' and (collective[k] or '').startswith('op')]
    other=[k for k in others if (collective[k] or '').startswith('op')]
    selected=(local or other)[:1]
    result={'voisins':{k:rows[k] for k in panel[2:5]},'mots_concordants_anneau':sum(collective[k] is not None for k in panel),
            'lieux_autres_feuillets':len(others),'lisibles_autres_feuillets':sum(collective[k] is not None for k in others),
            'autres_op_dans_anneau':local,'autres_op_hors_feuillet':[(k,collective[k]) for k in other],
            'cible':[(k,collective[k]) for k in selected]}
    (HERE/'sans-etoile/CIBLE.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')
    print(result)

if __name__=='__main__':main()
