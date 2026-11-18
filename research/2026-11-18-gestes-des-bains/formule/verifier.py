"""Ouvrir les successeurs réservés et comparer aux autres mots du poème."""
from collections import Counter, defaultdict
from functools import lru_cache
import sys
from pathlib import Path
import numpy as np
from epreuve import (FORMULAS, MODES, SEED, candidates, extend, label, latin, read,
                      records, ref, reveal, write)

@lru_cache(maxsize=200000)
def additions(seq,latin_word,width,mapping):
    return tuple(tuple(sorted(k.items())) for k in extend(seq,latin_word,width,dict(mapping)))


def latin_matches(calls,raw,lexicon):
    detail=[]
    by_case=defaultdict(lambda:defaultdict(Counter))
    other_counts=defaultdict(lambda:defaultdict(Counter))
    for call in calls:
        formula=tuple(call["formule"]); target=formula[2]; width=call["largeur"]
        orig=[tuple(sorted(k.items())) for k in call["cles"]]
        rows=call["lieux"]
        case=f"{' '.join(formula)}/{width}"
        total=by_case[case]
        total["amorces"]["distinctes"]+=1
        total["amorces"]["repetees_sur_autre_bifeuillet"]+=int(call["repetee_entre_bifeuillets"])
        total["cibles"]["annoncees"]+=len(rows)
        hidden=[reveal(s,raw) for s in rows]
        total["cibles"]["concordantes"]+=sum(w is not None for w in hidden)
        places=[]
        for s,v in zip(rows,hidden):
            if v is None:continue
            seq=ref.units(v)
            complete={ref.decode(seq,dict(k)) for k in orig}-{None}
            places.append(dict(site=label(s),bifeuillet=s["bifeuillet"],observé=v,
                               lectures_sans_extension=sorted(complete)))
        pool=sorted(w for w in lexicon if len(w)==len(target))
        assert target in pool
        for plain in pool:
            flags=[]; by_sheet=defaultdict(set)
            for s,v in zip(rows,hidden):
                if v is None:continue
                seq=ref.units(v)
                new={m for m0 in orig for m in additions(seq,plain,width,m0)}
                direct=any(ref.decode(seq,dict(m))==plain for m in orig)
                flags.append((s,seq,new,direct))
                by_sheet[s["bifeuillet"]].update(new)
            totals=other_counts[case][plain]
            totals["compatibles"]+=sum(bool(new) for _,_,new,_ in flags)
            totals["entieres"]+=sum(direct for _,_,_,direct in flags)
            witnesses=0
            for s,seq,new,direct in flags:
                training=set.union(set(),*(seen for b,seen in by_sheet.items() if b!=s["bifeuillet"]))
                trans=any(ref.decode(seq,dict(table))==plain for table in training)
                witnesses+=int(trans)
                if plain==target:
                    target_place=next(p for p in places if p["site"]==label(s))
                    target_place.update(compatible=bool(new),entier=direct,transfert=trans,
                                        nombre_cles_compatibles=len(new))
            totals["transfert"]+=witnesses
        if places and any(p.get("compatible") or p["lectures_sans_extension"] for p in places) or width==1:
            detail.append(dict(amorce=call["amorce"],formule=formula,largeur=width,
                               entre_bifeuillets=call["repetee_entre_bifeuillets"],lieux=places))
    for case,totals in by_case.items():
        name,w=case.split("/"); target=name.split()[-1]; ctrl=other_counts[case]
        totals["cibles"].update(ctrl[target])
        totals["autres_mots_de_meme_longueur"]={
            "total":len(ctrl)-1,"au_moins_autant_de_reponses_compatibles":
             sum(d["compatibles"]>=ctrl[target]["compatibles"] for k,d in ctrl.items() if k!=target),
             "au_moins_autant_de_transferts":sum(d["transfert"]>=ctrl[target]["transfert"] for k,d in ctrl.items() if k!=target),
             "resultats":{k:v for k,v in ctrl.items() if k!=target}}
    return dict(epreuves=dict(by_case),lieux_detailles=detail)


def structure(mode,rows,forecasts,raw):
    pool=defaultdict(list)
    for r in rows:
        v=reveal(r,raw)
        if v is not None:pool[r["face"]].append((label(r),v))
    details=[]; trials=[]
    for i,fc in enumerate(forecasts):
        src=fc["source"]; guess=fc["mot_annonce"]
        assert reveal(src,raw)==guess
        verification=[]
        for s in fc["reserve"]:
            act=reveal(s,raw)
            verification.append(dict(site=label(s),bifeuillet=s["bifeuillet"],observe=act,
                                     juste=guess==act if act and guess else None))
            if guess and act:trials.append((i,s["face"],label(s),guess,act))
        scored=[s for s in verification if s["juste"] is not None]
        details.append(dict(amorce=fc["amorce"],source=label(src),mot_predit=guess,lieux=verification,
                            essais=len(scored),justes=sum(s["juste"] for s in scored),
                            bifeuillets_testes=sorted({s['bifeuillet'] for s in scored}),
                            bifeuillets_avec_succes=sorted({s['bifeuillet'] for s in scored if s['juste']})))
    rng=np.random.default_rng(SEED)
    measures={}
    for test,selected in [("premiere",[t for t in trials if t[0]==0]),("ensemble",trials)]:
        n=9999
        draws=np.zeros(n,dtype=int)
        expectation=0
        for face,universe in pool.items():
            sub=[t for t in selected if t[1]==face]
            if not sub:continue
            # Échantillon ordonné sans remise aux places de test sur cette face.
            vocab={s:i for i,s in enumerate(sorted({w for _,w in universe}|{t[3] for t in sub}))}
            V=np.array([vocab[w] for _,w in universe])
            G=np.array([vocab[t[3]] for t in sub])
            lookup=dict(universe)
            assert len({t[2] for t in sub})==len(sub)
            assert all(lookup[t[2]]==t[4] for t in sub)
            expectation+=sum(np.count_nonzero(V==g)/len(V) for g in G)
            for begin in range(0,n,128):
                size=min(128,n-begin)
                sample=rng.random((size,len(V))).argsort(axis=1)[:,:len(G)]
                draws[begin:begin+size]+=np.sum(V[sample]==G,axis=1)
        successes=sum(t[3]==t[4] for t in selected)
        measures[test]=dict(testables=len(selected),justes=successes,
                            reponses_attendues=float(expectation),p_plus_un=(1+int(np.sum(draws>=successes)))/(n+1))
    return {"amorces":details,"temoins":measures}


def main(folder):
    _,lines=latin(folder)
    latin_vocab={w for ch in lines for line in ch for w in line}
    p=read("PREDICTIONS.json.gz")
    rows,statistics,raw=records()
    assert p["couverture"]==statistics
    out={}
    for mode in MODES:
        spec=p["experiences"][mode]
        out[mode]=dict(structure=structure(mode,rows[mode],spec["repetitions"],raw),
                       latin=latin_matches(spec["hypotheses_latines"],raw,latin_vocab))
        print(mode,out[mode]["structure"]["temoins"])
        for k,v in out[mode]["latin"]["epreuves"].items():
            print(k,v["amorces"],v["cibles"],
                  {a:b for a,b in v["autres_mots_de_meme_longueur"].items() if a!="resultats"})
    write("RESULTATS.json.gz",out)


if __name__=="__main__":
    main(Path(sys.argv[1]))
