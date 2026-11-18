"""Vérification d'existence sur quatre mots au moyen d'expressions avec références."""
from itertools import product
import json
import re
from chercher import HERE, SHAPES, corpus, sources, tokenize

def inserted(short, long):
    delta = len(long) - len(short)
    return delta >= 0 and any(short[:i]+long[i:i+delta]+short[i:] == long
                              for i in range(len(short)+1))

def pattern(codes, null, width):
    seen = set()
    letter = '[^ ]+?' if width is None else f'[^ ]{{1,{width}}}'
    words = []
    for seq in codes:
        parts = []
        for s in seq:
            if s == null:
                continue
            if s in seen:
                parts.append(f'(?P={s})')
            else:
                parts.append(f'(?P<{s}>'+letter+')')
                seen.add(s)
        words.append(''.join(parts))
    return re.compile(' '.join(words))

def test_all(data):
    verified = {}
    for step in (1,-1):
        eligible = []
        for section, words in data.items():
            indices = range(len(words)-3) if step==1 else range(3,len(words))
            for i in indices:
                quad = tuple(words[i+step*j] for j in range(4))
                if inserted(quad[2],quad[3]):
                    eligible.append((section, i+1, quad))
        for (name, ed), compounds, rev in product(SHAPES.items(),(True,False),(False,True)):
            codes = [tokenize(w,compounds,rev) for w in sources()[ed][4:8]]
            alphabet = sorted(set().union(*codes))
            for width, mute in product((1,2,None),(False,True)):
                regexes = [pattern(codes,s,width) for s in (alphabet if mute else [None])]
                matches = [(section,pos,quad) for section,pos,quad in eligible
                           if any(rx.fullmatch(' '.join(quad)) for rx in regexes)]
                key = '/'.join([name,'bancs' if compounds else 'separes','inverse' if rev else 'direct',
                                str(step),str(width or 'libre'),str(int(mute))])
                verified[key] = matches
    return verified

def main():
    summary = {}
    for lang in ('latin','francais'):
        verified = test_all(corpus(lang))
        expected = json.loads((HERE/lang/'VERIFICATION.json').read_text())['branches']
        for k,v in verified.items():
            assert {(sect,pos) for sect,pos,_ in v} == {(t['segment'],t['rang_depart']) for t in expected[k]['sites_corrects']}
        summary[lang] = {'regles_controlees':len(verified), 'quadruplets_compatibles_par_regle':
                         {k: rows for k,rows in verified.items() if rows}}
    cipher = [tokenize(w,True,False) for w in ['opcheor','opcheol','shody','sholdy']]
    assert pattern(cipher,'o',2).fullmatch('herba herbae tam taeam')
    assert not pattern(cipher,'o',2).fullmatch('herba herbae tam similis')
    (HERE/'CONTRE-EPREUVE.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
