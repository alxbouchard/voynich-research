"""Masquer les centres, comparer les catégories sur livres réservés et les fréquences hors face."""
import argparse
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-renvois-entre-plantes/phrase'))
from lecture import adjacent,load,read_books,save,texts
from croiser import metadata
from lexique import labels

LANG={'Celse':'latin','Macer':'latin','Mayence1485':'allemand','RIDGES':'allemand','regime':'français','viandier':'français','martino':'italien'}
SCORED={'nom','article','coordonnant','preposition'}
TARGET={'dar','daiin'}
MASK={14,18,23}


def historical(body):
    for loc,words in body.items():
        yield loc,loc,'ouvrage',words,[(i,) for i in range(1,len(words)+1)]


def manuscript():
    meta=metadata()
    for page,rows in sorted(texts('tout',True).items()):
        if not rows:
            continue
        leaf=int(re.match(r'f(\d+)',page)[1])
        if leaf in MASK:
            continue
        runs=defaultdict(list)
        for row in rows:
            runs[row[1],row[2]].append(row)
        for (loc,run),part in runs.items():
            assert all(adjacent(a,b) for a,b in zip(part,part[1:]))
            yield page,loc,meta[page].get('I','?'),[r[0] for r in part],[r[3] for r in part]


def ranking(global_rank,global_counts,omitted):
    # Dix formes intactes précèdent toute forme hors de cette fenêtre dès que la
    # totalité des formes dont la fréquence pourrait diminuer a été dépassée.
    window=global_rank[:10+len(omitted)]
    return set(sorted((w for w in window if global_counts[w]>omitted[w]),
                      key=lambda w:(omitted[w]-global_counts[w],w))[:10])


def compare(records,dictionary):
    records=list(records)
    frequencies=Counter()
    exclusion=defaultdict(Counter)
    for unit,_,_,words,_ in records:
        frequencies.update(words);exclusion[unit].update(words)
    rank=sorted(frequencies,key=lambda w:(-frequencies[w],w))
    top={u:ranking(rank,frequencies,c) for u,c in exclusion.items()}
    negatives=defaultdict(Counter)
    events=[]
    windows=0
    for unit,loc,section,words,ranks in records:
        # Pour le manuscrit, le tiers se rapporte au tronçon continu, sans franchir un dessin.
        for i,(x,b,z) in enumerate(zip(words,words[1:],words[2:])):
            windows+=1
            if b in (x,z):
                continue
            bucket=(section,x,min(2,3*(i+1)//len(words)))
            common=x in top[unit]
            fx=frequencies[x]-exclusion[unit][x]
            fb=frequencies[b]-exclusion[unit][b]
            state='egal' if fx==fb else 'juste' if (fx>fb)==common else 'faux'
            tag=dictionary.get(b,'inconnu')
            if x!=z:
                neg=negatives[bucket]
                neg['total']+=1;neg[state]+=1;neg['classe/'+tag]+=1
                neg['dar_ou_daiin']+=b in TARGET
            else:
                events.append(dict(unite=unit,lieu=loc,rangs=ranks[i:i+3],section=section,
                                   exterieur=x,centre=b,top10=common,tiers=bucket[-1],
                                   freq_externe_x=fx,freq_externe_b=fb,frequence=state,classe=tag,
                                   autour=list(words[max(0,i-2):i+5])))
    active=set()
    for e in events:
        key=(e['section'],e['exterieur'],e['tiers'])
        e['temoins']=dict(negatives[key])
        active.add(key)
    return dict(types=len(frequencies),mots=sum(frequencies.values()),fenetres=windows,
                controles_distincts_utiles=sum(negatives[k]['total'] for k in active),
                controles_distincts_disponibles=sum(v['total'] for v in negatives.values()),
                encadrements=events)


def distinguish(rows):
    weights={}
    for name,data in rows.items():
        by=defaultdict(Counter)
        for e in data['encadrements']:
            if e['classe'] in SCORED:
                for group in (str(e['top10']),'tous'):
                    by[group][e['classe']]+=1
        weights[name]=by
    out={}
    for group in ('tous','True','False'):
        means=Counter()
        for name,h in weights.items():
            c=h[group]
            if c:
                for tag,n in c.items():means[tag]+=n/c.total()
        out[group]=min(means,key=lambda k:(-means[k],k)) if means else None
    return out


def score(data,rule):
    freq=Counter()
    cats=Counter();prediction=Counter()
    per_ties=0;matched=0;baseline=0;actual=0;total_matched_with_ties=0
    gold=Counter()
    for e in data['encadrements']:
        state,tag,ng=e['frequence'],e['classe'],e['temoins']
        freq[state]+=1;gold[tag]+=1
        if ng.get('total'):
            total_matched_with_ties+=1
        if state!='egal' and ng.get('juste',0)+ng.get('faux',0):
            matched+=1;actual+=state=='juste'
            baseline+=ng.get('juste',0)/(ng.get('juste',0)+ng.get('faux',0))
        if tag in SCORED:
            chosen=rule[str(e['top10'])];cats['classables']+=1
            cats['justes']+=tag==chosen
            cats['temoin_ignorant_x']+=tag==rule['tous']
            prediction[str(chosen)]+=1
            total_class=sum(ng.get('classe/'+s,0) for s in SCORED)
            if total_class:
                cats['centres_et_temoins_classables']+=1
                cats['justes_dans_ce_lot']+=tag==chosen
                cats['esperance_temoins_apparies']+=ng.get('classe/'+str(chosen),0)/total_class
    return dict(positions=len(data['encadrements']),frequence=dict(freq),
                couples_apparies=matched,apparies_avant_retrait_egalites=total_matched_with_ties,
                justes_apparies=actual,attendus_apparies=baseline,classes=dict(gold),
                grammaire=dict(cats),predictions_par_categorie=dict(prediction))


def main(args):
    source=load(RESEARCH/'2026-11-18-renvois-entre-plantes/phrase/INTERPRETATIONS.json.gz')['sha256']
    assert sorted(source.values())==sorted(sha256(p.read_bytes()).hexdigest() for p in args.sources)
    books=read_books(*args.sources)
    lex=labels()
    hist={b:compare(historical(rows),lex[LANG[b]]) for b,rows in books.items()}
    models={b:distinguish({n:d for n,d in hist.items() if n!=b}) for b in hist}
    scores={b:score(v,models[b]) for b,v in hist.items()}
    save(HERE/'HISTOIRE.json.gz',dict(sources=source,lexique=lex,corpus=hist,modeles=models,scores=scores))
    vm=compare(manuscript(),{})
    whole=distinguish(hist)
    subsets={'tous':vm['encadrements']}
    for w in sorted(TARGET):
        subsets[w]=[e for e in subsets['tous'] if e['centre']==w]
    nums={k:score(dict(encadrements=v),whole) for k,v in subsets.items()}
    save(HERE/'VOYNICH.json.gz',dict(corpus=vm,modele_lexical=whole,bilans=nums))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources',nargs=3,type=Path)
    main(parser.parse_args())
