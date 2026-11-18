"""Un lecteur essaie de retrouver une clé cachée à partir des seules rubriques connues."""
import random
import string
import sys
sys.dont_write_bytecode = True
from ajuster import LATIN, MODELES, TARGETS, save, solve


def book(plain,seed):
    signs=['S'+str(i).zfill(2) for i in range(26)]
    random.Random(seed).shuffle(signs)
    hidden=dict(zip(string.ascii_lowercase,signs))
    def encrypt(w):return tuple(hidden[c] for c in w)
    return tuple(tuple(encrypt(w) for w in heading) for heading in plain), encrypt


def read(codes,key):
    return ''.join(key[u] for u in codes) if all(u in key for u in codes) else None


def verify():
    record={}
    for i,(mode,plain) in enumerate(MODELES.items()):
        cipher,encrypt=book(plain,951461+i)
        equations=tuple((codes,w) for heading,source in zip(cipher,plain) for codes,w in zip(heading,source))
        solutions=list(solve(equations,max_letters=1))
        assert len(solutions)==1
        key=dict(solutions[0])
        labels=set(key.values())
        results={}
        # « in » est bien attesté dans la première phrase au recto XCVI.
        for w in dict.fromkeys((*TARGETS[mode], *(('in',) if mode!='allemand' else ()))):
            holdout=encrypt(w)
            missing=sorted(set(w)-labels)
            if not missing:
                # À une lettre par signe et clé injective, les sorties prédisent chaque numéro.
                predicted=tuple(next(k for k,v in key.items() if v==char) for char in w)
                assert predicted==holdout and read(holdout,key)==w
                replaced=(*holdout[:-1],next(u for u in sorted(key) if u!=holdout[-1]))
                assert read(replaced,key)!=w
                results[w]={'prediction':predicted,'chiffre_verifie':holdout,'juste':True,
                            'dernier_signe_modifie':replaced[-1],'lecture_apres_modification':read(replaced,key),'juste_apres_modification':False}
            else:
                assert read(holdout,key) is None
                results[w]={'prediction':None,'chiffre_verifie':holdout,'lettres_manquantes':missing}
        record[mode]={'titres_chiffres':cipher,'table_apprise':key,'solutions':len(solutions),'essais':results}
    save('CALIBRATION.json',record)


if __name__=='__main__':verify()
