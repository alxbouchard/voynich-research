"""Séparer l'effet du rang initial de l'apport des graphies courtes."""
from collections import Counter,defaultdict
from suites import read, save, top, distributions, fit


def main():
    train=read('APPRENTISSAGE.json.gz')
    ann=read('ANNONCES-AB.json.gz')
    results=read('OUVERTURES.json.gz')
    model,_=fit(train);conditions=defaultdict(Counter)
    for r in train:
        if r['initial'] and r['suite']:conditions[r['ancre']][r['suite'][0]]+=1
    stats=defaultdict(Counter);examples={}
    for loc,row in ann.items():
        if not results[loc]['vrai']:continue
        y=results[loc]['vrai'][0]; word=row['ancre']
        d=distributions(model,row,'A'); c=conditions[word]
        literal=top(c or d['position'])[0]
        group=row['annonces']['A']['regroupe']['choix'][0]
        levels=row['classes']
        for lev in levels:
            sub=stats[row['lot']+'/'+lev]
            sub['n']+=1
            sub['exact_seul_debut']+=literal==y
            sub['regroupe']+=group==y
            if literal!=group:
                sub['changements']+=1
                sub['gains_court']+=group==y
                sub['pertes_court']+=literal==y
        if group==y or literal==y or (row['lot']=='dernier' and word=='dshedy'):
            examples[loc]={'ancre':word,'reponse':y,'debut_seul':literal,'regroupement':group,
                           'effectifs_debut':dict(c),'effectifs_court':dict(d['court'])}
    save('CONTROLE-POSITION.json',{'scores':stats,'lieux':examples})


if __name__=='__main__':main()
