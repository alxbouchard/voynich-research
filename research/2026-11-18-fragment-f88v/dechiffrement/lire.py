"""Énumérer les développements fixes compatibles avec deux graphies claires entières."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / '2026-11-18-formes-souterraines/nom'))
from abreger import macer_source, units, words

TARGET_ORDER = ('f89r2.fragment36', 'f88v.3')
CODES = ('opcheor', 'cpheor')
AFTER = ('cpheol', 'cpheor', 'chodar', 'opcheol')


def extensions(signs, plain, table, one_letter):
    """Tous les développements non vides ; les valeurs déjà connues sont imposées."""
    if not signs:
        if not plain:
            yield table
        return
    sign, *rest = signs
    if sign in table:
        known = table[sign]
        if plain.startswith(known):
            yield from extensions(rest, plain[len(known):], table, one_letter)
        return
    limit = len(plain) - sum(len(table.get(other, '?')) for other in rest)
    for n in range(1, min(limit, 1 if one_letter else limit) + 1):
        yield from extensions(rest, plain[n:], {**table, sign:plain[:n]}, one_letter)


def sequence(word, mode, reverse):
    s = units(word, mode)
    return s[::-1] if reverse else s


def spell(form):
    # Conserver chaque dénomination composée comme une seule hypothèse.
    # L'orthographe interne demeure identique. Les blancs ne sont pas des lettres.
    return ''.join(form.lower().split())


def test(names, codes, mode, reverse, strict, examples):
    cipher1,cipher2 = [sequence(w,mode,reverse) for w in codes]
    accepted, readings, n_tables, first_counts = {}, [], 0, {}
    for name in names[0]:
        tables = list(extensions(cipher1, spell(name), {}, strict))
        if tables:
            first_counts[name] = len(tables)
        for other in names[1]:
            key = (name,other)
            for t in tables:
                for complete in extensions(cipher2,spell(other),t,strict):
                    accepted[key] = accepted.get(key,0) + 1
                    n_tables += 1
                    if len(readings) < examples:
                        output = {w:'|'.join(complete.get(s,'?') for s in sequence(w,mode,reverse)) for w in AFTER}
                        readings.append({'noms':key,'table':complete,'developpements':output})
    return {'nombre_paires_testees':len(names[0])*len(names[1]),'premier_seul':first_counts,
            'nombre_paires_compatibles':len(accepted),'paires_noms_distincts':sum(a!=b for a,b in accepted),
            'nombre_tables':n_tables,'paires':[[a,b,n] for (a,b),n in accepted.items()],
            'exemples_de_tables':readings}


def check_calibration():
    # Deux noms français et leurs pluriels. Les codes sont attribués pour l'exercice.
    expected = {'o':'t','p':'e','ch':'nt','e':'a','r':'eur','cph':'am','l':'eurs'}
    def read(w,t):
        return ''.join(t[s] for s in sequence(w,'unites',False))
    first, second, third, gold = [read(w,expected) for w in (*CODES,'cpheol','opcheol')]
    assert [first,second,third,gold] == ['tentateur','amateur','amateurs','tentateurs']
    compatible = [{}]
    sizes = []
    for w,n in zip((*CODES,'cpheol'),(first,second,third)):
        compatible = [x for t in compatible for x in extensions(units(w,'unites'),n,t,False)]
        sizes.append(len(compatible))
    predictions = Counter(read('opcheol',t) for t in compatible)
    assert expected in compatible and set(predictions)=={gold}
    negative = test(([first],['amical']), CODES,'unites',False,False,0)
    assert negative['nombre_tables'] == 0
    return {'entrees':[first,second,third],'nombres_de_tables_apres_chaque_entree':sizes,
            'quatrieme_clair_masque':gold,'lectures_avant_comparaison_avec_quatrieme':predictions,
            'temoin_incompatible':[first,'amical'],'tables_incompatibles_retenues':0}


def transfer_secondary(names, results):
    """À partir des deux formes en r/s, tenter la forme en l avec le répertoire déjà fixé."""
    summary = []
    for first, second, count in results['paires']:
        rows = []
        for t in extensions(sequence('opcheos','unites',True),spell(first),{},False):
            for shared in extensions(sequence('cpheor','unites',True),spell(second),t,False):
                candidates = []
                for term in names[1]:
                    for extended in extensions(sequence('cpheol','unites',True),spell(term),shared,False):
                        fourth = ''.join(extended[s] for s in sequence('opcheol','unites',True))
                        candidates.append({'troisieme':term,'quatrieme_calcule':fourth,
                                           'quatrieme_dans_liste_un':fourth in set(map(spell,names[0]))})
                rows.append({'table':shared,'essais_compatibles':candidates})
        assert len(rows)==count
        summary.append({'paire':[first,second],'tables':rows})
    return summary


def run():
    stored = (HERE.parent/'noms/noms_figes.json').read_bytes()
    digest = sha256(stored).hexdigest()
    assert digest == 'cfaaeb4e28ad3ff4d8e8bf0b467e122505c0b84baa2e586f1c6cc849ae27ab9e'
    historical = json.loads(stored)['formes']
    macer = [' '.join(words(t)) for t,_ in macer_source()]
    assert len(macer) == len(set(macer)) == 77
    groups = {}
    for level,allowed in [('principaux',{'principal'}),('avec_secondaires',{'principal','secondaire'}),
                          ('avec_controles',{'principal','secondaire','controle_seul'})]:
        groups[level] = [[row['forme'] for row in historical if target in row['cibles'] and row['statut'] in allowed]
                         for target in TARGET_ORDER]
    groups['macer'] = [macer,macer]
    results = {}
    for group,names in groups.items():
        part = {}
        for a in ('opcheor','opcheos','opchear') if group != 'macer' else ('opcheor',):
            for mode in ('unites','caracteres'):
                for rev in (False,True):
                    for strict in (False,True):
                        tag = '_'.join([a,mode,'inverse' if rev else 'direct','lettre' if strict else 'variable'])
                        part[tag] = test(names,(a,CODES[1]), mode, rev, strict, 3)
        results[group] = {'noms':names,'modeles':part}
    (HERE/'resultats.json').write_text(json.dumps({'empreinte_noms':digest,'etalonnage':check_calibration(),
                  'etudes':results,'transfert_secondaire':transfer_secondary(groups['avec_secondaires'],
                     results['avec_secondaires']['modeles']['opcheos_unites_inverse_variable'])},indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    run()
