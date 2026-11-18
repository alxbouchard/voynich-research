"""Fabriquer quatre défis transparents ; le solveur ne reçoit ni table ni bonnes positions."""
from random import Random
from paralleles import FORMS, HERE, code, index, search, verify, save

HELD = ('qok','dol','kor','dalo','odk')
EXPERIMENTS = [('EVA',None,False),('ii',None,True),('aiin','ch',False),('EVA','o',True)]


def build(mode,mute,double,seed):
    units=sorted(set(sum([code(w,mode) for w in FORMS],())))
    rng=Random(seed)
    alphabet=list('abcdefgiklmnoprstuvz')
    rng.shuffle(alphabet)
    key=dict(zip(units,alphabet))
    if double:
        key['k']+=alphabet[-1]
    if mute:
        key[mute]=''
    def decode(word):
        return ''.join(key[s] for s in code(word,mode))
    a,b,c,d=map(decode,FORMS)
    n=[decode(w) for w in HELD]
    assert a!=b and c!=d and n[-1]!=c
    passages=[['de', 'facto', 'de'],['hic','est','hic'],[n[0],a,b,a,n[1]],['ar','s','ar'],
              [n[2],c,d,c,n[3]],[c,d,n[4]],['pur','um','pur'],['unum','in','unum']]
    rng.shuffle(passages)
    book={f'texte {i}':v for i,v in enumerate(passages,1)}
    correct=[next(place for place,line in book.items() if line==seq)
             for seq in ([n[0],a,b,a,n[1]],[n[2],c,d,c,n[3]])]
    return book,correct,key


def calibrate():
    all_trials=[]
    for i,(mode,mute,double) in enumerate(EXPERIMENTS,1):
        book,truth,key=build(mode,mute,double,29147+i)
        pats,tail=index({'contrôle':book})
        ann=search(pats,tail,languages={'contrôle':'inventé'})
        checks=verify(ann,HELD[:4],HELD[4])['tests']
        recovered=[]
        for j,sol in enumerate(ann['solutions']):
            places=[pats[sol[s]]['lieu'] for s in ('indice_gauche','indice_droite')]
            if (places==truth and sol['mode']==mode and sol['muet']==mute and sol['table']==key):
                check=checks[j]
                assert check['voisins']==['exact']*4
                assert any(a['etat']=='exact' for a in check['troisieme'])
                recovered.append(j)
        assert len(recovered)==1,(mode,mute,recovered)
        all_trials.append(dict(decoupage_genere=mode,muet_genere=mute,deux_lettres=double,
                               corpus=book,lieux_reels=truth,table_reelle=key,
                               entree_solveur=FORMS,groupes_caches=HELD,
                               solutions_retrouvees=recovered,annonces=ann,
                               validations=checks))
    save(HERE/'CALIBRATION.json.gz',all_trials)


if __name__=='__main__':
    calibrate()
