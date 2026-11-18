"""Vérifier les deux tables injectives sur un autre cahier quelle que soit la place du dessin."""
from collections import Counter, defaultdict
from itertools import permutations
import gzip
import json
import sys
from comparer import HERE, RESEARCH, permit, read, save, titles, units
sys.path.insert(0,str(RESEARCH/"2026-11-18-legendes-et-paragraphes"))
from comparer import corpus, tokens
from transfert import labels

def forecasts():
    src=titles()
    trained=json.loads(gzip.decompress((HERE/"PREDICTIONS.json.gz").read_bytes()))
    output=[]
    for b in trained:
        for r in b["models"].get("1",[]):
            key=r["key"]
            backwards={v:k for k,v in key.items()}
            books=["Carrara"] if r["book"]=="Carrara" else ["Macer","Gart"]
            vocab=sorted({w for book in books for _,w in src[book].values() if permit(w)})
            words={w:[backwards[c] for c in w] for w in vocab if set(w)<=set(backwards)}
            output.append(dict(source=r["book"],seed_labels=b["given"],seed_names=r["seed"],key=key,
                               words=words,vocab=vocab))
    return output

def heldout():
    editions,sections=corpus()
    all_tables=[labels(ed,cut) for ed in editions.values() for cut in ("joints","separes")]
    result={}
    for loc in sorted(set.intersection(*(set(t) for t in all_tables))):
        page=loc.split(".")[0]
        if page.startswith(("f88","f89")) or sections.get(page)!="P":
            continue
        ws=all_tables[0][loc]
        if len(ws)==1 and permit(ws[0]) and all(t[loc]==ws for t in all_tables):
            result[loc]=ws[0]
    assert all(loc.startswith(("f99","f100","f101","f102")) for loc in result)
    return result

def test(forecast,sites):
    current=forecast["key"]
    available={s for s in current}
    places=defaultdict(list)
    for loc,word in sites.items():
        if set(units(word))<=available:
            places[word].append(loc)
    newwords={w:units(w) for w in places if w not in forecast["seed_labels"]}
    # Only complete names encodable with this letter inventory can ever score.
    eligible=set(forecast["words"])-set(forecast["seed_names"])
    decoded={w:"".join(current[s] for s in units(w)) for w in places}
    hist=Counter()
    for assign in permutations(current.values()):
        key=dict(zip(current,assign))
        score=sum("".join(key[s] for s in signs) in eligible for signs in newwords.values())
        hist[score]+=1
    hits=[w for w in newwords if decoded[w] in eligible]
    return dict(source=forecast["source"],sites=len(sites),
            pages=sorted({loc.split(".")[0] for loc in sites}),
            covered={w:dict(loci=places[w],reading=v) for w,v in sorted(decoded.items())},
            novel_hits=hits,permutation=dict(sorted(hist.items())))

if __name__=="__main__":
    if sys.argv[1]=="predire":
        save("NOMS-PREDITS.json",forecasts())
    elif sys.argv[1]=="verifier":
        sites=heldout()
        save("NOMS-TRANSFERT.json",[test(f,sites) for f in read(HERE/"NOMS-PREDITS.json")])
