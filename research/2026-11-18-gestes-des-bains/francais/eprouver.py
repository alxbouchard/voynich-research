"""Relectures de toutes les positions et témoins à vocabulaire caché ou mélangé."""
from collections import Counter
from random import Random
import re
from mots import (GAP,books,catalog,corpus,forward,load,norm,pages,predict_sites,
                  save,shape,summarize,tier,tokens,verify_sites,window)


def bridged(data):
    # Tag soft drawing gaps and hard breaks differently; crossings must be one soft gap only.
    by_ed,_=corpus()
    out={}
    for loc in data:
        views=[]
        for rows in by_ed.values():
            raw=re.sub(r"\{[^}]*\}","?",rows[loc][3])
            chunks=re.split("("+GAP.pattern+")",raw,flags=re.I)
            for cut in ("joints","separes"):
                section=0; line=[]
                for i,part in enumerate(chunks):
                    if i%2:
                        section+=1 if part=="<->" else 100
                    else:
                        line.extend((section,w) for w in tokens(part,cut))
                views.append(tuple(line))
        out[loc]=views
    return out


def views_for_start(views,start):
    # Keep the original ranks, and allow at most one drawing gap beyond this starting word.
    result=[]
    for view in views:
        base=view[start][0]
        result.append([(base if s in (base,base+1) else s,w) for s,w in view])
    return result


def sites(data,lookup,n,stride,soft=False):
    if not soft:
        ps=predict_sites(data,lookup,n,stride,strict=True)
        return ps["blocs"],verify_sites(data,ps)
    all_rows=[];all_tests=[]
    for name,vs in data.items():
        for i in range(0,min(map(len,vs))-n+1,stride):
            first=window(vs,i,n)
            if first is None or tier(shape(first))!="principal":continue
            v=views_for_start(vs,i)
            subset={name:[line[i:i+n+2] for line in v]}
            ps=predict_sites(subset,lookup,n,n+2,strict=True)
            ck=verify_sites(subset,ps)
            for a,b in zip(ps["blocs"],ck,strict=True):
                a["rang"]=b["rang"]=i+1
                all_rows.append(a);all_tests.append(b)
    return all_rows,all_tests


def anonymize(texts):
    vocab=sorted({w for _,_,seq in texts for w in seq})
    ids=["z"+chr(97+i//676)+chr(97+i//26%26)+chr(97+i%26) for i in range(len(vocab))]
    Random(94731).shuffle(ids)
    return dict(zip(vocab,ids))


def calibration(parts,examples):
    code=anonymize(parts+examples); lookup=catalog(parts,6)
    metrics=Counter();details=[]
    for book,ref,seq in examples:
        for i in range(len(seq)-7):
            chunk=seq[i:i+8]; sig=shape(chunk[:6])
            if tier(sig)!="principal":continue
            metrics["huit_mots_eligibles"]+=1
            coded=tuple(code[w] for w in chunk)
            opts=[]
            for s,r,rank,train,after in lookup.get(sig,[]):
                if s!="bain":continue
                call=forward(train,after,coded[:6]); pred=[q for q in call if q]
                if not pred:continue
                correct=shape(tuple(train)+tuple(after))==shape(coded)
                opts.append(dict(ref=r,rang=rank,fr=train+after,propositions=call,reproduit=correct))
            if opts:
                original=list(coded)
                j=next(j for j in range(2) if any(x["propositions"][j] for x in opts))
                opposite=next(x for x in coded[:6] if x!=coded[6+j])
                original[6+j]=opposite
                for opt in opts:
                    opt["accord_apres_corruption"]=shape(tuple(opt["fr"]))==shape(tuple(original))
                if any(o["reproduit"] and o["propositions"][j] for o in opts):
                    metrics["alterations_de_cible_predite_correctement"]+=1
                    metrics["alignement_correct_et_cible_predite_survivant"]=metrics.get(
                        "alignement_correct_et_cible_predite_survivant",0)+any(
                        o["reproduit"] and o["propositions"][j] and o["accord_apres_corruption"] for o in opts)
            if opts:metrics["huit_mots_avec_prevision"]+=1
            truth=any(x["reproduit"] for x in opts)
            metrics["avec_alignement_integral_et_prevision"]+=truth
            metrics["avec_au_moins_un_mauvais_alignement_apres_corruption"]=metrics.get(
                    "avec_au_moins_un_mauvais_alignement_apres_corruption",0)+any(x["accord_apres_corruption"] for x in opts)
            for j in range(2):
                consensus={x["propositions"][j] for x in opts if x["propositions"][j]}
                if len(consensus)==1:
                    metrics["positions_predites"]+=1
                    metrics["positions_correctes"]+=int(coded[6+j] in consensus)
            if opts:details.append(dict(ref=ref,rang=i+1,fr=chunk,chiffre=coded,lectures=opts))
    return dict(comptes=dict(metrics),exemples=details)


def main():
    parts=books(); data=pages(); softdata=bridged(data); trials={}; strict_primary={}
    for n in (6,8,10):
        lookup=catalog(parts,n)
        for name,collection,soft in (("continu",data,False),("un_blanc",softdata,True)):
            r,c=sites(collection,lookup,n,1,soft)
            trials[str(n)+"_"+name]={s:summarize(r,c,s,"principal") for s in ("bain","exercice")}
        if n==6:
            r,c=sites(softdata,lookup,6,8,True)
            strict_primary=dict(blocs=r,verification=c)
    rng=Random(11876);histograms={}
    # Count null forecasts only on the same fixed set of testable Voynich prefixes.
    ps=load("PREDICTIONS.json.gz")
    checked=verify_sites(data,ps)
    lookup_sites=[(b,ver) for b,ver in zip(ps["blocs"],checked,strict=True) if b["critere"]=="principal"]
    for experiment in range(499):
        shuffled=[]
        for s,r,text in parts:
            if s=="bain":
                copy=list(text);rng.shuffle(copy);shuffled.append((s,r,tuple(copy)))
        catalogued=catalog(shuffled,6)
        eligible=tried=hits=0
        for b,v in lookup_sites:
            eva=tuple(b["amorce"]); options=catalogued.get(shape(eva),[])
            eligible+=bool(options)
            for j in range(2):
                calls={forward(tr,tail,eva)[j] for _,_,_,tr,tail in options}-{None}
                if len(calls)==1 and v["cible"][j]:
                    tried+=1;hits+=v["cible"][j] in calls
        for k,total in (("blocs_alignables",eligible),("positions_testees",tried),("justes",hits)):
            histograms.setdefault(k,Counter())[total]+=1
    old=[p for p in parts if p[0]=="bain"]
    manuscript=[("bain",r["ref"],norm(r["texte"])) for r in load("SLOANE.json")]
    return dict(tests=trials,blocs_avec_reprise=strict_primary,permutations=histograms,
                connu=calibration(parts,old),autre_copie=calibration(parts,manuscript))


if __name__=="__main__":
    save("COMPLEMENTS.json.gz",main())
