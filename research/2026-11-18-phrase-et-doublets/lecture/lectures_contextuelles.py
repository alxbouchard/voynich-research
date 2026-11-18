"""Former les tables sur A B C, enregistrer D avant de consulter la quatrième position."""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import takewhile
from pathlib import Path
import argparse
import json
import sys

from corpus_sources import HERE, RESEARCH, load_all
sys.path.insert(0, str(RESEARCH / "2026-11-18-carte-sept-etoiles/lecture"))
from essai import tables

WORDS = (("o","p","ch","e","o","r"), ("o","p","ch","e","o","l"),
         ("sh","o","d","y"), ("sh","o","l","d","y"))
MECHANISMS = ("fixe", "l_contextuel", "position")
INSERTIONS = {"attendu": 2, "plus_tot": 1, "plus_tard": 3}


def encode(word, model):
    out = []
    for i, s in enumerate(word):
        position = "debut" if i == 0 else "fin" if i == len(word)-1 else "interieur"
        if model == "position" or (model == "l_contextuel" and s == "l" and position=="interieur"):
            s += "_" + position
        out.append(s)
    return tuple(out)


def mute_options(codes, allow):
    plain = {s for seq in codes for s in seq}
    options = {frozenset()}
    if allow:
        options.update(frozenset([s]) for s in plain)
        for base in {s.split("_")[0] for s in plain}:
            options.add(frozenset(s for s in plain if s.split("_")[0] == base))
    return sorted(options, key=lambda o: tuple(sorted(o)))


def erase(codes, mute):
    return [tuple(s for s in seq if s not in mute) for seq in codes]


def prefix_length(a, b):
    return sum(1 for _ in takewhile(lambda pair: pair[0] == pair[1], zip(a,b)))


def dictionary_index(words):
    index = defaultdict(set)
    for word in words:
        for i in range(len(word)):
            for k in (1,2,3):
                if i+k <= len(word):
                    index[word[:i], word[i+k:]].add(word)
    return index


def completions(seq, insert, key, vocabulary, index):
    prefix = "".join(key[s] for s in seq[:insert])
    suffix = "".join(key[s] for s in seq[insert+1:])
    middle = seq[insert]
    if middle in key:
        word = prefix + key[middle] + suffix
        return [word] if word in vocabulary else []
    return sorted(index.get((prefix, suffix), ()))


def run(data, model, allow, vocab, index):
    codes = [encode(seq, model) for seq in WORDS]
    first, second, third, fourth = codes
    options = [(silent, erase(codes[:3], silent)) for silent in mute_options(codes, allow)]
    base = tuple(fourth)
    masks = {}
    for label, i in INSERTIONS.items():
        pieces = list(third)
        pieces.insert(i, base[2])
        assert label != "attendu" or tuple(pieces) == base
        masks[label] = tuple(pieces)
    @lru_cache(maxsize=4096)
    def paires(a,b):
        keys = []
        for silent, (sa,sb,sc) in options:
            if not (len(sa)<=len(a)<=3*len(sa) and len(sb)<=len(b)<=3*len(sb)):
                continue
            if prefix_length(a,b) < prefix_length(sa,sb):
                continue
            initial = dict.fromkeys(silent, "")
            for ka in tables(sa, a, 3, initial):
                for kb in tables(sb, b, 3, ka):
                    keys.append((kb, sc))
        return keys
    @lru_cache(maxsize=4096)
    def predictions(a,b,c):
        seen = set()
        found = {label: set() for label in masks}
        covered = Counter()
        for kb, sc in paires(a,b):
            if not len(sc)<=len(c)<=3*len(sc):
                continue
            for key in tables(sc,c,3,kb):
                sig = tuple(sorted(key.items()))
                if sig in seen:
                    continue
                seen.add(sig)
                for label, seq in masks.items():
                    found[label].update(completions(seq, INSERTIONS[label], key, vocab, index))
                covered["valeur_l_connue" if base[2] in key else "valeur_l_inconnue"] += 1
        return {"tables": len(seen),"couverture": dict(covered),
                "mots": {k: sorted(v) for k,v in found.items()}}
    found, n_pair, n = [], 0, 0
    for name, body in data.items():
        for j in range(len(body)-3):
            a,b,c = body[j:j+3]
            n += 1
            # A common initial sequence has five units; at most two were copies of any one sign.
            if a[:3] != b[:3] or not paires(a,b):
                continue
            n_pair += 1
            pred = predictions(a,b,c)
            if pred["tables"]:
                found.append({"segment": name, "rang": j+1, "debut": [a,b,c], **pred})
    return {"fenetres": n, "paires_ajustees": n_pair, "triplets": found}


def check():
    d = {"cas": ["herba","herbae","tam","terram"]}
    vocab = {"herba","herbae","tam","terram","teram"}
    index = dictionary_index(vocab)
    flexible = run(d, "l_contextuel", True, vocab, index)
    rigid = run(d, "fixe", True, vocab, index)
    assert set(flexible["triplets"][0]["mots"]["attendu"]) >= {"teram","terram"}
    assert not rigid["triplets"][0]["mots"]["attendu"]
    empty = run(d, "l_contextuel", False, vocab, index)
    assert not empty["triplets"]
    return {"cas_construit": flexible, "rigide": rigid, "sans_muet": empty}


def readback(predictions, corpora):
    out = {}
    for source, entries in predictions["essais"].items():
        data = corpora[source]
        out[source] = {}
        for label, recs in entries.items():
            stat = {k: Counter() for k in INSERTIONS}
            rows = []
            for rec in recs["triplets"]:
                name, start = rec["segment"], rec["rang"]-1
                actual = data[name][start+3]
                scores = {}
                for k, found in rec["mots"].items():
                    st = stat[k]
                    st["triplets_ajustes"] += 1
                    st["annonces_non_vides"] += bool(found)
                    st["annonces_uniques"] += len(found)==1
                    st["mot_dans_liste"] += actual in found
                    st["unique_juste"] += found==[actual]
                    scores[k] = {"nombre":len(found), "trouve": actual in found}
                rows.append({"segment":name,"rang":start+1,"debut":rec["debut"],"vrai":actual,"comparaison":scores})
            out[source][label]={"mesures":dict(stat), "sites":rows}
    return out


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1, sort_keys=True)+"\n")


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("mode", choices=["predire","verifier"])
    cli.add_argument("xml", type=Path)
    cli.add_argument("--ridges", type=Path)
    args = cli.parse_args()
    corpora = load_all(args.xml, args.ridges)
    pred = HERE / "PREDICTIONS.json"
    if args.mode == "verifier":
        j = json.loads(pred.read_text())
        assert set(corpora) == set(j["essais"])
        result = readback(j, corpora)
        save(HERE/"VERIFICATION.json",result)
        for name, rr in result.items():
            for model, row in rr.items():
                print(name,model,row["mesures"]["attendu"])
        return
    tests, sizes = {}, {}
    for name,data in corpora.items():
        vocab = {w for body in data.values() for w in body}
        idx = dictionary_index(vocab)
        sizes[name] = {"segments":len(data),"mots":sum(map(len,data.values())),"graphies":len(vocab),
                       "sha256_segments":sha256(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()).hexdigest()}
        tests[name] = {f"{model}-{int(mute)}":run(data, model, mute, vocab, idx)
                       for model in MECHANISMS for mute in (False,True)}
        print(name, sizes[name], {k:len(v["triplets"]) for k,v in tests[name].items()}, flush=True)
    save(pred, {"sources":sizes, "essais":tests,"controle":check()})


if __name__=="__main__":
    main()
