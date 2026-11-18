"""Compare the preregistered words with the published partial Bax table."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
EXCLUDED = {2, 3, 15, 16, 27, 29, 31, 41, 68, 116}
FACE = re.compile(r'^<(f(\d+)[rv]\d*)>\s+<! (.*?)>')
LINE = re.compile(r'^<((f\d+[rv]\d*)\.[^,>]+),.(\w{2})>\s*(.*)')
UNIT = re.compile('ckh|cth|cph|cfh|ch|sh|iin|in|ee|[a-z]')
TABLE = json.loads((HERE/'source/bax2014.json').read_text())['table_EVA']
NAMES = json.loads((HERE/'NOMS_FIXES.json').read_text())
# Consonants of the published sound options. An empty string is a vowel-only slot.
SKELETON = {'k':['k'], 'y':['n'], 'd':['t','d','θ','ð'], 'r':['r'], 'm':['r'],
            'n':['r'], 'sh':['kʰ','x','tʃ'], 's':['s'], 'o':[''], 'a':['','w'],
            'in':['r'], 'iin':['r'], 'e':[''], 'ee':['']}
assert set(TABLE) == set(SKELETON)

def parse(path, split):
    botanical = set()
    rows = {}
    for line in path.read_text().splitlines():
        head = FACE.match(line)
        if head and '$I=H' in head[3].split() and int(head[2]) not in EXCLUDED:
            botanical.add(head[1])
        record = LINE.match(line)
        if record:
            locus, page, kind, raw = record.groups()
            raw = re.sub(r'<![^>]*>|<[%$]>', '', raw)
            raw = re.sub(r'<[-~]>', '.', raw).replace('!', '')
            raw = raw.replace(',', '.' if split else '')
            rows[locus] = (page, kind, [w for w in raw.split('.') if w])
    return botanical, rows

def word_info(word):
    if not re.fullmatch('[a-z]+', word):
        return {'eva':word, 'simple':False}
    units = UNIT.findall(word)
    assert ''.join(units) == word
    values = [TABLE.get(unit) if unit != 'm' else ['r (conditionnel)'] for unit in units]
    return {'eva':word, 'simple':True, 'unites':units, 'sons':values,
            'couverture_stricte':all(u in TABLE and u != 'm' for u in units)}

def match(info, target):
    """At each target prefix, retain the fewest consonants supplied from a blank."""
    if not info['simple']:
        return None
    states = {0:0}
    for i, unit in enumerate(info['unites']):
        options = SKELETON.get(unit)
        if unit == 'm' and i+1 != len(info['unites']):
            options = None
        next_states = {}
        for pos, blanks in states.items():
            available = options if options is not None else (['', target[pos]] if pos < len(target) else [''])
            for consonant in available:
                if consonant and (pos == len(target) or target[pos] != consonant):
                    continue
                end = pos + bool(consonant)
                cost = blanks + (options is None and bool(consonant))
                next_states[end] = min(next_states.get(end, cost), cost)
        states = next_states
    if len(target) in states:
        cost = states[len(target)]
        return {'consonnes_par_valeur_admise':len(target)-cost,'consonnes_fournies_par_blanc':cost,
                'unites_toutes_couvertes':info['couverture_stricte']}
    return None

def analyse(path, split):
    pages, rows = parse(path, split)
    result = {'noms':{}, 'zodiaque':{}, 'couverture':{}, 'exemples_de_Bax':{}}
    for page, name in NAMES.items():
        words = next(words for pg, kind, words in rows.values() if pg == page and kind == 'P0')
        info = list(map(word_info,words))
        targets = name['consonnes']
        windows = []
        for i in range(len(info)-len(targets)+1):
            fits = [match(info[i+j], target) for j, target in enumerate(targets)]
            if all(fits):
                windows.append({'position':i+1,'mots':words[i:i+len(targets)],'details':fits})
        result['noms'][page] = {'ligne':info, 'premier_mot_contre_premier_nom':match(info[0],targets[0]),
                               'mots_initiaux_contre_noms':[match(info[j],t) for j,t in enumerate(targets)],
                               'fenetres_compatibles':windows}
    for locus in ['f71v.18','f72r1.18','f71r.18']:
        words = rows[locus][2]
        result['zodiaque'][locus] = {'positions':len(words),'simples':sum(word_info(w)['simple'] for w in words),
                                     'doary':words.count('doary'),'doaro':words.count('doaro'),'groupes':words}
    result['zodiaque']['f70v1'] = {'bordure_medallion':'vierge', 'positions':0}
    for locus in ['f68r3.11','f3v.1','f29v.1']:
        result['exemples_de_Bax'][locus] = word_info(rows[locus][2][0])
    starts = {}
    for locus, (page,kind,words) in rows.items():
        if page in pages and kind == 'P0' and page not in starts:
            starts[page] = dict(lieu=locus, **word_info(words[0]))
    result['couverture'] = {'faces_botaniques_eligibles':len(pages),'premiers_groupes':len(starts),
        'simples':sum(v['simple'] for v in starts.values()),
        'entierement_couverts':sum(v.get('couverture_stricte',False) for v in starts.values()),
        'faces_sans_P0':sorted(pages-starts.keys()),'detail':starts}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--donnees',type=Path,default=HERE.parents[1]/'voynich_20261028/data')
    p.add_argument('--sortie',type=Path,default=HERE/'RESULTATS.json')
    args=p.parse_args()
    result={}
    for key, filename in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        path=args.donnees/filename
        result[key] = {'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        for mode in ['joint','separe']:
            result[key][mode] = analyse(path, mode=='separe')
    args.sortie.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    main()
