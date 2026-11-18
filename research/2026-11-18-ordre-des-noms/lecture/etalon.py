"""Récupération à l'aveugle de positions et lectures sur des listes médiévales chiffrées."""
import json
from pathlib import Path
from random import Random
from string import ascii_lowercase
from comparer import HERE, maps, permit, predict, save, titles


def blocks(catalog):
    for book, entries in catalog.items():
        keys=sorted(entries)
        start=0
        while start<len(keys):
            end=start+1
            while end<len(keys) and keys[end]==keys[end-1]+1:
                end+=1
            for j in range(start,end-2,3):
                idx=keys[j]
                words=[entries[n][1] for n in keys[j:j+3]]
                if all(permit(w) for w in words):
                    yield book,idx,words
            start=end


def challenge(catalog):
    letters=list(ascii_lowercase)
    Random(514157).shuffle(letters)
    secret={a:f"S{ord(b)-96:02d}" for a,b in zip(ascii_lowercase,letters)}
    for book,idx,words in blocks(catalog):
        yield book,idx,[[secret[c] for c in word] for word in words]


def predictions(catalog):
    batch=[]
    for book,idx,(one,two,_) in challenge(catalog):
        batch.append(dict(source=book,index=idx,given=[one,two],candidates=predict(one,two,catalog,1)))
    return batch


def evaluate(catalog,stored):
    results=[]
    for row,(book,idx,coded) in zip(stored,challenge(catalog),strict=True):
        assert (row["source"],row["index"],row["given"])==(book,idx,coded[:2])
        ct=coded[2]
        changed=next(s for s in dict.fromkeys(coded[0]+coded[1]) if s!=ct[0])
        wrong=[changed,*ct[1:]]
        surviving=[]
        wrong_ok=[]
        for opt in row["candidates"]:
            if next(maps(ct,opt["expected"],1,opt["key"]),None):
                surviving.append([opt["book"],opt["index"]])
            if next(maps(wrong,opt["expected"],1,opt["key"]),None):
                wrong_ok.append([opt["book"],opt["index"]])
        correct,=[r for r in row["candidates"] if (r["book"],r["index"])==(book,idx)]
        names=sorted({r["expected"] for r in row["candidates"]})
        mask=[correct["key"].get(k,"?") for k in ct]
        results.append(dict(book=book,index=idx,source_names=[catalog[book][n][1] for n in (idx,idx+1,idx+2)],
            possible_names=names,possible_sites=len(row["candidates"]),true_mask="".join(mask),
            fully_known="?" not in mask,surviving=surviving,wrong_surviving=wrong_ok))
    return results


if __name__=="__main__":
    import sys
    data=titles()
    if sys.argv[1]=="predire":
        save("ETALON-PREDICTIONS.json",predictions(data))
    elif sys.argv[1]=="verifier":
        save("ETALON.json",evaluate(data,json.loads((HERE/"ETALON-PREDICTIONS.json").read_text())))
