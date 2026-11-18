"""Lectures indépendantes imposées par l'unique table qui donne cera."""
from collections import Counter
import gzip
import json
from pathlib import Path
import re
import sys

from phrase import HERE, RESEARCH, SIGNS, corpus, save, tables
sys.path.insert(0, str(RESEARCH/"2026-11-18-phrase-et-doublets/noms"))
from reprendre import agreed, corpus as voynich

PAGES = ("f2r","f2v","f3r","f3v")


def decode(word, key):
    units = re.findall(r"c[ktfp]h|ch|sh|.", word)
    if len(units) < 3 or "ch" in units[1:] or any(s not in key for s in units):
        return None
    return "".join(key[s] for s in units)


def concordances(parts, params, key):
    vocabulary = sorted({w for row in parts.values() for w in row})
    results = []
    for label, signs, center, step in params:
        possible = {w for w in vocabulary if next(tables(signs,w,3,key),None) is not None}
        matching = Counter()
        locations = total = 0
        for row in parts.values():
            for i,w in enumerate(row):
                if w == center:
                    locations += 1
                    if 0 <= i+step < len(row):
                        total += 1
                        if row[i+step] in possible:
                            matching[row[i+step]] += 1
        results.append(dict(test=label, anchor=center, step=step, occurrences=locations,
                            has_neighbor=total, lexical=sorted(possible), matches=matching))
    return results


def main():
    dictionary = corpus(Path(sys.argv[1]))["Celse"]
    vocab = {w for row in dictionary.values() for w in row}
    proposals = json.loads(gzip.decompress((HERE/"PREDICTIONS-MARQUE.json.gz").read_bytes()))
    seed = next(r for r in proposals["Celse"]["3"] if r["seed"]==["ulcera","cum"])
    keys = [dict(zip(SIGNS, row)) for row in seed["keys"]]
    key, = [key for key in keys if key["e"]+key["y"]=="cera"]
    pairs = []
    for locus,row in dictionary.items():
        for i in range(len(row)-1):
            if row[i:i+2] == seed["seed"]:
                pairs.append(dict(locus=locus, index=i, next_word=row[i+2] if i+2<len(row) else None))
    targets = [("otair",tuple("otair"),"ulcera",-1),("dar",tuple("dar"),"cum",-1),
               ("cheekey",("e","e","k","e","y"),"cum",1)]
    trials = concordances(dictionary, targets, key)
    editions,_ = voynich()
    lines = agreed(editions)
    pages = {}
    for page in PAGES:
        counts = Counter()
        sites = []
        total = 0
        for locus, (single, _, _) in lines.items():
            if locus.split(".")[0]!=page:
                continue
            for (word,),n in single.items():
                total += n
                reading = decode(word,key)
                if reading is not None:
                    counts[word] += n
                    sites.append(dict(locus=locus, word=word, n=n))
        readings = {w:dict(form=decode(w,key), n=n, attested=decode(w,key) in vocab)
                    for w,n in counts.items()}
        pages[page] = dict(total=total, readings=readings, locations=sites)
    save("TRANSFERT.json",dict(key=key, alternatives=seed["predicted"], hits=pairs,
                               neighbor_trials=trials, pages=pages))


if __name__ == "__main__":
    main()
