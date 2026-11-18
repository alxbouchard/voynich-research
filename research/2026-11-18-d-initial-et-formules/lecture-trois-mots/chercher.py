"""Tester une même lecture par lettres ou digrammes sur les quatre triplés."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from random import Random
import gzip,json,sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-phrase-et-doublets/lecture'))
from corpus_sources import LATIN,celsus
U=('q','o','k','e','e')
SHORT=U+('y',)
PREFIX=[(('d','a','i','n'),('ch','e','y')),(('s','a','i','i','n'),('sh','e','y'))]

def extend(signs,word,cap,mapping):
    if len(word)<len(signs) or len(word)>cap*len(signs):return
    if not signs:
        if not word:yield mapping
        return
    sign=signs[0]
    if sign in mapping:
        value=mapping[sign]
        if word.startswith(value):yield from extend(signs[1:],word[len(value):],cap,mapping)
        return
    for size in range(1,min(cap,len(word))+1):
        value=word[:size]
        if value not in mapping.values():
            yield from extend(signs[1:],word[size:],cap,{**mapping,sign:value})

def index(corpus):
    words=set(); triples=defaultdict(dict)
    for loc,ws in corpus.items():
        words.update(ws)
        for i,(a,b,c) in enumerate(zip(ws,ws[1:],ws[2:])):
            triples[c].setdefault((a,b),(loc,i+1))
    return words,triples

def search(third,prefix,cap,corpus):
    vocab,tri=corpus
    hits=[]; lexical=0; word_pairs=set()
    for c in sorted(vocab):
        for m in extend(third,c,cap,{}):
            lexical+=1
            if len(third)>len(SHORT):
                sister=''.join(m[g] for g in SHORT)
                if sister in vocab:word_pairs.add((c,sister))
            for (a,b),loc in tri.get(c,{}).items():
                # The last two glyphs of the second word already have fixed values.
                if not b.endswith(m['e']+m['y']):continue
                for bmap in extend(prefix[1],b,cap,m):
                    for final in extend(prefix[0],a,cap,bmap):
                        hits.append((a,b,c,loc,final))
    return hits,lexical,word_pairs

def compatible(a,b):
    k={**a,**b}
    return all(k[g]==v for g,v in a.items()) and len(set(k.values()))==len(k)

def analyze(encoded,cap,mute,corpus):
    bycontext=[];results={}
    for i,(a,b) in enumerate(PREFIX):
        local=(a[1:] if mute and i==0 else a,b)
        longform=U+(encoded,'y')
        lh,lwords,lexpairs=search(longform,local,cap,corpus)
        sh,swords,_=search(SHORT,local,cap,corpus)
        paired=[]
        for xa,xb,xc,loc,m in lh:
            short=''.join(m[s] for s in SHORT)
            other=corpus[1].get(short,{}).get((xa,xb))
            if other:paired.append([xa,xb,xc,short,loc,other,m])
        bycontext.append(paired)
        results[str(i)]={'lectures_longues':lh,'lectures_courtes':sh,'couples':paired,
                  'segmentations_mot_long':lwords,'segmentations_mot_court':swords,
                  'paires_mots_seuls':len(lexpairs),'exemples_mots_seuls':sorted(lexpairs)[:8]}
    results['tables_communes']=[{**a[-1],**b[-1]} for a in bycontext[0] for b in bycontext[1] if compatible(a[-1],b[-1])]
    return results

def positive(corpus):
    originals=list(corpus.values())[0][:3]
    # Inventaire de valeurs d'une ou deux lettres, avec un chiffrement fixé sans consulter le solveur.
    chunks=[]
    for word in originals:
        out=[]
        while word:
            value=next((v for v in ('qu','er') if word.startswith(v)),word[0])
            out.append(value);word=word[len(value):]
        chunks.append(out)
    values=sorted(set(sum(chunks,[])));alphabet=list('abcdefghijklmnopqrstuvwxyz')
    Random(8436).shuffle(alphabet)
    hidden=dict(zip(values,alphabet));shapes=[[hidden[v] for v in row] for row in chunks]
    # Retrouver toutes les lectures à partir du motif seul et du corpus entier.
    found=[]
    vocab,tri=index(corpus)
    for c in vocab:
        for m in extend(shapes[2],c,2,{}):
            for (a,b),loc in tri.get(c,{}).items():
                for mm in extend(shapes[1],b,2,m):
                    for final in extend(shapes[0],a,2,mm):
                        found.append(([a,b,c],final))
    secret={g:k for k,g in hidden.items()}
    assert (originals,secret) in found and max(map(len,secret.values()))==2
    return {'mots_source':originals,'groupes_chiffres':shapes,'solutions':len(found),'vraie_cle':secret,'vraie_cle_retrouvee':True}

def main(xml):
    merc=json.loads(LATIN.read_bytes())
    output={'calibration':positive(merc),'corpus':{},'sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in (LATIN,xml)}}
    for name,data in [('Macer',merc),('Celse',celsus(xml,r'[.;:!?]'))]:
        corpus=index(data)
        obj={'passages':len(data),'mots':sum(map(len,data.values())),'vocabulaire':len(corpus[0]),'modeles':{}}
        for cap in (1,2):
            for mute in (False,True):
                for g in ('d','a','i','n','ch','e','y','s','sh'):
                    k=f'{cap}/'+('muet' if mute else 'lu')+'/'+g
                    obj['modeles'][k]=analyze(g,cap,mute,corpus)
        output['corpus'][name]=obj
    raw=(json.dumps(output,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    (HERE/'RESULTATS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
if __name__=='__main__':main(Path(sys.argv[1]))
