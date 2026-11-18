"""Table stable EVA vers latin et contrôle à réponse connue sur Tycho, B1v."""
import csv
import hashlib
import importlib.util
import itertools
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[2]
PREVIOUS = ROOT / 'research/2026-11-18-mots-des-images/etoiles'
DATA = ROOT / 'voynich_20261028/data'
UNITS = re.compile('ckh|cth|cph|cfh|ch|sh|[a-z]')
CANDIDATES = ('stella', 'stellae', 'stellas', 'sideris')
CLUSTER = ('septem', 'pleiades', 'vergiliae', 'virgiliae')
SRC = {'IT': DATA/'IT2a-n.txt', 'ZL': DATA/'ZL3b-n.txt'}
RECORD = re.compile(r'^<(f68r[12]\.\d+),[@+]P0>\s*(.*)$')


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def latin(text):
    text = text.lower().replace('æ', 'ae').replace('&', ' et ').replace('v', 'u').replace('j', 'i')
    return re.findall(r'[a-z]+', ''.join(c for c in unicodedata.normalize('NFD', text)
                                        if not unicodedata.combining(c)))


def tables(signs, target, width, known=None):
    """Partition exhaustive du mot ; un ancien signe garde exactement sa valeur."""
    known = known or {}
    for cuts in itertools.combinations(range(1, len(target)), len(signs)-1):
        bounds = (0, *cuts, len(target))
        if any(b-a > width for a,b in zip(bounds, bounds[1:])):
            continue
        key = dict(known)
        for sign, a, b in zip(signs, bounds, bounds[1:]):
            value = target[a:b]
            if sign in key:
                if key[sign] != value:
                    break
            elif value in key.values():
                break
            else:
                key[sign] = value
        else:
            yield key


def decoded(signs, table):
    if all(x in table for x in signs):
        return ''.join(table[x] for x in signs)
    return None


def witness(brahe, width, masked):
    label = {k: latin(v) for k,v in brahe['legend'].items()}
    prose = latin(brahe['prose'])
    vocab = set(prose).union(*label.values())
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    mapping = {ch: 'u%02d' % ((i*7+11) % 26) if masked else ch for i,ch in enumerate(alpha)}
    def enc(word):
        return [mapping[c] for c in word]
    fits = []
    anchors = []
    for location, words in label.items():
        for i, word in enumerate(words, 1):
            keys = list(tables(enc(word), 'stella', width))
            anchors.append({'lieu': f'{location}/{i}', 'graphie': word, 'tables': len(keys)})
            for key in keys:
                readings = []
                for j, expected in enumerate(prose, 1):
                    guess = decoded(enc(expected), key)
                    if guess is not None and expected != 'stella':
                        readings.append({'rang': j, 'attendu': expected, 'lecture': guess,
                                         'exact': guess == expected, 'dans_vocabulaire': guess in vocab})
                fits.append({'lieu': f'{location}/{i}', 'graphie': word, 'table': key, 'prose': readings})
    return {'vocabulaire': sorted(vocab), 'nombre_mots_paragraphe':len(prose),
            'origines': anchors, 'tables_et_lectures': fits}


def parse_prose(path):
    rows = {}
    for line in path.read_text().splitlines():
        m = RECORD.match(line)
        if m:
            raw = re.sub(r'<![^>]*>|<[\$%]>', '', m[2]).translate(str.maketrans('','','{}! '))
            rows[m[1]] = raw.replace('<->','.').strip('.').split('.')
    assert re.search(r'^<f68r3\.11,@Ls>\s+doaro\s*$', path.read_text(), re.M)
    return rows


def consensus():
    h, zl = [parse_prose(SRC[ed]) for ed in ('IT','ZL')]
    assert h.keys() == zl.keys() and len(h) == 9
    allowed = []
    excluded = []
    for loc, words in h.items():
        if len(words) != len(zl[loc]):
            excluded.append({'lieu':loc,'IT':words,'ZL':zl[loc], 'motif':'nombre de cases différent'})
            continue
        for i,(w,z) in enumerate(zip(words,zl[loc]), 1):
            rank = f'{loc}/{i}'
            if w == z and re.fullmatch('[a-z]+', w):
                allowed.append((rank,w))
            else:
                excluded.append({'lieu':rank,'IT':w,'ZL':z, 'motif':'graphie différente ou incertaine'})
    return allowed, excluded


def labels():
    spec=importlib.util.spec_from_file_location('voy_legendes', PREVIOUS/'compter.py')
    lib=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    good = {}
    excluded = []
    for page, rows in lib.labels().items():
        if page == 'f68r2':
            continue
        for row in rows:
            words = lib.read_label(row['H'])
            if words and len(words)==1 and re.fullmatch('[a-z]+', words[0]) and words==lib.read_label(row['ZL']):
                good[row['locus']]=words[0]
            else:
                excluded.append(row)
    assert good['f68r1.26']=='otor'
    return good, excluded


def run(width, brahe, labels, words):
    control = witness(brahe, width, True)
    clear = witness(brahe, width, False)
    def outcomes(data):
        return [(row['lieu'], row['prose']) for row in data['tables_et_lectures']]
    assert clear['origines']==control['origines'] and outcomes(clear)==outcomes(control)
    vocab = set(control['vocabulaire'])
    cluster_signs = UNITS.findall('doaro')
    baseline = {w:list(tables(cluster_signs,latin(w)[0], width)) for w in CLUSTER}
    anchor = {w:list(tables(UNITS.findall('otor'), w, width)) for w in CANDIDATES}
    result = {}
    for loc, raw in labels.items():
        signs = UNITS.findall(raw)
        fits = []
        for key in tables(signs,'stella',width):
            shared = [key.get(s) for s in cluster_signs]
            possibilities = {w:list(tables(cluster_signs, latin(w)[0],width,key)) for w in CLUSTER}
            out = []
            for rank, word in words:
                if word == raw:
                    continue
                read = decoded(UNITS.findall(word),key)
                if read and len(read)>=3 and read!='stella':
                    out.append({'lieu':rank,'EVA':word,'latin':read,'dans_vocabulaire':read in vocab})
            fits.append({'table':key,'prose':out,'doaro_connu':shared,'doaro_completions':possibilities})
        result[loc] = {'EVA':raw,'tables':fits}
    return {'controle':control,'otor':anchor,'doaro_sans_ancre':baseline,'formes_voynich':result}


def main():
    brahe = json.loads((DIR/'brahe.json').read_text())
    assert checksum(DIR/'brahe-b1v.jpg') == brahe['image_sha256']
    eligible, excluded = labels()
    words, excluded_prose = consensus()
    data = {'empreintes':{str(p.relative_to(ROOT)):checksum(p) for p in
                            (PREVIOUS/'sources.tsv', PREVIOUS/'compter.py', *SRC.values(),
                             DIR/'brahe.json', DIR/'PROTOCOLE.md')},
            'legendes_valides':eligible,'legendes_exclues':excluded,
            'prose_valide':words,'prose_exclue':excluded_prose,
            'modeles':{str(width):run(width,brahe,eligible,words) for width in (1,3)}}
    (DIR/'RESULTATS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
