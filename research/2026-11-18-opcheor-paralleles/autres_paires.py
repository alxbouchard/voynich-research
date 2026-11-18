"""Appliquer sans réviser les correspondances de la lecture herba herbae tam."""
import json
import re
from chercher import HERE, corpus, tables

def units(word):
    return tuple(re.findall(r'c[kptf]h|ch|sh|[a-z]', word))

def extensions(blocks, clear, mapping):
    keys = [mapping]
    silent = {s for s, val in mapping.items() if val == ''}
    for word, target in zip(blocks, clear):
        seq = tuple(s for s in word if s not in silent)
        keys = [more for key in keys for more in tables(seq,target,2,key)]
        if not keys:
            break
    return keys

def display(seq, key):
    return ''.join(key.get(s, '['+s+']') for s in seq)

def check_site(words, pair_at, key, docs):
    codes = list(map(units,words))
    projected = [display(seq,key) for seq in codes]
    readings = []
    for chapter, text in docs.items():
        for i in range(len(text)-1):
            pair_maps = extensions(codes[pair_at:pair_at+2], text[i:i+2], key)
            if not pair_maps:
                continue
            start = i-pair_at
            available = 0 <= start and start+len(words) <= len(text)
            works = [extended for fitted in pair_maps for extended in
                     extensions(codes,text[start:start+len(words)],fitted)] if available else []
            readings.append({'segment':chapter,'rang_de_la_paire':i+1,'deux_mots':text[i:i+2],
                             'valeurs_ajoutees_pour_la_paire':[
                                 {s:v for s,v in m.items() if s not in key} for m in pair_maps],
                             'voisinage_conserve':available,'tables_sur_contexte':len(works)})
    return {'mots':words,'projection':projected,'voisinages_historiques':readings}

def main():
    docs = corpus('latin')
    train = ['opcheor','opcheol','shody']
    candidates = []
    for silent in sorted(set().union(*(units(w) for w in train))):
        candidates.extend(extensions(list(map(units,train)),['herba','herbae','tam'],{silent:''}))
    assert len(candidates)==3
    out = []
    for key in candidates:
        assert display(units('sholdy'),key)=='taeam'
        out.append({'table':key,'f100v.16':check_site(['ches','okeor','okeol','dy'],1,key,docs),
                    'f96r.1':check_site(['cpheol','cpheor','chodar'],0,key,docs)})
    (HERE/'AUTRES-PAIRES.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
