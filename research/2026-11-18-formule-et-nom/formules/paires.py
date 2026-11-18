"""Tous les cadres A B X et X A B, dans des tronçons lisibles."""
from collections import defaultdict

from formules import HERE, MODES_NAMES, annotate, choose, figures, folio, learn, load, null_rule, scan, sha256, write


def unique_pairs(spans):
    positions=defaultdict(list)
    for span in spans:
        for i in range(len(span)-1):
            positions[span[i][1],span[i+1][1]].append((span,i))
    return {pair:found[0] for pair,found in positions.items() if len(found)==1}


def two_positions(pages,lines):
    out=defaultdict(list)
    for locus,by_mode in lines.items():
        page=locus.partition(".")[0]
        if page not in pages:
            continue
        locations=[unique_pairs(spans) for spans in by_mode]
        for pair in sorted(set.intersection(*(set(pos) for pos in locations))):
            for side in (-1,1):
                ranks,words={},[]
                for name,pos in zip(MODES_NAMES,locations):
                    span,i=pos[pair]
                    j=i-1 if side<0 else i+2
                    exists=0<=j<len(span)
                    ranks[name]=[span[i][0],span[i+1][0],span[j][0] if exists else None]
                    words.append(span[j][1] if exists else None)
                if all(w is None for w in words):
                    continue
                target=words[0] if len(set(words))==1 else None
                out[pair,side].append(dict(locus=locus,panneau=page,rangs=ranks,cible=target))
    return out


def check(rule,positions,labels,old=()):
    rows=[]
    for r in positions:
        w=r["cible"]
        caps=labels[r["panneau"]].get(w,[]) if w not in rule[0] else []
        rows.append(dict(r,legendes=caps,nouveau=bool(caps and w not in old)))
    return rows


def score(source,test,lex,other):
    trained=[]
    covered=set()
    total_base=sum(bool(row["legendes"]) for rule,positions in test.items()
                   for row in check(rule,positions,other))
    for rule, positions in source.items():
        rows=check(rule,positions,lex)
        info=figures(rows)
        if not info["justes"]:
            continue
        legit=min(len(info["graphies"]),len(info["feuillets"]))>=2
        matches=check(rule,test.get(rule,[]),other,info["graphies"])
        if legit:
            for row in matches:
                if row["legendes"]:
                    covered.add((row["locus"],row["cible"]))
        trained.append(dict(fixe=rule[0],cote=rule[1],admis=legit,apprentissage=info,
                            exemples=[row for row in rows if row["legendes"]],
                            transfert=figures(matches),nouveaux=figures([r for r in matches if r["nouveau"]]),
                            appels_transfert=matches))
    max_leaves=max((len(r["apprentissage"]["feuillets"]) for r in trained),default=0)
    return dict(regles=trained,maximum_feuillets_apprentissage=max_leaves,
                paires_distinctes_locales_retrouvees=len(covered),succes_toutes_positions=total_base)


def artificial():
    groups=[["f1r","f2r"],["f3r","f4r","f5r","f6r"]]
    labels={}
    lines={}
    for p,name in zip(groups[0]+groups[1],["rosa","urtica","malva","betula","fraxinus","salvia"]):
        locus=p+".1"
        labels[p]={name:[p+".2"]}
        span=list(enumerate(["sucus","de",name],1))
        lines[locus]=[[span] for _ in MODES_NAMES]
    tr,te=groups
    a=two_positions(tr,lines)
    b=two_positions(te,lines)
    scores=score(a,b,labels,labels)
    good=[r for r in scores["regles"] if r["admis"]]
    assert len(good)==1 and good[0]["nouveaux"]["justes"]==4
    assert good[0]["fixe"]==("sucus","de") and good[0]["cote"]==1
    # Même données avec seulement « de » fixe : quatre positions justes sur quatre.
    chosen,_=choose(learn(tr,labels,lines,1),True)
    assert chosen["regle"] == ["de",1]
    left=scan(tr,lines,1)
    train=annotate(("de",1),left["de",1],labels)
    right=scan(te,lines,1)[("de",1)]
    test=annotate(("de",1),right,labels,figures(train)["graphies"])
    assert len({folio(x["panneau"]) for x in train if x["legendes"]})==2
    assert len([x for x in test if x["nouveau"]])==4
    null=null_rule(("de",1),test,te,labels,figures(train)["graphies"])["nouveaux"]
    assert (null["egal_ou_plus"],null["total"])==(1,24)
    # Une réattribution cyclique sur la réserve retire toutes les reprises.
    perm={p:labels[te[(i+1)%len(te)]] for i,p in enumerate(te)}
    assert not any(r["legendes"] for r in check((("sucus","de"),1),b[(("sucus","de"),1)],perm))
    return dict(pages=groups,noms=[next(iter(labels[p])) for p in tr+te],succes_apprentissage=2,
                succes_reserve=4,nouveaux_noms=4,succes_rotation=0,permutations=null)


if __name__=="__main__":
    assert sha256((HERE/"DEUX-MOTS.md").read_bytes()).hexdigest()=="76f1f08d28ff66afe7134cb46caac2d48d5f08b45e4a67196aa03194c386be83"
    groups, captions, lines=load()
    tables={q:two_positions(g,lines) for q,g in groups.items()}
    labels={q:captions(g) for q,g in groups.items()}
    write("DEUX-MOTS.json", {str(q):score(tables[q],tables[34-q],labels[q],labels[34-q])
                             for q in (15,19)})
    write("TEMOIN.json",artificial())
