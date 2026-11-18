"""Contrôle exhaustif des six appariements de noms et des deux mots de prose."""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def norms(value, dissolve):
    text = value.lower().replace('ſ', 's')
    return text.replace('ß','sz') if dissolve else text


def test_names(rows, guesses, dissolve):
    predicted = [norms(row["allemand_predit"], dissolve) for row in guesses]
    seen = [norms(row["rubrique_allemande"], dissolve) for row in rows]
    hits = sum(a == b for a, b in zip(predicted,seen))
    histogram = Counter(sum(a == b for a, b in zip(arrangement,seen))
                        for arrangement in itertools.permutations(predicted))
    occurrences = []
    for guess, row in zip(predicted, rows):
        words = norms(row["debut"],dissolve).split()
        assert len(words) == 24
        occurrences.append([i for i, word in enumerate(words,1) if word == guess])
    return dict(matches=hits, total=len(rows), permutations=dict(sorted(histogram.items())),
                au_moins_autant=sum(count for n, count in histogram.items() if n >= hits),
                occurrences_prose=occurrences)


def main():
    predicted = read('PREDICTIONS.json')
    seen = read('observations.json')
    assert [r["numero"] for r in predicted] == [r["chapitre"] for r in seen] == list(range(13,19))
    result = {
        "rubrique_allemande_grande_typographie": test_names(seen, predicted, False),
        "rubrique_allemande_apres_developpement_de_eszett": test_names(seen, predicted, True),
        "juxtaposition_correcte": sum(r["formule_dans_rubrique"] == p["verbe_predit"]
                                      for r, p in zip(seen,predicted)),
        "empreintes_images": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.jpg'))},
    }
    hidden = read('PROSE-PREDICTIONS.json')
    disclosed = read('prose-observee.json')
    assert [r['vue'] for r in hidden] == [r['vue'] for r in disclosed]
    result["prose_du_livre"] = {key: sum(norms(a['mot_predit'],False) == norms(b[key],False)
                                         for a,b in zip(hidden,disclosed))
                               for key in ('mot_imprime','temoin_imprime')}
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
