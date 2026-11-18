"""Replication: python3 compter.py [data_folder]. Standard library only."""
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parents[2] / "voynich_20261028/data"
PAGES = {"f71v": "Lz", "f72r1": "Lz", "f99r": "Lf", "f99v": "Lf"}
LOCUS = re.compile(r"^<(([^.]+)\.\d+),.([A-Za-z0-9]{2})(?:;[^>]*)?>\s+(.*)$")
DRAWING = re.compile(r"<[-~]>")
COMMENT = re.compile(r"<[^>]*>")
READING = re.compile(r"\[([^\]]+)\]")


def extract(path):
    rows = {page: {} for page in PAGES}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = LOCUS.match(line)
        if match:
            locus, page, kind, body = match.groups()
            if PAGES.get(page) == kind:
                assert locus not in rows[page] and "/" not in body
                rows[page][locus] = body
    assert [len(rows[p]) for p in PAGES] == [15, 15, 30, 21]
    return rows


def tokens(body, space, variant):
    clean = COMMENT.sub("", DRAWING.sub(".", body))
    clean = READING.sub(lambda m: m[1].split(":")[variant], clean)
    clean = clean.replace(",", space).replace("{", "").replace("}", "")
    return {word for word in clean.split(".") if word and "?" not in word}


def index(rows):
    lookup = defaultdict(list)
    for locus, words in rows.items():
        for word in sorted(words):
            lookup[word].append(locus)
    return dict(lookup)


def top(lookup):
    max_count = max(map(len, lookup.values()), default=0)
    return max_count, sorted(word for word, loci in lookup.items() if len(loci) == max_count)


def calibrate(a, b):
    rows = list(a.values()) + list(b.values())
    total = Counter(word for words in rows for word in words)
    count_a = Counter(word for words in a.values() for word in words)

    def score(count):
        peak = max(count.values(), default=0)
        return max((min(peak, total[word] - peak)
                    for word in count if count[word] == peak), default=0)

    observed = score(count_a)
    if max(total.values()) <= 1:
        return {"observed": observed, "p": 1, "method": "exact"}
    rng = random.Random(71172)
    null = Counter()
    for _ in range(20_000):
        draw = rng.sample(rows, len(a))
        counts = Counter(word for words in draw for word in words)
        null[score(counts)] += 1
    tail = sum(n for s, n in null.items() if s >= observed)
    return {"observed": observed, "null": dict(sorted(null.items())),
            "p": (tail + 1) / 20_001, "tail": tail, "n": 20_000, "seed": 71172}


def analyze(raw, space, variant):
    groups = {page: {l: tokens(b, space, variant) for l, b in rows.items()}
              for page, rows in raw.items()}
    a, b = groups["f71v"], groups["f72r1"]
    indices = {p: index(rows) for p, rows in groups.items()}
    peak, winners = top(indices["f71v"])
    max_b, winners_b = top(indices["f72r1"])
    shared = sorted(set(indices["f71v"]) & set(indices["f72r1"]))
    return {
        "n_loci": {p: len(rows) for p, rows in groups.items()},
        "n_types": {p: len(lookup) for p, lookup in indices.items()},
        "max_discovery": peak, "max_validation": max_b, "top_validation": winners_b,
        "top_discovery": {w: {p: indices[p].get(w, []) for p in PAGES} for w in winners},
        "shared_before_selection": {w: {p: indices[p].get(w, []) for p in PAGES} for w in shared},
        "null": calibrate(a, b),
        "groups": {p: {l: sorted(words) for l, words in rows.items()} for p, rows in groups.items()},
    }


def main():
    report = {}
    for edition in ["ZL3b-n", "IT2a-n"]:
        path = DATA / (edition + ".txt")
        raw = extract(path)
        report[edition] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "raw": raw,
            "runs": {f"{spacing}_{choice}": analyze(raw, space, variant)
                     for spacing, space in [("split", "."), ("join", "")]
                     for choice, variant in [("first", 0), ("last", -1)]},
        }
    (ROOT / "resultats.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for edition, data in report.items():
        for variant, result in data["runs"].items():
            print(edition, variant, result["top_discovery"], result["max_validation"],
                  result["null"], list(result["shared_before_selection"]))


if __name__ == "__main__":
    main()
