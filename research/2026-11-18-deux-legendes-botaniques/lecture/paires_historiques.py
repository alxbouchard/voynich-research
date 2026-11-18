"""Comparer les formes des titres, leurs épithètes et les noms allemands attestés."""
from itertools import product
import json
from lire import HERE, freeze, plain

def sides(row, field):
    words = []
    for entry in row['formes']:
        choices = {plain(entry[field])} if entry.get(field) else set()
        if field=='vernaculaire' and entry.get('autre_vernaculaire'):
            choices.add(plain(entry['autre_vernaculaire']))
        words.append(choices)
    return product(*words)

def main():
    entries = json.loads((HERE.parent/'noms/paires.json').read_text())
    index = {}
    for n,row in enumerate(entries,1):
        for field in ('nom','epithete','vernaculaire','tete'):
            for a,b in sides(row,field):
                for pair,side in [((a,b),'1-2'),((b,a),'2-1')]:
                    index.setdefault(pair,[]).append({'temoin':row['temoin'],'serie':row['serie'],
                        'forme':field,'ordre':side,'entree':n,'contexte':row['lieu_du_texte']})
    (HERE/'PARENTES-INDEX.json').write_text(json.dumps(
        [{'A':a,'B':b,'sources':v} for (a,b),v in sorted(index.items())],
        ensure_ascii=False,indent=1)+'\n')
    freeze(index,HERE/'PARENTES-PREDICTIONS.json.gz')

if __name__=='__main__':
    main()
