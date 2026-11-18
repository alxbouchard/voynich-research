"""Ouvrir le groupe masqué et comparer les listes de dessins sur la même prose."""
from collections import Counter
from fractions import Fraction
from functools import cache
import math
from contexte import RULES, folio, herbal, load, manuscript, save


def center_words(records):
    lookup = {}
    for _, loc, spans in records:
        for rank, word in enumerate((w for ws in spans for w in ws), 1):
            lookup[loc, rank] = word
    return lookup


def count(data, gallery, records):
    answers = center_words(records)
    scores, hits = {}, []
    for p, page in data.items():
        alternatives = page["listes"]
        matrices = {q: {rule: Counter() for rule in RULES} for q in alternatives}
        for loc, rank, left, right, guesses in page["cases"]:
            actual = answers[loc, rank]
            for q, call in zip(alternatives, guesses, strict=True):
                for rule, w in zip(RULES, call, strict=True):
                    totals = matrices[q][rule]
                    totals["cases"] += 1
                    if not actual:
                        totals["illisibles"] += 1
                        totals["annonces_illisibles"] += int(w is not None)
                        continue
                    totals["verifiables"] += 1
                    totals["noms_effectifs"] += int(actual in gallery[q])
                    if w is None:
                        continue
                    totals["annonces"] += 1
                    totals["justes"] += int(w == actual)
                    if w == actual and p == q:
                        hits.append(dict(page=p, lieu=loc, rang=rank, gauche=left, mot=w, droite=right, regle=rule))
        scores[p] = matrices
    return scores, hits


def distribution(block, weights):
    @cache
    def permutations(mask):
        i = mask.bit_count()
        if i == len(block):
            return Counter({0: 1})
        hist = Counter()
        for j, candidate in enumerate(block):
            if not mask & (1 << j):
                extra = weights.get((block[i], candidate), 0)
                for score, n in permutations(mask | (1 << j)).items():
                    hist[score + extra] += n
        return hist
    result = permutations(0)
    assert sum(result.values()) == math.factorial(len(block))
    return result


def metrics(scores, eligible, groups):
    output = {}
    for rule in RULES:
        real, other = Counter(), Counter()
        macro = Counter()
        for p in eligible:
            original = scores[p][p][rule]
            real.update(original)
            competitors = [scores[p][q][rule] for q in scores[p] if p != q]
            for c in competitors:
                other.update(c)
            if not competitors or not original["verifiables"]:
                continue
            macro["n"] += 1
            macro["vrais"] += Fraction(original["justes"], original["verifiables"])
            macro["faux"] += sum(Fraction(c["justes"], c["verifiables"]) for c in competitors) / len(competitors)
        weights = {(p, q): c[rule]["justes"] for p in eligible for q, c in scores[p].items()}
        hist = Counter({0: 1})
        for g in sorted(set(groups.values())):
            block = [p for p in sorted(groups) if groups[p] == g]
            local = distribution(block, weights)
            merged = Counter()
            for a, n in hist.items():
                for b, m in local.items():
                    merged[a+b] += n*m
            hist = merged
        tail = sum(n for a, n in hist.items() if a >= real["justes"])
        k = macro["n"]
        output[rule] = dict(vraies=dict(real), decalees_cumulees=dict(other),
            moyenne_par_panneau={"n": k, "vraies": float(macro["vrais"]/k) if k else None,
                                 "decalees": float(macro["faux"]/k) if k else None},
            permutations={"aussi_bonnes": tail, "total":sum(hist.values()),"p": float(Fraction(tail,sum(hist.values())))})
    return output


def report(data, gallery, groups, records, latin):
    scores, hits = count(data, gallery, records)
    lots = {"tous": sorted(scores)}
    if not latin:
        lots.update(principal=sorted(p for p in scores if folio(p) not in {"f89", "f100"}),
                    deja_etudies=sorted(p for p in scores if folio(p) in {"f89", "f100"}))
    return dict(resume={name:metrics(scores, pages, groups) for name,pages in lots.items()},
                lots=lots, reussites=hits, par_panneau=scores, legendes={p:sorted(v) for p,v in gallery.items()})


if __name__ == "__main__":
    guesses = load("PREDICTIONS.json.gz")
    g, h, r = manuscript()
    vg = report(guesses["voynich"], g, h, r, False)
    g, h, r, _ = herbal()
    mg = report(guesses["macer"], g, h, r, True)
    save("RESULTATS.json.gz", {"voynich":vg, "macer":mg})
    for name, obj, label in [("Voynich", vg, "principal"), ("Macer", mg, "tous")]:
        print(name, {k: (v["vraies"], v["permutations"]["p"]) for k,v in obj["resume"][label].items()})
