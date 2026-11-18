"""Projection depuis une seule flexion latine supposée, sans ajuster la ligne 32."""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import re
import sys

from lecture import ANCHOR, BEFORE, CONTROL, FORMS, RIGHT, SOURCES, load_all, save, tables


def evaluate(corpus, width):
    index = defaultdict(list)
    for locus, row in corpus.items():
        for pos, word in enumerate(row):
            index[word].append((locus, pos))
    words = set(index)

    @lru_cache(None)
    def predictions(ch, e, control):
        hole = ".{1,%d}" % width
        mid = e + hole + e + hole + e if control else e + e + hole + e + hole
        pattern = re.compile(ch + mid)
        return {w for w in words if pattern.fullmatch(w)}

    results = []
    for lemma, paradigm in FORMS.items():
        for form in paradigm.split():
            if form not in index:
                continue
            keys = list(tables(ANCHOR, form, width))
            record = dict(lemma=lemma, form=form, keys=len(keys), occurrences=len(index[form]),
                          with_right=sum(i+1 < len(corpus[s]) for s,i in index[form]))
            for label, shape in (("predicted", RIGHT), ("control", CONTROL)):
                options = set()
                pairs, triples = set(), set()
                for key in keys:
                    predicted = predictions(key["ch"], key["e"], label == "control")
                    options.update(predicted)
                    for locus, pos in index[form]:
                        row = corpus[locus]
                        if pos+1 >= len(row) or row[pos+1] not in predicted:
                            continue
                        pairs.add((locus, pos, row[pos+1]))
                        if pos == 0:
                            continue
                        for candidate in tables(shape, row[pos+1], width, key):
                            if next(tables(BEFORE, row[pos-1], width, candidate), None):
                                triples.add((locus, pos, *row[pos-1:pos+2]))
                record[label] = dict(dictionary=sorted(options), attested_right=sorted(pairs),
                                     attested_both=sorted(triples))
            results.append(record)
    return results


if __name__ == "__main__":
    corpora = load_all(Path(sys.argv[1]), SOURCES / "RIDGES.json")
    save("BOTANIQUE.json", {name: {str(w): evaluate(corpora[name], w) for w in (2, 3)}
                            for name in ("Macer", "Celse")})
