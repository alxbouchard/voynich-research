"""Restituer une graphie cachée en prolongeant les valeurs proposées pour otedy."""
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path

from lxml import html

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, segment

ANCHOR = "otedy"
NAMES = ("stella", "sidus", "astrum", "femina", "mulier", "nympha", "figura", "uirgo")


def write(name, obj):
    raw = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode()
    (HERE / name).write_bytes(gzip.compress(raw, mtime=0) if name.endswith(".gz") else raw)


def read(name):
    raw = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith(".gz") else raw)


def matches(symbols, latin, given):
    if not symbols:
        if not latin:
            yield given
        return
    if len(latin) < len(symbols) or len(latin) > 2 * len(symbols):
        return
    sign = symbols[0]
    if sign in given:
        value = given[sign]
        if latin.startswith(value):
            yield from matches(symbols[1:], latin[len(value):], given)
        return
    for length in (1, 2):
        value = latin[:length]
        if len(value) == length and value not in given.values():
            yield from matches(symbols[1:], latin[length:], {**given, sign: value})


def encode(word, table):
    @lru_cache(maxsize=None)
    def walk(i):
        if i == len(word):
            return [()]
        return [(s,) + tail for s, value in table.items() if word.startswith(value, i)
                for tail in walk(i + len(value))]
    return walk(0)


def blocks(cache):
    hashes, chunks = [], []
    for n in range(1, 5):
        path = cache / f"voy-hyginus-latin{n}.shtml"
        hashes.append(sha256(path.read_bytes()).hexdigest())
        page = html.parse(str(path))
        for k, p in enumerate(page.xpath('//body/p[not(@class)]'), 1):
            if p.xpath('.//table|.//a'):
                continue
            # Bold section titles and section numbers are excluded, retaining tails.
            s = (p.text or '') + ''.join((' ' if c.tag != 'b' else ' # ') +
                                         ('' if c.tag == 'b' else c.text_content()) +
                                         (c.tail or '') for c in p)
            for j, part in enumerate(re.split(r'[^a-zA-Z\s]+', s), 1):
                tokens = part.split()
                block = []
                for tok in tokens + ['#']:
                    if tok == '#' or re.fullmatch('[IVXLCDM]+', tok):
                        if block:
                            chunks.append(([n, k, j, len(chunks)+1], block))
                        block = []
                    else:
                        block.append(tok.lower().replace('v','u').replace('j','i'))
    return hashes, chunks


def latin(cache):
    hashes, chunks = blocks(cache)
    models = {}
    for name in NAMES:
        contexts = []
        for loc, words in chunks:
            for j,w in enumerate(words):
                if w == name:
                    contexts.append(dict(lieu=loc+[j+1], gauche=words[j-1] if j else None,
                                         droite=words[j+1] if j+1 < len(words) else None))
        models[name] = dict(tables=list(matches(tuple(ANCHOR), name, {})), contextes=contexts)
    data = dict(sha256=hashes, sources=[f"https://www.thelatinlibrary.com/hyginus/hyginus{n}.shtml" for n in range(1,5)],
                mots=sum(len(words) for _, words in chunks), ancres=models)
    write("HYGIN.json", data)


def manuscript():
    editions, sections = corpus()
    coverage = Counter()
    for loc,(page,kind,*_) in editions['H'].items():
        if kind != 'P0' or loc not in editions['ZL'] or editions['ZL'][loc][1] != 'P0':
            continue
        run = []
        last = None
        for row in aligned(editions,loc,page,sections.get(page),page,coverage):
            indices = tuple(map(int,row['rangs_quatre'].split('/')))
            if last and (last[0] != row['troncon'] or not all(a+1==b for a,b in zip(last[1],indices))):
                yield loc,run
                run = []
            last = row['troncon'], indices
            run.append((f"{loc}/{row['troncon']}/{indices[0]}",row['mot']))
        if run:
            yield loc,run


def extraction():
    by_direction = {'droite': [], 'gauche': []}
    pairs = []
    for _, run in manuscript():
        for j,(loc,w) in enumerate(run):
            if j and w != ANCHOR and run[j-1][1] != ANCHOR:
                a,b=run[j-1][1],w
                if set(segment(a)+segment(b)) <= set(ANCHOR):
                    pairs.append((run[j-1][0],a,b))
            if w == ANCHOR:
                for direction,ds in [('droite',1),('gauche',-1)]:
                    anchor_side = run[j-ds][1] if 0<=j-ds<len(run) else None
                    test_side = run[j+ds][1] if 0<=j+ds<len(run) else None
                    by_direction[direction].append((loc,anchor_side,test_side))
    return by_direction,pairs


def forecast(symbols, name, flank, direction, contexts):
    known = 'gauche' if direction == 'droite' else 'droite'
    options = defaultdict(set)
    for row in contexts:
        if row[known] and row[direction]:
            options[row[known]].add(row[direction])
    output, partial = set(), set()
    for base in matches(tuple(symbols),name,{}):
        for latent, targets in options.items():
            for table in matches(flank,latent,base):
                partial.add(latent)
                for third in targets:
                    for signs in encode(third,table):
                        output.add((signs,latent,third))
    return partial, sorted(output)


def predictions():
    latin = read('HYGIN.json')['ancres']
    by_direction,_=extraction()
    for direction,rows in by_direction.items():
        masked=[(loc,a,bool(b)) for loc,a,b in rows]
        write(f'MASQUES-{direction}.json',masked)
    for direction in by_direction:
        preds=[]
        for loc,neighbor,scorable in read(f'MASQUES-{direction}.json'):
            out={}
            if neighbor and scorable:
                for name,model in latin.items():
                    two,opts=forecast(ANCHOR,name,segment(neighbor),direction,model['contextes'])
                    if two:
                        out[name]={'paires_latines_conditionnement':sorted(two),'predictions':opts}
            preds.append([loc,neighbor,scorable,out])
        write(f'ANNONCES-{direction}.json',preds)


def positive(latin):
    # The test engine is given ciphertext units and the clear anchor, but not the cipher key.
    for name in NAMES:
        for row in latin[name]['contextes']:
            a,b=row['gauche'],row['droite']
            if a and b and set(b)<=set(a+name):
                cipher = {ch:chr(0xe000+i) for i,ch in enumerate(sorted(set(a+name+b)))}
                code=lambda s:tuple(cipher[ch] for ch in s)
                left_to_right=forecast(code(name), name, code(a), 'droite', latin[name]['contextes'])[1]
                words = set(vals[0] for vals in left_to_right)
                return dict(ancre=name,gauche=a,droite=b,lieu=row['lieu'],annonces=len(words),
                            graphie_exacte=code(b) in words,contenu=[''.join(map(str,vals)) for vals in sorted(words)])
    return None


def adjudicate(cache):
    registry=read('HYGIN.json')
    hashes,chunks=blocks(cache)
    assert hashes==registry['sha256']
    latin=registry['ancres']
    source_pairs=defaultdict(list)
    for loc, words in chunks:
        for j in range(1,len(words)):
            source_pairs[tuple(words[j-1:j+1])].append(loc+[j])
    by_direction,pairs=extraction()
    results={'positif':positive(latin),'paires_Voynich':pairs}
    for direction,rows in by_direction.items():
        preds=read(f'ANNONCES-{direction}.json')
        decoded=[]
        for (loc,neighbor,target),(pid,pn,ok,pm) in zip(rows,preds,strict=True):
            assert (pid,pn,ok)==(loc,neighbor,bool(target))
            flex=[]
            options=set()
            if neighbor and target:
                for name,record in pm.items():
                    options.update(tuple(x[0]) for x in record['predictions'])
                    other='gauche' if direction=='droite' else 'droite'
                    for row in latin[name]['contextes']:
                        if row[other] not in record['paires_latines_conditionnement'] or not row[direction]:
                            continue
                        for t0 in latin[name]['tables']:
                            for t1 in matches(segment(neighbor),row[other],t0):
                                for t2 in matches(segment(target),row[direction],t1):
                                    flex.append([name,row['gauche'],row['droite'],row['lieu'],t2])
            decoded.append({'lieu':loc,'connu':neighbor,'reponse':target,
                            'annonces':len(options),'exact':bool(target and segment(target) in options),
                            'ajustements_trigramme_apres_ouverture':flex})
        results[direction]=decoded
    pair_vocab={pair for pair in source_pairs}
    results['tables']=[]
    for name, model in latin.items():
        for table in model['tables']:
            def check(t, sample=pairs):
                words = {w for _,a,b in sample for w in (a,b)}
                decoded={w:''.join(t[s] for s in segment(w)) for w in words}
                return [[loc,a,b,decoded[a],decoded[b],source_pairs[(decoded[a],decoded[b])][0]] for loc,a,b in sample
                        if (decoded[a],decoded[b]) in pair_vocab]
            values=tuple(table[s] for s in ANCHOR)
            perm=Counter(len(check(dict(zip(ANCHOR,p)))) for p in permutations(values))
            enc={w:encode(w,table) for w in {v for pair in pair_vocab for v in pair}}
            writable=sorted(pair for pair in pair_vocab if all(enc[w] for w in pair))
            control=None
            if writable:
                a,b=writable[0]
                c,d=enc[a][0],enc[b][0]
                found=check(table,[('temoin',''.join(c),''.join(d))])
                control={'latin':[a,b],'chiffre':[c,d],'exact':bool(found and found[0][3:5]==[a,b])}
            results['tables'].append({'nom':name,'valeurs':values,'paires':check(table),
                'positions_parmi_permutations':perm,'paires_codables':writable,'controle':control})
    write('VERIFICATION.json.gz',results)


if __name__=='__main__':
    if sys.argv[1]=='latin':latin(Path(sys.argv[2]))
    elif sys.argv[1]=='annoncer':predictions()
    elif sys.argv[1]=='verifier':adjudicate(Path(sys.argv[2]))
