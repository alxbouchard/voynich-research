"""Énumération finie des substitutions prévues dans 01-protocole.json, bibliothèque standard."""
import csv
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROTOCOL = BASE / '01-protocole.json'
EXPECTED = '3cc4acfe59c8c1372183c323a09b0890602290ae5da3518ec0b49b11526eee60'
assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() == EXPECTED
SPEC = json.loads(PROTOCOL.read_text())


def variants(raw):
    if '.' in raw or ',' in raw:
        return [('espace', raw.replace('.', ' ').replace(',', ' ')),
                ('soudure', raw.replace('.', '').replace(',', ''))]
    return [('continu', raw.replace('!', ''))]


def tokenize(text, compound, reverse):
    tokens = []
    while text:
        sign = 'ch' if compound and text.startswith('ch') else text[0]
        tokens.append(sign)
        text = text[len(sign):]
    return tuple(reversed(tokens)) if reverse else tuple(tokens)


def tables(signs, target, limit, initial=None):
    """Chaque racine génère une affectation unique; un signe ordinaire ne franchit aucun espace."""
    if signs.count(' ') != target.count(' '):
        return
    mapping = dict(initial or {})

    def visit(i, start):
        if i == len(signs):
            if start == len(target):
                yield dict(mapping)
            return
        token = signs[i]
        if token == ' ' or token in mapping:
            fixed = ' ' if token == ' ' else mapping[token]
            if target.startswith(fixed, start):
                yield from visit(i + 1, start + len(fixed))
            return
        room = len(target) - start - (len(signs) - i - 1)
        end = min(room, limit) if limit else room
        for length in range(1, end + 1):
            value = target[start:start + length]
            if ' ' in value:
                break
            mapping[token] = value
            yield from visit(i + 1, start + length)
            del mapping[token]

    yield from visit(0, 0)


def project(signs, mapping):
    return ''.join(' ' if s == ' ' else mapping.get(s, '[' + s + ']') for s in signs)


def frozen(mapping):
    return tuple(sorted(mapping.items()))


def forced(mappings):
    if not mappings:
        return {}
    return {s: v for s, v in mappings[0].items() if all(m[s] == v for m in mappings)}


def one_direction(train, train_target, test, test_target, limit):
    maps = list(tables(train, train_target, limit))
    testsigns = set(test) - {' '}
    trainsigns = set(train) - {' '}
    unknown = sorted(testsigns - trainsigns)
    projections = Counter(project(test, m) for m in maps)
    full = [c for m in maps for c in tables(test, test_target, limit, m)]
    diagnostics = {'n_fit':len(maps), 'exact_frozen':projections[test_target],
                   'known_test_positions':sum(s in trainsigns for s in test if s != ' '),
                   'n_test_positions':sum(s != ' ' for s in test), 'unseen':unknown,
                   'forced_by_train':forced(maps), 'partial_predictions':dict(sorted(projections.items()))}
    return diagnostics, {frozen(m) for m in full}


def controls():
    a,b=SPEC['temoins']['castillan']['principales']
    alphabet=sorted(set(a+b)); cipher={letter:str(i) for i,letter in enumerate(alphabet,1)}
    encode=lambda text: tuple(cipher[c] for c in text)
    tr,te=encode(a),encode(b)
    ab,joint=one_direction(tr,a,te,b,1)
    ba,joint2=one_direction(te,b,tr,a,1)
    assert joint==joint2 and len(joint)==1 and ab['exact_frozen']==ba['exact_frozen']==0
    held=encode('ay')
    success,_=one_direction(tr,a,held,'ay',1)
    negative,_=one_direction(tr,a,held,'aa',1)
    backward_train=''.join(tr[::-1]); backward_test=''.join(held[::-1])
    reverse,_=one_direction(tokenize(backward_train,False,True),a,tokenize(backward_test,False,True),'ay',1)
    wrong_orientation,_=one_direction(tokenize(backward_train,False,False),a,tokenize(backward_test,False,False),'ay',1)
    assert wrong_orientation['exact_frozen']==0
    assert success['exact_frozen']==reverse['exact_frozen']==1 and negative['exact_frozen']==0
    exp_train=('K','L','M','K'); exp_test=('K','M')
    exp_diag,exp_maps=one_direction(exp_train,'açoraya',exp_test,'ay',None)
    assert exp_maps and exp_diag['exact_frozen']>0 and not list(tables(exp_train,'açoraya',1))
    return {'cipher_letters':cipher,'ciphertexts':[tr,te],'castilian_pair':{'forward':ab,'backward':ba,'n_joint':len(joint)},
            'fully_covered_ay':success,'false_aa':negative,'reversed_input_reversed_model':reverse,
            'expansion_positive':{'cipher_train':exp_train,'cipher_test':exp_test,'diagnostic':exp_diag,'n_joint':len(exp_maps)}}


def main():
    records=[]; positives=[]; rows=[]
    for tradition, witness in SPEC['temoins'].items():
        first,second=witness['principales']
        pairs=itertools.product([first,*witness['autres_3']],[second,*witness['autres_4']])
        for target_a,target_b in pairs:
            for reader,(raw_a,raw_b) in SPEC['lectures'].items():
                for spacing,btext in variants(raw_b):
                    for compounds,reverse,limit in itertools.product((True,False),(False,True),(1,None)):
                        a=tokenize(raw_a,compounds,reverse); b=tokenize(btext,compounds,reverse)
                        ab,joint=one_direction(a,target_a.lower(),b,target_b.lower(),limit)
                        ba,back=one_direction(b,target_b.lower(),a,target_a.lower(),limit)
                        assert joint==back
                        ident={'tradition':tradition,'nom_3':target_a,'nom_4':target_b,'principale':target_a==first and target_b==second,
                               'lecture':reader,'frontiere_X3':spacing,'unites':'ch' if compounds else 'char',
                               'sens':'inverse' if reverse else 'direct','largeur':'un' if limit else 'expansions'}
                        common=[dict(items) for items in sorted(joint)]
                        records.append(dict(ident,X1_vers_X3=ab,X3_vers_X1=ba,communes=common))
                        rows.append(dict(ident,ajustements_X1=ab['n_fit'],ajustements_X3=ba['n_fit'],
                                         exact_X1_vers_X3=ab['exact_frozen'],exact_X3_vers_X1=ba['exact_frozen'],
                                         tables_communes=len(joint),communes_injectives=sum(len(set(m.values()))==len(m) for m in common)))
                        if common:
                            line=tokenize('oalcheol',compounds,reverse)
                            positives.append(dict(ident,communes=common,impose_par_X1=ab['forced_by_train'],impose_par_X3=ba['forced_by_train'],
                                                  impose_par_paire=forced(common),nouvelles_X3=ab['unseen'],nouvelles_X1=ba['unseen'],
                                                  lectures_du_trait=[project(line,m) for m in common]))
    assert len(rows)==1008
    historical={'hypothese_publiee_separee':{'Grove':['doary','dchol!day'],'sorties':['taurn','tebartun']}}
    for compounds in [False,True]:
        x1=tokenize('doary',compounds,False); x3=tokenize('dcholday',compounds,False)
        ab, joint=one_direction(x1,'taurn',x3,'tebartun',None)
        ba, back=one_direction(x3,'tebartun',x1,'taurn',None)
        assert joint==back
        historical['ch_composé' if compounds else 'caractères']={'X1_vers_X3':ab,'X3_vers_X1':ba,'communes':[dict(m) for m in sorted(joint)]}
    (BASE/'ponzi-reconstitution.json').write_text(json.dumps(historical,ensure_ascii=False,indent=2)+'\n')
    with (BASE/'recensement.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    result={'protocole_sha256':EXPECTED,'controle':controls(),'nombre_configurations':len(rows),'solutions_conjointes':positives,'configurations':records}
    (BASE/'resultats.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    for group in (True,False):
        selected=[r for r in rows if r['principale']==group]
        print('principale',group,'n',len(selected),'avec solution conjointe',sum(r['tables_communes']>0 for r in selected),'tables',sum(r['tables_communes'] for r in selected),'transfert',sum(r['exact_X1_vers_X3']+r['exact_X3_vers_X1'] for r in selected))


if __name__=='__main__':
    main()
