"""Prévoir le milieu d'une phrase en utilisant les inscriptions d'un panneau."""
from collections import Counter, defaultdict
from functools import cache
import gzip
import json
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-opcheor-paralleles/variantes"))
from compter import GAP, corpus, langage, segment, tokens

MODES = ("joints", "separes")
RULES = ("deux_voisins", "un_voisin", "variante_finale", "frequence")
LATIN = RESEARCH / "2026-11-18-noms-dans-les-notices/historique/corpus.jsonl"


def save(name, data):
    out = (json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode()
    (HERE / name).write_bytes(gzip.compress(out, mtime=0) if name.endswith(".gz") else out)


def load(name):
    raw = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith(".gz") else raw)


@cache
def units(word, latin):
    return tuple(word) if latin else tuple(segment(word))


def variants(a, b, latin):
    ua, ub = units(a, latin), units(b, latin)
    return len(ua) >= 5 and len(ua) == len(ub) and ua[:-1] == ub[:-1] and ua[-1] != ub[-1]


def folio(page):
    match = re.match(r"f[0-9]+", page)
    return match[0] if match else page


def sequence(raw, cut):
    words = []
    for index, part in enumerate(GAP.split(raw)):
        safe = re.sub(r"\{[^}]*\}", "?", part)
        words.extend((index, w) for w in tokens(safe, cut))
    return words


def sections(views):
    """An uncertain word can be masked. A marked physical interruption splits the span."""
    lines = []
    for index in range(min(map(len, views))):
        if index == 0 or any(view[index - 1][0] != view[index][0] for view in views):
            lines.append([])
        choices = {view[index][1] for view in views}
        word = next(iter(choices)) if len(choices) == 1 else None
        lines[-1].append(word if word and re.fullmatch("[a-z]+", word) else None)
    return lines


def manuscript():
    editions, topics = corpus()
    pages = {p for p, topic in topics.items() if topic == "P"}
    gallery = defaultdict(set)
    records = []
    for loc in sorted(set.intersection(*(set(rows) for rows in editions.values()))):
        entries = [rows[loc] for rows in editions.values()]
        page, kind = entries[0][:2]
        if any(row[:2] != (page, kind) for row in entries):
            continue
        views = [sequence(row[3], cut) for row in entries for cut in MODES]
        if kind == "Lf" and page in pages:
            shared = set.intersection(*({w for _, w in view} for view in views))
            gallery[page].update(w for w in shared if re.fullmatch("[a-z]+", w) and len(units(w, False)) >= 3)
        elif kind == "P0":
            records.append((page, loc, sections(views)))
    # Some page labels may all be uncertain, so keep those panels as well.
    metadata = (langage.DATA / "ZL3b-n.txt").read_text()
    quires = dict(re.findall(r"^<(f\w+)>\s+<![^>]*\$Q=(\w)", metadata, re.M))
    return dict(gallery), {p: quires[p] for p in gallery}, records


def herbal(encrypted=False):
    rows = [json.loads(line) for line in LATIN.read_text().splitlines()]
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    random.Random(7832).shuffle(alphabet)
    table = str.maketrans("abcdefghijklmnopqrstuvwxyz", "".join(alphabet))
    def code(w):
        return w.translate(table) if encrypted else w
    records, gallery = [], defaultdict(set)
    for i, row in enumerate(rows):
        page = "lot" + str(i // 5 + 1)
        gallery[page].add(code(row["label"]))
        records.append((page, row["id"], [[code(w) for w in row["tokens"]]]))
    return dict(gallery), {p: "Macer" for p in gallery}, records, table


class Model:
    def __init__(self, records, held):
        self.freq = Counter()
        self.pairs = Counter()
        self.triples = Counter()
        for page, _, spans in records:
            if folio(page) == held:
                continue
            for ws in spans:
                self.freq.update(w for w in ws if w)
                self.pairs.update((a, b) for a, b in zip(ws, ws[1:]) if a and b)
                self.triples.update((a, b, c) for a, b, c in zip(ws, ws[1:], ws[2:]) if a and b and c)

    def propose(self, captions, left, right, latin):
        highs = [0] * len(RULES)
        winners = [None] * len(RULES)
        for w in captions:
            scores = (self.triples[left, w, right], self.pairs[left, w] + self.pairs[w, right],
                      int(variants(left, w, latin) or variants(right, w, latin)), self.freq[w])
            for j, count in enumerate(scores):
                if count > highs[j]:
                    highs[j], winners[j] = count, w
                elif count == highs[j]:
                    winners[j] = None
        return winners


def spots(records, selected):
    for page, loc, spans in records:
        if page != selected:
            continue
        offset = 0
        for ws in spans:
            for i in range(1, len(ws) - 1):
                if ws[i - 1] and ws[i + 1]:
                    yield loc, offset + i + 1, ws[i - 1], ws[i + 1]
            offset += len(ws)


def predictions(gallery, groups, records, latin=False):
    data = {}
    for held in sorted({folio(p) for p in gallery}):
        model = Model(records, held)
        for page in sorted(p for p in gallery if folio(p) == held):
            alternatives = sorted(p for p in gallery if groups[p] == groups[page])
            guesses = []
            for loc, rank, left, right in spots(records, page):
                calls = [model.propose(gallery[alt], left, right, latin) for alt in alternatives]
                guesses.append([loc, rank, left, right, calls])
            data[page] = {"listes": alternatives, "cases": guesses}
    return data


def calibration():
    data, groups, records, table = herbal()
    encoded, eg, er, _ = herbal(True)
    original = predictions(data, groups, records, True)
    cipher = predictions(encoded, eg, er, True)
    for p, value in original.items():
        for a, b in zip(value["cases"], cipher[p]["cases"], strict=True):
            assert a[:2] == b[:2] and [w.translate(table) for w in a[2:4]] == b[2:4]
            assert [[w.translate(table) if w else None for w in c] for c in a[4]] == b[4]
    return original


def checks():
    rows = [("f1r", "", [["la", "ortie", "seche"], ["la", "ortie", "ici"]]),
            ("f2v1", "", [["la", "sauge", "seche"]])]
    trained = Model(rows, "f2")
    assert trained.propose(["ortie", "sauge"], "la", "seche", True) == ["ortie", "ortie", None, "ortie"]
    assert trained.propose(["ortie", "sauge"], "ortia", "xx", True)[2] == "ortie"
    assert trained.propose(["ortie", "sauge"], "ortie", "xx", True)[2] is None
    assert trained.propose(["ortie", "sauge"], "ortia", "sauga", True)[2] is None
    assert sections([[(0, "a"), (0, "b"), (1, "c")], [(0, "a"), (0, "d"), (0, "c")]]) == [["a", None], ["c"]]
    assert variants("opcheor", "opcheol", False)
    assert not variants("cheor", "cheol", False)  # ch is one unit, with only three retained.


if __name__ == "__main__":
    checks()
    g, h, r = manuscript()
    assert len(g) == 15
    save("PREDICTIONS.json.gz", dict(voynich=predictions(g,h,r), macer=calibration()))
