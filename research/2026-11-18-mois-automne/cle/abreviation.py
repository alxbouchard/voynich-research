"""Teste la finale commune y compris comme un seul signe abréviatif."""
from itertools import product
import json
from pathlib import Path
from dechiffrer import THREE, FOURTH, SERIES, compatible, frozen, read_pages, save, tables, vocab

PAGES = [THREE[0], FOURTH, *THREE[1:]]
ENDING = ('e','o','d','y')
MARK = '[eody]'


def one_model(sequence, target, reverse, compact, mute):
    seq = sequence[:-4] + (MARK,) if compact else sequence
    if reverse:
        seq = seq[::-1]
    # Le signe déclaré muet n’occupe aucune lettre de sortie.
    audible = tuple(s for s in seq if s != mute)
    start = {mute:''} if mute is not None else {}
    return list(tables(audible, target, None, start))


def fit_four(books, targets, reverse, compact, mute):
    possible = {((),False): ()}
    steps = []
    for source, target in zip(books, targets):
        isolated = [(word, key) for word in source for key in one_model(word,target,reverse,compact,mute)]
        extended = {}
        for (old,already_used), witness in possible.items():
            previous = dict(old)
            for word, key in isolated:
                if compatible(previous,key):
                    combined = frozen(previous | key)
                    units = word[:-4]+(MARK,) if compact else word
                    extended.setdefault((combined,already_used or mute in units), (*witness,word))
        steps.append({'ajustements_locaux':len(isolated),'tables_compatibles':len(extended)})
        possible = extended
    return steps, {k:w for (k,used),w in possible.items() if mute is None or used}


def control():
    targets = ('septembre','octembre','novembre','decembre')
    words = [(prefix, *ENDING) for prefix in ['S','O','N','D']]
    books = [[w] for w in words]
    _,full = fit_four(books,targets,False,True,None)
    gold = frozen({MARK:'embre','S':'sept','O':'oct','N':'nov','D':'dec'})
    assert gold in full
    _,train = fit_four([books[i] for i in (0,2,3)], [targets[i] for i in (0,2,3)],False,True,None)
    assert all('O' not in dict(k) for k in train)
    return {'table_connue_retrouvee':dict(gold),'tables_apres_les_quatre_noms':len(full),
            'tables_apres_trois_noms':len(train),'nombre_avec_debut_octobre_connu':sum('O' in dict(k) for k in train)}


def inspect(scope, dataset, series):
    tables_by_edition = [vocab(dataset,scope,p,'Lz')[0] for p in PAGES]
    books = [[w for w in book if len(w)>4 and w[-4:]==ENDING] for book in tables_by_edition]
    sources = [{''.join(w):book[w] for w in words} for words,book in zip(books,tables_by_edition)]
    distinct = {tuple(choice) for choice in product(*books) if len(set(choice))==4}
    result = {}
    for name,(sept,nov,dec,october) in series.items():
        targets = (sept,october,nov,dec)
        results = []
        for reverse,compact in product((False,True),(False,True)):
            letters = sorted({s for group in books for w in group for s in (w[:-4] + (MARK,) if compact else w)})
            for mute in [None,*letters]:
                steps,maps = fit_four(books, targets, reverse,compact,mute)
                examples = [{'table':dict(k),'mots':[''.join(w) for w in ws]} for k,ws in maps.items()]
                results.append({'inverse':reverse,'abreviation_unique':compact,'signe_muet':mute,
                                'etapes':steps,'tables':examples})
        result[name] = results
    return {'lectures':sources,'choix_de_quatre_distincts':len(distinct),
            'choix_logographiques_apres_rattachement_arbitraire_des_debuts':
                [[ ''.join(w[:-4]) for w in row] for row in sorted(distinct)],'essais':result}


def main():
    data = read_pages(PAGES)
    ext = json.loads((Path(__file__).parent/'TEMOINS.json').read_text())
    series = SERIES | ext
    save('ABREVIATION.json', {'controle':control(),'series':series,
         'lectures':{mode:inspect(mode,data,series) for mode in ('accord','H','ZL')}})


if __name__=='__main__':
    main()
