"""Vérification indépendante avec coupures explicites et témoins à réponse connue."""
from itertools import combinations, product
import gzip
import json
from lire import HERE, A, B, PROSE, titles, plain, signs, solve, indices, evaluate

def split_table(seq, word, max_width, initial):
    for cuts in combinations(range(1,len(word)),len(seq)-1):
        bounds = (0,*cuts,len(word))
        chunks = [word[a:b] for a,b in zip(bounds,bounds[1:])]
        if max_width and any(len(c)>max_width for c in chunks):
            continue
        table = initial | dict(zip(seq,chunks))
        if all(table[s]==v for s,v in initial.items()) and [table[s] for s in seq]==chunks:
            yield table

def explicit(a,b,rev,width,null):
    x,y,z = (signs(w,True,rev) for w in (A,B,PROSE))
    xp,yp = (tuple(s for s in seq if s!=null) for seq in (x,y))
    for first in split_table(xp,a,width,{null:''} if null else {}):
        for both in split_table(yp,b,width,first):
            yield ''.join(both[s] for s in z)

def main():
    key = dict(o='a',p='v',k='t',ch='b',e='c',r='d')
    names = [''.join(key[s] for s in signs(f,True,False)) for f in (A,B)]
    pred = ''.join(key[s] for s in signs(PROSE,True,False))
    learned = solve([tuple(names)],True,False,1,False)[tuple(names)]
    assert list(learned)==[pred] and learned[pred]['n']==1
    rows = [{'A':names[0], 'B':names[1], 'prose':learned}]
    chapters = {names[0]:['ut','x'+pred], names[1]:['tu',pred,'et']}
    def check(doc):
        return evaluate(rows,{1:indices(doc,1)},{t:t for t in doc})[0]
    unique = check(chapters)
    assert unique['retenue_dans_sa_notice'] and list(unique['lieux'])==[names[1]]
    collision = check(chapters|{'temoin':[pred]})
    assert len(collision['lieux'])==2
    source = [plain(w) for w in titles()]
    # Deux chaînes ont la même première et les mêmes quatre dernières UNITÉS.
    # Une valeur non vide pour chaque unité impose un préfixe et un suffixe
    # communs. Écarter d'avance les paires dont les bords ne satisfont pas cela.
    candidates = [{(a,b) for a,b in product(source,repeat=2) if a!=b
                   and (a[:4]==b[:4] and a[-1:]==b[-1:] if rev else
                        a[:1]==b[:1] and a[-4:]==b[-4:])} for rev in (False,True)]
    archived = json.loads(gzip.decompress((HERE/'MACER-PREDICTIONS.json.gz').read_bytes()))
    checked = {}
    for rev,pairs in zip((False,True),candidates):
        for width in (2,None):
            calculated = {(a,b,p) for a,b in pairs for p in explicit(a,b,rev,width,None)}
            name = 'banc/'+('inverse' if rev else 'direct')+'/'+str(width or 'libre')+'/0'
            stored = {(r['A'],r['B'],p) for r in archived[name] if r['A']!=r['B'] for p in r['prose']}
            assert calculated==stored
            checked[name] = {'paires_apres_condition_sur_les_bords':len(pairs),'resultats':sorted(calculated)}
    for a,b in [('cassiafistula','cassialignea'),('aristologialonga','aristologiarotunda')]:
        for null in (None,'o','ch','p','k'):
            found = set(explicit(a,b,True,None,null))
            learned = solve([(a,b)],True,True,None,null is not None).get((a,b),{})
            assert found <= set(learned)
            if null is None:
                assert found==set(learned)
    result={'deux_chiffres':names,'mot_reserve':pred,'localisation_unique':unique,
            'contre_exemple_non_unique':collision,'macer_sans_muet':checked}
    (HERE/'CONTROLES.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
