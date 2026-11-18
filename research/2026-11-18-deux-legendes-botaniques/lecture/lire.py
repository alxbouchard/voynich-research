"""Apprendre sur les deux légendes, puis chercher les formes déposées dans la prose historique."""
from collections import defaultdict
import gzip
from itertools import product
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH/'2026-11-18-carte-sept-etoiles/lecture'))
from essai import tables
sys.path.insert(0, str(RESEARCH/'2026-11-18-noms-secteurs/herbier'))
from mesurer import HEADING, MACER, MACER_HASH, checked

A, B, PROSE = 'opcheor','okcheor','okeor'


def plain(text):
    """Retirer accents, casse et blancs, garder lettres et distinctions u/v et i/j."""
    return ''.join(c for c in unicodedata.normalize('NFD',text.lower()) if c.isalpha())


def titles():
    source = checked(gzip.decompress(MACER.read_bytes()),MACER_HASH)
    names = [m[2] for m in HEADING.finditer(source)]
    assert len(names)==len(set(names))==77
    return names


def signs(word, compound, reverse):
    seq = tuple(re.findall(r'ch|sh|.' if compound else '.',word))
    return seq[::-1] if reverse else seq


def decode(seq,key):
    return ''.join(key[s] for s in seq)


def record(found, pair, prediction, table):
    outputs = found.setdefault(pair,{})
    if prediction not in outputs:
        outputs[prediction] = {'n':0,'table':table.copy()}
    outputs[prediction]['n'] += 1


def solve(pairs, compound, reverse, width, one_null):
    """Les signes des deux étiquettes sont identiques sauf au site p/k."""
    source,target,held = [signs(w,compound,reverse) for w in (A,B,PROSE)]
    cut = target.index('k')
    before,after = target[:cut],target[cut+1:]
    possible = defaultdict(set)
    for a,b in pairs:
        possible[a].add(b)
    found = {}
    for null in (sorted(set(source+target)) if one_null else (None,)):
        pronounced = tuple(s for s in source if s!=null)
        for a,others in possible.items():
            keys = tables(pronounced,a,width)
            for mapping in keys:
                if null is not None:
                    mapping[null] = ''
                prefix,suffix = decode(before,mapping),decode(after,mapping)
                for b in others:
                    size = len(b)-len(prefix)-len(suffix)
                    if size < 0 or (null=='k') != (size==0) or (width and size>width):
                        continue
                    if not (b.startswith(prefix) and b.endswith(suffix)):
                        continue
                    full = mapping | {'k':b[len(prefix):len(prefix)+size]}
                    assert decode(source,full)==a and decode(target,full)==b
                    record(found,(a,b),decode(held,full),full)
    return found


def models():
    for domain,rev,width,mute in product((True,False),(False,True),(1,2,3,None),(False,True)):
        name='/'.join(['banc' if domain else 'caracteres','inverse' if rev else 'direct',
                       str(width or 'libre'),str(int(mute))])
        yield name,(domain,rev,width,mute)


def freeze(pairs, path):
    out={}
    for model, params in models():
        found = solve(pairs,*params)
        out[model] = [{'A':a,'B':b,'prose':opts} for (a,b),opts in sorted(found.items())]
    result = json.dumps(out,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
    path.write_bytes(gzip.compress(result,mtime=0))


def evaluate(records, indexes, title_by_word):
    hits = []
    for r in records:
        source_a, source_b = r['A'],r['B']
        title = title_by_word[source_b]
        slots = len(title.split())
        # Dans les notices, conserver les frontières des mots entourant la fenêtre.
        vocabularies = indexes[slots]
        for pred in r['prose']:
            occurrences = vocabularies.get(pred,{})
            if occurrences:
                hits.append({'A':source_a,'B':source_b,'pred':pred,'copie':pred==source_b,
                             'notice_attendue':title,'retenue_dans_sa_notice':title in occurrences,
                             'lieux':occurrences})
    return hits


def indices(chapters, length):
    index = defaultdict(lambda:defaultdict(list))
    for chapter, words in chapters.items():
        for j in range(1,length+1):
            for i in range(len(words)-j+1):
                token = ''.join(words[i:i+j])
                index[token][chapter].append([i+1,j])
    return index


def judge():
    names = titles()
    by_word = {plain(t):t for t in names}
    chapters = json.loads((RESEARCH/'2026-11-18-opcheor-paralleles/latin/corpus.json').read_text())
    assert chapters.keys()==set(names)
    path = HERE/'MACER-PREDICTIONS.json.gz'
    predictions = json.loads(gzip.decompress(path.read_bytes()))
    indexes = {length:indices(chapters,length) for length in {len(t.split()) for t in names}}
    results={}
    for model, rows in predictions.items():
        matches = evaluate(rows,indexes,by_word)
        results[model] = {'paires_compatibles':len(rows),
                          'paires_distinctes':sum(r['A']!=r['B'] for r in rows),
                          'paires_distinctes_avec_raccourcissement':sum(r['A']!=r['B'] and any(p!=r['B'] for p in r['prose']) for r in rows),
                          'formes_distinctes_produites':len({p for r in rows for p in r['prose']}),'rencontres':matches}
    baseline={t:{'autres_notices':len(set(indexes[len(t.split())].get(plain(t),{}))-{t}),
                 'presente_dans_sa_notice':t in indexes[len(t.split())].get(plain(t),{})} for t in names}
    (HERE/'MACER-RESULTATS.json').write_text(json.dumps({'branches':results,'titres_entiers':baseline},ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    if sys.argv[1]=='apprendre':
        terms = list(map(plain,titles()))
        freeze(list(product(terms, repeat=2)),HERE/'MACER-PREDICTIONS.json.gz')
    elif sys.argv[1]=='verifier':
        judge()
    else:
        raise ValueError(sys.argv[1])
