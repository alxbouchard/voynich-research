"""Prédire un ou deux mots par la graphie longue, sa base ou leur regroupement."""
import argparse
from collections import Counter, defaultdict
import gzip
import json
from math import log2
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, metadata, segment

MODELS=("identite","regroupe","court","position")

def save(name,data):
    blob=(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    (HERE/name).write_bytes(gzip.compress(blob,mtime=0) if name.endswith('.gz') else blob)

def read(name):
    data=(HERE/name).read_bytes()
    return json.loads(gzip.decompress(data) if name.endswith('.gz') else data)

def lots(page,meta):
    n=int(re.match(r'f(\d+)',page)[1])
    if meta.get("Q")=="T": return "dernier"
    if meta.get("I")=="B" or (meta.get("I")=="H" and meta.get("H")=="1" and n<=25): return "apprentissage"
    if (meta.get("I"),meta.get("H"),meta.get("L"))==("H","2","B"): return "herbier_B"
    return "autres"

def windows():
    ed,_=corpus()
    meta=metadata()
    for loc,(page,typ,_,_) in ed["H"].items():
        if typ!="P0" or loc not in ed["ZL"] or ed["ZL"][loc][1]!="P0":continue
        m=meta[page];lot=lots(page,m)
        rows=list(aligned(ed,loc,page,m.get("I"),page,Counter()))
        for i,row in enumerate(rows):
            ids=tuple(map(int,row["rangs_quatre"].split("/")))
            following=[]
            for offset,nextrow in enumerate(rows[i+1:i+3],1):
                ranks=tuple(map(int,nextrow["rangs_quatre"].split("/")))
                if nextrow['troncon']!=row['troncon'] or not all(a+offset==b for a,b in zip(ids,ranks)):break
                following.append(nextrow['mot'])
            yield {"lieu":f"{loc}/{row['troncon']}/{ids[0]}","lot":lot,"page":page,"ancre":row['mot'],
                   "initial":"debut" in row['positions'],"suite":following}

def categories(word,vocab):
    u=tuple(segment(word))
    if len(u)<2 or u[0]!="d": return []
    tags=[]
    if word=="dshedy":tags.append("dshedy")
    if u[1] in ("ch","sh"):tags.append("ch_sh")
    if len(u[1:])>=2 and word[1:] in vocab:tags.append("base_attestee")
    return tags

def extract(mode):
    allrows=list(windows())
    train=[r for r in allrows if r["lot"]=="apprentissage"]
    vocab={r["ancre"] for r in train}
    masks=[];actual={}
    for r in allrows:
        word=r["ancre"]
        classes=categories(word,vocab)
        if not r["initial"] or not classes or r["lot"]=="apprentissage":continue
        mask={k:r[k] for k in ("lieu","ancre","lot","page")}
        mask['classes']=classes
        if mode=="C":
            if not r['suite']:continue
            mask["deuxieme"]=r['suite'][0]
        masks.append(mask)
        actual[r['lieu']]=r['suite']
    if mode=="AB":save("APPRENTISSAGE.json.gz",train)
    if mode!="ouverture":save(f"MASQUES-{mode}.json.gz",masks)
    return actual

def store():
    return defaultdict(Counter)

def fit(data):
    vocab={r["ancre"] for r in data}
    model={n:{m:store() for m in ("brut","regroupe","fond")} for n in "ABC"}
    for r in data:
        w=r['ancre']; seq=r['suite']
        folded=w[1:] if r["initial"] and categories(w,vocab) else w
        for t in "ABC":
            if len(seq)<(1 if t=="A" else 2):continue
            second=seq[0] if t=="C" else ""
            out=seq[0] if t=="A" else " ".join(seq) if t=="B" else seq[1]
            model[t]["brut"][w,second][out]+=1
            model[t]["regroupe"][folded,second][out]+=1
            if r["initial"]:
                model[t]["fond"][second][out]+=1
                if t=="C":model[t]["fond"][""][out]+=1
    return model,vocab

def distributions(model,row,t):
    w=row["ancre"];second=row.get("deuxieme","") if t=="C" else ""
    m=model[t]
    fond=m["fond"].get(second) or m["fond"][""]
    return {"identite":m["brut"].get((w,second),{}),
            "regroupe":m["regroupe"].get((w[1:],second),{}),
            "court":m["brut"].get((w[1:],second),{}),
            "position":fond}

def top(counts):
    return sorted(counts,key=lambda s:(-counts[s],s))[:3]

def announce(mode):
    model,_=fit(read('APPRENTISSAGE.json.gz'))
    masks=read(f"MASQUES-{mode}.json.gz")
    rows={}
    for item in masks:
        ans={}
        for t in mode:
            ds=distributions(model,item,t)
            ans[t]={m:{"choix":top(c or ds['position']),"appui":sum(c.values())} for m,c in ds.items()}
        rows[item['lieu']]={**item,"annonces":ans}
    save(f"ANNONCES-{mode}.json.gz",rows)

def evaluate():
    actual=extract("ouverture")
    model,vocab=fit(read("APPRENTISSAGE.json.gz"))
    stat=defaultdict(lambda:defaultdict(Counter))
    changes=defaultdict(Counter)
    details={}
    for mode in ("AB","C"):
        for key,row in read(f"ANNONCES-{mode}.json.gz").items():
            seq=actual[key]
            if mode=="C":assert row["deuxieme"]==seq[0]
            result=details.setdefault(key,{"lot":row["lot"],"ancre":row["ancre"],"vrai":seq,"epreuves":{}})
            for t in mode:
                if len(seq)<(1 if t=="A" else 2):continue
                y=seq[0] if t=="A" else " ".join(seq) if t=="B" else seq[1]
                ds=distributions(model,row,t)
                pred=row['annonces'][t]
                probs={}
                if t=="A":
                    bg=ds["position"]
                    pbg=(bg.get(y,0)+1)/(sum(bg.values())+len(vocab)+1)
                    for m,c in ds.items():
                        probs[m]=(c.get(y,0)+5*pbg)/(sum(c.values())+5) if m!="position" else pbg
                result["epreuves"][t]={m:v['choix'][0] for m,v in pred.items()}
                groups=list(row['classes'])
                if "ch_sh" in groups and row["ancre"]!="dshedy":groups.append("ch_sh_sans_dshedy")
                for group in groups:
                    tag='/'.join((row['lot'],group,t))
                    for m,p in pred.items():
                        hits=stat[tag][m];hits['n']+=1;hits['appui']+=bool(p['appui'])
                        hits['exact']+=p['choix'][0]==y;hits['trois']+=y in p['choix']
                        if t=="A":hits['bits']-=log2(probs[m])
                    a,b=(pred[m]['choix'][0] for m in ("regroupe","identite"))
                    if a!=b:
                        v=changes[tag];v['changements']+=1;v['gains']+=a==y;v['pertes']+=b==y
                    if t=='A':
                        leaf=re.match(r'f\d+',key)[0]; stat_by_leaf=stat[tag+'/feuilles'][leaf]
                        stat_by_leaf['n']+=1
                        stat_by_leaf['gain_bits']+=log2(probs["regroupe"]/probs["identite"])
    save('COMPARAISONS.json',{'scores':stat,'reponses_modifiees':changes})
    save('OUVERTURES.json.gz',details)

if __name__=="__main__":
    par=argparse.ArgumentParser(description=__doc__)
    par.add_argument('mode',choices=["masquer_AB","annoncer_AB","masquer_C","annoncer_C","verifier"])
    cmd=par.parse_args().mode
    if cmd.startswith("masquer_"):extract(cmd.split("_")[1])
    elif cmd.startswith("annoncer_"):announce(cmd.split("_")[1])
    else:evaluate()
