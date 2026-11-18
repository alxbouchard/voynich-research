"""Tester les graphies annoncées comme mots et comme parties des deux légendes."""
from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "phrase"))
from lecture import extend, read_books, segment

LANGS = {"Celse": 0, "Macer": 0, "Mayence1485": 3, "RIDGES": 3,
         "regime": 1, "viandier": 1, "martino": 2}
LABELS = ("koldarod", "odalydary")


def dictionary():
    lines = (HERE / "AVANT.md").read_text().splitlines()
    result = {}
    for line in lines:
        if not line.startswith("| ") or line.startswith("| Sens"):
            continue
        meaning, *terms = [s.strip() for s in line.strip("|").split("|")]
        result[meaning] = [t.split() for t in terms]
    return result


def index(body):
    positions = defaultdict(list)
    for passage, words in body.items():
        for i, w in enumerate(words):
            positions[w].append((passage, i + 1))
    return positions


def concordance(word, positions, body):
    examples = []
    for place, rank in positions[word][:3]:
        words = body[place]
        examples.append({"lieu": place, "rang": rank,
                         "texte": words[max(0, rank - 6):rank + 5]})
    return {"occurrences": len(positions[word]), "exemples": examples}


def compare(positions, word, body):
    carriers = {w: concordance(w, positions, body) for w in sorted(positions) if word in w[1:-1]}
    start = list(extend(segment("dar"), word, 2, {}))
    individual = {}
    for label in LABELS:
        options = [(carrier, table) for carrier in carriers for known in start
                   for table in extend(segment(label), carrier, 2, known)]
        individual[label] = options
    both = []
    for left, known in individual[LABELS[0]]:
        for right in carriers:
            if left != right:
                both.extend({"mots": [left, right], "table": table}
                            for table in extend(segment(LABELS[1]), right, 2, known))
    return {"emplois_autonomes": len(positions[word]), "porteurs": carriers, "tables_dar": len(start),
            "simples": individual, "communes": both}


def calibration(body, positions, word):
    if word not in positions:
        return None
    examples = []
    for w in sorted(positions):
        if word not in w[1:-1]:
            continue
        if word == "froid" and not w.startswith("refroid"):
            continue
        if word == "coctio" and not w.startswith("decoctio"):
            continue
        if word == "ponit" and not w.startswith(("imponit", "superponit", "componit", "apponit")):
            continue
        examples.append({"mot": w, **concordance(w, positions, body)})
    return {"mot":word, "autonome":concordance(word, positions, body), "derives":examples}


def evaluate(books):
    out = {}
    for name, body in books.items():
        positions = index(body)
        lang = LANGS[name]
        terms = {meaning: {w: compare(positions, w, body) for w in forms[lang] if w in positions}
                 for meaning, forms in dictionary().items()}
        controls = []
        for word in (("froid",) if lang == 1 else ("coctio", "ponit") if lang == 0 else ()):
            result = calibration(body, positions, word)
            if result:
                controls.append(result)
        out[name] = {"tokens":sum(map(len,body.values())), "vocabulaire":len(positions),
                     "concepts":terms, "controles":controls}
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("xml_celse", "html_viandier", "html_martino"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    paths = list(vars(args).values())
    result = {"annonce_sha256":hashlib.sha256((HERE / "AVANT.md").read_bytes()).hexdigest(),
              "sources":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "corpus":evaluate(read_books(*paths))}
    print(json.dumps(result, ensure_ascii=False, indent=1))
