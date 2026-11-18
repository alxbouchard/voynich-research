"""Annoncer la suite de f75 et essayer hors des deux feuillets les clés ainsi complétées."""
from collections import Counter,defaultdict
from pathlib import Path
import gzip,json,random,sys
from corpus_vern import HERE,martino,load_book
from essayer import fit,encode
from ouvrir import units
from transferer import EXCL,forward,save,windows

def read(name):return json.loads(gzip.decompress((HERE/name).read_bytes()))

def encode_normal(w,k):
    return sorted({s for s in encode(w,k) if all(x in k for x in units(s,'blocs')) and ''.join(k[x] for x in units(s,'blocs'))==w})

def announce(path):
    initial=read('TRANSFERT-ANNONCES.json.gz'); revealed=read('TRANSFERT-OUVERTURE.json.gz')
    follow=[]
    fullbook=load_book(martino(path))
    spent=set(EXCL)
    seen=set()
    for k,rows in zip(initial['cles'],revealed):
        for row in rows:
            w=row['vrai']
            for clear in row['suites_italiennes']:
                trio=tuple(row['italien']+[clear])
                for ext in fit(units(w,'blocs'),clear,{},k['cle']):
                    key=tuple(sorted(ext.items()))
                    if key in seen:continue
                    seen.add(key); locations=[]
                    for ref,seq in fullbook:
                        recipe=int(ref.split()[1])
                        if recipe in EXCL:continue
                        for i in range(len(seq)-2):
                            if tuple(seq[i:i+3])!=trio:continue
                            spent.add(recipe)
                            following=seq[i+3:i+5]
                            locations.append({'ref':ref,'rang':i+1,'suite':following,'annonces':[encode_normal(v,ext) for v in following]})
                    assert locations
                    follow.append({'trio':trio,'cle':ext,'positions':locations})
    corpus=windows([x['cle'] for x in follow],False,('f43r','f43v','f75r','f75v'))
    pats=defaultdict(list)
    for a,b,r in corpus:pats[a,b].append(r)
    pattern=[(a,b,v) for (a,b),v in pats.items()]
    after=defaultdict(set)
    for ref,seq in fullbook:
        if int(ref.split()[1]) in spent:continue
        for i,pair in enumerate(zip(seq,seq[1:])):after[pair].add(seq[i+2] if i+2<len(seq) else '')
    rng=random.Random(7533)
    for item in follow:
        k=item['cle'];stat,rows=forward(k,pattern,after,True)
        item['transfert']=rows;item['compte']=stat
        null=[];perms=set()
        while len(perms)<199:
            v=list(k.values());rng.shuffle(v)
            if v==list(k.values()) or tuple(v) in perms:continue
            perms.add(tuple(v))
            # Pour la comparaison au hasard, garder les annonces par lieu afin de les scorer après ouverture.
            totals,guesses=forward(dict(zip(k,v)),pattern,after,True)
            null.append({'totaux':totals,'annonces':[[r['loc'],list(r['annonces'])] for r in guesses if r['annonces'] and r['evaluable']]})
        item['permutations']=null
    save('F75-ANNONCES.json.gz',{'exclusions':sorted(spent),'paires':len(corpus),'mot_suivant_present':sum(r['evaluable'] for _,_,r in corpus),'paires_formes':len(pattern),'lectures':follow})
    for i,x in enumerate(follow):
        local={j:sorted({w for r in x['positions'] for w in r['annonces'][j]}) for j in (0,1) if all(len(r['annonces'])>j for r in x['positions'])}
        print(i+1,x['trio'],local,x['compte'])

def check():
    from corpus_dam import aligned,corpus,metadata
    announced=read('F75-ANNONCES.json.gz')['lectures']
    ed,_=corpus();loc='f75r.11';meta=metadata()
    span=[r for r in aligned(ed,loc,'f75r',meta['f75r']['I'],'f75r',Counter()) if r['troncon']==2]
    target=[]
    for rank in (8,9):
        r=next((r for r in span if int(r['rangs_quatre'].split('/')[0])==rank),None)
        # Le début de la suite doit suivre chekam de façon contiguë dans les quatre traitements.
        base=next(r for r in span if int(r['rangs_quatre'].split('/')[0])==7)
        ok=r is not None and all(int(b)-int(a)==rank-7 for a,b in zip(base['rangs_quatre'].split('/'),r['rangs_quatre'].split('/')))
        target.append(r['mot'] if ok else None)
    actual={r['loc']:r.get('vrai') for _,_,r in windows([x['cle'] for x in announced],True,('f43r','f43v','f75r','f75v'))}
    results=[]
    for item in announced:
        cases=[]
        for r in item['transfert']:
            if r['annonces'] and r['evaluable']:
                t=actual[r['loc']];cases.append({**r,'vrai':t,'compatible':t in r['annonces']})
        local=[]
        for r in item['positions']:
            surviving=[item['cle']]
            for clear,cipher in zip(r['suite'],target):
                if cipher is None:break
                surviving=[x for k in surviving for x in fit(units(cipher,'blocs'),clear,{},k)]
                if not surviving:break
            local.append({**r,'justes':[t in p if t and p else None for t,p in zip(target,r['annonces'])],
                          'extensions_de_la_suite':len(surviving) if r['suite'] and all(target[:len(r['suite'])]) else None})
        def nullscore(tab):
            hits=[(loc,actual[loc] in preds,len(preds)==1) for loc,preds in tab['annonces']]
            return [len(hits),sum(h for _,h,_ in hits),sum(h and unique for _,h,unique in hits)]
        results.append({'trio':item['trio'],'local':local,'vrai_f75':target,'ailleurs':cases,'nuls':[nullscore(x) for x in item['permutations']]})
    save('F75-OUVERTURE.json.gz',results)
    print('f75',target,'ailleurs',[(len(r['ailleurs']),sum(c['compatible'] for c in r['ailleurs'])) for r in results])
if __name__=='__main__':
    if sys.argv[1]=='annoncer':announce(Path(sys.argv[2]))
    else:check()
