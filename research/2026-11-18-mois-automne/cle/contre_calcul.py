"""Vérification sans préfiltre des modèles à deux lettres et de la prédiction positive H."""
from itertools import combinations
import gzip
import json
from dechiffrer import HERE, SERIES, THREE, read_pages, vocab, save


def assignments(sequence, clear, width):
    for mid in combinations(range(1,len(clear)),len(sequence)-1):
        cuts = (0,*mid,len(clear))
        words = [clear[a:b] for a,b in zip(cuts,cuts[1:])]
        if all(len(w)<=width for w in words):
            mapping = dict(zip(sequence,words))
            if [mapping[s] for s in sequence]==words:
                yield mapping


def encoded(clear,table):
    queue = [(clear, ())]
    while queue:
        suffix, signs = queue.pop()
        if not suffix:
            yield signs
        for token,out in table.items():
            if suffix.startswith(out):
                queue.append((suffix[len(out):], (*signs,token)))


def brute(books, clear, width, rev, predicted):
    from dechiffrer import segment
    maps = {()}
    counts = []
    n_isolated = []
    for vocab_p, name in zip(books,clear[:3]):
        single = [m for w in vocab_p for m in assignments(w[::-1] if rev else w,name,width)]
        n_isolated.append(len(single))
        fixed = set()
        for key in maps:
            prev = dict(key)
            for m in single:
                if all(prev[s]==m[s] for s in prev.keys() & m.keys()):
                    fixed.add(tuple(sorted((prev|m).items())))
        maps = fixed
        counts.append(len(maps))
    projected = set()
    for key in maps:
        for units in encoded(clear[3],dict(key)):
            word = units[::-1] if rev else units
            if segment(''.join(word))==word:
                projected.add(''.join(word))
    assert projected==set(predicted)
    return {'dictionnaires_isoles':n_isolated,'dictionnaires_communs_apres_chaque_mois':counts,
            'predictions_confirmees':sorted(projected)}


def main():
    training = read_pages(THREE)
    frozen = json.loads(gzip.decompress((HERE/'PREDICTIONS.json.gz').read_bytes()))
    checks = {}
    for scope,width,kinds in [('accord',2,('Lz','Cc')),('H',9,('Lz',))]:
        for kind in kinds:
            for rev in (False,True):
                key = f'{scope}/developpes/{kind}/{width}/' + ('inverse' if rev else 'direct')
                books = [vocab(training,scope,p,kind)[0] for p in THREE]
                checks[key] = brute(books,SERIES['developpes'],width,rev,frozen[key])
    save('CONTRE-CALCUL.json',checks)


if __name__=='__main__':
    main()
