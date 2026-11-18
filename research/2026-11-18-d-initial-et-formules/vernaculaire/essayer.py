"""Rechercher les deux amorces de f43 dans les témoins et annoncer leur mot suivant."""
from collections import Counter,defaultdict
from pathlib import Path
import gzip
import json
import random
import sys
from corpus_vern import HERE,URLS,fingerprint,sources

X=('d','sh','e','d','y')
CUTS={'d_lu':(X,('q','o')), 'd_de_ligne':(X[1:],('q','o')),
      'qo_lie_d_lu':(X,('qo',)), 'qo_lie_d_de_ligne':(X[1:],('qo',))}
Y=('t','e','d','y')


def fit(codes,word,spec,key):
    if not codes:
        if not word: yield key
        return
    c,tail=codes[0],codes[1:]
    if c in key:
        value=key[c]
        if word.startswith(value):
            yield from fit(tail,word[len(value):],spec,key)
    else:
        for n in spec.get(c,(1,2)):
            value=word[:n]
            if len(value)!=n or value in key.values():continue
            yield from fit(tail,word[n:],spec,{**key,c:value})


def encode(clear,key):
    if not clear:return [""]
    return [v+k for v,letters in key.items() if clear.startswith(letters)
            for k in encode(clear[len(letters):],key)]


def index(book):
    out=defaultdict(lambda:defaultdict(list))
    for ref,words in book:
        for i in range(len(words)-1):
            out[words[i]][words[i+1]].append([ref,i+1,words[i+2] if i+2<len(words) else None])
    return out


def coarse(first,short,long):
    prefix=long[:-len(short)]
    if not 1<=len(prefix)<=4:return
    for n in range(1,min(4,len(first)-1,len(short)-1)+1):
        if first[-n:]!=short[-n:]:continue
        key={'sh':first[:-n],'t':short[:-n],'edy':short[-n:],'qo':prefix}
        if max(len(key['sh']),len(key['t']))<=8 and len(set(key.values()))==4:
            yield key


def contextualize(loci,key):
    return [{'ref':ref,'rang':i,'troisieme':w,'annonces':sorted(set(encode(w,key))) if w else []} for ref,i,w in loci]


def analyse(book,details=True):
    lookup=index(book)
    rows=[]
    singles=[]
    contrast=Counter()
    paired=Counter()
    for first,seconds in lookup.items():
        for long in seconds:
            for n in range(1,min(4,len(long)-1)+1):
                short=long[n:]
                if short not in seconds:continue
                contrast['paires_avec_prefixe']+=1
                for mode,(a,prefix) in CUTS.items():
                    if first[-3:]!=short[-3:] or len(short)<4 or not 1<=len(long)-len(short)<=4:continue
                    for first_key in fit(a,first,{},{}):
                        for short_key in fit(Y,short,{},first_key):
                            for table in fit(prefix+Y,long,{},short_key):
                                paired[mode]+=1
                                if details:rows.append([mode,first,short,long,table])
                for table in coarse(first,short,long):
                    paired['blocs']+=1
                    if details:rows.append(['blocs',first,short,long,table])
        if not details:continue
        for second,uses in seconds.items():
            if first[-3:]!=second[-3:] or not 3<=len(first)<=10:continue
            for mode,(a,prefix) in CUTS.items():
                for target,codes in [('verso',Y),('recto',prefix+Y)]:
                    if target=='verso' and 'qo_lie' in mode:continue
                    for first_key in fit(a,first,{},{}):
                        for table in fit(codes,second,{},first_key):
                            singles.append({'mode':mode,'face':target,'premiers':[first,second],
                                            'cle':table,'lieux':contextualize(uses,table)})
    enriched=[]
    for mode,first,short,long,table in rows:
        enriched.append({'mode':mode,'premiers':[first,short,long],'cle':table,
                         'recto':contextualize(lookup[first][long],table),
                         'verso':contextualize(lookup[first][short],table)})
    return {'bigrammes_distincts':sum(map(len,lookup.values())),**contrast,
            'tables_communes':dict(paired),'deux_faces':enriched,'une_face':singles}


def calibration(book):
    # Première fenêtre au troisième mot distinct des deux premiers et entièrement codable.
    # La clé secrète est une bijection par lettre ; elle change pour chaque langue.
    ordered=sorted(set(c for _,words in book for w in words for c in w))
    rng=random.Random(119043)
    reps=ordered.copy();rng.shuffle(reps); cipher=dict(zip(ordered,reps))
    for ref,words in book:
        for a,b,c in zip(words,words[1:],words[2:]):
            if c in (a,b) or len(c)<3 or not set(c)<=set(a+b):continue
            first,second,hidden=[tuple(cipher[x] for x in word) for word in (a,b,c)]
            spec={code:(1,) for code in cipher.values()}
            tables=[k for fk in fit(first,a,spec,{}) for k in fit(second,b,spec,fk)]
            assert len(tables)==1
            forecast=encode(c,tables[0]);assert forecast==[''.join(hidden)]
            return {'ref':ref,'clair':[a,b,c],'chiffre':[''.join(w) for w in (first,second,hidden)],'annonce':forecast}
    raise AssertionError('aucun contrôle admissible')


def main(fr,it):
    rng=random.Random(430913)
    out={}
    for name,book in sources(fr,it).items():
        primary=analyse(book)
        shuffles=[]
        for _ in range(99):
            perm=[]
            for ref,words in book:
                a=list(words);rng.shuffle(a);perm.append((ref,tuple(a)))
            d=analyse(perm,False)
            shuffles.append([d.get('paires_avec_prefixe',0),d['tables_communes']])
        out[name]={'source':URLS.get(name,'CORPUS.json du Régime du corps'),'sha256_segmente':fingerprint(book),
                   'segments':len(book),'mots':sum(len(row) for _,row in book),'resultats':primary,
                   'temoin_melange':shuffles,'temoin_positif':calibration(book)}
    raw=(json.dumps(out,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    (HERE/'ANNONCES.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    for name,d in out.items():
        r=d['resultats'];print(name,d['mots'],r.get('paires_avec_prefixe'),r['tables_communes'],len(r['une_face']))
        for which in ['deux_faces','une_face']:
            for row in r[which]:
                if which=='deux_faces' or any(h['annonces'] for h in row.get('lieux',[])):print(which,row)
        print('temoin',d['temoin_positif'])
if __name__=='__main__':main(*map(Path,sys.argv[1:]))
