"""Entraînement, dépôt des positions et contrôle des légendes par cahier."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "2026-11-18-cheor-en-contexte/distribution"))
from localite import MODES, common_words, corpus, folio, inventory, runs
from comparer import permutation_distribution

MODES_NAMES = [f"{ed}_{space}" for ed, space in MODES]
PROTOCOL = "1a3a9a8b2113bf298b068e366c50cf30f3f989d3ff951cc9166dc1641396262c"


def write(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True)+"\n")


def load():
    pages, quires, views = inventory()
    editions, _ = corpus()
    groups = defaultdict(list)
    for p in pages:
        if p != "f101r":
            groups[15 if int(folio(p)[1:]) < 99 else 19].append(p)
    for q in groups:
        groups[q].sort()
        assert len({quires[p] for p in groups[q]}) == 1
    assert quires[groups[15][0]] != quires[groups[19][0]]

    def captions(pages):
        return {p: common_words([views[mode][0][p] for mode in MODES]) for p in pages}

    locs = sorted(set.intersection(*(set(v) for v in editions.values())))
    lines = {}
    for loc in locs:
        if any(data[loc][1] != "P0" for data in editions.values()):
            continue
        if loc.partition(".")[0] not in pages:
            continue
        lines[loc] = []
        for ed, cut in MODES:
            raw = re.sub(r"\{[^}]*\}", "?", editions[ed][loc][3])
            lines[loc].append([list(s) for s in runs(raw, cut)])
    return groups, captions, lines


def locations(spans):
    by_word = defaultdict(list)
    for span in spans:
        for i, (_, word) in enumerate(span):
            by_word[word].append((span, i))
    return {w: pos[0] for w,pos in by_word.items() if len(pos) == 1}


def scan(pages, lines, distance, rule=None, masked=False):
    """L'appel dépend seulement de la présence du marqueur et d'une position voisine."""
    output = defaultdict(list)
    for locus, by_mode in lines.items():
        page = locus.partition(".")[0]
        if page not in pages:
            continue
        positions = [locations(s) for s in by_mode]
        markers = set.intersection(*(set(m) for m in positions))
        if rule:
            markers &= {rule[0]}
        for marker in sorted(markers):
            for offset in ([-distance, distance] if not rule else [rule[1]]):
                ranks, neighbors = {}, []
                for mode, view in zip(MODES_NAMES, positions):
                    span, i = view[marker]
                    j = i + offset
                    exists = 0 <= j < len(span)
                    ranks[mode] = [span[i][0], span[j][0] if exists else None]
                    if not masked:
                        step = 1 if offset > 0 else -1
                        neighbors.append(tuple(span[k][1] for k in range(i+step,j+step,step))
                                         if exists else None)
                if not any(end is not None for _, end in ranks.values()):
                    continue
                row = dict(locus=locus,panneau=page,rangs=ranks)
                if not masked:
                    agreed = neighbors[0] is not None and len(set(neighbors)) == 1
                    row["cible"] = neighbors[0][-1] if agreed else None
                    row["interpose"] = neighbors[0][0] if agreed and distance==2 else None
                output[marker, offset].append(row)
    return output


def annotate(rule, rows, labels, old=()):
    out = []
    for row in rows:
        p, w = row["panneau"], row["cible"]
        matched = labels[p].get(w, []) if w != rule[0] else []
        out.append(dict(row, legendes=matched, nouveau=bool(matched and w not in old)))
    return out


def figures(rows):
    hits = [r for r in rows if r["legendes"]]
    names = sorted({r["cible"] for r in hits})
    folios = sorted({folio(r["panneau"]) for r in hits})
    return dict(appels=len(rows),lisibles=sum(r["cible"] is not None for r in rows),
                justes=len(hits), graphies=names, feuillets=folios)


def rank(stats):
    return (len(stats["feuillets"]),len(stats["graphies"]),
            Fraction(stats["justes"],stats["appels"]),stats["justes"])


def learn(pages, labels, lines, distance):
    candidates = []
    for rule, calls in scan(pages,lines,distance).items():
        rows = annotate(rule,calls,labels)
        stats = figures(rows)
        if stats["justes"]:
            witnesses = [{k:r[k] for k in ("locus","cible","legendes","interpose")} for r in rows if r["legendes"]]
            candidates.append(dict(regle=list(rule),apprentissage=stats,depuis=witnesses))
    return sorted(candidates,key=lambda x:(tuple(-n for n in rank(x["apprentissage"])),x["regle"]))


def choose(candidates, strict):
    valid = [c for c in candidates if not strict or
             min(len(c["apprentissage"][n]) for n in ["feuillets","graphies"]) >= 2]
    if not valid:
        return None, []
    return valid[0], [c["regle"] for c in valid if rank(c["apprentissage"]) == rank(valid[0]["apprentissage"])]


def prepare(q, groups, captions, lines):
    reserve = groups[34-q]
    labels = captions(groups[q])
    result = {}
    for d in (1,2):
        candidates = learn(groups[q],labels,lines,d)
        attempts = {}
        for name in ("principal","un_exemple"):
            chosen, ties = choose(candidates,name=="principal")
            if chosen:
                rule = tuple(chosen["regle"])
                positions = scan(reserve,lines,d,rule,masked=True)[rule]
            else:
                positions = []
            attempts[name] = dict(choix=chosen,ex_aequo=ties,positions=positions)
        result[d] = dict(modeles=candidates,depots=attempts)
    write(f"PREDICTIONS-{q}.json",dict(apprentissage=groups[q],reserve=reserve,distances=result))


def null_rule(rule, rows, pages, labels, old):
    summary = {}
    for only_new in (True,False):
        matrix = {p:{q:sum(bool(w != rule[0] and (not only_new or w not in old) and w in labels[q])
                            for row in rows if row["panneau"] == p for w in [row["cible"]])
                    for q in pages} for p in pages}
        hist = permutation_distribution(pages,matrix)
        real = sum(matrix[p][p] for p in pages)
        summary["nouveaux" if only_new else "tous"] = dict(observe=real,
            attendus=str(Fraction(sum(s*n for s,n in hist.items()),hist.total())),
            egal_ou_plus=sum(n for s,n in hist.items() if s>=real),total=hist.total(),
            histogramme=dict(sorted(hist.items())))
    return summary


def readout(q, groups, captions, lines):
    frozen = json.loads((HERE/f"PREDICTIONS-{q}.json").read_text())
    pages=frozen["reserve"]
    labels = captions(pages)
    result = {}
    for sd, item in frozen["distances"].items():
        d=int(sd)
        all_calls = scan(pages,lines,d)
        background = Counter()
        for rule, calls in all_calls.items():
            suffix = str(rule[1])
            stats=figures(annotate(rule,calls,labels))
            background["appels_"+suffix]+=stats["appels"]
            background["lisibles_"+suffix]+=stats["lisibles"]
            background["locaux_"+suffix]+=stats["justes"]
        trials={}
        for method, trial in item["depots"].items():
            if not trial["choix"]:
                trials[method]=dict(decision="abstention")
                continue
            chosen=trial["choix"]
            rule=tuple(chosen["regle"])
            old=chosen["apprentissage"]["graphies"]
            rows=annotate(rule,all_calls[rule],labels,old)
            assert [{k:r[k] for k in ("panneau","locus","rangs")} for r in rows] == trial["positions"]
            newrows=[r for r in rows if r["nouveau"]]
            perm=null_rule(rule,rows,pages,labels,old)
            newstats=figures(newrows)
            success=(min(len(newstats[n]) for n in ["feuillets","graphies"])>=2 and
                     20*perm["nouveaux"]["egal_ou_plus"]<=perm["nouveaux"]["total"])
            lexical=[(r["locus"],next(iter(labels[r["panneau"]])),r["cible"]) for r in rows
                     if len(labels[r["panneau"]])==1]
            trials[method]=dict(regle=rule,reserve=figures(rows),nouveaux=newstats,appels=rows,
                                predictions_nom_unique=lexical,permutations=perm,critere_rempli=success)
        diagnostics=[]
        pooled={p:{other:0 for other in pages} for p in pages}
        for model in item["modeles"]:
            rule=tuple(model["regle"])
            old=model["apprentissage"]["graphies"]
            rows=annotate(rule,all_calls[rule],labels,old)
            hits=[r for r in rows if r["nouveau"]]
            for row in rows:
                w=row["cible"]
                if w is None or w==rule[0] or w in old:
                    continue
                for other in pages:
                    pooled[row["panneau"]][other] += int(w in labels[other])
            diagnostics.append(dict(regle=rule,appels=len(rows),lisibles=sum(r["cible"] is not None for r in rows),tous=sum(bool(r["legendes"]) for r in rows),
                                    nouveaux=len(hits), details=[(r["locus"],r["cible"]) for r in hits]))
        maximum=max((r["nouveaux"] for r in diagnostics),default=0)
        pooled_hist=permutation_distribution(pages,pooled)
        control=dict(reprises_nouvelles_reelles=sum(pooled[p][p] for p in pages),
                     p_au_moins_une=str(Fraction(pooled_hist.total()-pooled_hist[0],pooled_hist.total())),
                     nombre_zero=pooled_hist[0],total=pooled_hist.total(),histogramme=dict(sorted(pooled_hist.items())))
        result[d]=dict(diagnostic_permutations_toutes_regles=control,fond=background,epreuves=trials,diagnostic_regles=diagnostics,
                       maximum_exploratoire=maximum)
    write(f"VERIFICATION-{q}.json",dict(apprentissage=q, tailles_legendes={p:len(v) for p,v in labels.items()}, distances=result))


if __name__=="__main__":
    assert sha256((HERE/"PROTOCOLE.md").read_bytes()).hexdigest()==PROTOCOL
    parser=ArgumentParser()
    parser.add_argument("operation",choices=["predire","verifier"])
    parser.add_argument("cahier",type=int,choices=[15,19])
    args=parser.parse_args()
    groups,captions,lines=load()
    if args.operation=="predire":
        prepare(args.cahier,groups,captions,lines)
    else:
        readout(args.cahier,groups,captions,lines)
