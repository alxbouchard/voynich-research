"""Voisins de otoldy dans deux éditions et rapprochements exploratoires avec fRos."""
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import factorial
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_20261028/data"
ED = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}
HEAD = re.compile(r"^<([^.,> ]+)>\s*<!\s*([^>]*)>")
LOC = re.compile(r"^<(([^.>]+)\.[^,>]+),.([A-Za-z0-9]{2})>\s*(.*)")
OFFSETS = (-2, -1, 1, 2)
TARGET = "otoldy"
PAIR = ("otchdy","otoldy")


@dataclass
class Row:
    page: str
    locus: str
    kind: str
    hand: str
    language: str
    picture: str
    opening: bool
    ending: bool
    words: list
    gaps: set

    def in_botanical_prose(self):
        return self.picture == "H" and self.kind.startswith("P")


def load(path, separated):
    pages = {}
    for line in path.read_text().splitlines():
        header = HEAD.match(line)
        if header:
            pages[header[1]] = dict(re.findall(r"\$(\w)=([^\s]+)",header[2]))
        match = LOC.match(line)
        if not match:
            continue
        loc, page, kind, raw = match.groups()
        meta = pages[page]
        clean = re.sub(r"<![^>]*>|<@[^>]*>|<[%$]>", "",raw).replace("!", "")
        clean = clean.replace(",", "." if separated else "")
        words, gaps = [], set()
        for i, segment in enumerate(re.split(r"<[-~]>", clean)):
            if i:
                gaps.add(len(words))
            words.extend(w for w in segment.split(".") if w)
        yield Row(page,loc,kind,meta.get("H","?"),meta.get("L","?"),meta.get("I","?"),
                  "<%>" in raw,"<$>" in raw,words,gaps)


def clear(w):
    return bool(re.fullmatch(r"[a-z]+", w))


def edge(row, i):
    if len(row.words) == 1:
        return "seul"
    if i == 0:
        return "initial"
    if i+1 == len(row.words):
        return "final"
    return "intérieur"


def neighbour(row, i, shift, barrier):
    j = i+shift
    if not 0 <= j < len(row.words):
        return None
    if barrier and any(min(i,j) < gap <= max(i,j) for gap in row.gaps):
        return None
    return row.words[j] if clear(row.words[j]) else None


def context(hits, barrier):
    available = Counter()
    matching = defaultdict(list)
    frames = []
    for (a,i),(b,j) in combinations(hits,2):
        if a.page == b.page:
            continue
        matches = []
        for offset in OFFSETS:
            x, y = neighbour(a,i,offset,barrier), neighbour(b,j,offset,barrier)
            if x is None or y is None:
                continue
            available[offset] += 1
            if x == y:
                matching[offset].append([a.locus,b.locus,x])
                matches.append(offset)
        if -1 in matches and 1 in matches:
            frames.append([a.locus,b.locus])
    return {"comparables":{k:available[k] for k in OFFSETS},
            "accords":{k:matching[k] for k in OFFSETS},"score":len(matching[-1])+len(matching[1]),"cadres":frames}


def controls(index, target, barrier):
    def hands(hits):
        return Counter((r.hand,r.language) for r,i in hits)
    def edges(hits):
        return Counter(edge(r,i) for r,i in hits)
    target_rows = index[target]
    target_hands, target_edges = hands(target_rows), edges(target_rows)
    n_pages = len({r.page for r,i in target_rows})
    score = context(target_rows,barrier)["score"]
    groups = {"fréquence_main_langue_faces":{}, "positions_identiques":{}}
    for word, hits in sorted(index.items()):
        if word == target or len(hits) != len(target_rows) or hands(hits) != target_hands:
            continue
        if len({r.page for r,i in hits}) != n_pages:
            continue
        counts = context(hits,barrier)
        result = {"score":counts["score"],"comparables":counts["comparables"]}
        groups["fréquence_main_langue_faces"][word] = result
        if edges(hits) == target_edges:
            groups["positions_identiques"][word] = result
    for name, group in groups.copy().items():
        scores = [v["score"] for v in group.values()]
        groups[name] = {"n":len(scores),"au_moins_cible":sum(s >= score for s in scores),
                        "scores":dict(sorted(Counter(scores).items())),"mots":group}
    return groups


def crossed_labels(labels, botanical):
    # Count assignments of second words to first words that avoid every known botanical pair.
    values = list(labels.values())
    allowed = []
    hits = 0
    for first, _ in values:
        available = 0
        for j, (_, second) in enumerate(values):
            if (first,second) in botanical:
                hits += 1
            else:
                available |= 1 << j
        allowed.append(available)
    n = len(values)
    if n == 0:
        return None
    @lru_cache(None)
    def without_matches(unused):
        if not unused:
            return 1
        choices = unused & allowed[n-unused.bit_count()]
        total = 0
        while choices:
            bit = choices & -choices
            total += without_matches(unused ^ bit)
            choices ^= bit
        return total
    all_orders = factorial(n)
    none = without_matches((1 << n)-1)
    return {"permutations":all_orders,"zéro":none,"au_moins_un":str(Fraction(all_orders-none,all_orders)),
            "possibilités_de_couple":n*n,"possibilités_donnant_un_bigramme_botanique":hits}


def rosettes(rows):
    # Exploratoire. Compare chaque légende entière de deux mots à tous les bigrammes botaniques.
    labels = {}
    manuscript = []
    reverse = []
    botanical = defaultdict(list)
    for row in rows:
        words = row.words
        if row.page == "fRos" and row.kind.startswith("L") and len(words) == 2 and all(map(clear,words)):
            labels[row.locus] = tuple(words)
        for i, pair in enumerate(zip(words,words[1:])):
            if i+1 in row.gaps or not all(map(clear,pair)):
                continue
            if row.in_botanical_prose():
                botanical[pair].append([row.locus,i+1])
            if pair == PAIR:
                manuscript.append([row.locus,i+1,row.kind])
            if pair == PAIR[::-1]:
                reverse.append([row.locus,i+1,row.kind])
    return {"fRos_lignes":sum(r.page=="fRos" for r in rows),"fRos_étiquettes":sum(r.page=="fRos" and r.kind.startswith("L") for r in rows),
            "couple_exact_tout_manuscrit":manuscript,"étiquettes_de_deux_mots_lisibles":len(labels),
            "couple_inverse_tout_manuscrit":reverse,
            "permutations_second_mot":crossed_labels(labels,botanical),
            "couples_distincts":len(set(labels.values())),"étiquettes_avec_reprise_en_prose_botanique":
            {loc:{"mots":words,"prose":botanical[words]} for loc,words in labels.items() if words in botanical}}


def analyse(rows):
    index = defaultdict(list)
    selected = [r for r in rows if r.in_botanical_prose()]
    for row in selected:
        for i, word in enumerate(row.words):
            if clear(word):
                index[word].append((row,i))
    hits = index[TARGET]
    index_a = {word: [(r,i) for r,i in hits if (r.hand,r.language) == ("1","A")] for word,hits in index.items()}
    table = []
    for r,i in hits:
        table.append({"lieu":r.locus,"main":r.hand,"Currier":r.language,"position":i+1,"longueur_ligne":len(r.words),
                      "ligne_ouvre_paragraphe":r.opening,"ligne_ferme_paragraphe":r.ending,
                      "statut":edge(r,i),"voisins":{k:neighbour(r,i,k,False) for k in OFFSETS},
                      "coupures_dessin_après_position":sorted(r.gaps)})
    return {"faces_prose":len({r.page for r in selected}),"lignes_prose":len(selected),
            "positions":sum(len(r.words) for r in selected),"positions_simples":sum(map(len,index.values())),
            "lignes_otoldy":table,"comparaisons":{name:{"cible":context(hits,b),"témoins":controls(index,TARGET,b)}
            for b,name in [(False,"même_ligne"),(True,"même_segment")]},
            "complément_main_1_A":{"cible":context(index_a[TARGET],False),"témoins":controls(index_a,TARGET,False)},
            "rosettes_exploratoire":rosettes(rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sortie",type=Path,default=HERE/"RESULTATS.json")
    options = parser.parse_args()
    out = {}
    for name,filename in ED.items():
        path = DATA/filename
        out[name] = {"sha256":sha256(path.read_bytes()).hexdigest(),
                     "variantes":{mode:analyse(list(load(path,sep))) for sep,mode in [(True,"séparés"),(False,"joints")]}}
    options.sortie.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")


if __name__ == "__main__":
    main()
