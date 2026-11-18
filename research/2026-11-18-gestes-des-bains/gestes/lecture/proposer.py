"""Fixer les lectures de trois étiquettes à partir des ouvrages historiques seuls."""
from collections import defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
STUDY=HERE.parents[1]
sys.path.insert(0,str(STUDY/"francais"))
from mots import norm
sys.path.insert(0,str(STUDY/"formule"))
from epreuve import ref, latin

VERBS={
 "français":{"prendre":["prendent","prenge"],"laver":["laver"],"tenir":[],"toucher":[],"verser":[]},
 "latin":{"tenere":["tenet"],"tangere":["tacte"],"sumere":["sumere","sumpta","sumant","sumit"],
          "capere":["capit"],"accipere":["accipiunt"],"fundere":["fundit"],
          "lavare":["lauare","lavari","lavat","lavantur"]}}
SEEDS=("olchdy","okchdy","otchdy")


def save(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n")


def books(cache):
    fr=STUDY/"francais"/"CORPUS.json"
    data,lines=latin(cache)
    la=cache/"vers.json"
    return {"français":[(r["ref"],norm(r["texte"])) for r in json.loads(fr.read_text())],
            "latin":[(r["titre"]+", v. "+str(j),w) for r,chapter in zip(data,lines) for j,w in enumerate(chapter,1)]}, {
                "francais":sha256(fr.read_bytes()).hexdigest(),"latin":sha256(la.read_bytes()).hexdigest()}


def signature_map(vocab,width):
    d=defaultdict(set)
    for w in vocab:
        for i,j in product(range(1,width+1),repeat=2):
            s=w[i+j:]
            if 3<=len(s)<=3*width:d[w[:i],s].add(w)
    return d


def transitions(words,width):
    pairs=set()
    for options in signature_map(words,width).values():
        pairs.update((a,b) for a,b in product(options,repeat=2) if a!=b)
    return len(pairs)


def analyze(corpus,forms,width):
    vocab={w for _,words in corpus for w in words}
    roots=signature_map(vocab,width)
    supplied={w for f in forms.values() for w in f}
    citations=[]
    for loc,words in corpus:
        for i,w in enumerate(words):
            if w in supplied:
                citations.append(dict(ref=loc,forme=w,rang=i+1,contexte=words[max(0,i-3):i+4]))
    represented={w for w in vocab if 5<=len(w)<=width*5}
    symbols=ref.units(SEEDS[0])
    guesses=[]
    for lemma,group in forms.items():
        assert all(w in vocab for w in group)
        for a,b in product(group,repeat=2):
            for k in ref.tables(symbols,a,width):
                for key in ref.tables(ref.units(SEEDS[1]),b,width,k):
                    options=roots[key["o"],key["ch"]+key["d"]+key["y"]]
                    assert a in options and b in options
                    thirds=[]
                    for word in sorted(set(group)&options):
                        values=list(ref.tables(ref.units(SEEDS[2]),word,width,key))
                        assert len(values)==1
                        thirds.append(dict(mot=word,table=values[0]))
                    guesses.append(dict(lemme=lemma,premier=a,second=b,base=key,
                        troisieme=thirds,homophonie_triple=a if key["l"]==key["k"] else None,
                        tiers_autres_mots=sorted(options-set(group))))
    return {"vocabulaire":len(vocab),"une_seule_forme":len(represented),
            "mots_autres_que_les_verbes_choisis":len(represented-supplied),
            "couples_orientes_distincts_sans_contrainte_de_sens":transitions(vocab,width),
            "formes_attestees":forms,"attestations":citations,"previsions":guesses}


if __name__=="__main__":
    data,hashes=books(Path(sys.argv[1]))
    out={"empreintes":hashes,"experiences":{}}
    for lang,records in data.items():
        for w in (1,2):
            result=analyze(records,VERBS[lang],w)
            out["experiences"][f"{lang}/{w}"]=result
            print(lang,w,result['vocabulaire'],result['une_seule_forme'],result['mots_autres_que_les_verbes_choisis'],
                  result['couples_orientes_distincts_sans_contrainte_de_sens'],
                  sorted({(r['premier'],r['second']) for r in result['previsions']}),len(result['previsions']))
    save("PREDICTIONS.json",out)
