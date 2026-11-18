"""Projection d’une table gelée, contrôle de tous les ordres et des autres inscriptions."""
from collections import Counter
from itertools import permutations
import json
from abreviation import ENDING, MARK, PAGES, fit_four
from dechiffrer import HERE, vocab, read_pages, save, segment
from transfert import corpus, labels, tokens


def sequence(word, compact, reverse):
    seq = segment(word)
    if compact and seq[-4:] == ENDING:
        seq = (*seq[:-4],MARK)
    return seq[::-1] if reverse else seq


def project(seq, table):
    return ''.join(table.get(s,'['+s+']') for s in seq)


def all_labels():
    editions,_ = corpus()
    tables = {}
    for ed, rows in editions.items():
        whole = labels(rows,'joints')
        whole.update({l:tokens(raw,'joints') for l,(p,k,_,raw) in rows.items() if k=='Lz'})
        tables[ed] = whole
    return tables


def check(name, names, branch, books, corpus_labels):
    reverse,compact,mute = (branch[k] for k in ('inverse','abreviation_unique','signe_muet'))
    ranks = []
    for order in permutations(range(4)):
        _, mappings = fit_four(books, [names[i] for i in order], reverse,compact,mute)
        ranks.append({'ordre_des_mois':order, 'tables':len(mappings)})
    assert ranks[0]['tables']==len(branch['tables'])
    held = [Counter() for i in range(4)]
    hits = Counter()
    for entry in branch['tables']:
        words,table = entry['mots'],entry['table']
        seqs = [sequence(w,compact,reverse) for w in words]
        assert [project(s,table) for s in seqs]==list(names)
        for i,s in enumerate(seqs):
            known = {u for j,t in enumerate(seqs) if j!=i for u in t}
            proj = project(s, {k:v for k,v in table.items() if k in known})
            held[i][proj] += 1
        for loc, raw in corpus_labels['H'].items():
            # L’épreuve porte sur l’inscription complète, toutes les apparitions d’un mot isolé sont conservées.
            if len(raw)!=1 or not raw[0].isalpha() or not raw[0].isascii():
                continue
            pred = project(sequence(raw[0],compact,reverse),table)
            if pred in names:
                hits[loc,raw[0],pred] += 1
    return {
        'serie':name,'inverse':reverse,'abreviation_unique':compact,'signe_muet':mute,
        'ordres_avec_solution':sum(r['tables']>0 for r in ranks),
        'ordres_avec_au_moins_autant_de_tables_que_ordre_reel':sum(r['tables']>=ranks[0]['tables'] for r in ranks),
        'ordres':ranks,'predictions_sans_la_valeur_propre_au_mois':held,
        'formes_entieres_de_mois_sans_reapprentissage':[
             {'locus':loc,'forme_H':w,'nom_lu':n,'forme_ZL':corpus_labels['ZL'].get(loc), 'n_tables':count}
             for (loc,w,n),count in sorted(hits.items())],
    }


def main():
    prior = json.loads((HERE/'ABREVIATION.json').read_text())
    data = read_pages(PAGES)
    books = [[w for w in vocab(data,'H',p,'Lz')[0] if len(w)>4 and w[-4:]==ENDING] for p in PAGES]
    assert all(not b['tables'] for values in prior['lectures']['accord']['essais'].values() for b in values)
    corp = all_labels()
    outputs = []
    for name,(sep,nov,dec,octo) in prior['series'].items():
        for branch in prior['lectures']['H']['essais'][name]:
            if branch['tables']:
                outputs.append(check(name,(sep,octo,nov,dec),branch,books,corp))
    save('CONTROLES.json',outputs)


if __name__=='__main__':
    main()
