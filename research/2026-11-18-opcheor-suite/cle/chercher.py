"""Ajuster une table commune sur deux triplets, en gardant la suite du témoin cachée."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import gzip
import json
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import segment
sys.path.insert(0, str(RESEARCH / "2026-11-18-phrase-et-doublets/lecture"))
from corpus_sources import LATIN, celsus, gart

A = ("opcheor", "opcheol", "shody")
B = ("okeor", "okeol", "dy")
FOLLOW = "sholdy"
THIRD_PAGE = ("ctheor", "ctheol", "cheeor")
RIDGES = RESEARCH / "2026-11-18-phrase-et-doublets/lecture/RIDGES.json"


def write(name, obj):
    raw = (json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode()
    (HERE / name).write_bytes(gzip.compress(raw, mtime=0) if name.endswith(".gz") else raw)


def corpora(xml):
    return {"Macer": json.loads(LATIN.read_bytes()), "Celse": celsus(xml, r"[.;:!?]"),
            "Mayence1485": gart(), "RIDGES": json.loads(RIDGES.read_bytes())}


def merged(word, pairs):
    units = segment(word)
    result = []
    i = 0
    while i < len(units):
        pair = units[i:i+2]
        if len(pair) == 2 and pair in pairs:
            result.append("+".join(pair))
            i += 2
        else:
            result.append(units[i])
            i += 1
    return tuple(result)


def configurations():
    pairs = set()
    for word in A + B:
        u = segment(word)
        pairs.update(zip(u, u[1:]))
    for n in range(3):
        yield from combinations(sorted(pairs), n)


def common(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


def index(body):
    candidates = []
    for loc, words in body.items():
        for i, triple in enumerate(zip(words, words[1:], words[2:])):
            overlap = common(*triple[:2])
            if overlap:
                candidates.append((loc, i, triple, overlap))
    return candidates


def extend(units, word, cap, key):
    if not len(units) <= len(word) <= cap * len(units):
        return
    if not units:
        yield key
        return
    tok = units[0]
    if tok in key:
        value = key[tok]
        if word.startswith(value):
            yield from extend(units[1:], word[len(value):], cap, key)
        return
    for n in range(1, min(cap, len(word)) + 1):
        value = word[:n]
        if value not in key.values():
            yield from extend(units[1:], word[n:], cap, {**key, tok: value})


def decode(word, pairs, key):
    units = merged(word, pairs)
    if all(x in key for x in units):
        return "".join(key[x] for x in units)
    return None


def candidates_for(shapes, cap, pool):
    overlap_needed = common(*shapes[:2])
    hits = []
    for loc, pos, triple, overlap in pool:
        if overlap < overlap_needed:
            continue
        if not all(len(s) <= len(w) <= cap * len(s) for w, s in zip(triple, shapes)):
            continue
        for ka in extend(shapes[0], triple[0], cap, {}):
            for kb in extend(shapes[1], triple[1], cap, ka):
                for key in extend(shapes[2], triple[2], cap, kb):
                    hits.append((loc, pos, triple, key))
    return hits


def unite(left, right):
    union = {**left, **right}
    if all(union[k] == v for k, v in left.items()) and len(set(union.values())) == len(union):
        return union
    return None


def predictions(body):
    pool = index(body)
    cached = lru_cache(maxsize=None)(lambda shape, cap: candidates_for(shape, cap, pool))
    stats, singles, joint = {}, {}, {}
    for pairs in configurations():
        a, b = [tuple(merged(w, pairs) for w in triple) for triple in (A, B)]
        for cap in (1, 2):
            left, right = cached(a, cap), cached(b, cap)
            label = json.dumps([pairs, cap], separators=(",", ":"))
            count = 0
            for loc, pos, words, key in left:
                nxt = decode(FOLLOW, pairs, key)
                site = (loc, pos, nxt)
                if site not in singles:
                    singles[site] = dict(lieu=[loc, pos + 1], mots=words, suite=nxt, fusions=pairs, table=key)
                for loc2, pos2, words2, k2 in right:
                    if (loc, pos) == (loc2, pos2):
                        continue
                    both = unite(key, k2)
                    if both is None:
                        continue
                    count += 1
                    ident = (loc, pos, loc2, pos2, tuple(sorted(both.items())), pairs)
                    joint[ident] = dict(f89=[loc, pos + 1, words], f100=[loc2, pos2 + 1, words2],
                                        suite=decode(FOLLOW, pairs, both), fusions=pairs, table=both,
                                        f52=[decode(w, pairs, both) for w in THIRD_PAGE])
            stats[label] = [len(left), len(right), count]
    return {"segments": len(body), "mots": sum(map(len,body.values())),
            "triplets": sum(max(0, len(words) - 2) for words in body.values()), "regles":stats,
            "f89_lieux_sorties":list(singles.values()), "deux_passages":list(joint.values())}


def control():
    # Une unité écrit deux lettres. Le couple de
    # glyphes o+p forme une seule lettre, sans quoi le premier mot est trop court.
    pairs = (("o","p"),)
    key = {"o+p":"a","ch":"b","e":"c","o":"d","r":"e","l":"f","sh":"gh","d":"i","y":"j","k":"k"}
    seqs = [[decode(w,pairs,key) for w in t] for t in (A,B)]
    end = decode(FOLLOW,pairs,key)
    body = {"A":[*seqs[0],end], "B":[*seqs[1],"suite"], "A_leurre":[*seqs[0],end[::-1]]}
    pred = predictions(body)
    true_keys = [r for r in pred["deux_passages"] if r["f89"][0]=="A" and r["f100"][0]=="B"
                 and dict(r["table"]) == key and r["suite"] == end and r["fusions"]==pairs]
    no_merge = pred["regles"]['[[],2]']
    decoys = [r for r in pred["deux_passages"] if r["f89"][0]=="A_leurre" and r["f100"][0]=="B"
              and r["table"]==key and r["fusions"]==pairs]
    assert true_keys and not no_merge[0] and decoys
    assert all(r["suite"]==body["A"][3] for r in true_keys)
    assert all(r["suite"]!=body["A_leurre"][3] for r in decoys)
    return {"textes":body, "chiffre": [A,B], "fusion_attendue":pairs, "cle_attendue":key,
            "cle_recuperee":True, "quatrieme":end, "contre_exemple":end[::-1],
            "triplets_f89_sans_fusion":no_merge[0]}


def announce(xml):
    out = {"controle":control(), "corpus":{}}
    for name, body in corpora(xml).items():
        out["corpus"][name]=predictions(body)
    write("ANNONCES.json.gz", out)


def verify(xml):
    prior = json.loads(gzip.decompress((HERE/"ANNONCES.json.gz").read_bytes()))
    results={}
    for name, body in corpora(xml).items():
        part=prior["corpus"][name]
        def actual(loc, pos):
            words = body[loc]
            return words[pos+2] if pos+2 < len(words) else None
        def opened(rows, joint):
            detail=[]
            for row in rows:
                loc,pos=row["f89"][:2] if joint else row["lieu"]
                w=actual(loc,pos)
                detail.append({**row, "quatrieme_atteste":w, "succes":None if None in (w,row["suite"]) else w==row["suite"]})
            return detail
        results[name]={"un":opened(part["f89_lieux_sorties"],False),"deux":opened(part["deux_passages"],True)}
    write("OUVERTURE.json.gz",results)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("annoncer","ouvrir"))
    parser.add_argument("xml",type=Path)
    args=parser.parse_args()
    (announce if args.mode=="annoncer" else verify)(args.xml)
