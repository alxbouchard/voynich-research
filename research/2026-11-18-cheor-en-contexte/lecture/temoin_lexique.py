"""Témoin exploratoire : deux mots latins successifs quelconques comme cheor cheekey."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import sys

from lecture import FORMS, SOURCES, load_all, save


@lru_cache(maxsize=150000)
def pair_possible(first, following, width):
    # Première forme ch,e,o,r. Deuxième forme ch,e,e,k,e,y.
    if not (4 <= len(first) <= 4 * width and 6 <= len(following) <= 6 * width):
        return False
    for chlen in range(1, width + 1):
        for elen in range(1, width + 1):
            if not 2 <= len(first) - chlen - elen <= 2 * width:
                continue
            ch = first[:chlen]
            e = first[chlen:chlen+elen]
            prefix = ch + e + e
            if not following.startswith(prefix):
                continue
            tail = following[len(prefix):]
            for klen in range(1, width + 1):
                if 1 <= len(tail)-klen-elen <= width and tail[klen:klen+elen] == e:
                    return True
    return False


def count(parts, width):
    eligible = Counter()
    fits = Counter()
    hits = []
    names = {w for paradigm in FORMS.values() for w in paradigm.split()}
    for section, row in parts.items():
        for pos, (a, b) in enumerate(zip(row, row[1:])):
            if not (4 <= len(a) <= 4 * width and 6 <= len(b) <= 6 * width):
                continue
            group = "botanique" if a in names else "autres"
            eligible[group] += 1
            if pair_possible(a, b, width):
                fits[group] += 1
                hits.append(dict(section=section, position=pos, words=[a, b], group=group))
    return dict(eligible=dict(eligible), hits=dict(fits), occurrences=hits)


if __name__ == "__main__":
    corpora = load_all(Path(sys.argv[1]), SOURCES / "RIDGES.json")
    save("TEMOIN-LEXIQUE.json", {n: {str(w): count(corpora[n], w) for w in (2, 3)}
                                 for n in ("Macer","Celse")})
