"""Deux contrôles supplémentaires déclarés dans COMPLEMENT.md."""
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import sys
from calibrer import Bibliotheque, ICI, SIGNES, assignments, bilan, coder, mots


def echanger(chiffre):
    premier = chiffre[0][0]
    second = next((s for w in chiffre for s in w if s!=premier),SIGNES[(SIGNES.index(premier)+1)%26])
    echanges = {premier:second,second:premier}
    return tuple(tuple(echanges.get(s,s) for s in w) for w in chiffre)


def coupes(mot, n):
    if not n<=len(mot)<=2*n:
        return
    for doubles in combinations(range(n),len(mot)-n):
        depart=0
        pieces=[]
        for i in range(n):
            fin=depart+1+(i in doubles)
            pieces.append(mot[depart:fin])
            depart=fin
        yield pieces


def cles_independantes(signaux,clair):
    mots_a,mots_b=signaux
    for a,b in product(coupes(clair[0],len(mots_a)),coupes(clair[1],len(mots_b))):
        affectations=list(zip(mots_a+mots_b,a+b,strict=True))
        cle=dict(affectations)
        if all(cle[s]==x for s,x in affectations):
            yield tuple(sorted(cle.items()))


def verbe_XVI(bib):
    amorce=(('l','k','ch','y'),('t','o','l','y'))
    suivant=(('t','o','l','y'),('t','o','l'))
    resultat=[]
    for paire in bib.positions:
        a=set(cles_independantes(amorce,paire))
        b=set(tuple(sorted(k.items())) for k in assignments(amorce,paire,2))
        assert a==b
        for enreg in sorted(a):
            cle=dict(enreg)
            clair=tuple(''.join(cle[s] for s in w) for w in suivant)
            resultat.append({'amorce':' '.join(paire),'cle':cle,'transfert':' '.join(clair),
                    'lieux_transfert':bib.positions.get(clair,[])})
    return resultat


def main(cache):
    from hashlib import sha256
    source=cache/'vers.json'
    assert sha256(source.read_bytes()).hexdigest()==json.loads((ICI.parent/'SOURCE.json').read_text())['sha256']
    corpus=[[mots(v) for v in c['vers']] for c in json.loads(source.read_text())]
    bib=Bibliotheque(corpus)
    details=[]
    compte=[Counter(),Counter()]
    for numero,vers in enumerate(corpus[1:],1):
        paires=[tuple(v[:2]) for v in vers[:3]]
        codes=coder(paires,numero)
        for i in range(2):
            perturbe=echanger(codes[i+1])
            couvert,fixes,extensions=bib.transfert(codes[0],perturbe)
            assert perturbe!=codes[i+1]
            item={'notice':numero,'vers':i+2,'clair':' '.join(paires[i+1]),'couverture':couvert}
            for nom,solutions in [('fixes',fixes),('extensions',extensions)]:
                item[nom]=bilan(solutions,paires[i+1])
                compte[i][nom+'_avec_lecture']+=bool(solutions)
                compte[i][nom+'_exact_inclus']+=paires[i+1] in solutions
                compte[i][nom+'_exact_unique']+=solutions=={paires[i+1]}
                compte[i][nom+'_au_moins_une_fausse']+=bool(solutions-{paires[i+1]})
            details.append(item)
    return {'echange':compte,'detail_echange':details,'XVI_un_ou_deux_caracteres':verbe_XVI(bib)}


if __name__=='__main__':
    print(json.dumps(main(Path(sys.argv[1])),indent=1,ensure_ascii=False))
