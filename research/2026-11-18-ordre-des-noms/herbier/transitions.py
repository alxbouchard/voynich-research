"""Prédire le premier signe de la notice suivante, dans l'ordre matériel conservé."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-formes-souterraines"))
from langage import DATA, UNIT, tokens

LOTS = {"apprentissage": "ABC", "reserve": "DEFG"}
FIELDS = {"debut": (0, 0), "deuxieme_mot": (0, 1), "deuxieme_ligne": (1, 0), "sans_potence": (0, 0)}
GALLOWS = {"t", "p", "k", "f", "cth", "cph", "ckh", "cfh"}


def write(name, result):
    (HERE/name).write_text(json.dumps(result, ensure_ascii=False, indent=1)+"\n")


def metadata():
    records = {}
    for line in (DATA/"ZL3b-n.txt").read_text().splitlines():
        match = re.match(r"^<(f\d+[rv])>\s",line)
        if match:
            data = dict(re.findall(r"\$(\w)=(\w+)",line))
            if data.get("Q") in tuple("ABCDEFG"):
                records[match[1]] = data
    return records


def adjacent(meta, lot):
    pairs = []
    for face,a in meta.items():
        if face[-1]!="v" or a["Q"] not in lot:
            continue
        next_face = f"f{int(face[1:-1])+1}r"
        b = meta.get(next_face,{})
        if a.get("I")==b.get("I")=="H" and a["Q"]==b.get("Q") and a["B"]!=b.get("B"):
            if all(a.get(k) and a[k]==b.get(k) for k in ("H","L")):
                pairs.append((face,next_face))
    return pairs


def views(faces):
    data = {f:defaultdict(list) for f in faces}
    for split in ("joints","separes"):
        for ed, records in tokens(faces,split).items():
            for face, items in records.items():
                rows = {}
                for loc,w in items:
                    line, _ = loc.rsplit("/",1)
                    rows.setdefault(line,[]).append(w)
                # Les loci sont dans l'ordre de la transcription, sans reclasser des numéros.
                places = list(rows.items())[:2]
                for field, (line, col) in FIELDS.items():
                    word = place = None
                    if line<len(places) and col<len(places[line][1]):
                        place, words = places[line]
                        word = words[col]
                    units = UNIT.findall(word or "")
                    if field=="sans_potence" and units and units[0] in GALLOWS:
                        units = units[1:]
                    data[face][field].append((place, word, units[0] if units else None))
    readings = {}
    for face, fields in data.items():
        readings[face] = {}
        for field, versions in fields.items():
            loci = {v[0] for v in versions}
            alternatives = {v[2] for v in versions}
            readings[face][field] = {"signe":versions[0][2] if len(loci)==len(alternatives)==1 else None,
                     "loci":sorted(x for x in loci if x), "mots": sorted({v[1] for v in versions if v[1]})}
    return readings


def predict(meta):
    sources = {f for f in meta if f.endswith("v")}
    features = views(sources)
    predictions = {}
    for name, quires in LOTS.items():
        predictions[name] = [{"source":a,"destination":b,"cahier":meta[a]["Q"],
            "main":meta[a]["H"],"currier":meta[a]["L"],"gauche":features[a]}
            for a,b in adjacent(meta,quires)]
    return predictions


def blocks(meta, quire):
    sheets = defaultdict(list)
    for face,m in meta.items():
        if m['Q']==quire:
            sheets[m['B']].append(face)
    groups = defaultdict(list)
    for faces in sheets.values():
        faces.sort(key=lambda f:(int(f[1:-1]),f[-1]))
        signature = tuple(tuple(meta[f].get(k) for k in ('I','H','L')) for f in faces)
        groups[signature].append(faces)
    return list(groups.values())


def reshuffle(groups):
    for select in product(*(permutations(g) for g in groups)):
        yield {dest:source for g,order in zip(groups,select) for to,fr in zip(g,order)
               for dest,source in zip(to,fr)}


def summary(pairs, values, field, mask=()):
    eligible = [(a,b) for a,b in pairs if all(values[f].get(k) is not None
                for f in (a,b) for k in (field,*mask))]
    return sum(values[a][field]==values[b][field] for a,b in eligible), len(eligible)


def distribution(meta, quires, values, field, mask=(), pair_rule=adjacent, fixed_left=False):
    distribution = Counter({(0,0):1})
    for q in quires:
        pairs = pair_rule(meta,q)
        stats = Counter()
        for mapping in reshuffle(blocks(meta,q)):
            replaced = [(a if fixed_left else mapping[a],mapping[b]) for a,b in pairs]
            stats[summary(replaced,values,field,mask)] += 1
        merged = Counter()
        for (c,n),m in distribution.items():
            for (d,o),freq in stats.items():
                merged[c+d,n+o] += m*freq
        distribution = merged
    c,n = summary(pair_rule(meta,quires),values,field,mask)
    total = sum(distribution.values())
    valid = sum(m for (x,y),m in distribution.items() if y)
    ge = sum(m for (x,y),m in distribution.items() if y and n and x*n>=c*y)
    return dict(succes=c, testables=n, configurations=total, avec_denominateur=valid,
                moyenne_nulle=(float(sum(Fraction(x*m,y) for (x,y),m in distribution.items() if y)/valid)
                               if valid else None),
                egale_ou_superieure=ge, probabilite=ge/valid if valid and n else None,
                histogramme={f"{x}/{y}":m for (x,y),m in sorted(distribution.items())})


def main(mode):
    meta = metadata()
    if mode=="predire":
        write("PREDICTIONS.json",predict(meta))
        return
    saved = json.loads((HERE/"PREDICTIONS.json").read_text())
    assert saved==predict(meta)
    detailed = views(meta)
    values = {f:{k:v["signe"] for k,v in fields.items()} for f,fields in detailed.items()}
    result = {}
    for name,qs in LOTS.items():
        pairs = adjacent(meta,qs)
        checks = []
        for a,b in pairs:
            checks.append(dict(source=a,destination=b,cahier=meta[a]["Q"],droite=detailed[b]))
        observed = {field:distribution(meta,qs,values,field) for field in FIELDS}
        joint = tuple(FIELDS)[:3]
        pos = {field:distribution(meta,qs,values,field,joint) for field in joint}
        initial_freq = Counter(values[b]["debut"] for a,b in pairs
                               if values[b]["debut"] and values[a]["debut"])
        # Blocs artificiels avec quatre faces consécutives par classe de mot.
        artificial = {f:{"debut":(int(f[1:-1])-1)//2} for f in meta}
        control = distribution(meta,qs,artificial,"debut")
        result[name] = dict(tous_les_couples=len(pairs), appels=sum(bool(values[a]["debut"]) for a,b in pairs),
              frequences_droite=initial_freq, mesures=observed, joint=pos,
              affectations_par_cahier={q:[len(g) for g in blocks(meta,q)] for q in qs},
              controle_artificiel=control, cibles=checks)
    macer = json.loads((RESEARCH/"2026-11-18-opcheor-paralleles/latin/corpus.json").read_text())
    seq = [s.lower() for s in macer]
    result["controle_macer"] = {}
    for name,series in (("ordre_du_poeme",seq),("ordre_alphabetique",sorted(seq))):
        result["controle_macer"][name] = {f"prefixe_{length}":
              sum(a[:length]==b[:length] for a,b in zip(series,series[1:])) for length in (1,2)}
    result["controle_macer"]["transitions"] = len(seq)-1
    initial = Counter(x[0] for x in seq)
    result["controle_macer"]["accord_initial_aleatoire"] = float(sum(n*(n-1) for n in initial.values())/(len(seq)*(len(seq)-1)))
    write("RESULTATS.json",result)


if __name__=="__main__":
    main(sys.argv[1])
