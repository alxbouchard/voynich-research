"""Geler les annonces à deux mots visibles avant d'ouvrir le troisième."""
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from random import Random
from xml.etree import ElementTree as ET
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0,str(RESEARCH/'2026-11-18-ordre-des-noms/lecture'))
from comparer import maps, units
from transfert import corpus, langage, tokens

PARTS = ['capitis','dentium','lateris','stomachi','coli','lumborum']
SOURCE = '903823a2c00454deccb2e30ffc3651b1d204d53b4bce1c8b9128275e79dc9687'
STOPS = re.compile(r'<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>',re.I)
POTENCES = {'t','f','p','k','cth','cph','cfh','ckh'}


def save(name,data):
    (HERE/name).write_text(json.dumps(data,indent=1,ensure_ascii=False)+'\n')


def load(name):
    return json.loads((HERE/name).read_text())


def extract_latin(path):
    assert sha256(path.read_bytes()).hexdigest()==SOURCE
    tree=ET.parse(path)
    recipes={}
    for chapter in tree.iter():
        if chapter.get('subtype')!='compositio': continue
        # La préface et la liste des matières sont hors des notices numérotées.
        paragraph=chapter.find('{*}p')
        words=re.findall(r'[^\W\d_]+',''.join(paragraph.itertext()).lower(),re.U)[:3]
        if chapter.get('n')=='5':
            assert words==['ad','capitis','dolorein']
            words[2]='dolorem'
        recipes[chapter.get('n')]=words
    assert len(recipes)==271 and [n for n,w in recipes.items() if len(w)!=3]==['169']
    save('LATIN.json',recipes)


def latin_test():
    recipes=load('LATIN.json')
    phrases=dict(recipes, **{'Wellcome f30v':'ad dolorem dentium'.split()})
    vocab=sorted(set(w for row in phrases.values() for w in row))
    shuffled=list(range(len(vocab))); Random(292810).shuffle(shuffled)
    enc=dict(zip(vocab,shuffled))
    code={i:tuple(enc[w] for w in row) for i,row in phrases.items()}
    a,b,c=code['1']; aa,d,cc=code['53']; assert (aa,cc)==(a,c)
    excluded={'1','53','Wellcome f30v'}
    def test(accept):
        calls={k:row[2]==c for k,row in code.items() if k not in excluded and accept(*row[:2])}
        return dict(appels=len(calls),succes=sum(calls.values()),succes_notices=[k for k,v in calls.items() if v])
    return dict(recettes=len(recipes),commencent_ad=sum(row[0]=='ad' for row in recipes.values()),
        ad_X_dolorem=sum(len(row)==3 and row[0]=='ad' and row[2]=='dolorem' for row in recipes.values()),
        rang3_dolorem=sum(len(row)==3 and row[2]=='dolorem' for row in recipes.values()),ad_seul=test(lambda x,y:x==a),
        deux_organes_ancres=test(lambda x,y:x==a and y in (b,d)),
        temoin_inverse=dict(amorce=list(code['Wellcome f30v'][:2]),source=list(code['53']),
            predit=d,observe=code['Wellcome f30v'][2],succes=code['Wellcome f30v']==(a,c,d)))



def latin_letters():
    recipes=load('LATIN.json')
    letters=sorted(set(''.join(w for row in recipes.values() for w in row)))
    codes=[f's{i}' for i in range(len(letters))]
    Random(41932).shuffle(codes)
    encoder=dict(zip(letters,codes))
    def encoded(w): return tuple(encoder[c] for c in w)
    cipher={n:[encoded(w) for w in row] for n,row in recipes.items()}
    a,b,c=cipher['1']
    initial,=maps(a,'ad',1)
    seed,=maps(b,'capitis',1,initial)
    key,=maps(c,'dolorem',1,seed)
    calls={}
    for n,row in cipher.items():
        if n in ('1','53') or len(row)<3 or row[0]!=a:continue
        if any(next(maps(row[1],part,1,key),None) is not None for part in PARTS):
            calls[n]=row[2]==c
    return dict(ancre='1',exclues=['1','53'],signes_appris=len(key),annonces=len(calls),
        succes=[n for n,v in calls.items() if v],erreurs=[n for n,v in calls.items() if not v],
        comparaison_recette_60_PHI='candorem',theme='contrôle rétrospectif de la mécanique de substitution')

def records(nreserve=2):
    editions,_=corpus()
    meta={}
    for line in (langage.DATA/'ZL3b-n.txt').read_text().splitlines():
        head=re.match(r'^<(f\d+[rv]\d*)>',line)
        if head: meta[head[1]]=dict(re.findall(r'\$(\w)=(\w+)',line))
    out={}; coverage=Counter()
    for loc in sorted(set.union(*(set(ed) for ed in editions.values()))):
        face=loc.split('.')[0]; m=meta.get(face,{})
        q,section=m.get('Q'),m.get('I')
        if not ((section=='H' and q in list('ABCDEFG')) or (section=='P' and q in ['O','S'])): continue
        group='train' if q in 'ABCO' else 'reserve'
        eds=[ed.get(loc) for ed in editions.values()]
        isopen=[e and e[1].startswith('P') and e[3].startswith('<%>') for e in eds]
        if not any(isopen): continue
        coverage[f'{group}_{section}_ouvertures_union']+=1
        if not all(isopen): continue
        coverage[f'{group}_{section}_ouvertures_communes']+=1
        n=3 if group=='train' else nreserve
        views=[tokens(STOPS.split(e[3],1)[0],mode)[:n] for e in eds for mode in ('joints','separes')]
        agreement=[]
        for i in range(n):
            vals={row[i] if i<len(row) else None for row in views}
            w=next(iter(vals)) if len(vals)==1 else None
            agreement.append(w if w and re.fullmatch('[a-z]+',w) else None)
        out[loc]={'lot':group,'face':face,'bif':q+'/'+m['B'],'section':section,'w':agreement}
    return out,coverage


def rank(tr):
    groups=defaultdict(list)
    for loc,r in tr.items():
        a,b,c=r['w'];
        if len({a,b,c})==3:groups[a,c].append((loc,r['bif'],b))
    ret=[]
    for (a,c),items in groups.items():
        ret.append(dict(first=a,third=c,bifs=len({i[1] for i in items}),seconds=len({i[2] for i in items}),count=len(items),sources=[i[0] for i in items]))
    return sorted(ret,key=lambda r:(-r['bifs'],-r['seconds'],-r['count'],r['first'],r['third']))


def firstunits(w,orn):
    seq=units(w)
    return seq[1:] if orn and seq[0] in POTENCES else seq


def strict_models(train):
    models=[]; initial=Counter()
    for orn in [False,True]:
        for width in [1,2]:
            for loc,r in train.items():
                a,b,c=r['w']; u=firstunits(a,orn)
                for ka in maps(u,'ad',width):
                    initial[f'{orn}/{width}/AD']+=1
                    for part in PARTS:
                        for kb in maps(units(b),part,width,ka):
                            initial[f'{orn}/{width}/AD_genitif']+=1
                            for kc in maps(units(c),'dolorem',width,kb):
                                models.append(dict(src=loc,a=a,b=b,c=c,part=part,width=width,orn=orn,key=kc))
    return models,dict(initial)


def predict():
    data,cov=records()
    train={k:r for k,r in data.items() if r['lot']=='train' and all(r['w'])}
    reserve={k:r for k,r in data.items() if r['lot']=='reserve'}
    assert all(len(r['w'])==2 for r in reserve.values())
    ranks=rank(train); valid=[r for r in ranks if r['bifs']>=2 and r['seconds']>=2]
    third=Counter(r['w'][2] for r in train.values())
    baseline=min(third,key=lambda w:(-third[w],w))
    firsts=defaultdict(Counter); flipped=defaultdict(set)
    for r in train.values():
        a,b,c=r['w'];firsts[a][c]+=1
        if len({a,b,c})==3: flipped[a,c].add(b)
    diagnostic={a:min(count,key=lambda c:(-count[c],c)) for a,count in firsts.items()}
    models,initial=strict_models(train)
    attempts={m:{} for m in ('principal','meilleur','tout_premier','inverse','signe','signe_inverse')}
    def call(m,loc,w):attempts[m].setdefault(loc,set()).add(w)
    for loc,r in reserve.items():
        a,b=r['w']
        if not a: continue
        for name,ranking in [('principal',valid),('meilleur',ranks)]:
            if ranking and a==ranking[0]['first']:call(name,loc,ranking[0]['third'])
        if a in diagnostic: call('tout_premier',loc,diagnostic[a])
        if not b:continue
        for w in flipped.get((a,b),()):call('inverse',loc,w)
        for model in models:
            width,orn,key=model['width'],model['orn'],model['key']
            # AD must be entirely readable under the frozen table. Fit novel body-part signs only.
            seq=firstunits(a,orn)
            if any(s not in key for s in seq) or ''.join(key[s] for s in seq)!='ad':continue
            if any(next(maps(units(b),p,width,key),None) is not None for p in PARTS):call('signe',loc,model['c'])
            if model['part']=='dentium' and (a,b)==(model['a'],model['c']):call('signe_inverse',loc,model['b'])
    frozen={m:{loc:sorted(vals) for loc,vals in calls.items()} for m,calls in attempts.items()}
    save('PREDICTIONS.json',dict(couverture=cov,modeles_signes=models,ancres_par_signe=initial,
        entrainement_complet=len(train),classement=ranks[:8],couples_admissibles=len(valid),
        premier_admissible=valid[:1],mot_temoin=baseline,essais=frozen))


def verify():
    frozen=load('PREDICTIONS.json'); data,_=records(3)
    reserve={k:r for k,r in data.items() if r['lot']=='reserve'}; experience={}
    for name,calls in frozen['essais'].items():
        relevant={loc:r for loc,r in reserve.items() if loc in calls}
        complete={loc:r for loc,r in relevant.items() if r['w'][2] and len(calls[loc])==1}
        correct=[k for k,r in complete.items() if calls[k][0]==r['w'][2]]
        pools=defaultdict(list)
        for k,r in reserve.items():
            if r['w'][2]:pools[r['face']].append((k,r['w'][2]))
        # Exact convolution of all independent cyclic offsets by face.
        null=Counter({0:1}); movable=0
        for pool in pools.values():
            if not any(k in complete for k,w in pool): continue
            scores=Counter(sum(k in complete and calls[k][0]==pool[(i+off)%len(pool)][1] for i,(k,w) in enumerate(pool)) for off in range(len(pool)))
            if len(scores)>1: movable+=1
            new=Counter()
            for i,x in null.items():
                for j,y in scores.items(): new[i+j]+=x*y
            null=new
        experience[name]=dict(annonces=len(relevant),illisibles=sum(not r['w'][2] for r in relevant.values()),
           equivoques=sum(bool(r['w'][2]) and len(calls[k])!=1 for k,r in relevant.items()),
           evaluees=len(complete),par_section={s:[sum(k in correct for k,r in complete.items() if r['section']==s),sum(r['section']==s for r in complete.values())] for s in ('H','P')},
           succes=correct,bifeuillets_touches=sorted({complete[k]['bif'] for k in correct}),
           succes_temoin_frequence=sum(r['w'][2]==frozen['mot_temoin'] for r in complete.values()),
           nul_faces_avec_variation=movable,p_exact=sum(n for s,n in null.items() if s>=len(correct))/sum(null.values()) if complete else None,
           detail={k:{'observe':r['w'][2],'annonces':calls[k],'debut':r['w'][:2]} for k,r in relevant.items()})
    coverage=Counter()
    for r in data.values():
        for n in (1,2,3):
            if all(r['w'][:n]):coverage[f"{r['lot']}_{r['section']}_{n}"]+=1
    save('RESULTATS.json',dict(empreinte_predictions=sha256((HERE/'PREDICTIONS.json').read_bytes()).hexdigest(),
        latin=latin_test(),latin_substitution=latin_letters(),couverture_mots=coverage,experiences=experience))


if __name__=='__main__':
    if sys.argv[1]=='source':extract_latin(Path(sys.argv[2]))
    elif sys.argv[1]=='predire':predict()
    elif sys.argv[1]=='verifier':verify()
    else:raise SystemExit('source <XML>, predire, verifier')
