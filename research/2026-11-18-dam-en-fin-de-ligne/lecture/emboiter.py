"""Résoudre exactement les trois équations de mots et prévoir les voisins indépendants."""
from collections import Counter,defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
from random import Random
import gzip
import json
import re
import sys

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-phrase-et-doublets/lecture'))
from corpus_sources import celsus,LATIN
sys.path.insert(0,str(RESEARCH/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import corpus,sequence,MODES,units

RIDGES=RESEARCH/'2026-11-18-phrase-et-doublets/lecture/RIDGES.json'
SIGNS='oldam'; PREFS='dola ms'.replace(' ','')
ROOTS={'latin':('bifid','bifur','furc','gemin','dupl','divid','divis','bipart','ram'),
    'allemand':('gabel','gabl','zweyg','zweig','zwaig','zweifach','zwifach','zweyfach','zwifalt','zweifalt','zweyfalt','doppel','teil','teyl','tail')}


def read(p):return json.loads(p.read_text())
def save(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=1)+'\n').encode()
    (HERE/name).write_bytes(gzip.compress(data,mtime=0) if name.endswith('.gz') else data)


def corpora(path):
    rid=read(RIDGES); out={'Macer':read(LATIN),'Celse':celsus(path)}
    for cut in sorted({q.partition(':')[0] for q in rid}):
        out[cut]={k:ws for k,ws in rid.items() if k.startswith(cut+':')}
    return out


def inventory(rows):
    hits=defaultdict(set);before=defaultdict(Counter);n=0
    for loc,words in rows.items():
        for i,w in enumerate(words):
            hits[w].add(loc);n+=1
            if i:before[w][words[i-1]]+=1
    return hits,before,n


def chunks(w,width,n):
    if not (n<=len(w)<=width*n):return
    if n==1:yield (w,);return
    for size in range(max(1,len(w)-(n-1)*width),min(width,len(w)-n+1)+1):
        for tail in chunks(w[size:],width,n-1):yield (w[:size],)+tail


def solve_triplets(words,width):
    prefix=defaultdict(set)
    for w in words:
        for i in range(1,min(width,len(w)-1)+1):prefix[w[i:]].add(w[:i])
    for w in sorted(words & prefix.keys()):
        values=prefix[w]
        for parts in chunks(w,width,5):
            o,l,d,a,m=parts
            follow=a+l+d+a+m
            for s in sorted(prefix.get(follow,())):
                key=dict(zip(SIGNS+'s',parts+(s,)))
                # Reading W3 requires commitment to a sign already fixed by W1 or W2.
                for q in PREFS:
                    if key[q] in values:yield q,(w,s+follow,key[q]+w),key


def encode(word,key):
    if not word:return ['']
    return [s+suffix for s,v in key.items() if word.startswith(v) for suffix in encode(word[len(v):],key)]


def previous_options(w,before,key):
    counter=before[w]
    if not counter:return None
    top=counter.most_common();word,n=top[0]
    if len(word)<3 or (len(top)>1 and n==top[1][1]):return None
    return dict(mot=word,occurrences=n,annonces=sorted(set(encode(word,key))))


def project(key,word):return ''.join(key.get(s,'['+s+']') for s in word)


def held_words(vocab,key,width,injective):
    left=key['o']+key['l'];between=key['a'];right=key['d']+key['a']+key['m'];found=[]
    for w in sorted(vocab):
        if not w.startswith(left) or not w.endswith(right):continue
        core=w[len(left):len(w)-len(right)]
        for n in range(1,width+1):
            if core[n:n+len(between)]!=between:continue
            k,r=core[:n],core[n+len(between):]
            if not (k and 1<=len(r)<=width):continue
            if injective and len(set(key.values())|{k,r})!=len(key)+2:continue
            found.append(dict(mot=w,k=k,r=r))
    return found


def announce(xml):
    groups=corpora(xml);summary={};models=[]
    for name,rows in groups.items():
        hist,prev,n=inventory(rows);vocab=set(hist);dims={}
        language='latin' if name in ('Macer','Celse') else 'allemand'
        recorded=sorted(w for w in vocab if w.startswith(ROOTS[language]))
        for width in (2,3):
            counts={flag:Counter() for flag in ('distincts','homophones_admis')}
            trips={flag:defaultdict(set) for flag in counts}
            for q,words,key in solve_triplets(vocab,width):
                flags=['homophones_admis']
                if len(set(key.values()))==len(key):flags.append('distincts')
                for flag in flags:
                    counts[flag][q]+=1;trips[flag][q].add(words)
                if q!='d':continue
                meanings=[w for w in words if w.startswith(ROOTS[language])]
                shared=set.intersection(*(hist[w] for w in words))
                new=dict(corpus=name,largeur=width,injective='distincts' in flags,mots=words,cle=key,
                     sens=meanings,lieux={w:sorted(hist[w]) for w in words},segment_commun=sorted(shared),
                     f55r=project(key,'olkardam'),mots_compatibles_f55r=held_words(vocab,key,width,'distincts' in flags),
                     annonces={eva:previous_options(w,prev,key) for eva,w in zip(['oldam','saldam','doldam'],words)})
                models.append(new)
            dims[width]={f:{q:dict(tables=counts[f][q],triplets=len(trips[f][q])) for q in PREFS} for f in counts}
        summary[name]=dict(positions=n,types=len(vocab),resultats=dims,lexemes_semantiques=recorded)
    save('MODELES.json.gz',models);save('ANNONCES.json',dict(corpus=summary,n_modeles=len(models),
       empreinte_modeles=sha256((HERE/'MODELES.json.gz').read_bytes()).hexdigest(),sources={p.name:sha256(p.read_bytes()).hexdigest() for p in (LATIN,RIDGES,xml)}))


def calibration():
    mac=read(LATIN);forms=[('radix','Artemisia'),('radice','Pastinaca'),('radicis','Lilium')]
    rng=Random(29112);alphabet=list('abcdefghijklmnopqrstuvwxyz');rng.shuffle(alphabet)
    secret=dict(zip('abcdefghijklmnopqrstuvwxyz',alphabet));enc=lambda w:''.join(secret[c] for c in w)
    key={}
    for w,loc in forms:
        assert w in mac[loc]
        for c,k in zip(enc(w),w):assert key.setdefault(c,k)==k
    place='Plantago';known=enc('radices');decode={v:k for k,v in key.items()}
    guess=''.join(decode[c] for c in 'radices');assert guess==known and 'radices' in mac[place]
    return dict(ancres=[(enc(w),w,loc) for w,loc in forms],reserve=place,attendu=guess,releve=known,appris=key)


def verify():
    frozen=read(HERE/'ANNONCES.json');assert sha256((HERE/'MODELES.json.gz').read_bytes()).hexdigest()==frozen['empreinte_modeles']
    models=json.loads(gzip.decompress((HERE/'MODELES.json.gz').read_bytes()))
    before=defaultdict(set)
    for it in models:
        for eva,rec in it['annonces'].items():
            if rec:before[eva].update(rec['annonces'])
    ed,_=corpus(); sites=[]
    for loc in sorted(set.intersection(*(set(rows) for rows in ed.values()))):
        a,b=[rows[loc] for rows in ed.values()];p,t=a[:2]
        if not t.startswith('P') or b[:2]!=(p,t) or re.match(r'f(?:55|89|99)[rv]',p):continue
        vs=[sequence(row[3],cut) for row in [a,b] for cut in MODES]
        for i in range(min(map(len,vs))):
            current={v[i][1] for v in vs}
            if len(current)!=1 or not (current&{'oldam','saldam','doldam'}):continue
            w=current.pop();left={v[i-1][1] if i and v[i-1][0]==v[i][0] else None for v in vs};prior=left.pop() if len(left)==1 else None
            if prior and not re.fullmatch('[a-z]+',prior):prior=None
            opts=sorted(before[w]);sites.append(dict(loc=loc,rang=i+1,ancre=w,avant=prior,predictions=opts,succes=prior in opts if prior and opts else None))
    save('VERIFICATION.json',dict(temoin=calibration(),voisins_de_reserve=sites))


if __name__=='__main__':
    if sys.argv[1]=='annoncer':announce(Path(sys.argv[2]))
    else:verify()
