"""Ouvrir les paragraphes annoncés et déplacer les légendes à lieux de lecture fixes."""
from collections import Counter
from itertools import permutations
from math import factorial
import re
from preparer import MODES, corpus, load, save, sequence
from predire import RULES


def truth(editions, page):
    views={}
    for loc,(p,kind,_,_) in editions["H"].items():
        if p==page and kind=="P0" and loc in editions["ZL"] and editions["ZL"][loc][1]=="P0":
            views[loc]=[[w for _,w in sequence(rows[loc][3],cut)] for rows in editions.values() for cut in MODES]
    return views


def lookup(views):
    observed={}
    for loc,readings in views.items():
        common=set.intersection(*(set(v) for v in readings))
        strict=[ws[0] if len(set(ws))==1 and re.fullmatch("[a-z]+",ws[0]) else None
                for ws in zip(*readings)]
        observed[loc]={"rangs":strict, "concordant":{w for w in strict if w},
                       "local": {w for w in common if re.fullmatch("[a-z]+",w)},
                       "H": set(readings[0])}
    return observed


def exact_tail(rows):
    """Only the captions with an actual mention can affect the total score."""
    n=len(rows)
    active=[j for j in range(n) if any(row[j] for row in rows)]
    states={(0,0):1}
    for i in range(n):
        current=Counter(states)
        for (mask,score),count in states.items():
            for k,j in enumerate(active):
                if not mask & (1<<k):
                    current[mask | (1<<k),score+rows[i][j]]+=count
        states=current
    full=(1<<len(active))-1
    dist={score:cnt*factorial(n-len(active)) for (mask,score),cnt in states.items() if mask==full}
    assert sum(dist.values())==factorial(n)
    return dist


def evaluate_item(info,paras,obs):
    word=info["mot"]
    where={}
    for mode in ("concordant","local","H"):
        where[mode]=[j for j,group in enumerate(paras) if any(word in obs[loc][mode] for loc in group)]
    choice=info["annonces"]["colonne"]
    positions=[]
    if choice is not None:
        for loc,rank in info["rangs_par_ligne"][choice].items():
            ws=obs[loc]["rangs"]
            slots={"ligne":loc,"rang":rank}
            for shift,name in [(0,"ouvert"),(1,"decale")]:
                if rank is None or not ws:
                    slots[name]=None
                else:
                    # Only wrap at the right end of the geometric line, not at a truncated collation.
                    full=obs[loc]["longueur_carte"]
                    index=(rank-1+shift)%full
                    slots[name]=ws[index] if index<len(ws) else None
            positions.append(slots)
    return {"mot":word,"reprises":where,"annonces":info["annonces"],"cases":positions}


def evaluate_page(page,data,geometry,editions):
    obs=lookup(truth(editions,page))
    for loc,coords in geometry["lignes"].items():
        if loc in obs:
            obs[loc]["longueur_carte"]=len(coords)
    sets={}
    for cut,layout in data["decoupages"].items():
        paras=layout["paragraphes"]
        verified={loc:evaluate_item(v,paras,obs) for loc,v in layout["legendes"].items()}
        sets[cut]={"paragraphes":paras,"legendes":verified}
    return sets


def combine(a,b):
    r=Counter()
    for s,n in a.items():
        for t,m in b.items():
            r[s+t]+=n*m
    return r


def metrics(panels,rule,mode):
    summary=Counter()
    distribution={0:1}
    observed=[]
    for p,data in panels:
        paras=data["paragraphes"]
        records=list(data["legendes"].items())
        if not records:
            continue
        summary["panneaux"]+=1
        summary["paragraphes"]+=len(paras)
        summary["etiquettes"]+=len(records)
        mat=[]
        for loc,item in records:
            choice=item["annonces"][rule]
            places=item["reprises"][mode]
            if choice is None:summary["abstention"]+=1
            else:summary["annonces"]+=1
            if places:
                summary["reprises_quelque_part"]+=1
                summary["reprises_dans_plusieurs"]+=len(places)>1
                observed.append(dict(page=p,legende=loc,mot=item["mot"],cibles=places,predit=choice,
                                     n_paragraphes=len(paras),juste=choice in places))
            if choice in places:
                summary["coups_justes"]+=1
            if rule=="colonne":
                for row in item["cases"]:
                    for k in ("ouvert","decale"):
                        if row[k] is not None:
                            summary[k+"_lisibles"]+=1
                            summary[k+"_justes"]+=int(row[k]==item["mot"])
                summary["cases_annoncees"]+=sum(r["rang"] is not None for r in item["cases"])
                summary["legendes_avec_case_exacte"]+=any(r["ouvert"]==item["mot"] for r in item["cases"])
            mat.append([int(choice in other["reprises"][mode]) for _,other in records])
        distribution=combine(distribution,exact_tail(mat))
    total=sum(distribution.values())
    n_good=summary["coups_justes"]
    tail=sum(v for s,v in distribution.items() if s>=n_good)
    expected=sum(s*v for s,v in distribution.items())/total
    return dict(comptes=dict(summary),reprises=observed,permutations=dict(total=total,au_moins=tail,p=tail/total,
                attendu=expected, distribution=dict(distribution)))


def main():
    votes=load("PREDICTIONS.json.gz")
    masked=load("CARTE-MASQUEE.json.gz")
    ed,_=corpus()
    evaluated={p:evaluate_page(p,v,masked[p],ed) for p,v in votes.items()}
    summary={}
    for cut in ("strict","reunis","H","ZL"):
        panels=[(p,d[cut]) for p,d in evaluated.items()]
        groups={"concurrence":[(p,d) for p,d in panels if len(d["paragraphes"])>=2],
                "force":[(p,d) for p,d in panels if len(d["paragraphes"])==1]}
        for name, selected in (("f99",{"99"}),("f102",{"102"}),("autres",{"88","89","100","101"})):
            groups[name]=[(p,d) for p,d in groups["concurrence"] if re.match(r"f(\d+)",p)[1] in selected]
        summary[cut]={name:{rule:{mode:metrics(items,rule,mode) for mode in ("concordant","local","H")}
            for rule in RULES} for name,items in groups.items()}
    save("RESULTATS.json.gz",dict(panneaux=evaluated,resumes=summary))
    for cut in ("strict","reunis","H","ZL"):
        print(cut, {g:(summary[cut][g]["colonne"]["concordant"]["comptes"].get("etiquettes",0),
                summary[cut][g]["colonne"]["concordant"]["comptes"].get("reprises_quelque_part",0),
                summary[cut][g]["colonne"]["concordant"]["comptes"].get("coups_justes",0))
                for g in groups})


if __name__=="__main__":
    matrix=[[1,1,0,0],[0,1,0,0],[1,0,0,0],[0,1,0,0]]
    assert exact_tail(matrix)==Counter(sum(matrix[i][j] for i,j in enumerate(p)) for p in permutations(range(4)))
    main()
