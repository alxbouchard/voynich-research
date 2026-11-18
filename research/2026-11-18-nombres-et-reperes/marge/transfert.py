"""Compare l'ordre 1–5 de f49v aux deux listes cibles. Python 3.9+."""
import csv
import hashlib
import itertools
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parents[2] / "voynich_phase8" / "data"
HASH = {
    "ZL3b": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
    "IT2a": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
}

def read_tsv(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f, delimiter="\t"))

def segments(seq):
    starts = [i for i in range(len(seq)-1) if seq[i:i+2] == ["o", "l"]]
    assert len(starts) == 4 and starts[0] == 0
    return [seq[a:b] for a,b in zip(starts, starts[1:]+[len(seq)])]

def historical(raw):
    form = raw.replace("!", "").rstrip("=")
    form = re.sub(r"^\{[1-5]-\}", "", form)
    return re.sub(r"^\*\{&(\d+)\}$", r"@\1;", form)

def inputs():
    col = read_tsv("positions-f49v.tsv")
    raw_h = {r["locus"]: r["lecture_H"] for r in read_tsv("extraits-historiques-H.tsv")}
    corpus = {}
    for ed, expected in HASH.items():
        file = CORPUS / f"{ed}-n.txt"
        assert hashlib.sha256(file.read_bytes()).hexdigest() == expected
        text = file.read_text()
        source = [f.strip() for f in re.findall(r"^<f49v\.\d+,[@*]L0>\s+([^\r\n]+)", text, re.M)]
        k = source[1:6]
        assert k == [r["ZL3b" if ed=="ZL3b" else "H_converti_IT2a"] for r in col[1:6]]
        words = re.search(r"^<f57v\.3,\+Cc>\s+([^\r\n]+)",text,re.M).group(1)
        words = re.sub(r"<![^>]*>", "", words).strip()
        cycles = segments(words.split("." if ed=="ZL3b" else "<->"))
        margin = [f.strip() for f in re.findall(r"^<f76r\.\d+,[@*]L0>\s+([^\r\n]+)",text,re.M)]
        corpus[ed] = (k,cycles,margin)
    key = [historical(raw_h[f"<f49v.L.{i};H>"]) for i in range(2,7)]
    cycles = [[historical(s) for s in z.rstrip("-").split("-")] for z in raw_h["<f57v.R2.1;H>"].split("{|}")]
    margin = [historical(v) for k,v in raw_h.items() if k.startswith("<f76r.L.")]
    corpus["H_historique"] = key,cycles,margin
    for ed,(k,cyc,margin) in corpus.items():
        assert margin == list("sdqsolkrs")
        assert list(map(len,cyc)) == ([17,17,17,17] if ed=="ZL3b" else [17,17,17,18])
    return corpus

def choices(form):
    if form in {"?", "*"}:
        return frozenset()
    if form.startswith("["):
        return frozenset(form[1:-1].split(":")) - {"?"}
    return frozenset([form])

def alignments(cycles, length, ring=False, reverse=False):
    windows, blocks = [], set()
    for seq in cycles:
        for direction in ([1,-1] if reverse else [1]):
            for start in range(len(seq)):
                positions = [start+i*direction for i in range(length)]
                if ring:
                    positions = [j%len(seq) for j in positions]
                else:
                    positions = [j for j in positions if 0<=j<len(seq)]
                window = tuple(seq[j] for j in positions)
                # Même un petit bloc en bord de marge peut être comparé à toute partie de la clé.
                for end in range(1,len(window)+1):
                    blocks.add(window[:end])
                if len(window) == length:
                    windows.append(tuple(choices(s) for s in window))
    return set(windows), {tuple(choices(s) for s in block) for block in blocks}

def measure(ordered, windows, blocks):
    score = max(sum(not a.isdisjoint(b) for a,b in zip(ordered,w)) for w in windows)
    # Longueur du plus long fragment sans sauts commun à la clé et à la cible.
    common = max((len(b) for b in blocks if any(
        all(not x.isdisjoint(y) for x,y in zip(ordered[i:],b))
        for i in range(len(ordered)-len(b)+1))),default=0)
    return score,common

def summarize(keys, targets, detailed):
    digits = tuple(keys)
    windows,blocks=targets
    records = {}
    for perm in itertools.permutations(digits):
        name = "".join(perm)
        records[name] = measure([keys[i] for i in perm], windows, blocks)
    own = records["".join(digits)]
    scores = Counter(s for s,b in records.values())
    maxscore = max(scores)
    summary = {
        "positions": own[0], "bloc": own[1], "longueur": len(keys),
        "histogramme_positions": dict(sorted(scores.items())),
        "ordres_strictement_superieurs": sum(n for s,n in scores.items() if s>own[0]),
        "ordres_ex_aequo_incluant_prescrit": scores[own[0]],
        "maximum_positions": maxscore, "nombre_ordres": len(records),
    }
    if detailed:
        summary["meilleurs_ordres"] = [p for p,(s,b) in records.items() if s==maxscore]
        summary["exemple_ordre_superieur"] = next((p for p,(s,b) in records.items() if s>own[0]),None)
    return summary

def main():
    corpus=inputs()
    report={}
    for ed,(key,cycles,margin) in corpus.items():
        by_digit = {str(n):choices(k) for n,k in enumerate(key,1)}
        cases={"strict":by_digit, "sans_1":{d:v for d,v in by_digit.items() if d!="1"},
               "sans_5":{d:v for d,v in by_digit.items() if d!="5"}}
        cases["2_r_ou_s"] = dict(by_digit, **{"2":by_digit["2"]|{"s"}})
        cases["2_r_ou_192"] = dict(by_digit, **{"2":by_digit["2"]|{"@192;"}})
        # La forme 5 est indéterminée dans IT2a. Ne lui importer aucun succès.
        if by_digit["5"]:
            cases["5_140_ou_163"] = dict(by_digit, **{"5":by_digit["5"]|{"@163;"}})
        report[ed]={"cle":key,"quarts":cycles,"marge_f76r":margin,"calculs":{}}
        for case,keys in cases.items():
            targets={"f57v_quarts_meilleur":(cycles,True,True),
                     "f76r_descendant":([margin],False,False),
                     "f76r_deux_sens":([margin],False,True)}
            if case=="strict":
                for i,c in enumerate(cycles,1):
                    targets[f"f57v_quart_{i}"]=([c],True,True)
                if ed=="ZL3b":
                    split = [[v for token in c for v in
                              (["@169;", "v"] if token=="@169;v" else [token])]
                             for c in cycles]
                    assert list(map(len,split))==[18]*4
                    targets["f57v_169v_scinde"]=(split,True,True)
                else:
                    assert cycles[-1][-2:]==["r","n"]
                    joined = cycles[:-1]+[cycles[-1][:-2]+["rn"]]
                    targets["f57v_rn_final_reuni"]=(joined,True,True)
            report[ed]["calculs"][case]={}
            for target,(seqs,closed,reverse) in targets.items():
                views=alignments(seqs,len(keys),closed,reverse)
                report[ed]["calculs"][case][target] = summarize(keys,views,case=="strict" and "quart_" not in target)
    # Cas positifs avec inversion et bouclage, et contrôle des correspondances inconnues.
    test = {str(i): choices(x) for i,x in enumerate("ab?de",1)}
    result = summarize(test,alignments([list("deab?")],5,True,True),False)
    assert result["positions"]==4 and result["bloc"]==2
    assert measure([choices(x) for x in "ab"],*alignments([list("ab")],2))==(2,2)
    assert measure([choices(x) for x in "ab"],*alignments([list("ba")],2,reverse=True))==(2,2)
    (HERE/"transfert-resultats.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
