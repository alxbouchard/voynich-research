"""Essayer la même lecture corrigée avant et après les quatre mots connus."""
from collections import Counter
from pathlib import Path
import gzip
import json
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/"cle"))
from chercher import celsus, extend, segment
sys.path.insert(0,str(HERE.parents[1]))
from suites import adjacent, aligned, corpus


def groups(word):
    u=segment(word)
    def combine(seq,left,right,result):
        i=0
        while i<len(seq):
            if i+1<len(seq) and (seq[i],seq[i+1])==(left,right):
                yield result
                i+=2
            else:
                yield seq[i]
                i+=1
    first=list(combine(u,"e","e","e+e"))
    second=list(combine(first,"ch","e","ch"))
    return tuple(combine(second,"o","l","o+l"))


def translated(word,key):
    u=groups(word)
    if all(g in key for g in u):
        return "".join(key[g] for g in u)
    return None


def windows():
    editions,sections=corpus()
    for loc,(face,kind,*_) in editions["H"].items():
        n=int(re.match(r"f(\d+)",face)[1])
        if n in {52,89,96,100} or kind!="P0" or loc not in editions["ZL"] or editions["ZL"][loc][1]!=kind:
            continue
        rows=list(aligned(editions,loc,face,sections[face],n,Counter()))
        for i,r in enumerate(rows):
            for length in (2,3):
                group=rows[i:i+length]
                if len(group)==length and all(adjacent(a,b) for a,b in zip(group,group[1:])):
                    yield (loc,r["troncon"],r["rang_troncon_IT"]),tuple(x["mot"] for x in group)


def check(xml):
    body=celsus(xml,r"[.;:!?]")
    corpus_digest=gzip.decompress((HERE.parent/"LECTURES-ANNONCEES.json.gz").read_bytes())
    fits=json.loads(corpus_digest)["Celse"]["avec_autre"]
    held={k:v for k,v in body.items() if ".".join(k.split(".")[:2]) not in {"3.22","4.23","5.26"}}
    lookup={}
    for n in (2,3):
        lookup[n]={tuple(words[i:i+n]) for words in held.values() for i in range(len(words)-n+1)}
    counter=Counter(w for line in body.values() for w in line)
    empirical=list(windows())
    out=[]
    for row in fits:
        key=row["table"]
        n52,p,_=row["f52"]
        n100,q,_=row["autre"][1:]
        def context(loc,start,n):
            text=body[loc]; i=start-1
            return [text[i-1] if i else None,text[i:i+n],text[i+n] if i+n<len(text) else None]
        l52,words,r52=context(n52,p,4)
        l100,words100,r100=context(n100,q,3)
        assert [translated(w,key) for w in ("ctheor","ctheol","cheeor","cheol")]==words
        assert [translated(w,key) for w in ("okeor","okeol","dy")]==words100
        candidates=[key]; checks={}
        for label,w,expected in [("f52_gauche","tchor",l52),("f52_droite","chckheey",r52),("f100_gauche","ches",l100)]:
            shape=groups(w)
            valid=lambda plaintext: next(extend(shape,plaintext,2,key),None) is not None
            independent=list(extend(shape,expected,2,key)) if expected else []
            background=sum(n for word,n in counter.items() if valid(word))
            if expected:
                candidates=[nk for k in candidates for nk in extend(shape,expected,2,k)]
            checks[label]=dict(signes=shape,observe=expected,tables=independent,
                               temoins_compatibles=background,temoins_total=sum(counter.values()))
        tally=Counter(); examples=[]
        for loc,sequence in empirical:
            text=tuple(translated(x,key) for x in sequence)
            if None in text:continue
            n=len(text);tally[str(n)]+=1
            if text in lookup[n]:
                tally[str(n)+"_atteste"]+=1;examples.append([loc,sequence,text])
        out.append(dict(table=key,source52=[n52,p,l52,words,r52],source100=[n100,q,l100,words100,r100],
                        controles=checks,extensions_conjointes=candidates,photos_a_recouper=words,
                        ailleurs=tally,correspondances=examples))
    (HERE/"RESULTATS.json").write_text(json.dumps(out,ensure_ascii=False,indent=1,sort_keys=True)+"\n")


if __name__=="__main__":
    check(Path(sys.argv[1]))
