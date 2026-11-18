"""Contrôle indépendant. Lancer avec Python 3.10+ depuis tout répertoire."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from math import factorial, prod
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
WITNESSES = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}


def read(path):
    return json.loads(path.read_text())


def witnesses():
    rows = {}
    meta = {}
    hashes = {}
    for ed, filename in WITNESSES.items():
        content = (ROOT / "voynich_20261028/data" / filename).read_bytes()
        hashes[ed] = sha256(content).hexdigest()
        data = defaultdict(list)
        for line in content.decode().splitlines():
            if not line.startswith("<"):
                continue
            address, _, value = line[1:].partition(">")
            if "." not in address:
                if ed == "ZL":
                    meta[address] = dict(re.findall(r"\$(\w)=(\w+)", value))
                continue
            locus, _, kind = address.partition(",")
            if kind not in {"+P0", "@P0", "=P0", "*P0"}:
                continue
            face = locus.partition(".")[0]
            data[face].append((locus, value.strip()))
        rows[ed] = data
    eligible = {f: v["Q"] for f, v in meta.items()
                if v.get("I") == "H" and v.get("L") == "A" and v.get("H") == "1"
                and v.get("Q") in set("ABCDEFG") and all(f in x for x in rows.values())}
    return rows, eligible, hashes


def readers(lot):
    key = read(STUDY / f"cle-{lot}.json")
    panel = [read(STUDY / f"lecteur-{r}-{lot}.json") for r in ("I", "II")]
    assert all(set(r) == set(key) for r in panel)
    return {meta["face"]: tuple(r[card]["vote"] for r in panel) for card, meta in key.items()}


def concordance(pair):
    return pair[0] if pair[0] == pair[1] else "?"


def vote_summary(pairs):
    return {"consensus": dict(Counter(concordance(pair) for pair in pairs.values())),
            "paires": dict(Counter("/".join(pair) for pair in pairs.values()))}


def parse(rows, split):
    tokens = []
    for locus, line in rows:
        def markup(match):
            tag = match[0]
            if tag in {"<->", "<~>"}:
                return "."
            if tag in {"<%>", "<$>"} or tag.startswith("<!"):
                return ""
            raise ValueError((locus, tag))
        line = re.sub(r"<[^>]*>", markup, line)
        line = line.translate(str.maketrans("", "", "!{}")).replace(",", "." if split else "")
        words = re.findall(r"[^.]+", line)
        for slot, value in enumerate(words, start=1):
            tokens.append((f"{locus}/{slot}", value if re.fullmatch("[a-z]+", value) else None))
    return tokens


def index(tokens, rule):
    forms = defaultdict(list)
    for address, word in (tokens if rule == "otoldy" else tokens[:60]):
        if word is None:
            continue
        if rule == "finale":
            units = re.findall(r"ckh|cph|cfh|cth|sh|ch|.", word)
            parts = [" ".join(units[-n:]) for n in (2, 3) if n < len(units)]
        else:
            parts = [word]
        for form in parts:
            forms[form].append([address, word])
    return forms


def both(faces, tokens, rule):
    index_by_form = defaultdict(dict)
    for face in faces:
        tables = {ed: index(data[face], rule) for ed, data in tokens.items()}
        for form in tables["H"].keys() & tables["ZL"].keys():
            index_by_form[form][face] = {ed: t[form] for ed, t in tables.items()}
    return index_by_form


def learn(forms, labels, quires):
    pos = {f for f, v in labels.items() if v == "O"}
    neg = {f for f, v in labels.items() if v == "N"}
    ranks = []
    for form, hits in forms.items():
        tp = pos.intersection(hits)
        fp = neg.intersection(hits)
        if len(tp) >= 3 and len({quires[f] for f in tp}) >= 2:
            j = Fraction(len(tp), len(pos)) - Fraction(len(fp), len(neg))
            ranks.append((-j, -len(tp), form, sorted(tp), sorted(fp)))
    ranks.sort()
    best = ranks[0]
    assert best[0] < 0
    return {"forme": best[2], "score": str(-best[0]), "positifs": best[3],
            "negatifs": best[4], "candidats_admissibles": len(ranks),
            "ex_aequo_avant_ordre_alphabetique": [r[2] for r in ranks if r[:2] == best[:2]]}


def confusion(labels, hit):
    buckets = {k: [] for k in ("VP", "FP", "FN", "VN", "annonces_indecises", "silences_indecis")}
    for face, vote in sorted(labels.items()):
        if vote == "?":
            bucket = "annonces_indecises" if face in hit else "silences_indecis"
        elif vote == "O":
            bucket = "VP" if face in hit else "FN"
        else:
            bucket = "FP" if face in hit else "VN"
        buckets[bucket].append(face)
    return buckets


def compare_counts(buckets, published):
    tp, fp, fn, tn = (len(buckets[k]) for k in ("VP", "FP", "FN", "VN"))
    assert all(len(buckets[k]) == published[k] for k in ("VP", "FP", "FN", "VN"))
    j = str(Fraction(tp, tp + fn) - Fraction(fp, tn + fp)) if (tp + fn) and (tn + fp) else None
    assert j == published["score"]


def permute_exact(labels, hit, reserve):
    """Deux faces orientées par feuillet. Les cotes exclues ont un poids nul."""
    n_yes = sum(t == "O" for t in labels.values())
    n_no = sum(t == "N" for t in labels.values())
    if not (n_yes and n_no):
        return None
    weights = {"O": n_no, "N": -n_yes, "?": 0}
    cutoff = sum(weights[v] for f, v in labels.items() if f in hit)
    distribution = Counter({0: 1})
    strata = {}
    for quire in "DEFG":
        pages = sorted(f for f, q in reserve.items() if q == quire)
        assert len(pages) % 2 == 0
        leaves = list(zip(pages[::2], pages[1::2]))
        assert all(a[:-1] == b[:-1] and a.endswith("r") and b.endswith("v") for a, b in leaves)
        costs = []
        for a, b in leaves:
            costs.append([weights[labels.get(a, "?")] * (r in hit)
                          + weights[labels.get(b, "?")] * (v in hit) for r, v in leaves])
        m = len(leaves)
        dp = {0: Counter({0: 1})}
        for row in costs:
            new = defaultdict(Counter)
            for used, counts in dp.items():
                for i, value in enumerate(row):
                    bit = 1 << i
                    if used & bit:
                        continue
                    dest = new[used | bit]
                    for score, count in counts.items():
                        dest[score + value] += count
            dp = new
        qdist = dp[(1 << m) - 1]
        assert sum(qdist.values()) == factorial(m)
        # Second calcul par énumération directe, praticable pour ces petites strates.
        direct = Counter(sum(costs[i][j] for i, j in enumerate(p))
                         for p in permutations(range(m)))
        assert qdist == direct
        joint = Counter()
        for a, na in distribution.items():
            for b, nb in qdist.items():
                joint[a + b] += na * nb
        distribution = joint
        strata[quire] = {"feuillets": m, "permutations": factorial(m)}
    exceed = sum(v for k, v in distribution.items() if k >= cutoff)
    total = sum(distribution.values())
    assert total == prod(s["permutations"] for s in strata.values())
    return {"seuil": cutoff, "au_moins_observe": exceed, "permutations": total,
            "p": str(Fraction(exceed, total)), "p_decimal": exceed / total, "strates": strata}


def main():
    raw, qs, hashes = witnesses()
    freeze = read(STUDY / "PREDICTIONS.json")
    assert hashes == freeze["entrees_sha256"]
    train, test = readers("apprentissage"), readers("reserve")
    assert set(train) == {f for f, q in qs.items() if q in "ABC"}
    reserve = {f: q for f, q in qs.items() if q in "DEFG"}
    assert set(test) == set(reserve)
    index_yale = {"f" + row["label"]: row for row in read(ROOT / "voynich_resources/yale/image_index.json")}
    for lot in ("apprentissage", "reserve"):
        for rec in read(STUDY / f"cle-{lot}.json").values():
            f = rec["face"]
            assert rec["cahier"] == qs[f]
            assert rec["url"] == index_yale[f]["url"] and rec["sha256_original"] == index_yale[f]["sha256"]
    train_labels = {f: concordance(p) for f, p in train.items()}
    assert {f: t for f, t in train_labels.items() if t != "?"} == freeze["cotation_apprentissage"]
    labels = {f: concordance(p) for f, p in test.items()}
    old = {x["face"] for x in read(STUDY.parent / "2026-11-18-otoldy-dessin/photos/CLE-CARTES.json").values()}
    without_old = {f: t for f, t in labels.items() if f not in old}
    seen_leaves = {f[:-1] for f in set(reserve).intersection(old)}
    virgin = {f: q for f, q in reserve.items() if f[:-1] not in seen_leaves}
    virgin_labels = {f: labels[f] for f in virgin}
    out = {"votes_apprentissage": vote_summary(train), "votes_reserve": vote_summary(test),
           "anciennes_parmi_85": sorted(old.intersection(qs)), "anciennes_parmi_40": sorted(old.intersection(test)),
           "par_cahier": {q: vote_summary({f: test[f] for f in reserve if reserve[f] == q}) for q in "DEFG"},
           "evaluations": {}}
    for convention in ("joints", "separes"):
        protocol = freeze["conventions"][convention]
        tokens = {ed: {f: parse(raw[ed][f], convention == "separes") for f in qs} for ed in raw}
        assert {ed: {f: len(words) for f, words in data.items()} for ed, data in tokens.items()} == protocol["positions"]
        for rule in ("mot", "finale", "otoldy"):
            forms = both(qs, tokens, rule)
            model = learn(forms, train_labels, qs) if rule != "otoldy" else {"forme": "otoldy"}
            hit = forms[model["forme"]]
            frozen_model = protocol["regles"][rule]
            assert all(frozen_model[k] == v for k, v in model.items())
            assert frozen_model["lieux"] == hit
            assert frozen_model["presence"] == {f: f in hit for f in qs}
            tests = {"reserve": labels, "hors_anciennes": without_old,
                     "lecteur_I": {f: p[0] for f, p in test.items()},
                     "lecteur_II": {f: p[1] for f, p in test.items()}}
            result = {"modele": model, "apprentissage": confusion(train_labels, hit), "tests": {},
                      "cahiers": {q: confusion({f: t for f, t in labels.items() if qs[f] == q}, hit) for q in "DEFG"}}
            for name, subset in tests.items():
                result["tests"][name] = {"faces": confusion(subset, hit),
                                         "permutation_exacte": permute_exact(subset, hit, reserve)}
            result["tests"]["hors_feuillets_anciens"] = {
                "faces": confusion(virgin_labels, hit),
                "permutation_exacte": permute_exact(virgin_labels, hit, virgin)}
            out["evaluations"][convention + "_" + rule] = result
            if convention == "separes" and rule == "finale":
                fixed = freeze["conventions"]["joints"]["regles"]["finale"]["forme"]
                out["finale_primaire_fixee_espaces_separes"] = {
                    "forme": fixed, "reserve": confusion(labels, forms[fixed]),
                    "permutation_exacte": permute_exact(labels, forms[fixed], reserve)}
    published = read(STUDY / "RESULTATS.json")
    assert published["votes"] == {f: list(p) for f, p in (train | test).items()}
    assert published["reserve_primaire"] == {f: t for f, t in labels.items() if t != "?"}
    assert published["anciens_dessins"] == out["anciennes_parmi_85"]
    for name, exp in out["evaluations"].items():
        other = published["formes"][name]
        assert other["forme"] == exp["modele"]["forme"]
        compare_counts(exp["apprentissage"], other["apprentissage"])
        for q, rows in exp["cahiers"].items():
            compare_counts(rows, other["reserves"][q])
        for ours, theirs in (("reserve", "ensemble"), ("hors_anciennes", "hors_anciennes")):
            rounded = other["reserves"][theirs]
            check = exp["tests"][ours]
            compare_counts(check["faces"], rounded)
            check["p_monte_carlo_publiee"] = rounded["permutations"]["p_plus_un"]
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
