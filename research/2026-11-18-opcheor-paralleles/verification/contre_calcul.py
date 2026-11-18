"""Énumération des longueurs d'émission. Le quatrième mot reste hors de l'apprentissage."""
from collections import defaultdict
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIGNS = (('o','p','ch','e','o','r'), ('o','p','ch','e','o','l'),
         ('sh','o','d','y'), ('sh','o','l','d','y'))
PAIR_SIGNS = ('o','p','ch','e','r','l')
THIRD_SIGNS = ('sh','d','y')


def usable_widths(signs, nulls):
    for widths in product(range(3), repeat=len(signs)):
        if widths.count(0) <= nulls:
            yield dict(zip(signs, widths))


def cut(word, signs, widths, table):
    """Fixer les lettres aux positions découlant du modèle de longueurs."""
    if sum(widths[s] for s in signs) != len(word):
        return None
    result = table.copy()
    cursor = 0
    for s in signs:
        end = cursor + widths[s]
        chunk = word[cursor:end]
        if s in result and result[s] != chunk:
            return None
        result[s] = chunk
        cursor = end
    return result


@lru_cache(None)
def pair_widths():
    patterns = defaultdict(list)
    for widths in usable_widths(PAIR_SIGNS, 1):
        ix = tuple(sum(widths[s] for s in signs) for signs in SIGNS[:2])
        patterns[ix].append(widths)
    return patterns


@lru_cache(None)
def pairs(a, b, within):
    # Le radical commun perd au maximum les deux lettres de chaque terminaison.
    stemsize = max(len(a),len(b)) - 2
    if stemsize <= 0 or (a[:stemsize] != b[:stemsize] if within==1 else a[-stemsize:] != b[-stemsize:]):
        return ()
    results = []
    for widths in pair_widths().get((len(a),len(b)), ()):
        first = cut(a, SIGNS[0][::within], widths, {})
        if first is not None:
            second = cut(b, SIGNS[1][::within], widths, first)
            if second is not None:
                results.append(second)
    return tuple(results)


@lru_cache(None)
def train(a, b, c, within):
    result = []
    for known in pairs(a, b, within):
        free_nulls = 1 - sum(not x for x in known.values())
        for extra in usable_widths(THIRD_SIGNS, free_nulls):
            widths = dict(extra, o=len(known['o']))
            table = cut(c, SIGNS[2][::within], widths, known)
            if table is not None:
                result.append((table,''.join(table[s] for s in SIGNS[3][::within])))
    return result


def fits_insert(short, long):
    extra = len(long) - len(short)
    return extra > 0 and any(short == long[:i] + long[i+extra:] for i in range(len(short)+1))


def count(corpus, within, passage):
    windows = 0
    paired = {'sans_muet':0,'avec_au_plus_un_muet':0}
    insert = dict(tout_ajout=0, ajout_une_ou_deux_lettres=0, repetition=0)
    occurrences = []
    exemples_insertion = []
    ajustements_deux = []
    for notice, original in corpus.items():
        words = original[::passage]
        for i in range(len(words)-3):
            windows += 1
            a,b,c,d = words[i:i+4]
            index = i+1 if passage==1 else len(words)-i
            admissible = pairs(a,b,within)
            if admissible:
                paired['avec_au_plus_un_muet'] += 1
                paired['sans_muet'] += int(any(all(t.values()) for t in admissible))
                ajustements_deux.append(dict(notice=notice, rang_depart=index, mots=[a,b,c,d],
                    nombre_tables=len(admissible)))
            predictions = train(a,b,c,within)
            if predictions:
                occurrences.append(dict(notice=notice, rang_depart=index, mots=[a,b,c,d],
                    tables=[{'valeurs':t,'prediction':w,'exacte':w==d} for t,w in predictions]))
            if c==d:
                insert['repetition'] += 1
            elif fits_insert(c,d):
                insert['tout_ajout'] += 1
                insert['ajout_une_ou_deux_lettres'] += int(len(d)-len(c)<=2)
                exemples_insertion.append(dict(notice=notice,rang_depart=index,paire=[c,d],
                    premieres_formes_ajustables=bool(admissible)))
    return dict(fenetres=windows,paires_ajustees=paired,
        occurrences_apres_trois=occurrences,diagnostic_insertion=insert,
        lieux_insertion=exemples_insertion,lieux_apres_deux=ajustements_deux)


def sanity():
    table = dict(o='a',p='b',ch='cd',e='e',r='f',l='g',sh='hi',d='j',y='k')
    for within in (1,-1):
        for silent in (None,'l','d'):
            t = table.copy()
            if silent:
                t[silent] = ''
            a,b,c,d = [''.join(t[s] for s in signs[::within]) for signs in SIGNS]
            result = train(a,b,c,within)
            assert (t,d) in result and fits_insert(c,d)==bool(t['l'])
            assert len({tuple(sorted(key.items())) for key,_ in result}) == len(result)
    assert fits_insert('pera','petra') and not fits_insert('pera','preta') and not fits_insert('a','a')


def main():
    sanity()
    result={}
    for label in ('latin','francais'):
        source=HERE.parent / label / 'corpus.json'
        data=json.loads(source.read_text())
        modes={}
        for within, passage in product((1,-1),repeat=2):
            answer=count(data,within,passage)
            modes[f'unites_{within}_corpus_{passage}']=answer
            print(label, within, passage, answer['fenetres'], answer['paires_ajustees'],
                  len(answer['occurrences_apres_trois']), answer['diagnostic_insertion'])
        result[label]=dict(sha256=hashlib.sha256(source.read_bytes()).hexdigest(), resultats=modes)
    (HERE/'resultat.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
