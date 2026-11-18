"""Prédire le centre entier à partir d'autres répétitions du même mot extérieur."""
from collections import Counter,defaultdict
from pathlib import Path
import re,sys
from categories_centres import HERE,TARGET,historical,manuscript,read_books,save


def holdout(book,loc):
    if book=='Celse':return re.split(r'\.p\d',loc)[0]
    if book=='RIDGES':return loc.split(':')[0]
    if book=='Mayence1485':return loc.split('.')[0]
    if book=='regime':return re.search(r'p\. (\d+)',loc)[0]
    if book in ('viandier','martino'):return re.sub(r'^\d+ | §\d+$','',loc)
    return loc


def most(c):
    top=c.most_common(2)
    return top[0][0] if top and (len(top)==1 or top[0][1]>top[1][1]) else None


def one(book,records):
    pos=defaultdict(Counter);neg=defaultdict(Counter)
    negby=defaultdict(Counter);events=[]
    for uid,loc,section,words,ranks in records:
        u=holdout(book,uid)
        for i,(a,b,z) in enumerate(zip(words,words[1:],words[2:])):
            if b in (a,z):continue
            grp=(section,a)
            third=min(2,3*(i+1)//len(words))
            key=(section,a,third)
            db=pos if a==z else neg
            db[grp][b]+=1;db[grp+(u,)][b]+=1
            if a==z:
                events.append(dict(exterieur=a,centre=b,lieu=loc,rang=ranks[i+1],section=section,
                                   unite_exclue=u,tiers=third))
            else:
                negby[key][b]+=1;negby[key+(u,)][b]+=1
    totals=Counter()
    for r in events:
        u=r['unite_exclue']; g=(r['section'],r['exterieur']); g3=g+(r['tiers'],)
        training=pos[g]-pos[g+(u,)]
        fallback=neg[g]-neg[g+(u,)]
        control=negby[g3]-negby[g3+(u,)]
        pred=most(training);base=most(fallback)
        compared=pred is not None and base is not None
        measured=pred is not None and bool(control)
        r.update(prediction=pred,prediction_apres_x_ordinaire=base,exemples_apprentissage=sum(training.values()),
                 temoins_hors_unite=sum(control.values()),temoins_avec_mot_annonce=control[pred],
                 exact=bool(pred and pred==r['centre']),exact_temoin=bool(base and base==r['centre']))
        totals['positions']+=1
        totals['annonces']+=bool(pred);totals['exacts']+=r['exact']
        totals['temoin_annonce']+=bool(base);totals['temoin_exact']+=r['exact_temoin']
        if compared:
            totals['annonces_des_deux']+=1;totals['exacts_deux']+=r['exact']
            totals['exacts_temoin_deux']+=r['exact_temoin']
        if measured:
            totals['avec_temoins_apparies']+=1;totals['exacts_apparies']+=r['exact']
            totals['attendus_apparies']+=control[pred]/sum(control.values())
    return dict(bilan=dict(totals),positions=events)


def main(files):
    books=read_books(*files)
    res={b:one(b,historical(body)) for b,body in books.items()}
    hist=one('Voynich',manuscript())
    save(HERE/'MOTS.json.gz',dict(historiques=res,manuscrit=hist))


if __name__=='__main__':
    main([Path(p) for p in sys.argv[1:]])
