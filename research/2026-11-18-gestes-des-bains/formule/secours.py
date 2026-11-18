"""Peut-on prédire OPEM à la fin d'une autre ligne sous la même clé ?"""
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from epreuve import (SIMPLE, cipher, extend, latin, read, records, ref, write)


def inventory():
    from transfert import langage
    where={}
    for line in (langage.DATA/"ZL3b-n.txt").read_text().splitlines():
        page=re.match(r"^<(f\d+[rv])>",line)
        if page and "$Q=M " in line:where[page[1]]=int(re.search(r"\$B=(\d+)",line)[1])
    _,_,all_lines=records()
    dataset={}
    for loc,vs in all_lines.items():
        if any(len(v)<2 or not v[-1] or not v[-2] for v in vs):continue
        penult={v[-2] for v in vs}
        if len(penult)!=1 or not SIMPLE.fullmatch(vs[0][-2]):continue
        dataset[loc]=(where[loc.split(".")[0]],vs[0][-2],vs)
    return dataset


def last(vs):
    vals={v[-1] for v in vs}
    return vs[0][-1] if len(vals)==1 and SIMPLE.fullmatch(vs[0][-1]) else None


def calibration(data,lines):
    crypt=cipher(lines)
    positions=[(i,j) for i,ch in enumerate(lines) for j,line in enumerate(ch) if line[-2:]==["prestat","opem"]]
    result=[]
    for c,ch in enumerate(crypt):
        i,j=next(loc for loc in positions if loc[0]!=c)
        x,y=crypt[i][j][-2:]
        key=extend(x,"prestat",1,{})[0]
        keys=extend(y,"opem",1,key)
        assert len(keys)==1
        key=keys[0]
        rev={v:k for k,v in key.items()}
        target=tuple(rev[s] for s in "opem")
        for k,line in enumerate(ch):
            if len(line)>=2 and ref.decode(line[-2],key)=="prestat":
                result.append(dict(notice=c,vers=k+1,appris_sur=[i,j+1],predit="".join(target),
                    observe="".join(line[-1]),juste=tuple(line[-1])==target))
    actual=[dict(notice=i,titre=data[i]["titre"],vers=j+1,texte=data[i]["vers"][j])
            for i,j in positions]
    all_hits=sum(w=="prestat" for ch in lines for line in ch for w in line)
    return dict(fin_de_vers=actual,occurrences_prestat_toutes_positions=all_hits,epreuve=result)


def train(data,terms):
    initial={}; all_learned=defaultdict(lambda:defaultdict(list))
    for width in (1,2):
        keys={loc:(w,extend(ref.units(w),"prestat",width,{})) for loc,(b,w,_) in data.items()}
        initial[str(width)]=[{"lieu":loc,"bifeuillet":data[loc][0],"penultieme":w,"nombre_cles":len(ks)}
                             for loc,(w,ks) in keys.items() if ks]
        for loc,(w,ks) in keys.items():
            b,_,vs=data[loc]
            if not ks or b%2!=1: continue
            z=last(vs)
            if not z:continue
            signs=ref.units(z)
            for t in terms:
                for k in ks:
                    for m in extend(signs,t,width,k):
                        all_learned[width,t][tuple(sorted(m.items()))].append(loc)
    plans={}
    for width in (1,2):
        for term in terms:
            regs=all_learned[width,term]; lessons=[]
            for frozen,sources in sorted(regs.items()):
                k=dict(frozen)
                bets=[loc for loc,(b,w,vs) in data.items() if b%2==0 and ref.decode(ref.units(w),k)=="prestat"]
                lessons.append(dict(table=k,origines=sources,reserve=bets))
            plans[str(width)+"/"+term]=lessons
    return dict(candidats=initial,lecons=plans)


def verify(data,plan):
    out={}
    for config,calls in plan["lecons"].items():
        mode,term=config.split("/"); width=int(mode)
        sites=plan["candidats"][mode]
        compt=Counter(); transfer=[]; direct=[]
        for site in sites:
            loc=site["lieu"];b,w,vs=data[loc]
            compt["annonces"]+=1; third=last(vs)
            if not third:continue
            compt["lisibles"]+=1
            ks=extend(ref.units(w),"prestat",width,{})
            if any(extend(ref.units(third),term,width,k) for k in ks):
                compt["ajustables"]+=1
                if term=="opem":direct.append(dict(lieu=loc,penultieme=w,dernier=third))
            if any(ref.decode(ref.units(third),k)==term for k in ks):compt["entier"]+=1
        sites_eval=set(); sites_read=set(); hits=set()
        for item in calls:
            for loc in item["reserve"]:
                sites_eval.add(loc)
                third=last(data[loc][2])
                if third:
                    sites_read.add(loc)
                    if ref.decode(ref.units(third),item["table"])==term:
                        hits.add(loc)
                        if term=="opem":transfer.append(dict(lieu=loc,mot=third,**item))
        out[config]=dict(comptes=compt,cles_apprises=len(calls),cibles_reserve=len(sites_eval),
                         cibles_verifiables=len(sites_read),succes=len(hits))
        if term=="opem":out[config].update(accords_possibles=direct,reussites_transfert=transfer)
    return out


if __name__=="__main__":
    data,lines=latin(Path(sys.argv[2]))
    samples=inventory()
    terms=sorted({line[-1] for ch in lines for line in ch if len(line[-1])==4})
    assert "opem" in terms
    if sys.argv[1]=="predire":
        plan=train(samples,terms)
        write("SECOURS-PREDICTIONS.json.gz",plan)
        for w in (1,2):
            print(w,len(plan["candidats"][str(w)]),
                  len(plan["lecons"][f"{w}/opem"]),len({l for k in plan["lecons"][f"{w}/opem"] for l in k["reserve"]}))
    else:
        assert sys.argv[1]=="verifier"
        tests=verify(samples,read("SECOURS-PREDICTIONS.json.gz"))
        write("SECOURS.json",dict(lignes_avec_penultieme_lisible=len(samples),
              latin=calibration(data,lines),comparaisons=tests))
        for w in (1,2):print(w,tests[f"{w}/opem"])
