"""Teste une occurrence de sub et de l'ablatif dans chaque paragraphe complet."""
import argparse
import csv
import hashlib
import itertools
import json
import random
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-secteurs-rouges"))
from tables import MODELS, merge, normalize, options
sys.path.insert(0, str(HERE.parent / "temoin"))
from extrait_bale import decode

WITNESS = json.loads((HERE.parent / "temoin/bale1429.json").read_text())
BAS = WITNESS["notices"]
DOM = json.loads((RESEARCH / "2026-11-18-sept-astres/domiciles.json").read_text())
SECTORS = tuple(DOM["secteurs"])
PLANETS = ("Saturne","Jupiter","Mars","Soleil","Vénus","Mercure","Lune")  # ordre de Bâle
NAMES = tuple(normalize(row["ablative"]) for row in BAS)
ASSIGNMENTS = [tuple(PLANETS.index(name) for name in d["astres"]) for d in DOM["solutions"]]
SOURCE = RESEARCH / "2026-11-18-secteurs-rouges/photos/secteurs.csv"


def merged(first, second, model):
    m = merge(first, second, model == 'bijection')
    return None if m is None else tuple(sorted(m.items()))


def freeze(path, result):
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


def encode_windows(rows, rng):
    plain = [list(map(normalize, words)) for _, _, words in decode(rows)]
    alphabet = sorted(set("".join(w for ws in plain for w in ws)))
    glyphs = [f"G{i:02}" for i in range(len(alphabet))]
    rng.shuffle(glyphs)
    code = dict(zip(alphabet, glyphs))
    return [[tuple(code[c] for c in w) for w in ws] for ws in plain]


def solve_calibration(training, cribs):
    keys = {()}
    for row, name in zip(training, cribs):
        row_keys = set()
        for first, second in zip(row,row[1:]):
            for one in options((first,), "sub", "bijection"):
                for two in options((second,), name, "bijection"):
                    key = merged(one,two,"bijection")
                    if key is not None:
                        row_keys.add(key)
        keys = {k for a in keys for b in row_keys if (k := merged(a,b,"bijection")) is not None}
    return keys


def read_held(cipher, key):
    table = dict(key)
    def read(group):
        return "".join(table.get(sign,("?",))[0] for sign in group)
    return [[{"first_word_position":j+1,"reading":read(neighbor)}
             for j,(word,neighbor) in enumerate(zip(row,row[1:])) if read(word) == "sub"]
            for row in cipher]


def calibration():
    seed = 1871429
    cipher = encode_windows(WITNESS, random.Random(seed))
    keys = solve_calibration(cipher[:4], NAMES[:4])
    assert len(keys) == 1
    key, = keys
    predictions = read_held(cipher[4:],key)
    scored = []
    for prediction, row in zip(predictions, BAS[4:]):
        assert len(prediction) == 1
        found, = prediction
        expected = normalize(row["ablative"])
        match = sum(c == d for c,d in zip(found["reading"],expected))
        assert len(found["reading"]) == len(expected) and found["first_word_position"] == row['sub_position_1based']
        scored.append(dict(found, expected=expected, correct_letters=match, total_letters=len(expected)))
    return {"seed":seed,"training_notices":["I.1","I.2","I.3","I.4"],"transfer_notices":["I.5","I.6","I.7"],
            "training_partial_keys":len(keys),"frozen_key":dict(key),"masked_16_word_passages":cipher,"held_predictions_scored":scored,
            "correct_letters":sum(x["correct_letters"] for x in scored),"total_letters":sum(x["total_letters"] for x in scored)}


def parse_row(text, first_line, alphabet, spaces, alternatives):
    """Return contiguous full words, preserving unknowns and word/locus coordinates."""
    out = []
    for i,line in enumerate(text.split(" | ")):
        line = re.sub(r'<[^>]*>','',line)
        for j,raw in enumerate(line.replace(',', '.' if spaces == 'split' else '').split('.')):
            variants = [raw]
            while True:
                next_variants = []
                changed = False
                for v in variants:
                    match = re.search(r'\[([a-z]+):([a-z]+)\]',v) if v is not None else None
                    if not match:
                        next_variants.append(v)
                    else:
                        changed = True
                        if alternatives == "omit":
                            next_variants.append(None)
                        else:
                            next_variants.extend(v[:match.start()]+alt+v[match.end():] for alt in match.groups())
                variants = next_variants
                if not changed:
                    break
            patt = r"ckh|cth|cph|cfh|ch|sh|." if alphabet == "EVA" else "."
            units = tuple(tuple(re.findall(patt, v)) for v in variants if v and re.fullmatch('[a-z]+',v))
            out.append((f".{first_line+i}/{j+1}",units))
    return out


def windows(row,layout):
    if layout == "separate":
        for (loc_a,group_a),(loc_b,group_b) in zip(row,row[1:]):
            for a,b in itertools.product(group_a,group_b):
                yield (loc_a,loc_b), (a,b)
    else:
        for loc,group in row:
            for a in group:
                yield (loc,), (a,)


@lru_cache(None)
def keys_at(sequences,name,model):
    if len(sequences) == 1:
        return options(sequences,"sub"+name,model)
    first,second = sequences
    return tuple(sorted({k for a in options((first,),"sub",model) for b in options((second,),name,model)
                         if (k := merged(a,b,model)) is not None}))


def collect(paragraphs,layout,model):
    matrix = []
    for row in paragraphs:
        candidate_list = list(windows(row,layout))
        locus = []
        for name in NAMES:
            seen = {}
            for loc,seq in candidate_list:
                for key in keys_at(seq,name,model):
                    seen.setdefault(key,[]).append((loc,tuple("".join(w) for w in seq)))
            locus.append(seen)
        matrix.append(locus)
    return matrix


def evaluate(matrix, assignment, model):
    edges = [matrix[j][n] for j,n in enumerate(assignment)]
    local = [j for j, opts in enumerate(edges) if opts]
    def solve(subset):
        ranked = sorted(subset,key=lambda j:len(edges[j]))
        keys = {()}
        for j in ranked:
            keys = {v for a in keys for b in edges[j] if (v := merged(a,b,model)) is not None}
            if not keys:
                break
        return keys
    for size in range(len(local),-1,-1):
        best = []
        for subset in itertools.combinations(local,size):
            keys = solve(subset)
            if keys:
                key = min(keys)
                example = []
                for j in subset:
                    valid = [pair for part,opts in edges[j].items() if merged(key,part,model)==key for pair in opts]
                    example.append({"sector":SECTORS[j],"ablative_normalized":NAMES[assignment[j]],"readable_at":sorted(set(valid))})
                best.append({"sectors":[SECTORS[j] for j in subset],"partial_keys":len(keys),"example_key":dict(key),"example":example})
        if best:
            break
    return {"individually":[SECTORS[j] for j in local],"maximum":size,"maximal_subsets":best}


def enumerate_null(matrix,model):
    """Compatible injective partial assignments; use individual masks before costly merging."""
    pieces = {()}
    frontier = {():{()}}
    while frontier:
        next_frontier = {}
        for indexed, partials in frontier.items():
            used = {n for _,n in indexed}
            for sector in range(indexed[-1][0]+1 if indexed else 0,7):
                for n, opts in enumerate(matrix[sector]):
                    if n in used or not opts:
                        continue
                    compatible = {v for a in partials for b in opts if (v:=merged(a,b,model)) is not None}
                    if compatible:
                        new = (*indexed,(sector,n))
                        pieces.add(new)
                        next_frontier[new] = compatible
        frontier = next_frontier
    # Covering all full permutations with each compatible partial yields their maxima.
    scores = {}
    for piece in sorted(pieces,key=len):
        free_sectors = sorted(set(range(7))-{s for s,_ in piece})
        free_names = sorted(set(range(7))-{n for _,n in piece})
        for names in itertools.permutations(free_names):
            sol = dict(piece)
            sol.update(zip(free_sectors,names))
            scores[tuple(sol[i] for i in range(7))] = len(piece)
    return scores


def manuscript():
    with SOURCE.open() as f:
        rows = {int(r['secteur']):r for r in csv.DictReader(f)}
    out = {"source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
           "sectors":SECTORS,"normalized_names":NAMES,
           "assignment_order":[[PLANETS[n] for n in v] for v in ASSIGNMENTS],
           "variants":{}}
    best_across = Counter()
    null_cache = {}
    for ed,alphabet,spaces in itertools.product(("H","ZL"), ("EVA","ASCII"), ("join","split")):
        for alt in (("literal","omit") if ed=="ZL" else ("literal",)):
            paragraphs = [parse_row(rows[s][ed+"_paragraphe_dans_ordre"],int(rows[s]['loci_paragraphe'].split('–')[0]),alphabet,spaces,alt) for s in SECTORS]
            label = "/".join((ed,alphabet,spaces,alt))
            result = []
            for layout,model in itertools.product(("separate","fused"),MODELS):
                matrix = collect(paragraphs,layout,model)
                entry = {"layout":layout,"model":model,"assignments":[evaluate(matrix,p,model) for p in ASSIGNMENTS]}
                signature = (model, tuple(tuple(frozenset(cell) for cell in r) for r in matrix))
                if signature not in null_cache:
                    null_cache[signature] = enumerate_null(matrix,model)
                scores = null_cache[signature]
                entry["distribution_maximum_5040_permutations"] = dict(sorted(Counter(scores.values()).items()))
                for preset, diagnostic in zip(ASSIGNMENTS,entry["assignments"]):
                    assert scores[preset] == diagnostic["maximum"]
                for perm,score in scores.items():
                    best_across[perm] = max(best_across[perm],score)
                unknown = [s for s,paragraph in zip(SECTORS,paragraphs) if any(not words for _,words in paragraph)]
                entry["sectors_with_unresolved_groups"] = unknown
                for diagnostic in entry["assignments"]:
                    diagnostic["upper_if_unresolved_groups_fully_favorable"] = min(7,diagnostic["maximum"]+len(unknown))
                result.append(entry)
            out["variants"][label] = result
    # Pour toute permutation de noms, autoriser aussi l'échange des deux luminaires.
    sol, luna = PLANETS.index("Soleil"), PLANETS.index("Lune")
    swap = {sol:luna, luna:sol}
    best_with_swap = {p:max(score,best_across[tuple(swap.get(n,n) for n in p)])
                      for p,score in best_across.items()}
    out["multiple_selection"] = {
        "n_analysis_cells": sum(map(len,out["variants"].values())),
        "n_distinct_key_matrices": len(null_cache),
        "max_across_all_variants_layouts_models": dict(sorted(Counter(best_across.values()).items())),
        "max_including_optional_exchange_of_solar_and_lunar_names":dict(sorted(Counter(best_with_swap.values()).items()))}
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase",choices=("etalonnage","manuscrit"))
    selected = p.parse_args().phase
    result = calibration() if selected == "etalonnage" else manuscript()
    freeze(HERE/(selected+".json"),result)
