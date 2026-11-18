"""Concordances historiques et prédictions des voisins des trois cheor."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
SOURCES = RESEARCH / "2026-11-18-phrase-et-doublets/lecture"
sys.path.insert(0, str(SOURCES))
sys.path.insert(0, str(RESEARCH / "2026-11-18-carte-sept-etoiles/lecture"))
from corpus_sources import load_all
from essai import tables

LEFT = tuple("dar")
ANCHOR = ("ch", "e", "o", "r")
ENDING = {"H": ("sh", "e", "o", "r"), "ZL": ("sh", "o", "a", "r")}
RIGHT = ("ch", "e", "e", "k", "e", "y")
CONTROL = ("ch", "e", "k", "e", "y", "e")
BEFORE = tuple("yotaiin")
MIDDLE = {"H": [("os", "al")], "ZL": [("osal",), ("o", "s", "al"), ("o", "sal"), ("os", "al")]}
FORMS = {
    "radix": "radix radicis radici radicem radice radices radicum radicibus",
    "herba": "herba herbae herbam herbarum herbis herbas",
    "folium": "folium folii foli folio folia foliorum foliis",
    "flos": "flos floris flori florem flore flores florum floribus",
}


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=1) + "\n")


def compatible_pair(a, b, width):
    return any(a.endswith(b[-k:]) and 2 <= len(a) - k <= 2 * width
               and 3 <= len(b) - k <= 3 * width for k in range(1, width + 1))


def fit(triple, edition, width):
    a, b, c = triple
    if b[-1] != c[-1] or not 4 <= len(c) <= 4 * width:
        return
    if edition == "H" and b[-3:] != c[-3:]:
        return
    for anchor_key in tables(ANCHOR, b, width):
        for two_key in tables(LEFT, a, width, anchor_key):
            yield from tables(ENDING[edition], c, width, two_key)


def potential(corpus):
    vocabulary = sorted({w for row in corpus.values() for w in row})

    @lru_cache(None)
    def projected(ch, e, width, control):
        # k and y occur once each. The other letters are fixed by the seed.
        hole = ".{1," + str(width) + "}"
        e = re.escape(e)
        prefix = re.escape(ch)
        body = e + hole + e + hole + e if control else e + e + hole + e + hole
        pattern = re.compile(prefix + body)
        return [w for w in vocabulary if pattern.fullmatch(w)]
    counts = Counter(w for row in corpus.values() for w in row)
    output = []
    for width in (2, 3):
        for edition in ENDING:
            windows = pair = 0
            records = []
            for locus, row in corpus.items():
                for i in range(1, len(row)-1):
                    triple = row[i-1:i+2]
                    windows += 1
                    if not compatible_pair(*triple[:2], width):
                        continue
                    pair += 1
                    for key in fit(triple, edition, width):
                        records.append(dict(section=locus, center=i, words=triple, key=key,
                            predicted=projected(key["ch"], key["e"], width, False),
                            control=projected(key["ch"], key["e"], width, True)))
            botanical = {}
            for lemma, forms in FORMS.items():
                attested = {w: counts[w] for w in forms.split() if counts[w]}
                hits = sorted({r["words"][1] for r in records if r["words"][1] in attested})
                botanical[lemma] = dict(attested=attested, fits=hits)
            output.append(dict(width=width, edition=edition, windows=windows, pair=pair,
                               botanical=botanical, records=records))
    return output


def match_sequence(pattern, words, width, key):
    if len(pattern) != len(words):
        return
    yield from tables(tuple(" ".join(pattern)), " ".join(words), width, key)


def heldout(corpus, group):
    index = defaultdict(list)
    for locus, row in corpus.items():
        for i, w in enumerate(row):
            if 0 < i < len(row)-1:
                index[w].append((locus, i))
    result = Counter()
    details = []
    for record in group["records"]:
        key, center = record["key"], record["words"][1]
        for locus, i in index[center]:
            if (record["section"], record["center"]) == (locus, i):
                continue
            row = corpus[locus]
            forward = locus == record["section"] and 0 < i - record["center"] <= 120
            for label, shape in (("predicted", RIGHT), ("control", CONTROL)):
                if row[i+1] not in record[label]:
                    continue
                result[label + "_anywhere_right"] += 1
                if forward:
                    result[label + "_forward_right"] += 1
                for right_key in tables(shape, row[i+1], group["width"], key):
                    for two_key in tables(BEFORE, row[i-1], group["width"], right_key):
                        result[label + "_anywhere_two_sides_keys"] += 1
                        if not forward:
                            continue
                        result[label + "_forward_two_sides_keys"] += 1
                        for j in range(record["center"]+1, i):
                            if row[j] != center:
                                continue
                            for spelling in MIDDLE[group["edition"]]:
                                words = row[j+1:j+1+len(spelling)]
                                for full_key in match_sequence(spelling, words, group["width"], two_key):
                                    details.append(dict(seed=record["words"], section=locus,
                                        centers=[record["center"], j, i], neighbors=row[i-1:i+2],
                                        middle=words, spelling=spelling, key=full_key, test=label))
    return dict(width=group["width"], edition=group["edition"], counts=dict(result),
                local_three_occurrences=details)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["predire", "verifier"])
    parser.add_argument("celsus", type=Path)
    args = parser.parse_args()
    corpora = load_all(args.celsus, SOURCES / "RIDGES.json")
    if args.mode == "predire":
        save("PREDICTIONS.json", {name: potential(corpus) for name, corpus in corpora.items()})
    else:
        predictions = json.loads((HERE / "PREDICTIONS.json").read_text())
        save("VERIFICATION.json", {name: [heldout(corpora[name], g) for g in groups]
                                   for name, groups in predictions.items()})


if __name__ == "__main__":
    main()
