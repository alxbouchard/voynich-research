"""Contrôle positif supplémentaire sur deux triplets et un voisin réel de Celse."""
from pathlib import Path
from random import Random
import sys
from paralleles import HERE,code,index,save,search,verify
from corpus_sources import celsus

LEFT='3.18.p1.70'
RIGHT='3.4.p3.42'
THIRD='1.3.p2.18'


def control(xml):
    body=celsus(xml,r'[.;:!?]')
    patterns,tails=index({'Celse':body})
    left,=[r for r in patterns if r['lieu']==LEFT and r['centre']=='objurgatione']
    right,=[r for r in patterns if r['lieu']==RIGHT and r['centre']=='eodem']
    forms=[r[k] for r in (left,right) for k in ('exterieur','centre')]
    plain_neighbors=[r[k] for r in (left,right) for k in ('gauche','droite')]
    real,=[r for r in tails['Celse',*forms[2:]] if r[0]==THIRD]
    letters=sorted(set(''.join(forms)))
    assert set(''.join(plain_neighbors)+real[2])<=set(letters)
    tokens=list('adfgklmnopqrstvxyz');Random(8314).shuffle(tokens)
    encoder=dict(zip(letters,tokens)); assert len(encoder)==len(letters)
    pack=lambda w:''.join(encoder[c] for c in w)
    ciphertext=tuple(map(pack,forms))
    hidden=list(map(pack,plain_neighbors+[real[2]]))
    assert all(list(code(pack(w),'EVA'))==[encoder[c] for c in w] for w in forms)
    ann=search(patterns,tails,forms=ciphertext,languages={'Celse':'latin'})
    tests=verify(ann,hidden[:4],hidden[-1])['tests']
    recovered=[]
    for i,sol in enumerate(ann['solutions']):
        if sol['mode']!='EVA' or sol['muet'] is not None:
            continue
        pts=[patterns[sol[k]]['lieu'] for k in ('indice_gauche','indice_droite')]
        if pts==[LEFT,RIGHT] and sol['table']=={v:k for k,v in encoder.items()}:
            evidence=tests[i]
            assert evidence['voisins']==['exact']*4
            assert any(r['lieu']==THIRD and r['etat']=='exact' for r in evidence['troisieme'])
            recovered.append(i)
    assert len(recovered)==1
    save(HERE/'CELSE.json.gz',dict(ajustement= forms,voisins=plain_neighbors,autre=real,
             chiffre=ciphertext,voisins_chiffres=hidden,table_reelle=encoder,
             solution_reelle=recovered,tests=tests,annonces=ann))


if __name__=='__main__':
    control(Path(sys.argv[1]))
