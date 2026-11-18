"""Prédictions textuelles, sans lecture des commentaires décrivant les dessins."""
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent/'2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, tokens, langage


def either(decisions):
    return True if True in decisions else (None if None in decisions else False)


def certain(w):
    return re.fullmatch('[a-z]+', w) is not None


def compatible(pattern, w):
    if certain(w):
        return pattern == w
    # Les lectures ambiguës ou manquantes restent explicites.
    return None


def radial_prediction(rows,split):
    out = {}
    for i in range(7,19):
        loc = 'f68v2.'+str(i)
        page,kind,_,raw = rows[loc]
        assert kind == 'Ro'
        seq = tokens(raw,split)
        pre = seq[0].startswith('ot') if certain(seq[0]) else None
        out[loc] = {'groupes':seq,'otor':either([compatible('otor',w) for w in seq]),
                    'premier_ot':pre,'ot_partout_rangs':[j for j,w in enumerate(seq,1) if certain(w) and 'ot' in w],
                    'lisibles':sum(certain(w) for w in seq)}
    return out


def quire(rows,faces,split):
    result = {}
    for f in sorted(faces):
        lines = []
        for loc,(page,kind,_,raw) in rows.items():
            if page != f or kind != 'P0':
                continue
            seq = tokens(raw,split)
            lines.append({'lieu':loc,'rangs':[i for i,w in enumerate(seq,1) if w=='otor'],
                          'positions':len(seq),'lisibles':sum(certain(w) for w in seq)})
        result[f] = lines
    return result


def comparison(pages):
    sources = [(ed,cut,ls) for ed,by_cut in pages.items() for cut,ls in by_cut.items()]
    known = {}
    all_lines = set()
    for ed,cut,ps in sources:
        for f,ls in ps.items():
            for line in ls:
                loc = line['lieu']
                all_lines.add(loc)
                if line['rangs']:
                    known.setdefault(loc,{})[ed+'_'+cut] = line['rangs']
    def key(loc):
        number,side,line = re.fullmatch(r'f(\d+)([rv])\.(\d+)',loc).groups()
        return int(number),side,int(line)
    triples = []
    for loc in sorted(known,key=key):
        f = loc.split('.')[0]
        lines = sorted([s for s in all_lines if s.split('.')[0]==f], key=key)
        index = lines.index(loc)
        after = lines[index+1:] + list(reversed(lines[:index]))
        control = next((s for s in after if s not in known),None)
        triples.append({'lieu':loc,'temoin':control,'lectures':known[loc],
                        'toutes_conventions':len(known[loc])==len(sources)})
    return triples


def main():
    eds,_ = corpus()
    raw = (langage.DATA/'ZL3b-n.txt').read_text().splitlines()
    faces = {m[1] for line in raw if (m:=re.match(r'^<([^.,>]+)>.*\$Q=T\b',line))}
    assert 'f103r' in faces and 'f116r' in faces
    q,r = {},{}
    for ed,rows in eds.items():
        q[ed],r[ed] = {},{}
        for cut in ('joints','separes'):
            r[ed][cut] = radial_prediction(rows,cut)
            q[ed][cut] = quire(rows,faces,cut)
    counts = {}
    for ed,rows in eds.items():
        counts[ed] = {}
        for cut in ('joints','separes'):
            counts[ed][cut] = {loc:{'groupes':tokens(raw,cut),'nombre':len(tokens(raw,cut))}
                                for loc,(page,kind,_,raw) in rows.items() if page=='f67r1' and kind=='Ri'}
            assert len(counts[ed][cut]) == 12
    out={'multiplicite':counts,'rayons':r,'paires_marge':comparison(q),'faces':sorted(faces),'exposition':{}}
    for ed,convs in q.items():
        for cut,ps in convs.items():
            out['exposition'][ed+'_'+cut] = {
                f:{'lignes':len(ls),'positions':sum(x['positions'] for x in ls),
                   'lisibles':sum(x['lisibles'] for x in ls)} for f,ls in ps.items()}
    (HERE/'PREDICTIONS.json').write_text(json.dumps(out,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
