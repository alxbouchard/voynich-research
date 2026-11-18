"""Acquérir les fiches GDN pour les lectures prédites et les mots témoins."""
import sys
import time
from paires import HERE, PREV, load, plain, save

sys.path.insert(0, str(PREV / 'lecture/tucker/dictionnaire'))
from interroger import interroger


def main():
    predictions = load(HERE / 'PREDICTIONS.json')
    words = sorted({
        plain(word) for row in predictions['lectures']['Tucker-Janick']
        for pair in row['paires'] for word in pair['lues'] if word
    })
    result = {}
    for word in ['atl', 'xochitl', 'zzzxqvzzzz', *words]:
        if result:
            time.sleep(0.3)
        row = interroger(word)
        if row['etat'] == 'erreur_http':
            raise RuntimeError((word, row))
        result[word] = row
        print(word, row['total'], flush=True)
    save(HERE / 'gdn.json', result)


if __name__ == '__main__':
    main()
