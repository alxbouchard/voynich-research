"""Prolonger chaque clé sur les seuls feuillets pairs avant de prédire le pluriel."""
from collections import Counter
from functools import reduce
from operator import and_
from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'cle'))
from chercher import alphabet, corpus, encode, fit, freeze, macer, runs, segment, tables

TARGET='radicis'
RESERVED='radices'

def manuscript():
    editions,sections=corpus()
    records=[]
    for loc,(page,kind,_,_) in editions['ZL'].items():
        number=int(re.match(r'f(\d+)',page)[1]) if re.match(r'f\d',page) else None
        if kind!='P0' or sections.get(page)!='H' or number in (11,15) or loc not in editions['H'] or editions['H'][loc][1]!='P0':
            continue
        views=[]
        for rows in editions.values():
            raw=re.sub(r'\{[^}]*\}','?',rows[loc][3])
            for spacing in ('joints','separes'):
                pairs=Counter()
                for run in runs(raw,spacing):
                    words=[segment(w) for _,w in run]
                    pairs.update(zip(words,words[1:]))
                views.append(pairs)
        records.append((number,loc,reduce(and_,views)))
    data=json.loads((HERE.parent/'cle/voynich.json').read_bytes())['modeles']['2']['details']
    seed=[row['tables_possibles'] for row in data if [row[k] for k in ('A','M','B','graphie')]==['chol','cthy','daiin','foliis']]
    assert len(seed)==2 and seed[0]==seed[1] and len(seed[0])==6
    assert all('c' not in ''.join(key.values()) for key in seed[0])
    return records,seed[0],segment('cthy')

def challenge():
    # Seul le générateur connaît l'alphabet. Aucune valeur de cette
    # permutation n'est passée à la routine d'apprentissage ou de transfert.
    plaintext=macer()
    encoder=alphabet((),220812)
    encrypted=[]
    for num,(title,chapter) in enumerate(plaintext.items(),1):
        if title=='Chelidonia':continue
        for v,words in chapter.items():
            coded=[encode(w,(),encoder) for w in words]
            encrypted.append((num,f'{title}#{v}',Counter(zip(coded,coded[1:]))))
    return encrypted,[encode(w,(),encoder) for w in ('radix','eius','foliis')]

def keydata(key):
    return dict(sorted(key.items()))

def study(records,keys,middle):
    domains={};accepted={}
    for parity,part in ((0,'genitif'),(1,'pluriel')):
        rows=[row for row in records if row[0]%2==parity]
        allpairs=sum(sum(v.values()) for num,loc,v in rows)
        probes=[];n_tokens=0
        for num,loc,v in rows:
            for pair,count in v.items():
                anchor,pick=pair if parity==0 else pair[::-1]
                if anchor!=middle:continue
                probes.append((num,loc,pick,count));n_tokens+=count
        candidates=keys if parity==0 else list(accepted.values())
        counttests=Counter()
        details=[];allhits=[]
        for num,loc,word,n in probes:
            hits=[];length=[];novel=[]
            for index,key in enumerate(candidates,1):
                unknown=set(word)-set(key)
                if len(unknown)>(1 if parity==0 else 0):continue
                novel.append(index)
                target=TARGET if parity==0 else RESERVED
                base=sum(len(key[x]) for x in word if x in key)
                missing=sum(x in unknown for x in word)
                if not (base+missing<=len(target)<=base+2*missing):continue
                length.append(index)
                counttests['compatible_longueur']+=1
                for extension in tables(word,target,2,key):
                    assert ''.join(extension[x] for x in middle)=='eius'
                    assert ''.join(extension[x] for x in word)==target
                    info={'cle_depart':index,'nouveau':{x:extension[x] for x in sorted(unknown)},'cle':keydata(extension)}
                    hits.append(info)
                    if parity==0:
                        accepted[freeze(extension)]=extension
            counttests['assez_de_valeurs_connues']+=len(novel)
            out={'unite':num,'ligne':loc,'voisin':''.join(word),'unites':word,'occurrences':n,
                 'au_plus_nouveaux_autorises':novel,'longueur_possible':length,'solutions':hits}
            details.append(out)
            if hits:allhits.append(out)
        domains[part]={'unites_terrain':len(set(num for num,_,_ in rows)),'lignes_terrain':len(rows),
                       'paires_stables_occurrences':allpairs,'occurrences_voisin':n_tokens,'lignes_voisin':len({r[1] for r in probes}),
                       'voisins_distincts':len({r[2] for r in probes}),'cles_entree':len(candidates),
                       'couples_cle_lieu_forme_avant_filtre':len(candidates)*len(probes),
                       'couples_etapes':dict(counttests),'lignes_avec_solution':sorted({d['ligne'] for d in allhits}),
                       'details':details}
    return {'genitif_et_pluriel':domains,'nouvelles_cles_distinctes':len(accepted)}

def main():
    actual,keys,m=manuscript()
    real=study(actual,keys,m)
    test,(a,p,b)=challenge()
    learned=[dict(key) for key in fit(a,p,b,'foliis',2)]
    assert len(learned)==1
    positive=study(test,learned,p)
    desc=positive['genitif_et_pluriel']
    assert 'Lilium#812' in desc['genitif']['lignes_avec_solution']
    assert 'Paratella#2008' in desc['pluriel']['lignes_avec_solution']
    both={'voynich':real,'macer_chiffre':positive,'graines_chiffrees':(a,p,b),'cles_controle_apprises':learned}
    (HERE/'resultats.json').write_text(json.dumps(both,ensure_ascii=False,indent=1)+'\n')
    for name,obj in [('Voynich',real),('Macer',positive)]:
        print(name,obj['nouvelles_cles_distinctes'])
        for part,d in obj['genitif_et_pluriel'].items():
            print(part,{k:v for k,v in d.items() if k!='details'})
            if name=='Voynich':
                print('mots',[(r['ligne'],r['voisin'],r['longueur_possible']) for r in d['details']])
if __name__=='__main__':main()
