"""Épreuve d’une formule à deux mots, avec successeurs masqués ou révélés."""
from collections import Counter, defaultdict
from functools import lru_cache
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
sys.path.insert(0,str(RESEARCH/"2026-11-18-baigneuses-et-conduits"/"lecture"))
import confronter as ref
from transfert import corpus, langage, tokens

FORMULAS=[("tollit","genus","omne"),("breve","nomen","habet"),
          ("splene","tumente","iecur"),("et","si","forte")]
MODES=("ligne","local")
BREAK=re.compile(r"<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>",re.I)
SIMPLE=re.compile(r"[a-z]+")
SEED=20261118


def write(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=1)+"\n").encode()
    (HERE/name).write_bytes(gzip.compress(data,mtime=0) if name.endswith(".gz") else data)


def read(name):
    return ref.read(HERE/name)


def words(lines):
    return [(i,j,k,tuple(w[k:k+3])) for i,chapter in enumerate(lines) for j,w in enumerate(chapter,1)
            for k in range(len(w)-2)]


def latin(folder):
    path=folder/"vers.json"
    assert sha256(path.read_bytes()).hexdigest()==ref.read(ref.HERE/"SOURCE.json")["sha256"]
    data=ref.read(path)
    return data,[[ref.words(line) for line in c["vers"]] for c in data]


def fit(seq,tgt,width):
    if not all(len(a)<=len(b)<=len(a)*width for a,b in zip(seq,tgt)): return []
    src=(*seq[0]," ",*seq[1])
    return [k for k in ref.tables(src," ".join(tgt),width)
            if width!=1 or len(set(k.values()))==len(k)]


def extend(seq,text,width,key):
    if not len(seq)<=len(text)<=len(seq)*width:return []
    return [k for k in ref.tables(seq,text,width,key) if width!=1 or len(set(k.values()))==len(k)]


def parse(raw,space):
    stream=[]
    for j,span in enumerate(BREAK.split(raw)):
        if j:stream.append(None)
        stream.extend(tokens(span,space))
    return stream


def anchors(seq):
    table=defaultdict(list)
    for i in range(len(seq)-2):
        a,b,c=seq[i:i+3]
        if a and b and c and SIMPLE.fullmatch(a) and SIMPLE.fullmatch(b):
            table[a,b].append(i)
    return table


def records():
    batches,_=corpus()
    meta={}
    for line in (langage.DATA/"ZL3b-n.txt").read_text().splitlines():
        page=re.match(r"^<(f\d+[rv])>",line)
        if page and "$Q=M " in line:meta[page[1]]=int(re.search(r"\$B=(\d+)",line)[1])
    result={m:[] for m in MODES}
    stats=Counter()
    raw={}
    for loc in sorted(set.union(*(set(x) for x in batches.values())),
                      key=lambda loc:(int(re.search(r'\d+',loc)[0]) if re.search(r'\d+',loc) else -1,loc.split('.')[0],int(loc.split('.')[1]))):
        face=loc.split(".")[0]
        if face not in meta:continue
        src=[ed.get(loc) for ed in batches.values()]
        if not all(r and r[1] in ("P0","P1","Pb","Pc","Pr","Pt") for r in src):continue
        stats["lignes_prose"]+=1
        vs=[parse(r[3],cut) for r in src for cut in ("joints","separes")]
        raw[loc]=vs
        ads=[anchors(v) for v in vs]
        same_layout=len({(len(v),tuple(i for i,w in enumerate(v) if w is None)) for v in vs})==1
        if same_layout:stats["lignes_meme_disposition"]+=1
        any_s={m:False for m in MODES}
        stats["places_H_jointes_avant_concordance"]+=sum(map(len,ads[0].values()))
        for pair,indices in ads[0].items():
            for i in indices:
                def add(mode,coord):
                    rec=dict(lieu=loc,face=face,bifeuillet=meta[face],rang=i+1,positions=coord,
                             amorce=pair)
                    result[mode].append(rec)
                    any_s[mode]=True
                if same_layout and all(i in a.get(pair,()) for a in ads[1:]):
                    add("ligne",[i]*4)
                if all(len(a.get(pair,()))==1 for a in ads):
                    add("local",[a[pair][0] for a in ads])
        for mode in MODES: stats["lignes_avec_places_"+mode]+=int(any_s[mode])
    for m in MODES:stats["places_"+m]=len(result[m])
    return result,stats,raw


def reveal(site,raw):
    third=[seq[i+2] for seq,i in zip(raw[site["lieu"]],site["positions"])]
    return third[0] if len(set(third))==1 and SIMPLE.fullmatch(third[0]) else None


def label(x):
    return f"{x['lieu']}@{x['rang']}"


@lru_cache(None)
def candidates(pair,latin_pair,width):
    return fit([ref.units(w) for w in pair],latin_pair,width)


def predictions():
    inventory,stats,raw=records()
    all_sets={}
    for mode,rows in inventory.items():
        groups=defaultdict(list)
        for s in rows:groups[s["amorce"]].append(s)
        repeated={p:l for p,l in groups.items() if len({s["bifeuillet"] for s in l})>=2}
        order=sorted(repeated,key=lambda p:(-len({s["bifeuillet"] for s in repeated[p]}),-len(repeated[p]),p))
        forecasts=[]
        for p in order:
            occurrences=repeated[p]
            source=occurrences[0]
            guess=reveal(source,raw)
            forecasts.append(dict(amorce=p,source=source,mot_annonce=guess,
                reserve=[s for s in occurrences if s["bifeuillet"]!=source["bifeuillet"]]))
        latin_calls=[]
        for a,b,c in FORMULAS:
            for width in (1,2):
                for p,occs in groups.items():
                    keys=candidates(p,(a,b),width)
                    if keys:
                        latin_calls.append(dict(formule=[a,b,c],amorce=p,largeur=width,cles=keys,
                            repetee_entre_bifeuillets=p in repeated,lieux=occs))
        all_sets[mode]={"amorces_distinctes":len(groups),"repetitions":forecasts,"hypotheses_latines":latin_calls}
    write("PREDICTIONS.json.gz",dict(couverture=stats,experiences=all_sets))


def cipher(lines):
    # La table du générateur ne quitte pas cette fonction.
    alphabet=sorted({c for chapter in lines for line in chapter for w in line for c in w})
    ciphertext=alphabet[:]
    Random(20261118).shuffle(ciphertext)
    key=dict(zip(alphabet,ciphertext))
    return [[[tuple(key[c] for c in w) for w in line] for line in ch] for ch in lines]


def calibrate(folder):
    corpus,lines=latin(folder)
    clear=words(lines)
    crypt=words(cipher(lines))
    out={}
    for a,b,c in FORMULAS:
        authentic=[(i,j,k) for i,j,k,seq in clear if seq==(a,b,c)]
        known=[(i,j,k,seq) for i,j,k,seq in crypt if (i,j,k) in authentic]
        training=[]
        for i,j,k,seq in known:
            mapping=fit(seq[:2],(a,b),1)[0]
            complete=extend(seq[2],c,1,mapping)
            assert len(complete)==1
            training.append((i,{"notice":i,"vers":j,"rang":k+1},complete[0]))
        calls=[]
        shape=[(i,j,k,seq) for i,j,k,seq in crypt if fit(seq[:2],(a,b),1)]
        expectations=[]
        for ch in range(len(lines)):
            _,source,key=next(x for x in training if x[0]!=ch)
            rev={v:s for s,v in key.items()}
            forecast=tuple(rev[t] for t in c)
            pool=[seq[2] for i,j,k,seq in crypt if i==ch]
            for i,j,k,seq in shape:
                if i!=ch or not all(ref.decode(w,key)==t for w,t in zip(seq[:2],(a,b))):continue
                calls.append(dict(notice=i,vers=j,rang=k+1,appris=source,predit="".join(forecast),
                                  observe="".join(seq[2]),mot_latin=c,correct=forecast==seq[2]))
                expectations.append(pool.count(forecast)/len(pool))
        out[" ".join((a,b,c))]=dict(lignes=[dict(notice=i,titre=corpus[i]["titre"],vers=j,
                texte=corpus[i]["vers"][j-1]) for i,j,k in authentic],
            cle_inconnue=dict(lieux_de_meme_forme_de_deux_mots=len(shape),previsions=calls,
                 verifiees=sum(r["correct"] for r in calls),
                 reussites_attendues_successeurs_reaffectes=sum(expectations)))
    print({g:(v["cle_inconnue"]["lieux_de_meme_forme_de_deux_mots"],v["cle_inconnue"]["verifiees"]) for g,v in out.items()})
    write("LATIN.json",out)


if __name__=="__main__":
    if sys.argv[1]=="calibrer":calibrate(Path(sys.argv[2]))
    elif sys.argv[1]=="predire":predictions()
    else: raise ValueError("calibrer ou predire")
