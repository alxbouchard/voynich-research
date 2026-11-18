"""Apprend toutes les tables transférables sur trois panneaux puis teste les graphies prédites."""
from collections import defaultdict
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0,str(HERE.parents[1] / '2026-11-18-carte-sept-etoiles/lecture'))
from essai import tables
sys.path.insert(0,str(HERE.parents[1] / '2026-11-18-formes-souterraines/nom/second'))
from transfert import tokens

DATA = REPO/'voynich_20261028/data'
FILES = {'H':'IT2a-n.txt','ZL':'ZL3b-n.txt'}
PANELS = 'f70v2 f70v1 f71r f71v f72r1 f72r2 f72r3 f72v3 f72v2 f72v1 f73r f73v'.split()
THREE = ['f72v2','f73r','f73v']
FOURTH = 'f72v1'
SERIES = {'developpes':('septembr','novembre','decebre','octembre'),
          'base':('septeb','novebre','decebre','octebre'),
          'reguliers':('septembre','novembre','decembre','octembre')}
SCOPES = {'accord':list(itertools.product(FILES, ('joints','separes'))),
          'H':[('H','joints')], 'ZL':[('ZL','joints')]}
LINE = re.compile(r'^<(f\w+)\.(\d+),([@&+*=-])(Cc|Lz)>\s*(.*)$')
UNITS = re.compile(r'c[kptf]h|ch|sh|[a-z]')


def segment(word):
    return tuple(UNITS.findall(word))


def read_pages(pages):
    source = {}
    for ed, filename in FILES.items():
        for cut in ('joints','separes'):
            words = {p:{kind:{} for kind in ('Lz','Cc')} for p in pages}
            for line in (DATA/filename).read_text().splitlines():
                m = LINE.match(line)
                if not m or m[1] not in words:
                    continue
                page, rank, _, kind, raw = m.groups()
                parts = tokens(raw, cut)
                eligible = [w for w in parts if re.fullmatch('[a-z]+',w)]
                if kind=='Lz' and len(parts)!=1:
                    eligible = []
                words[page][kind][page+'.'+rank] = set(eligible)
            source[ed,cut] = words
    return source


def vocab(source, scope, page, kind):
    readings = [source[version][page][kind] for version in SCOPES[scope]]
    loci = sorted(set.union(*(set(r) for r in readings)))
    out = defaultdict(list)
    for loc in loci:
        common = set.intersection(*(r.get(loc,set()) for r in readings))
        for w in common:
            out[segment(w)].append(loc)
    return dict(out), len(loci)


def frozen(mapping):
    return tuple(sorted(mapping.items()))


def spell(target, pieces):
    reachable = {0}
    for i in range(len(target)):
        if i in reachable:
            reachable.update(i+len(s) for s in pieces if target.startswith(s,i))
    return len(target) in reachable


@lru_cache(maxsize=None)
def substrings(other, limit):
    return frozenset(w[i:j] for w in other for i in range(len(w))
                     for j in range(i+1,min(i+limit,len(w))+1))


def candidates(words, names, i, limit, reverse):
    remaining = tuple(w for k,w in enumerate(names[:3]) if k!=i)
    available = substrings(remaining,limit)
    total = 0
    found = []
    for physical in sorted(words):
        seq = physical[::-1] if reverse else physical
        for mapping in tables(seq,names[i],limit):
            total += 1
            if spell(names[3], available | set(mapping.values())):
                found.append((physical,mapping))
    return found, total


def encodings(word, mapping, reverse):
    @lru_cache(maxsize=None)
    def visit(i):
        if i == len(word):
            return [()]
        return [(sign,*rest) for sign,clear in mapping.items() if word.startswith(clear,i)
                for rest in visit(i+len(clear))]
    for seq in visit(0):
        physical = seq[::-1] if reverse else seq
        if segment(''.join(physical)) == physical:
            yield physical


def compatible(left, right):
    return all(left.get(sign, value)==value for sign,value in right.items())


def learn(books, names, limit, reverse):
    singles = []
    stats = []
    for i, vocab_p in enumerate(books):
        good, total = candidates(vocab_p,names,i,limit,reverse)
        singles.append(good)
        stats.append({'mots':len(vocab_p),'ajustements':total,'admissibles_pour_transfert':len(good)})
    order = sorted(range(3), key=lambda i:len(singles[i]))
    a,b,c = order
    # Créer les tables à partir des deux plus petits répertoires.
    pairs = {}
    for wa,ma in singles[a]:
        for wb,mb in singles[b]:
            if compatible(ma,mb):
                pairs.setdefault(frozen(ma | mb), (wa,wb))
    predicted, seen = {},set()
    total_fit = 0
    for common, pair in pairs.items():
        base = dict(common)
        for wc,mc in singles[c]:
            if not compatible(base,mc):
                continue
            total_fit += 1
            full = base | mc
            if not spell(names[3], set(full.values())):
                continue
            key = frozen(full)
            if key in seen:
                continue
            seen.add(key)
            example = {a:pair[0],b:pair[1],c:wc}
            for seq in encodings(names[3], full, reverse):
                word = ''.join(seq)
                if word not in predicted:
                    predicted[word] = {'n':0,'table':dict(key),'sources':[''.join(example[i]) for i in range(3)]}
                predicted[word]['n'] += 1
    metrics = {'sources':stats,'ordre_jointure':order,'tables_deux_panneaux':len(pairs),
               'jointures_3_compatibles_apres_filtrage':total_fit,
               'tables_produisant_la_cible':len(seen),'graphies_physiques_predites':len(predicted)}
    return metrics, predicted


def controls():
    names = SERIES['developpes']
    charmap = dict(zip(sorted(set(''.join(names))), 'abdfgijklmpqrstvxyz'))
    mask = lambda w: tuple(charmap[c] for c in w)
    true = mask(names[3])
    books = [{mask(n),mask(n[::-1]),mask(n[1:]+n[0])} for n in names[:3]]
    fits, pred = learn(books,names,1,False)
    assert ''.join(true) in pred
    extras = ['mars','aberil','may','iollet','augst']
    other = {''.join(charmap.get(c,'z') for c in w) for w in extras}
    assert not (other & pred.keys())
    _,inv = learn([{x[::-1] for x in v} for v in books],names,1,True)
    assert ''.join(true[::-1]) in inv
    # Les rotations non identiques et l’inversion conservent les signes du mot réservé.
    distractors = [''.join(true[i:]+true[:i]) for i in range(1,len(true))]
    distractors.append(''.join(reversed(true)))
    scrambled_panel_hits = sorted(set(distractors) & pred.keys())
    assert not scrambled_panel_hits
    neg = ('sepembr', *names[1:])
    assert not learn(books,neg,2,False)[1]
    chunk = 'br'
    def coded(text):
        return tuple('x' if part==chunk else charmap[part] for part in re.findall('br|.',text))
    _,short = learn([{coded(n)} for n in names[:3]],names,2,False)
    assert ''.join(coded(names[3])) in short and not learn([{coded(n)} for n in names[:3]],names,1,False)[1]
    return {'chiffre_connue_apres_calcul':charmap,'mots_par_panneau':[[ ''.join(s) for s in sorted(book)] for book in books],
            'octobre':''.join(true),'graphiques_predites':sorted(pred),'indices':fits,
            'leurres_permutations_octobre':distractors,'leurres_acceptes':scrambled_panel_hits,
            'expansion_br':'x','octobre_avec_expansion':''.join(coded(names[3]))}


def programs():
    for scope,serie,kind,lmax,rev in itertools.product(SCOPES,SERIES,('Lz','Cc'),(1,2,9),(False,True)):
        if scope!='accord' and serie!='developpes':
            continue
        yield scope,serie,kind,lmax,rev


def branch(scope,serie,kind,lmax,rev):
    return '/'.join([scope,serie,kind,str(lmax),'inverse' if rev else 'direct'])


def fit():
    dataset = read_pages(THREE)
    out, words = {},{}
    for scope,serie,kind,limit,rev in programs():
        readings = [vocab(dataset,scope,p,kind) for p in THREE]
        key = branch(scope,serie,kind,limit,rev)
        out[key],words[key] = learn([r[0] for r in readings],SERIES[serie],limit,rev)
        out[key]['loci_disponibles'] = [r[1] for r in readings]
    save('APPRENTISSAGE.json',{'validations':controls(),'branches':out})
    with (HERE/'PREDICTIONS.json.gz').open('wb') as f:
        f.write(gzip.compress(json.dumps(words,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print('Branches',len(out),'prédictions émises',sum(map(len,words.values())))


def evaluate():
    data = json.loads(gzip.decompress((HERE/'PREDICTIONS.json.gz').read_bytes()))
    held = [p for p in PANELS if p not in THREE]
    dataset = read_pages(held)
    scores = {}
    for scope,serie,kind,limit,rev in programs():
        key = branch(scope,serie,kind,limit,rev)
        predicted = data[key]
        rows = {}
        for p in held:
            book,loc_count = vocab(dataset,scope,p,kind)
            hits = {''.join(w):locs for w,locs in book.items() if ''.join(w) in predicted}
            for w in hits:
                entry = predicted[w]
                sources = entry['sources'] + [w]
                for source, target in zip(sources, SERIES[serie]):
                    physical = segment(source)
                    units = physical[::-1] if rev else physical
                    assert ''.join(entry['table'][u] for u in units)==target
            rows[p] = {'loci':loc_count,'mots_distincts':len(book),'rencontres':hits}
        scores[key] = rows
    save('RESERVE.json',{'empreinte_predictions':hashlib.sha256((HERE/'PREDICTIONS.json.gz').read_bytes()).hexdigest(),'branches':scores})


def save(name, obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=1)+'\n')


if __name__ == '__main__':
    {'apprendre':fit,'verifier':evaluate}[sys.argv[1]]()
