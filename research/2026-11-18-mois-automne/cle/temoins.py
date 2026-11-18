"""Applique séparément la prédiction gelée à deux listes de noms historiquement documentées."""
import gzip
import hashlib
import json
import sys
from dechiffrer import HERE, PANELS, THREE, learn, read_pages, save, vocab, segment


def run(stage):
    targets = json.loads((HERE/'TEMOINS.json').read_text())
    fitting = stage == 'apprendre'
    if not fitting and stage != 'verifier':
        raise ValueError(stage)
    held = [p for p in PANELS if p not in THREE]
    dataset = read_pages(THREE if fitting else held)
    path = HERE/'PREDICTIONS-TEMOINS.json.gz'
    learned = {} if fitting else json.loads(gzip.decompress(path.read_bytes()))
    stats = {}
    for name, names in targets.items():
        for kind in ('Lz','Cc'):
            for limit in (1,2,9):
                for reverse in (False, True):
                    key = f'{name}/{kind}/{limit}/' + ('inverse' if reverse else 'direct')
                    if fitting:
                        books = [vocab(dataset,'accord',p,kind)[0] for p in THREE]
                        stats[key], learned[key] = learn(books,names,limit,reverse)
                    else:
                        stats[key] = {}
                        for p in held:
                            book, _ = vocab(dataset,'accord',p,kind)
                            hits = {''.join(w):locs for w,locs in book.items() if ''.join(w) in learned[key]}
                            for word in hits:
                                entry = learned[key][word]
                                for x, y in zip([*entry['sources'],word],names):
                                    units = segment(x)
                                    assert ''.join(entry['table'][s] for s in (units[::-1] if reverse else units)) == y
                            stats[key][p] = hits
    if fitting:
        path.write_bytes(gzip.compress(json.dumps(learned,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    save('APPRENTISSAGE-TEMOINS.json' if fitting else 'RESERVE-TEMOINS.json',
         {'empreinte_predictions':hashlib.sha256(path.read_bytes()).hexdigest(), 'branches':stats})


if __name__=='__main__':
    run(sys.argv[1])
