"""Comparer deux passages partageant X Y et différant à la troisième position."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from croiser import adjacent, load, save, texts
sys.path.insert(0,str(HERE.parents[1]/"2026-11-18-opcheor-suite/cle"))
from chercher import corpora, extend, segment
sys.path.insert(0,str(HERE.parents[1]/"2026-11-18-d-initial-et-formules/vernaculaire"))
from corpus_vern import sources

CIPHER=("qokol","daiin","oky")
SOURCE=("f18v","f18v.7")
TARGET=("f102r2","f102r2.18")


def read_books(xml,fr,it):
    books=corpora(xml)
    for name,records in sources(fr,it).items():
        books[name]={str(i)+" "+str(loc):list(row) for i,(loc,row) in enumerate(records)}
    return books


def code(word,mode):
    seq=segment(word)
    if mode=="EVA":return seq
    join=("i","i") if mode=="ii" else ("a","i","i","n")
    parts=[];i=0
    while i<len(seq):
        if seq[i:i+len(join)]==join:
            parts.append(mode);i+=len(join)
        else:
            parts.append(seq[i]);i+=1
    return tuple(parts)


def signs_for(plaintext):
    for mode in ("EVA","ii","aiin"):
        shapes=[code(w,mode) for w in CIPHER]
        for mute in [None,*sorted(set(sum(shapes,())))]:
            keys=[{}]
            for part,w in zip(shapes,plaintext):
                spoken=[g for g in part if g!=mute]
                keys=[k for start in keys for k in extend(spoken,w,2,start)]
                if not keys:break
            for key in keys:
                if mute:key={**key,mute:""}
                yield mode,mute,key


def inverse(word,key):
    if word is None:return []
    @lru_cache(maxsize=None)
    def visit(start):
        if start==len(word):return [""]
        return [g+rest for g,v in key.items() if v and word.startswith(v,start)
                for rest in visit(start+len(v))]
    return sorted(set(visit(0)))


def book_announcements(body):
    triples=defaultdict(list)
    for loc,words in body.items():
        for i,(x,y,z) in enumerate(zip(words,words[1:],words[2:])):
            if x==y:continue
            triples[(x,y)].append((z,loc,i))
    announcements=[]
    for (x,y),contexts in triples.items():
        repeats=[(place,i) for z,place,i in contexts if z==x]
        if not repeats:continue
        for z,place2,j in contexts:
            if z in (x,y):continue
            keys=list(signs_for((x,y,z)))
            for place1,i in repeats:
                w1,w2=body[place1],body[place2]
                neighbors=[w1[i-1] if i else None,w1[i+3] if i+3<len(w1) else None,
                           w2[j-1] if j else None,w2[j+3] if j+3<len(w2) else None]
                lexical=dict(zip((x,y,z),CIPHER))
                predicted=[lexical.get(w) for w in neighbors]
                forecasts=[dict(mode=mode,muet=mute,table=k,prevus=[inverse(w,k) for w in neighbors])
                           for mode,mute,k in keys]
                announcements.append(dict(triple=[x,y,z],source=[place1,i+1],autre=[place2,j+1],
                                          autour=neighbors,lexique=predicted,signes=forecasts))
    return announcements


def selected():
    rows=[texts("plantes",True)[SOURCE[0]],texts("panneaux",True)[TARGET[0]]]
    out=[]
    for source,(page,loc),third in zip(rows,(SOURCE,TARGET),(CIPHER[0],CIPHER[2])):
        line=[r for r in source if r[1]==loc]
        hits=[i for i in range(len(line)-2) if tuple(r[0] for r in line[i:i+3])==(*CIPHER[:2],third)
              and adjacent(line[i],line[i+1]) and adjacent(line[i+1],line[i+2])]
        assert len(hits)==1
        i=hits[0]
        out.extend([line[i-1][0] if i and adjacent(line[i-1],line[i]) else None,
                    line[i+3][0] if i+3<len(line) and adjacent(line[i+2],line[i+3]) else None])
    return out


def open_contexts(ann):
    obs=selected(); out={}
    for name,rows in ann.items():
        stats=Counter(); selected_examples=[];sign_rows=[]
        for i,r in enumerate(rows):
            known=[(w,h) for w,h in zip(obs,r["lexique"]) if w and h]
            n=len(known);right=sum(w==h for w,h in known)
            stats["solutions_mots"]+=1;stats["mots_comparables"]+=n;stats["mots_exacts"]+=right
            # Une égalité du modèle par mots doit rester compatible avec ses trois équivalences.
            compatible={g:w for g,w in zip(CIPHER,r["triple"])}
            unique={v:k for k,v in compatible.items()}
            possible=True
            for g,w in zip(obs,r["autour"]):
                if not g or not w:continue
                if compatible.get(g,w)!=w or unique.get(w,g)!=g:possible=False;break
                compatible[g]=w;unique[w]=g
            if right:selected_examples.append(dict(indice=i,comparables=n,justes=right,compatibilite=possible))
            stats["extensions_mots_coherentes"]+=possible
            for t in r["signes"]:
                k=t["table"]
                proposed=[(g,guesses) for g,guesses in zip(obs,t["prevus"]) if g and guesses]
                exact=sum(g in opts for g,opts in proposed)
                ext=[k]
                individually=[]
                for g,w in zip(obs,r["autour"]):
                    if not g or not w:individually.append(None);continue
                    units=[c for c in code(g,t["mode"]) if c!=t["muet"]]
                    individually.append(bool(list(extend(units,w,2,k))))
                    ext=[new for m in ext for new in extend(units,w,2,m)]
                stats["solutions_signes"]+=1;stats["predictions_signes"]+=len(proposed)
                stats["succes_signes"]+=exact;stats["extensions_signes_coherentes"]+=bool(ext)
                sign_rows.append(dict(indice=i,**t,individuellement=individually,predictions=len(proposed),succes=exact,
                                      extensions=ext))
        out[name]={"bilan":dict(stats),"mots_avec_une_confirmation":selected_examples,"signes":sign_rows}
    return {"voisins":obs,"corpus":out}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("annoncer","ouvrir"));p.add_argument("sources",nargs="*",type=Path)
    a=p.parse_args();file=HERE/"INTERPRETATIONS.json.gz"
    if a.mode=="annoncer":
        books=read_books(*a.sources)
        save(file,{"sha256":{str(i.name):sha256(i.read_bytes()).hexdigest() for i in a.sources},
                   "corpus":{n:book_announcements(b) for n,b in books.items()}})
    else:save(HERE/"VOISINS.json.gz",open_contexts(load(file)["corpus"]))
