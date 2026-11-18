"""Même mot = même groupe : déposer une prévision avant d'accéder à la suite d'une ligne."""
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/"2026-11-18-opcheor-paralleles/variantes"))
from compter import GAP, corpus, tokens


def save(name,value):
    data=(json.dumps(value,indent=1,ensure_ascii=False)+"\n").encode()
    target=HERE/name
    if target.suffix==".gz":
        data=gzip.compress(data,mtime=0)
    target.write_bytes(data)


def load(name):
    path=HERE/name
    data=path.read_bytes()
    if path.suffix==".gz":
        data=gzip.decompress(data)
    return json.loads(data)


def norm(text):
    text="".join(c for c in unicodedata.normalize("NFD",text.lower()) if not unicodedata.combining(c))
    return tuple(re.findall("[a-z]+",text.replace("œ","oe").replace("æ","ae")))


def books():
    return [(r["section"],r["ref"],norm(r["texte"])) for r in load("CORPUS.json")]


@lru_cache(maxsize=32768)
def shape(seq):
    vocabulary={}
    return tuple(vocabulary.setdefault(w,len(vocabulary)) for w in seq)


def tier(signature):
    reps=Counter(signature)
    if sum(n>=2 for n in reps.values())>=2:
        return "principal"
    if len(reps)<=4 and max(reps.values(),default=0)>1:
        return "souple"
    return None


def catalog(parts,n):
    result=defaultdict(list)
    for section,ref,words in parts:
        for i in range(len(words)-n-1):
            train=words[i:i+n]
            pat=shape(train)
            if tier(pat):
                result[pat].append((section,ref,i+1,train,words[i+n:i+n+2]))
    return result


def each_view(raw,cut):
    out=[]
    for seg,piece in enumerate(GAP.split(raw)):
        for w in tokens(re.sub(r"\{[^}]*\}","?",piece),cut):
            out.append((seg,w))
    return tuple(out)


def pages():
    editions,_=corpus()
    result={}
    for loc in sorted(set.intersection(*(set(d) for d in editions.values())),key=order_locus):
        if not re.fullmatch(r"f(?:7[5-9]|8[0-4])[rv]\.\d+",loc):
            continue
        records=[rows[loc] for rows in editions.values()]
        if all(r[1]=="P0" for r in records):
            result[loc]=[each_view(r[3],cut) for r in records for cut in ("joints","separes")]
    return result


def order_locus(loc):
    return tuple(int(s) if s.isdigit() else s for s in re.split(r"(\d+)",loc))


def window(views,start,n):
    candidates=[]
    for view in views:
        span=view[start:start+n]
        if len(span)!=n or span[0][0]!=span[-1][0]:
            return None
        seq=tuple(w for _,w in span)
        if any(not re.fullmatch("[a-z]+",w) for w in seq):
            return None
        candidates.append(seq)
    return candidates[0] if len(set(candidates))==1 else None


def forward(train, after, eva):
    key=dict(zip(train,eva))
    return [key.get(w) for w in after]


def predict_sites(data, lookup, n=6, stride=8, strict=False):
    rows=[]
    stats=Counter()
    for loc,views in data.items():
        for i in range(0,min(map(len,views))-n+1,stride):
            stats["departs"]+=1
            given=window(views,i,n)
            if given is None:continue
            stats["prefixes_concordants"]+=1
            pat=shape(given)
            t=tier(pat)
            if not t or (strict and t!="principal"):continue
            stats[t]+=1
            possibilities=[]
            for book,ref,k,train,after in lookup.get(pat,[]):
                pred=forward(train,after,given)
                possibilities.append(dict(section=book,ref=ref,rang=k,fr=train,suite=after,annonce=pred))
            rows.append(dict(lieu=loc,rang=i+1,n=n,critere=t,amorce=given,lectures=possibilities))
    return dict(compteurs=dict(stats),blocs=rows)


def verify_sites(data, predicted):
    out=[]
    for row in predicted["blocs"]:
        i=row["rang"]-1
        n=row["n"]
        views=data[row["lieu"]]
        actual=[]
        for j in (1,2):
            seq=window(views,i,n+j)
            actual.append(seq[-1] if seq else None)
        # An unreadable first target can still leave the second readable. Keep the
        # primary strict contiguous and report the inability to judge it as a gap.
        outcome=[]
        for k,opt in enumerate(row["lectures"]):
            calls=opt["annonce"]
            right=[None if w is None or a is None else w==a for w,a in zip(calls,actual)]
            known=all(a is not None for a in actual)
            full=known and shape(tuple(row["amorce"])+tuple(actual))==shape(tuple(opt["fr"])+tuple(opt["suite"]))
            outcome.append(dict(id=k,justes=right,compatible=full))
        out.append(dict(lieu=row["lieu"],rang=row["rang"],n=n,cible=actual,issues=outcome))
    return out


def summarize(rows,checks,section,t):
    c=Counter()
    candidates=[]
    for row,ver in zip(rows,checks,strict=True):
        if row["critere"]!=t:continue
        c["blocs_motif"]+=1
        opts=[(opt,check) for opt,check in zip(row["lectures"],ver["issues"],strict=True) if opt["section"]==section]
        if not opts:continue
        c["blocs_alignables"]+=1
        c["alignements"]+=len(opts)
        if all(ver["cible"]):c["blocs_deux_cibles_lisibles"]+=1
        for k in (0,1):
            known={opt["annonce"][k] for opt,check in opts if opt["annonce"][k] is not None}
            if len(known)==1 and ver["cible"][k] is not None:
                c["positions_avec_consensus"]+=1
                c["positions_justes"]+=int(ver["cible"][k] in known)
        for opt,check in opts:
            if check["compatible"]:
                c["alignements_integraux"]+=1
            if check["compatible"] and any(ok is True for ok in check["justes"]):
                c["alignements_confirmes_avec_prevision"]+=1
                candidates.append(dict(lieu=row["lieu"],rang=row["rang"],n=row["n"],fr=opt["fr"],suite=opt["suite"],
                    ref=opt["ref"],indice=opt["rang"],eva=row["amorce"],apres=ver["cible"],
                    verifies=sum(ok is True for ok in check["justes"])))
    return dict(comptes=dict(c),candidats=candidates)


if __name__=="__main__":
    data=pages()
    if sys.argv[1]=="predire":
        save("PREDICTIONS.json.gz",predict_sites(data,catalog(books(),6)))
    elif sys.argv[1]=="verifier":
        ps=load("PREDICTIONS.json.gz")
        checked=verify_sites(data,ps)
        save("CONTROLE.json.gz",dict(verification=checked,resume={s:{t:summarize(ps["blocs"],checked,s,t)
             for t in ("principal","souple")} for s in ("bain","exercice")}))
    else:
        raise ValueError("predire ou verifier")
