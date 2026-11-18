"""Projections d'une lecture latine et vérification sur deux cryptogrammes à clé cachée."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import json
import re
import sys

from lectures_contextuelles import HERE, RESEARCH, WORDS, encode, save, tables
from corpus_sources import celsus
sys.path.insert(0, str(RESEARCH/"2026-11-18-opcheor-paralleles/variantes"))
from compter import corpus, runs, segment

CLEAR = ("adhibenda", "adhibendi", "lenes", "leniores")


def keys():
    result = [{}]
    for signs, word in zip(WORDS, CLEAR):
        seq = encode(signs, "position")
        result = [updated for known in result for updated in tables(seq, word, 3, known)]
    assert result
    return result


def translated(group, key):
    seq = encode(segment(group),"position")
    return "".join(key.get(k,"["+k+"]") for k in seq)


def spans(raw, cut):
    return [[w for _,w in span] for span in runs(re.sub(r"\{[^}]*\}","?",raw), cut)]


def manuscript(data, mappings):
    edition, _ = corpus()
    views = {}
    local = {"f89r2.5":{}, "f89r2.22":{}, "f100v.10":{}, "f100v.16":{}}
    for name, rows in edition.items():
        for cut in ("joints","separes"):
            index = {}
            for loc,(page,kind,_,raw) in rows.items():
                if loc in local:
                    local[loc][name+"-"+cut] = [w for group in spans(raw,cut) for w in group]
                if kind=="P0" and re.match(r"f\d+",page)[0] not in ("f89","f100"):
                    count = Counter()
                    for group in spans(raw,cut):
                        count.update(zip(group, group[1:]))
                    index[loc]=count
            views[name+"-"+cut] = index
    agreed = defaultdict(dict)
    for loc in sorted(set.intersection(*(set(v) for v in views.values()))):
        head,*tail = [v[loc] for v in views.values()]
        shared = head.copy()
        for rest in tail:
            shared &= rest
        for pair,n in shared.items():
            agreed[pair][loc] = n
    lex = {w for chapter in data.values() for w in chapter}
    real_pairs = {pair for chapter in data.values() for pair in zip(chapter,chapter[1:])}
    all_words = {w for pair in agreed for w in pair}
    records = []
    for key in mappings:
        locs = {l:{view:[translated(w,key) for w in words] for view,words in rd.items()} for l,rd in local.items()}
        rendered = {w:translated(w,key) for w in all_words}
        complete = {w:v for w,v in rendered.items() if "[" not in v}
        out = []
        for g, hits in sorted(agreed.items()):
            if all(w in complete for w in g):
                target = tuple(complete[w] for w in g)
                out.append({"groupes":g, "latin":target, "occurrences":sum(hits.values()),
                            "lieux":hits, "deux_mots_attestes":all(w in lex for w in target),
                            "suite_attestee":target in real_pairs})
        records.append({"cle":key,"projections":locs,"couples":out})
    return {"par_table":records,"paires_vues":sum(sum(v.values()) for v in agreed.values()),
            "paires_distinctes":len(agreed), "loci":local}


def true_control(data, start, rank):
    actual = tuple(data[start][rank:rank+4])
    # Substitution injective opaque, fixe. L'apprenant reçoit seulement les identifiants.
    import random
    alphabet = sorted({c for w in actual for c in w})
    ids = [f"s{i}" for i in range(len(alphabet))]
    random.Random(1487).shuffle(ids)
    key = dict(zip(alphabet,ids))
    cipher = [tuple(key[c] for c in w) for w in actual]
    hits = []
    for loc, body in data.items():
        for j in range(len(body)-3):
            words = body[j:j+3]
            if tuple(map(len, words)) != tuple(map(len, cipher[:3])):
                continue
            mapping = {}
            for ids, word in zip(cipher[:3], words):
                for unit,c in zip(ids,word):
                    if mapping.setdefault(unit,c)!=c:
                        break
                else:
                    continue
                break
            else:
                if len(set(mapping.values()))==len(mapping):
                    result = ''.join(mapping.get(s,"?") for s in cipher[3])
                    hits.append({"locus":loc, "rang":j+1,"debut":words,
                                 "prediction":result,"quatrieme":body[j+3]})
    return {"locus":start,"rang":rank+1,"chiffre":cipher,"vraie_suite":actual,"candidats":hits}


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("xml",type=Path)
    args = cli.parse_args()
    data = celsus(args.xml)
    record = next(r for r in json.loads((HERE/"PREDICTIONS.json").read_text())
                  ["essais"]["Celse"]["position-0"]["triplets"])
    first = true_control(data, record["segment"],record["rang"]-1)
    assert first["vraie_suite"][:3] == CLEAR[:3]
    assert any(row["prediction"]=="e?" for row in first["candidats"])
    start, rank = next((loc,j) for loc,body in data.items() if loc.startswith("4.12.")
                       for j in range(len(body)-3) if len(body[j+3])>=4
                       and body[j+3] not in body[j:j+3]
                       and set(body[j+3])<=set("".join(body[j:j+3])))
    second = true_control(data,start,rank)
    assert any(r["prediction"]==second["vraie_suite"][-1] for r in second["candidats"])
    # Autres attestations de la seule sortie lexicale de la règle sans signe muet.
    other = {l:w.count("leniores") for l,w in data.items() if not l.startswith("4.") and "leniores" in w}
    proj = manuscript(data, keys())
    def compatible(prediction, distractor):
        return len(prediction)==len(distractor) and all(
            a=="?" or a==b for a,b in zip(prediction, distractor))
    save(HERE/"TRANSFERT.json",{"voynich":proj,"temoin_partiel":first,"temoin_complet":second,
                                "leurre_ad_compatible_avec_la_prediction":any(compatible(r["prediction"],"ad") for r in first["candidats"]),
                                "leniores_hors_livre_IV":other})
    print("tables",len(proj["par_table"]), "éligibles avant clé",proj["paires_vues"])
    print("paires couvertes", Counter((len(r["couples"]),sum(x["occurrences"] for x in r["couples"]),
                                       sum(x["occurrences"] for x in r["couples"] if x["suite_attestee"]))
                                      for r in proj["par_table"]))
    print("témoins",first["vraie_suite"],first["candidats"],second["vraie_suite"],second["candidats"])


if __name__=="__main__":
    main()
