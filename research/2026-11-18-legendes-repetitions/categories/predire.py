"""Rejouer le classement hors feuillet des légendes entières."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import re


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "2026-11-18-deux-legendes-botaniques/lecture/tucker/prefixe/resultats.json"
FIGURES = "Ln_un_locus_par_ligne_sans_reunir_les_paires_de_f75v"
POTS = "Lc_un_locus_par_ligne"
SEED = 68075


def inventory(data, group_figures=False, split_pots=False):
    tables = dict(data["par_code"])
    if not group_figures:
        tables["Ln"] = data[FIGURES]
    if split_pots:
        tables["Lc"] = data[POTS]
    rows = []
    for kind, table in sorted(tables.items()):
        for locus, word in sorted(table["mots_par_locus"].items()):
            leaves = {int(re.match(r"f(\d+)", part)[1]) for part in locus.split("+")}
            assert len(leaves) == 1
            rows.append((leaves.pop(), locus, word, kind))
    assert len({row[1] for row in rows}) == len(rows)
    return rows


def winner(scores):
    if not scores:
        return None
    best = max(scores.values())
    leaders = [kind for kind, n in scores.items() if n == best]
    return leaders[0] if len(leaders) == 1 else None


def predict(rows, with_details=False):
    votes = defaultdict(set)
    class_counts = Counter()
    local_counts = defaultdict(Counter)
    for leaf, locus, word, kind in rows:
        votes[word].add((leaf, kind))
        class_counts[kind] += 1
        local_counts[leaf][kind] += 1
    total = Counter()
    by_kind = defaultdict(Counter)
    details = []
    modes = {leaf: winner(class_counts - counts) for leaf, counts in local_counts.items()}
    for leaf, locus, word, kind in rows:
        others = sorted((other, cat) for other, cat in votes[word] if other != leaf)
        scores = Counter(cat for _, cat in others)
        prediction = winner(scores)
        outcome = "absent" if not others else "egalite"
        if prediction:
            outcome = "juste" if prediction == kind else "faux"
            if modes[leaf] == kind:
                total["temoin_juste"] += 1
                by_kind[kind]["temoin_juste"] += 1
        total[outcome] += 1
        by_kind[kind][outcome] += 1
        if with_details:
            details.append(dict(feuillet=leaf, lieu=locus, mot=word, attendu=kind, prediction=prediction,
                                voix=others, issue=outcome, majorite_sans_mot=modes[leaf]))
    return dict(total=total, par_categorie=by_kind, lieux=details)


def generic_names(rows):
    by_kind = defaultdict(Counter)
    for leaf, locus, word, kind in rows:
        by_kind[kind][word] += 1
    result = {}
    for kind, words in by_kind.items():
        best = max(words.values())
        leaders = sorted(w for w, n in words.items() if n == best)
        result[kind] = dict(total=words.total(), graphies=len(words), maximum=best, candidats={
            w: {cat: counts[w] for cat, counts in by_kind.items() if counts[w]} for w in leaders})
    return result


def randomize(rows):
    strata = defaultdict(list)
    for i, row in enumerate(rows):
        strata[row[0]].append(i)
    rng = random.Random(SEED)
    null = Counter()
    for _ in range(999):
        shuffled = list(rows)
        for indices in strata.values():
            kinds = [rows[i][3] for i in indices]
            if len(set(kinds)) < 2:
                continue
            rng.shuffle(kinds)
            for i, kind in zip(indices, kinds):
                shuffled[i] = (*rows[i][:3], kind)
        null[predict(shuffled)["total"]["juste"]] += 1
    mixed = {k: len(ii) for k, ii in strata.items() if len({rows[i][3] for i in ii}) > 1}
    return dict(graine=SEED, permutations=sum(null.values()), histogramme_justes=dict(sorted(null.items())),
                feuillets_mixtes=mixed, nombre_de_feuillets=len(strata))


def main():
    data = json.loads(SOURCE.read_bytes())
    rows = inventory(data)
    results = predict(rows, with_details=True)
    simulations = randomize(rows)
    correct = results["total"]["juste"]
    above = sum(n for s, n in simulations["histogramme_justes"].items() if s >= correct)
    simulations["au_moins_observe"] = above
    out = dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(), principal=results,
               generiques=generic_names(rows), controle=simulations, sensibilite={})
    # Un témoin emploie un nom constant par catégorie, l'autre par feuillet.
    same_kind = [(leaf, locus, kind, kind) for leaf, locus, word, kind in rows]
    same_leaf = [(leaf, locus, str(leaf), kind) for leaf, locus, word, kind in rows]
    controls = {"mot_par_categorie": predict(same_kind)["total"],
                "mot_par_feuillet": predict(same_leaf)["total"]}
    assert controls["mot_par_categorie"]["juste"] == len(rows)
    assert controls["mot_par_feuillet"]["absent"] == len(rows)
    out["verifications_artificielles"] = controls
    for c, alt in [("figures_groupees", inventory(data, group_figures=True)),
                   ("recipients_par_ligne", inventory(data, split_pots=True))]:
        tmp = predict(alt)
        del tmp["lieux"]
        out["sensibilite"][c] = tmp
    (HERE / "resultats.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(len(rows), results["total"], simulations)


if __name__ == "__main__":
    main()
