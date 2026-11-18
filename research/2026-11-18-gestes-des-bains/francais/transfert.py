"""Tester telles quelles les deux correspondances de dix mots, sur les autres bifeuillets."""
from collections import Counter, defaultdict
from mots import books, catalog, corpus, save, shape, tokens
from compter import runs
import re


def adjacent(groups,n):
    return [tuple(groups[i:i+n]) for i in range(len(groups)-n+1)]


def scan(editions,allowed):
    views=[]
    for rows in editions.values():
        for mode in ("joints","separes"):
            read={}
            for loc,(page,kind,pos,raw) in rows.items():
                if page not in allowed or kind!="P0":continue
                chunks=runs(re.sub(r"\{[^}]*\}","?",raw),mode)
                pairs=Counter()
                for span in chunks:
                    seq=[w for _,w in span]
                    for n in (1,2,3,4):
                        pairs.update(adjacent(seq,n))
                read[loc]=pairs
            views.append(read)
    phrases=defaultdict(dict)
    for loc in sorted(set.intersection(*(set(d) for d in views))):
        counts=views[0][loc].copy()
        for other in views[1:]:counts &= other[loc]
        for p,n in counts.items():
            phrases[p][loc]=n
    return phrases


def test(voy,candidates):
    outcomes=[]
    for section,ref,pos,fr,suite in candidates:
        q=tuple("qotar ytedy tedy dar olkedy qotedy shckhy chtol tedy dar".split())
        key=dict(zip(q,fr))
        lex=defaultdict(set)
        for topic,_,seq in books():
            for n in (3,4):
                lex[topic].update(adjacent(seq,n))
        findings=[]; cnt=Counter()
        for v,sites in voy.items():
            if not all(w in key for w in v):continue
            text=tuple(key[w] for w in v)
            fitted=text in adjacent(fr,len(text))
            cnt[str(len(v))+"_lisibles"]+=sum(sites.values())
            if len(v)<3:continue
            if len(v)==3 and not fitted:cnt["triplets_nouveaux"]+=sum(sites.values())
            matches=[topic for topic,terms in lex.items() if text in terms]
            if not fitted and matches:
                findings.append(dict(eva=v,lus=text,lieux=sites,chapitres=matches))
        outcomes.append(dict(ref=ref,rang=pos,valeurs=key,annonce=suite,total=dict(cnt),rencontres=findings))
    return outcomes


if __name__=="__main__":
    base=books()
    seed=tuple("qotar ytedy tedy dar olkedy qotedy shckhy chtol tedy dar".split())
    cand=[r for r in catalog(base,10)[shape(seed)] if r[0]=="bain"]
    assert len(cand)==2
    editions,_=corpus()
    readings={ed:{cut:tokens(rows["f84r.32"][3],cut) for cut in ("joints","separes")}
                for ed,rows in editions.items()}
    assert all(seq[:10]==seed for d in readings.values() for seq in d.values())
    inside={f"f{i}{s}" for i in range(76,84) for s in "rv"}
    outside={r[0] for rows in editions.values() for r in rows.values()
             if not re.fullmatch(r"f(?:7[5-9]|8[0-4])[rv]",r[0])}
    save("F84R.json",dict(lectures=readings,groupes={group:test(scan(editions,selection),cand)
                for group,selection in (("autres_bifeuillets_bains",inside),("autres_cahiers",outside))}))
