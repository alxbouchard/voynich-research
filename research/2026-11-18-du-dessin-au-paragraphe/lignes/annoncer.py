"""Prédire en ne lisant que la géométrie et les mots supérieurs."""
from collections import defaultdict
import sys
from fichiers import PASSAGES,HERE,load,save,digest
sys.path.insert(0,str(PASSAGES))
from predire import center,winners


def apparier(pair,slope):
    project=lambda box: center(box)[0]+slope*center(box)[1]
    source=[project(b) for b in pair['boites_haut']];target=[project(b) for b in pair['boites_bas']]
    possible=defaultdict(list)
    for i,(w,x) in enumerate(zip(pair['mots_haut'],source)):
        if w is None or not min(target)<=x<=max(target):continue
        distances=[abs(x-p) for p in target];nearest=winners(distances)
        if len(nearest)==1 and 0<nearest[0]<len(target)-1:
            j=nearest[0];possible[j].append((distances[j],i,w))
    calls=[]
    for j,choices in sorted(possible.items()):
        best=winners([r[0] for r in choices]);
        if len(best)!=1: continue
        _,i,w=choices[best[0]]
        calls.append(dict(rang_haut=i+1,rang_bas=j+1,decale=2+(j%(len(target)-2)),mot=w))
    return dict(haut=pair['haut'],bas=pair['bas'],longueur=len(target),annonces=calls)


def main():
    pages=load('CARTE-MASQUEE.json.gz')
    pred={p:{'lot':data['lot'],'paires':[apparier(pair,data['pente']) for pair in data['paires']]} for p,data in pages.items()}
    save('PREDICTIONS.json.gz',dict(carte=digest(HERE/'CARTE-MASQUEE.json.gz'),pages=pred))


if __name__=='__main__': main()
