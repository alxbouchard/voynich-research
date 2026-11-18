"""Contrôle à clé cachée du moteur utilisé sur les deux triplets."""
from collections import Counter
from pathlib import Path
from random import Random
import gzip
import json

from lecture import code, extend, inverse

HERE = Path(__file__).resolve().parent
PLACES = ["5.26.p21.9", 2], ["6.7.p3.13", 3]


def challenge(row, seed):
    """La graine et la correspondance restent du côté du générateur."""
    words = row["triple"] + row["autour"]
    letters = sorted(set("".join(words)))
    alphabet = list("adfklmnoprstxy")
    Random(seed).shuffle(alphabet)
    key = dict(zip(letters, alphabet))
    assert len(key) == len(letters)
    encode = lambda word: "".join(key[ch] for ch in word)
    triples = tuple(encode(word) for word in row["triple"])
    hidden = tuple(encode(word) for word in row["autour"])
    return triples, hidden


def solve(chiffres, candidates):
    """Le chercheur reçoit uniquement les trois chiffres et le corpus de référence."""
    solutions = []
    for row in candidates:
        tables = [{}]
        for chiffre, word in zip(chiffres, row["triple"]):
            tables = [extra for table in tables for extra in extend(code(chiffre, "EVA"), word, 2, table)]
            if not tables:
                break
        for table in tables:
            solutions.append((row, [inverse(w, table) for w in row["autour"]]))
    return solutions


def run():
    data = json.loads(gzip.decompress((HERE / "INTERPRETATIONS.json.gz").read_bytes()))
    candidates = data["corpus"]["Celse"]
    truth, = [r for r in candidates if (r["source"], r["autre"]) == PLACES]
    attempts = []
    for seed in (72064, 73064, 74064):
        cipher, sealed = challenge(truth, seed)
        predictions = solve(cipher, candidates)
        scores = Counter(sum(g in words for g, words in zip(sealed, proposals))
                         for _, proposals in predictions)
        true_solutions = [
            {"annonce": guesses, "exacts": sum(g in ws for g, ws in zip(sealed, guesses))}
            for r, guesses in predictions if (r["source"], r["autre"]) == PLACES
        ]
        attempts.append(dict(graine_generateur=seed, trois_chiffres=cipher,
                             nombre_solutions=len(predictions), histogramme=dict(scores),
                             annonces_aux_bons_lieux=true_solutions, voisins_ouverts=sealed))
        assert sum(result["exacts"] == 4 for result in true_solutions) == 1
    return dict(candidats=len(candidates), lieux=PLACES, mots=truth["triple"], voisins=truth["autour"],
                essais=attempts)


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
