"""Mesurer séparément le doublet de f102r2 et les trois autres voisins."""
from collections import Counter
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
GLYPHS = ("qokol", "daiin", "oky")


def load(name):
    return json.loads(gzip.decompress((HERE / (name + ".json.gz")).read_bytes()))


def can_extend(triple, observed, neighbors):
    key = dict(zip(GLYPHS, triple))
    inverse = {value: symbol for symbol, value in key.items()}
    for symbol, word in zip(observed, neighbors):
        if key.get(symbol, word) != word or inverse.get(word, symbol) != symbol:
            return False
        key[symbol] = word
        inverse[word] = symbol
    return True


def counts():
    announced = load("INTERPRETATIONS")["corpus"]
    recorded = load("VOISINS")
    visible = recorded["voisins"]
    totals = Counter()
    for title, rows in announced.items():
        for row in rows:
            words = row["autour"]
            if words[3] is not None:
                totals["quatrieme_disponible"] += 1
                totals["quatrieme_double"] += words[3] == row["triple"][2]
            if all(words):
                totals["quatre_visibles"] += 1
                totals["compatibles_quatre"] += can_extend(row["triple"], visible, words)
            if all(words[:3]):
                totals["trois_visibles"] += 1
                totals["compatibles_trois"] += can_extend(row["triple"], visible[:3], words[:3])
            totals["annonces_mots_trois"] += sum(w is not None for w in row["lexique"][:3])
            totals["annonces_mots_quatrieme"] += row["lexique"][3] is not None
        for record in recorded["corpus"][title]["signes"]:
            for i, (answers, extension) in enumerate(zip(record["prevus"], record["individuellement"])):
                group = "quatrieme" if i == 3 else "trois"
                totals["annonces_signes_" + group] += bool(answers)
                totals["exactes_signes_" + group] += visible[i] in answers
                totals["extensions_signes_testables_" + group] += extension is not None
                totals["extensions_signes_justes_" + group] += extension is True
    return dict(sorted(totals.items()))


if __name__ == "__main__":
    print(json.dumps(counts(), indent=2))
