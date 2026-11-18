"""Tester les graphies annoncées sur les lieux choisis indépendamment des mots."""
from collections import Counter,defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import langage
TARGETS=('opchy','ocphy','opches')
ROW = re.compile(r'^<([^,>]+)\.(\d+),(.)([A-Za-z0-9]+)>\s*(.*)$')


def compatible(word):
    current=word.replace('{','').replace('}','')
    chunks=re.split(r'(\[[^\]]*\])',current)
    groups=[x[1:-1].split(':') if x.startswith('[') else [x] for x in chunks]
    out=set()
    for choice in product(*groups):
        raw=''.join(choice)
        if all(x not in raw for x in ('?', '*')):
            if raw in TARGETS:
                out.add(raw)
        else:
            bits=re.split(r'(\?\?\?|\?|\*)',raw)
            pattern=''.join('.+' if x=='???' else '.' if x in ('?','*') else re.escape(x) for x in bits)
            out.update(w for w in TARGETS if re.fullmatch(pattern,w))
    return sorted(out)


def search(faces):
    res={}
    for ed,stem in langage.EDITIONS.items():
        source=(langage.DATA/(stem+'-n.txt')).read_bytes()
        assert sha256(source).hexdigest()==langage.HASH[ed]
        for split in langage.SPLITS:
            groups={f:defaultdict(Counter) for f in faces}
            hits=defaultdict(list)
            all_hits=defaultdict(list)
            for line in source.decode().splitlines():
                m=ROW.match(line)
                if not m or m[3]=='!':
                    continue
                face,n,_,kind,raw=m.groups()
                raw=re.sub(r'<![^>]*>|<[%$]>|!', '',raw)
                raw=re.sub(r'<[-~]>', '.',raw).replace(',','.' if split=='separes' else '')
                for i,w in enumerate(filter(None,raw.split('.')),1):
                    w=w.replace('{','').replace('}','')
                    loc=f'{face}.{n}/{i}'
                    if w in TARGETS:
                        all_hits[w].append([loc,kind])
                    if face not in faces:
                        continue
                    counter=groups[face][kind]
                    counter['positions']+=1
                    allowed=compatible(w)
                    if w in TARGETS:
                        counter[w]+=1
                    if allowed:
                        hits[face].append({'loc':loc,'type':kind,'lu':w,'compatible':allowed,'certain':w in TARGETS})
            res[ed+'_'+split]={'emplacements_des_cibles':groups,'rencontres_cibles':hits,'toutes_occurrences_certaines':all_hits}
    return res


if __name__=='__main__':
    target=json.loads((HERE/'lieux.json').read_text())
    (HERE/'resultats.json').write_text(json.dumps(search(target['faces']),indent=1,ensure_ascii=False,sort_keys=True)+'\n')
