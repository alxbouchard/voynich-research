"""Ajuster trois modèles sur les seules légendes des fragments, et geler leurs lectures."""
from collections import Counter, defaultdict
import csv
from functools import cache
import gzip
import hashlib
from itertools import permutations
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RESEARCH/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import MODES, corpus, sequence, units

TABLE = RESEARCH/'2026-11-18-paires-ingredients/rangees/rangees.tsv'
MODELES = {
    'latin_deux_mots': (('nasturcium','ortulanum'),('nasturcium','aquaticum')),
    'qualificatifs': (('ortulanum',),('aquaticum',)),
    'allemand': (('gartenkresz',),('brunkresz',))
}
LATIN=('nasturcium','ortulanum','aquaticum','domesticum','et','agreste')
TARGETS={'latin_deux_mots':LATIN,'qualificatifs':LATIN,'allemand':('kresz','gartenkresz','brunkresz')}


def save(name, obj):
    raw=(json.dumps(obj,ensure_ascii=False,separators=(',',':'),sort_keys=True)+'\n').encode()
    (HERE/name).write_bytes(gzip.compress(raw,mtime=0) if name.endswith('.gz') else raw)


def load(name):
    p=HERE/name
    return json.loads(gzip.decompress(p.read_bytes()) if name.endswith('.gz') else p.read_bytes())


def registre():
    editions,_=corpus()
    assert hashlib.sha256(TABLE.read_bytes()).hexdigest()=='584a27515c49c4c2cb4a527c0c54c30c02f7a34893001cdeeb1e047514afc5a4'
    rows=[]
    for row in csv.DictReader(TABLE.open(),delimiter='\t'):
        items=[]
        for group in row['fragments'].split(','):
            locs=[row['page']+'.'+n for n in group.split('+')]
            views=[]
            for ed in editions.values():
                assert all(ed[loc][1]=='Lf' for loc in locs)
                for cut in MODES:
                    views.append(tuple(w for loc in locs for _,w in sequence(ed[loc][3],cut)))
            unique=len(set(views))==1 and len(views[0])>0 and all(re.fullmatch('[a-z]+',w) for w in views[0])
            items.append({'id':'+'.join(locs),'mots':views[0] if unique else None,'lectures':views})
        rows.append({'page':row['page'],'rang':int(row['rang']),'fragments':items})
    return rows


def solve(equations,max_letters=3):
    """Dictionnaire constant et non nécessairement injectif, avec frontières des mots fixes."""
    def extend(tokens, target, key, pos=0):
        if not tokens:
            if pos==len(target): yield key
            return
        sign=tokens[0]; remaining=tokens[1:]; known=key.get(sign)
        if known is not None:
            if target.startswith(known,pos):
                yield from extend(remaining,target,key,pos+len(known))
            return
        left=len(target)-pos
        for size in range(max(1,left-max_letters*len(remaining)),min(max_letters,left-len(remaining))+1):
            val=target[pos:pos+size]
            yield from extend(remaining,target,{**key,sign:val},pos+size)
    def run(pos,key):
        if pos==len(equations):
            yield tuple(sorted(key.items()))
        else:
            syms,text=equations[pos]
            if len(syms)<=len(text)<=len(syms)*max_letters:
                for new in extend(syms,text,key): yield from run(pos+1,new)
    return run(0,{})


def canon(word):
    return units(word,False)


def equations(a,b,model,direction):
    p,q=MODELES[model]
    if direction=='inverse':p,q=q,p
    if len(a)!=len(p) or len(b)!=len(q):return None
    if model=='latin_deux_mots' and a[0]!=b[0]:return None
    return tuple((canon(word),goal) for fs,gs in ((a,p),(b,q)) for word,goal in zip(fs,gs))


def readbacks(key,word):
    pairs=tuple(sorted(key.items()))
    @cache
    def visit(i):
        if i==len(word):return [()]
        return [(s,*tail) for s,text in pairs if word.startswith(text,i) for tail in visit(i+len(text))]
    return sorted({''.join(t) for t in visit(0) if canon(''.join(t))==t})


def fit():
    rows=registre(); save('REGISTRE.json.gz',rows)
    adj=[]; items={}; owner={}
    for row in rows:
        for f in row['fragments']:
            if f['mots']:
                items[f['id']]=f['mots'];owner[f['id']]=row['page']
        adj.extend((a['id'],b['id']) for a,b in zip(row['fragments'],row['fragments'][1:]))
    valid=[(a,b) for a,b in adj if a in items and b in items]
    undirected={frozenset((a,b)) for a,b in adj}
    result={}; fallback={}
    for model in MODELES:
        for direction in ('direct','inverse'):
            name=model+'_'+direction; stored=defaultdict(list); patterns=0
            for a,b in valid:
                eq=equations(items[a],items[b],model,direction)
                if eq is None:continue
                patterns+=1
                for key in solve(eq):
                    stored[key].append({'gauche':a,'droite':b,'panneau':owner[a]})
            tables=[]
            for pairs,places in sorted(stored.items()):
                key=dict(pairs)
                tables.append({'table':key,'origines':places,'max':max(map(len,key.values())),
                               'injective':len(set(key.values()))==len(key),
                               'formes_predites':{goal:readbacks(key,goal) for goal in TARGETS[model]}})
            result[name]={'structure_admise':patterns,'tables':tables}
            if tables:continue
            # Sensibilité existentielle. Une paire non voisine n'est pas une origine de tables confirmatoires.
            matches=[]; structural=0
            occupied=list(items)
            for ia,a in enumerate(occupied):
                for b in occupied[ia+1:]:
                    if frozenset((a,b)) in undirected:continue
                    eq=equations(items[a],items[b],model,direction)
                    if eq is None:continue
                    structural+=1
                    first=next(solve(eq),None)
                    if first:matches.append({'gauche':a,'droite':b,'meme_panneau':owner[a]==owner[b],'exemple_table':dict(first)})
            fallback[name]={'structure_admise':structural,'paires':matches}
    save('PREDICTIONS.json.gz',{'couverture':{'rangees':len(rows),'panneaux':len({r['page'] for r in rows}),
         'fragments':sum(len(r['fragments']) for r in rows),'lectures_concordantes':len(items),
         'paires_adjacentes':len(adj),'paires_adjacentes_lisibles':len(valid)},'modeles':result,
         'non_voisines_si_absence':fallback,'cible_double':['nasturcium','aquaticum'],
         'controle_ligne':['nasturcium','domesticum','et','agreste']})


if __name__=='__main__':
    fit()
