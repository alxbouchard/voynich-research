"""Appliquer la même recherche de textes clairs aux vers chiffrés et aux folios."""
from collections import Counter, defaultdict
import csv
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-carte-sept-etoiles/lecture'))
from essai import tables
sys.path.insert(0,str(RESEARCH/'2026-11-18-opcheor-paralleles/variantes'))
from compter import corpus, runs, segment

HIST = RESEARCH/'2026-11-18-opcheor-paralleles/latin'
ALTERNATIVES = ('foliis','foleis')
TARGETS = ('de','ed','in')

def save(name, value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=1)+'\n')

def windows(parts):
    """Deux mots contigus et, si lisible, leur voisin de gauche sur la même ligne."""
    bigrams=defaultdict(set)
    for part in parts:
        for i,(first,second) in enumerate(zip(part,part[1:])):
            prior=part[i-1] if i else None
            bigrams[first,second].add(prior)
    return bigrams

def consensus(views):
    pairs=set.intersection(*(set(view) for view in views))
    return {p:set.intersection(*(view[p] for view in views)) for p in sorted(pairs)}

def herb():
    editions,sections=corpus()
    pages=defaultdict(dict)
    for loc,(p,kind,_,_) in editions['ZL'].items():
        if kind!='P0' or sections.get(p)!='H' or loc not in editions['H'] or editions['H'][loc][1]!='P0':
            continue
        views=[]
        for ed in editions.values():
            raw=re.sub(r'\{[^}]*\}','?',ed[loc][3])
            for spacing in ('joints','separes'):
                spans=[[segment(word) for rank,word in part] for part in runs(raw,spacing)]
                views.append(windows(spans))
        pages[p][int(loc.rsplit('.',1)[1])]=consensus(views)
    return pages

def macer():
    corpus_path=HIST/'corpus.json'
    assert sha256(corpus_path.read_bytes()).hexdigest()=='c251598bbab3f9f93de40a72d4e039c17f52ce079dd95e86c7322f9a2283893b'
    chapters=json.loads(corpus_path.read_bytes())
    pages=defaultdict(dict)
    with (HIST/'vers.tsv').open() as f:
        for row in csv.DictReader(f,delimiter='\t'):
            begin=int(row['premier_mot_notice'])-1; end=int(row['dernier_mot_notice'])
            words=chapters[row['titre']][begin:end]
            pages[row['titre']][int(row['rang_du_vers'])]=[w.replace('j','i') for w in words]
    assert pages['Chelidonia'][1704][-3:-1]==['radix','eius']
    assert pages['Chelidonia'][1707][:3]==['de','foliis','eius']
    return pages

def alphabet(groups,seed):
    units=sorted(set('abcdefghijklmnopqrstuvwxyz')|set(groups))
    glyphs=[f'#{i:02}' for i in range(len(units))];random.Random(seed).shuffle(glyphs)
    return dict(zip(units,glyphs))

def encode(word, groups, cipher):
    out=[];i=0
    while i<len(word):
        unit=next((g for g in groups if word.startswith(g,i)),word[i])
        out.append(cipher[unit]);i+=len(unit)
    return tuple(out)

def encrypted(pages,groups,variant=False,shuffle_seed=None):
    cipher=alphabet(groups,46281+len(groups))
    encoded={}
    rng=random.Random(shuffle_seed)
    for p,lines in pages.items():
        encoded[p]={}
        for n,original in lines.items():
            plain=original.copy()
            if variant and (p,n)==('Chelidonia',1707):
                plain[1]='foleis'
            if shuffle_seed is not None:
                rng.shuffle(plain)
            encoded[p][n]=windows([[encode(w,groups,cipher) for w in plain]])
    return encoded,cipher

def freeze(mapping):
    return tuple(sorted(mapping.items()))

@lru_cache(maxsize=120000)
def starter(a,m,width):
    return tuple(freeze(key) for partial in tables(a,'radix',width)
                 for key in tables(m,'eius',width,partial))

@lru_cache(maxsize=200000)
def fit(a,m,b,target,width):
    keys=[]
    for first in starter(a,m,width):
        for full in tables(b,target,width,dict(first)):
            keys.append(freeze(full))
    return tuple(keys)

def display(word):
    return ''.join(word)

def search(pages,width,record=True):
    counts=Counter(); details=[];seated=set();qualified={kind:set() for kind in TARGETS}
    all_before=defaultdict(set)
    for page,lines in pages.items():
        # D’abord indexer le second membre par position et par graphie du pronom présumé.
        following=defaultdict(list)
        for n,pairs in lines.items():
            for (b,m),prevs in pairs.items():
                if 6<=len(b)*width and len(b)<=6 and 4<=len(m)*width and len(m)<=4:
                    following[n,m].append((b,prevs))
        for n,pairs in lines.items():
            for a,m in pairs:
                if not(len(a)<=5<=len(a)*width and len(m)<=4<=len(m)*width):
                    continue
                for k in range(n+1,n+7):
                    for b,priors in following.get((k,m),[]):
                        if b==a: continue
                        counts['fenetres_de_longueurs_compatibles']+=1
                        if not starter(a,m,width):
                            continue
                        counts['radix_eius_compatibles']+=1
                        for spelling in ALTERNATIVES:
                            keys=fit(a,m,b,spelling,width)
                            if not keys:
                                continue
                            identity=(page,n,k,a,m,b)
                            seated.add(identity);counts['ajustements_de_graphie']+=1
                            results=[]
                            for prev in sorted(p for p in priors if p):
                                readings=Counter()
                                for frozen in keys:
                                    key=dict(frozen)
                                    result=''.join(key[s] for s in prev) if all(s in key for s in prev) else '?'
                                    readings[result]+=1
                                for word in TARGETS:
                                    if word in readings:qualified[word].add(identity)
                                results.append({'precedent':display(prev),'lectures':dict(readings)})
                            if not results or None in priors:
                                all_before[identity].add('?')
                            for result in results:
                                all_before[identity].update(result['lectures'])
                            if record:
                                details.append(dict(page=page,ligne_A=n,ligne_B=k,A=display(a),M=display(m),B=display(b),
                                    graphie=spelling,tables=len(keys),precedents=results,
                                    sans_precedent_certain=not results,
                                    tables_possibles=[dict(key) for key in keys]))
    return {'fenetres':dict(counts),'localisations_distinctes':len(seated),
            'avec_prediction_possible':{s:len(values) for s,values in qualified.items()},
            'avec_prediction_imposee':{s:sum(opts=={s} for opts in all_before.values()) for s in TARGETS},'details':details}

def verified(row,word):
    return any(word in entry['lectures'] for entry in row['precedents'])

def control(pages,groups,variant,width):
    encoded,cipher=encrypted(pages,groups,variant)
    whole=search(encoded,width)
    location=[r for r in whole['details'] if (r['page'],r['ligne_A'],r['ligne_B'])==('Chelidonia',1704,1707)]
    informative=[]
    for r in location:
        true={cipher[s]:s for s in cipher}
        expected='foleis' if variant else 'foliis'
        oracle=any(all(true[g]==v for g,v in table.items()) for table in r['tables_possibles'])
        informative.append({'graphie':r['graphie'],'vraie_graphie':r['graphie']==expected,
                            'vraie_table_parmi_les_solutions':oracle,'predictions':r['precedents']})
    fake=[(r['page'],r['ligne_A'],r['ligne_B']) for r in whole['details']
          if verified(r,'de') and (r['page'],r['ligne_A'],r['ligne_B'])!=('Chelidonia',1704,1707)]
    return {k:v for k,v in whole.items() if k!='details'}|{'fenetre_attendue':informative,'autres_lieux_de':sorted(set(fake))}

def main():
    plain=macer(); controls={}
    for name,groups,width in [('une_lettre',(),1),('di_absorbe',('di','iu','fo','is'),2),
                              ('d_et_e_independants',('ra','fo','is'),2)]:
        for variant in (False,True):
            result=control(plain,groups,variant,width)
            controls[name+'/'+('copie_foleis' if variant else 'edition_foliis')]=result
            assert any(r['vraie_table_parmi_les_solutions'] and r['vraie_graphie'] for r in result['fenetre_attendue'])
    # Témoin sur la même distribution de mots et les mêmes longueurs de vers.
    null=[];locations_null=[]
    for i in range(99):
        shuffled,_=encrypted(plain,(),shuffle_seed=70318+i)
        sample=search(shuffled,1,False)
        null.append([sample['localisations_distinctes'],sample['avec_prediction_possible']['de']])
        if sample['avec_prediction_possible']['de']:
            for row in search(shuffled,1)['details']:
                if verified(row,'de'):
                    locations_null.append({'graine':70318+i,'notice':row['page'],'vers':[row['ligne_A'],row['ligne_B']]})
    save('calibration.json',{'chiffrages':controls,'permutations_ajustements_et_de':null,'localisations_de_apres_melange':locations_null})
    pages=herb(); physical={re.match(r'f(\d+)',p)[1] for p in pages}
    outcomes={str(width):search(pages,width) for width in (1,2)}
    save('voynich.json',dict(faces=len(pages),feuillets=len(physical),lignes=sum(map(len,pages.values())),
                              fenetres_distinctes_par_ligne=sum(len(pairs) for lines in pages.values() for pairs in lines.values()),modeles=outcomes))
    for name,c in controls.items():
        print(name,c['localisations_distinctes'],c['avec_prediction_possible'],c['fenetre_attendue'])
    print('permutations avec solution',sum(r[0]>0 for r in null),'avec de',sum(r[1]>0 for r in null))
    print('Voynich',len(pages),len(physical),sum(map(len,pages.values())),
          [(w,r['fenetres'],r['localisations_distinctes'],r['avec_prediction_possible']) for w,r in outcomes.items()])

if __name__=='__main__': main()
