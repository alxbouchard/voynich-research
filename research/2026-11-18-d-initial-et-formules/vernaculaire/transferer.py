"""Tester hors f43 les tables ajustées aux trois mots des deux lignes."""
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import gzip,json,random,sys
from corpus_vern import HERE,martino,load_book
from essayer import encode
from ouvrir import units
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-dam-en-fin-de-ligne'))
from corpus_dam import aligned,corpus,metadata

EXCL={15,66,102,126,145,179,183,254}

def save(name,doc):
    data=(json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    (HERE/name).write_bytes(gzip.compress(data,mtime=0))


def tables():
    obs=json.loads((HERE/'OUVERTURE.json').read_bytes())['comparaisons']['martino']['trois_mots_compatibles_des_deux_cotes']
    result=[]
    for item in obs:
        for pair in item['paires']:
            k=pair['cle_completee']
            if k not in result: result.append(k)
    return result

def words(w,initial):
    return units(w[1:] if w=='dshedy' and initial else w,'blocs')

def windows(keys,show,excluded=("f43r","f43v")):
    ed,_=corpus(); sections=metadata(); out=[]
    legal=set(keys[0])
    for loc,(page,kind,_,_) in ed['H'].items():
        if page in excluded or kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0':continue
        seq=list(aligned(ed,loc,page,sections.get(page,{}).get('I',''),page,Counter()))
        packed=[(r,tuple(map(int,r['rangs_quatre'].split('/')))) for r in seq]
        def adjacent(a,b):return a[0]['troncon']==b[0]['troncon'] and all(i+1==j for i,j in zip(a[1],b[1]))
        for i,(one,two) in enumerate(zip(packed,packed[1:])):
            if not adjacent(one,two):continue
            a,b=one[0],two[0]
            x=words(a['mot'],'debut' in a['positions'])
            y=words(b['mot'],'debut' in b['positions'])
            if not (set(x)|set(y))<=legal:continue
            third=i+2<len(seq) and adjacent(two,packed[i+2])
            row={'loc':f"{loc}/{a['troncon']}/{one[1][0]}","mots":[a['mot'],b['mot']],'evaluable':third}
            if show and third:row['vrai']=seq[i+2]['mot']
            out.append((x,y,row))
    return out


def forward(k,matches,after,detail):
    acc=Counter();out=[]
    def dec(word):return ''.join(k[c] for c in word)
    enc_cache={}
    for first,second,data in matches:
        pair=(dec(first),dec(second))
        if pair not in after:continue
        acc['paires_distinctes']+=1
        acc['paires_attestees']+=len(data)
        opts={}
        for z in after[pair]:
            if not z:continue
            if z not in enc_cache:enc_cache[z]=encode(z,k)
            for w in enc_cache[z]:
                # Un recodage valide doit également se décoder sous la même segmentation.
                if all(c in k for c in units(w,'blocs')) and dec(units(w,'blocs'))==z:
                    opts.setdefault(w,[]).append(z)
        if opts:
            acc['avec_annonce']+=len(data)
            acc['avec_annonce_evaluable']+=sum(r['evaluable'] for r in data)
        if detail:
            out.extend({**r,'italien':list(pair),'suites_italiennes':sorted(z for z in after[pair] if z),'annonces':opts} for r in data)
    return dict(acc),out


def announce(path):
    keys=tables();data=windows(keys,False); grouped=defaultdict(list)
    for a,b,row in data:grouped[a,b].append(row)
    matches=[(a,b,v) for (a,b),v in grouped.items()]
    after=defaultdict(set);book=load_book((ref,text) for ref,text in martino(path) if int(ref.split()[1]) not in EXCL)
    for ref,seq in book:
        for i,pair in enumerate(zip(seq,seq[1:])):
            after[pair].add(seq[i+2] if i+2<len(seq) else '')
    rng=random.Random(431022);summaries=[]
    for k in keys:
        observed,rows=forward(k,matches,after,True)
        pending=set();null=[]
        while len(pending)<199:
            vals=list(k.values());rng.shuffle(vals)
            if tuple(vals) in pending or vals==list(k.values()):continue
            pending.add(tuple(vals));v,_=forward(dict(zip(k,vals)),matches,after,False);null.append(v)
        @lru_cache(None)
        def rend(w):
            return [rep for rep in encode(w,k) if all(c in k for c in units(rep,'blocs')) and ''.join(k[c] for c in units(rep,'blocs'))==w]
        power=[];control=None
        for ref,seq in book:
            for i,trio in enumerate(zip(seq,seq[1:],seq[2:])):
                if all(rend(w) for w in trio):
                    power.append([ref,i+1,*trio])
                    if control is None:
                        a,b,c=[rend(w)[0] for w in trio]
                        _,pred=forward(k,[(units(a,'blocs'),units(b,'blocs'),[{'evaluable':True}])],after,True)
                        assert c in pred[0]['annonces']
                        control={'clair':trio,'chiffre':[a,b,c],'previsions':list(pred[0]['annonces']),'ref':ref}
        summaries.append({'cle':k,'paires':rows,'compte':observed,'controles':null,'trigrammes_codables':power,'auto_controle':control})
    save('TRANSFERT-ANNONCES.json.gz',{'fenetres':len(data),'paires_graphiques':len(grouped),
          'positions_avec_troisieme':sum(row['evaluable'] for _,_,row in data),'italien_mots':sum(len(w) for _,w in book),
          'cles':summaries})
    for r in summaries:print(r['compte'],len(r['trigrammes_codables']),r['auto_controle'])
    print('annonces',[(n,r['loc'],r['mots'],r['italien'],r['annonces']) for n,table in enumerate(summaries) for r in table['paires'] if r['annonces']][:15])


def check():
    ann=json.loads(gzip.decompress((HERE/'TRANSFERT-ANNONCES.json.gz').read_bytes()))
    actual={r['loc']:r.get('vrai') for _,_,r in windows(tables(),True)}
    full=[]
    for table in ann['cles']:
        results=[]
        for row in table['paires']:
            true=actual[row['loc']]
            results.append({**row,'vrai':true,'exact':true in row['annonces'] if true and row['annonces'] else None})
        full.append(results)
    save('TRANSFERT-OUVERTURE.json.gz',full)
    print([(sum(r['exact'] is not None for r in rs),sum(r['exact'] is True for r in rs)) for rs in full])
if __name__=='__main__':
    if sys.argv[1]=='annoncer':announce(Path(sys.argv[2]))
    else:check()
