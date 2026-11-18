"""Contrôles à clé récupérable, avec un leurre de même longueur et mêmes lettres."""
import json
from chercher import HERE, analyze, cases, corpus, tokenize


def projected(signs, data, width, mute=False):
    direct = next(iter(cases(data)))[1]
    result = analyze(signs, direct, width, mute)
    return {(r['segment'],r['rang_physique_historique_depart']): set(r['sorties'])
            for r in result['reservations']}


def main():
    forms = ['opcheor','opcheol','shody','sholdy']
    signs = [tokenize(w,True,False) for w in forms]
    known = dict(zip(sorted(set().union(*signs)), 'abcdefghijk'))
    def render(table):
        return [''.join(table[s] for s in word) for word in signs]
    tests = {}
    for mode in ['litteral','deux_lettres','un_muet']:
        key = dict(known)
        if mode=='deux_lettres':
            key['l'] += 'z'
        if mode=='un_muet':
            key['o'] = ''
        clear = render(key)
        wrong = clear[3][1:] + clear[3][0]
        assert wrong != clear[3]
        data = {'chiffre_reel':clear, 'temoin_avec_mot_reserve_permute':[*clear[:3],wrong]}
        preds = projected(signs,data,2 if mode=='deux_lettres' else 1, mode=='un_muet')
        truths = preds['chiffre_reel',1]
        assert clear[3] in truths and wrong not in truths
        assert preds['temoin_avec_mot_reserve_permute',1] == truths
        if mode=='deux_lettres':
            assert ('chiffre_reel',1) not in projected(signs,data,1)
        if mode=='litteral':
            assert not projected([s[::-1] for s in signs],data,1)
        tests[mode] = {'trois_mots':clear[:3],'bon_quatrieme':clear[3],
                       'predits':sorted(truths),'mauvais_quatrieme':wrong}
    docs = corpus('latin')
    eligible = ((chapter, start, words) for chapter, words in docs.items()
                for start in range(len(words)-3)
                if len(set(words[start:start+3])) == 3 and len(words[start+3]) >= 4
                and set(words[start+3]) <= set(''.join(words[start:start+3])))
    chapter, start, words = next(eligible)
    clear = words[start:start+4]
    alphabet = sorted(set(''.join(clear[:3])))
    secret = {ch: f'code-{i}' for i,ch in enumerate(alphabet)}
    encrypted = [tuple(secret[ch] for ch in word) for word in clear]
    preds = projected(encrypted,docs,1)
    actual = preds[chapter,start+1]
    assert actual == {clear[3]}
    correct_sites = [(loc,i) for (loc,i), choices in preds.items() if docs[loc][i+2] in choices]
    tests['phrase_latine'] = {'segment':chapter,'rang_depart':start+1,'trois_mots':clear[:3],
                              'mot_reserve':clear[3],'sorties_a_cette_position':sorted(actual),
                              'tous_les_lieux_predits':len(preds),'lieux_avec_mot_quatre_correct':correct_sites}
    (HERE/'CONTROLES.json').write_text(json.dumps(tests,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
