"""Compare seven astronomical inscriptions with every seven-place zodiacal window."""
import hashlib
import itertools
import json
import math
import re
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "voynich_20261028/data"
SOURCE = (15,22,28,31,34,37,47)
TARGET = tuple(range(27,34))
PARTNERS = (31,47,15,37,34,22,28)  # source locus for each target place
PUBLISHED = tuple(SOURCE.index(n) for n in PARTNERS)
FIXED = (0,1,3)  # op, yfa, ytoa on f72r3
PREFIX = ("ytoa","yfa","op")
ROW = re.compile(r"^<(f[^.,>]+)\.(\d+),(.)([A-Za-z0-9]{2})>\s+(.*)$")
PERMS = tuple(itertools.permutations(range(7)))
PAT = {"ASCII": re.compile("."), "EVA": re.compile("ckh|cth|cph|cfh|ch|sh|.")}


def read(path):
    loci, rings = {}, []
    last = None
    for line in path.read_text().splitlines():
        m = ROW.fullmatch(line)
        if not m:
            continue
        page, number, marker, kind, raw = m.groups()
        n = int(number)
        if marker == "!":
            continue
        key = (page,n)
        assert key not in loci
        loci[key] = kind, raw
        if kind == "Lz" and re.fullmatch(r"f(?:70|71|72|73)[rv]\d*",page):
            if last != (page,n-1,"Lz") or marker == "@":
                rings.append([])
            rings[-1].append(key)
        last = page,n,kind
    return loci,rings


def forms(raw, split, variant):
    text = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)
    text = re.sub(r"<[-~]>", ".", text)
    def alternatives(match):
        if variant == "strict":
            return "?"
        return match[1].split(":")[0 if variant == "first" else -1]
    text = re.sub(r"\[([^\]]+)\]", alternatives, text)
    text = re.sub(r"\{([a-z]+)\}", r"\1", text)
    text = text.replace(",", "." if split else "")
    return [w for w in text.strip(".").split(".") if w]


def windows(rings):
    out = {}
    for ring in rings:
        if len(ring) < 7:
            continue
        for i in range(len(ring) if len(ring)>7 else 1):
            keys = tuple(ring[(i+j)%len(ring)] for j in range(7))
            label = f"{keys[0][0]}.{keys[0][1]}-{keys[-1][1]}"
            assert label not in out
            out[label] = keys
    return out


def first_units(word, alphabet):
    m = re.match("[a-z]*",word)
    prefix = tuple(PAT[alphabet].findall(m[0]))
    return prefix, len(m[0]) == len(word)


def fixed_presence(words):
    hits, undecided = [], []
    possible_places = []
    for prefix in PREFIX:
        status = []
        for word in words:
            head = re.match("[a-z]*",word)[0]
            if head.startswith(prefix):
                status.append(True)
            elif head != word and prefix.startswith(head):
                status.append(None)
            else:
                status.append(False)
        possible_places.append([i for i,x in enumerate(status) if x is not False])
        if any(s is True for s in status):
            hits.append(prefix)
        elif None in status:
            undecided.append(prefix)
    possible_trio = any(len(set(assign)) == 3 for assign in itertools.product(*possible_places))
    return hits,undecided,possible_trio


def flexible(source, panel, alphabet):
    a = [first_units(w,alphabet) for w in source]
    b = [first_units(w,alphabet) for w in panel]
    possibilities = {}
    for size in (4,3,2):
        left = {u[:size] for u,_ in a if len(u)>=size}
        right = {u[:size] for u,_ in b if len(u)>=size}
        possibilities[size] = left & right
    for long,mid,short in itertools.product(*(sorted(possibilities[n]) for n in (4,3,2))):
        # Distinct initial two units imply distinct loci on each side.
        if len({long[:2], mid[:2], short[:2]}) == 3:
            return ["".join(prefix) for prefix in (long,mid,short)]
    if any(len(u)<4 and not complete for u,complete in a+b):
        return None
    return False


@lru_cache(maxsize=None)
def distance(s,t):
    previous = list(range(len(t)+1))
    for i,x in enumerate(s,1):
        row = [i]
        for j,y in enumerate(t,1):
            row.append(min(row[-1]+1,previous[j]+1,previous[j-1]+(x!=y)))
        previous = row
    return previous[-1]


def optimal(costs):
    best = {0:0}
    for row in costs:
        nxt = {}
        for used,price in best.items():
            for j,c in enumerate(row):
                bit = 1 << j
                if used & bit:
                    continue
                key = used | bit
                value = price+c
                if key not in nxt or nxt[key]>value:
                    nxt[key] = value
        best = nxt
    return best[(1<<len(costs))-1]


def rank(costs, permitted):
    score = sum(row[j] for row,j in zip(costs,PUBLISHED))
    tally = Counter(sum(row[j] for row,j in zip(costs,perm)) for perm in permitted)
    return {"meilleures":sum(n for val,n in tally.items() if val<score),
            "egales":tally[score],"total":sum(tally.values()),
            "optimum":min(tally),"publie":score}


def exact_rate(n,counts,slots):
    # All categories are disjoint. Inclusion-exclusion counts draws that contain all.
    den = math.comb(n,slots)
    good = 0
    for size in range(len(counts)+1):
        for missed in itertools.combinations(counts,size):
            rem = n-sum(missed)
            good += (-1)**size * (math.comb(rem,slots) if rem>=slots else 0)
    return str(Fraction(good,den))


def population(loci, all_forms):
    excluded = {("f67r2",i) for i in SOURCE}
    out = {}
    for sample in ("toutes_legendes","zodiaque"):
        choices = [(k,v[0]) for k,v in all_forms.items() if v and k not in excluded
                   and (loci[k][0].startswith("L") if sample=="toutes_legendes" else loci[k][0]=="Lz")]
        counts = Counter()
        unknown = 0
        for _,word in choices:
            hits,amb,_ = fixed_presence([word])
            if hits:
                counts[hits[0]] += 1
            elif amb:
                unknown += 1
        n = len(choices)-unknown
        values = [counts[p] for p in PREFIX]
        out[sample] = {"lignes_non_vides":len(choices),"filtrees":unknown,"denominateur":n,
                       "ytoa_yfa_op":values, "tirage_uniforme_sept":exact_rate(n,values,7),
                       "six_autres_places_si_une_ancre_identifiee":exact_rate(n-1,values[1:],6)}
    return out


def evaluate(loci, window, split, variant):
    readings = {k:forms(v[1],split,variant) for k,v in loci.items() if v[0].startswith("L")}
    first = {k:(words[0] if words else "?") for k,words in readings.items()}
    source = [first[("f67r2",n)] for n in SOURCE]
    target_id = "f72r3.27-33"
    out = {"population":population(loci,readings),"prefixes":{},"comparaisons":{}}
    for name,keys in window.items():
        chosen = [first[k] for k in keys]
        hits,amb,possible_trio = fixed_presence(chosen)
        out["prefixes"][name] = {"fixes":hits,"indecis":amb,"trio_possible":possible_trio,
                                 **{a:flexible(source,chosen,a) for a in PAT}}
    for width in ("premier","entier"):
        for alphabet,pat in PAT.items():
            seq = {}
            for key in set(k for keys in window.values() for k in keys) | {("f67r2",i) for i in SOURCE}:
                words = readings[key]
                text = (words[0] if width=="premier" else "".join(words)) if words else ""
                seq[key] = tuple(pat.findall(text)) if re.fullmatch("[a-z]+",text) else None
            ref = [seq[("f67r2",n)] for n in SOURCE]
            common = math.lcm(*(len(s) for s in seq.values() if s))
            scores = {}
            for name,keys in window.items():
                if None in ref or any(seq[k] is None for k in keys):
                    continue
                costs = [[distance(seq[k],s)*(common//max(len(seq[k]),len(s))) for s in ref] for k in keys]
                scores[name] = optimal(costs)
                if name == target_id:
                    out["comparaisons"][width+"_"+alphabet] = {
                        "lignes_f72_colonnes_f67":costs,"rang_attribution":rank(costs,PERMS),
                        "rang_quatre_restantes":rank(costs,(p for p in PERMS if all(p[i]==PUBLISHED[i] for i in FIXED)))}
            cell = out["comparaisons"].setdefault(width+"_"+alphabet,{})
            cell.update({"echelle":common,"couts_minimaux":scores})
    return out


def main():
    report = {}
    for edition in ("IT2a-n","ZL3b-n"):
        path = DATA/(edition+".txt")
        loci,rings = read(path)
        study = windows(rings)
        item = {"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                "series":{p:[k[1] for k in keys] for p,keys in study.items()},
                "source":[loci[("f67r2",n)][1] for n in SOURCE],
                "cible":[loci[("f72r3",n)][1] for n in TARGET],"lectures":{}}
        for split in (False,True):
            for variant in ("strict","first","last"):
                item["lectures"][("separe" if split else "joint")+"_"+variant] = evaluate(loci,study,split,variant)
        report[edition] = item
    assert optimal([[0,10],[4,0]]) == 0 and optimal([[0,1],[0,9]]) == 1
    assert fixed_presence(["?", "ydar"])[2] is False
    assert fixed_presence(["y?","yfa","op"])[2] is True
    assert fixed_presence(["ytoar","yfary","opalal"]) == (list(PREFIX),[],True)
    clear = ["abcdef","xyzuv","pqrst","jklm","ghi","abc","xy"]
    assert flexible(clear,["abcd","xyz","pq"],"ASCII") == ["abcd","xyz","pq"]
    assert flexible(clear,["abcdef","abcde","abcd"],"ASCII") is False
    toy = [tuple("AB"),tuple("CCC"),tuple("ADC")]
    code = [[distance(t,s) for s in toy] for t in reversed(toy)]
    assert optimal(code) == 0 and sum(code[i][i] for i in range(3)) > 0
    assert exact_rate(5,[1,2],2)=="1/5" and len(set(PUBLISHED))==7
    (HERE/"comparaisons.json").write_text(json.dumps(report,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n")


if __name__ == "__main__":
    main()
