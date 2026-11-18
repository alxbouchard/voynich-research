"""Count whole words attached to plant fragments on the fixed study folios."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
RECORD = re.compile(r'^<((f99r|f99v|f102v2)\.[^,>]+),.([A-Za-z0-9]{2})>\s*(.*)')
PAGES = ('f99r', 'f99v', 'f102v2')

def split_tokens(raw, split):
    text = re.sub(r'<![^>]*>|<[%$]>', '', raw).replace('!', '')
    text = re.sub(r'<[-~]>', '.', text).replace(',', '.' if split else '')
    return [w for w in text.split('.') if w]

def inspect_labels(path, split):
    entries = {page:{} for page in PAGES}
    leaf_paragraph_started = False
    for line in path.read_text().splitlines():
        record = RECORD.match(line)
        if not record:
            continue
        locus, page, kind, raw = record.groups()
        if page == 'f102v2' and kind.startswith('P'):
            leaf_paragraph_started = True
        if kind != 'Lf' or (page == 'f102v2' and leaf_paragraph_started):
            continue
        entries[page][locus] = split_tokens(raw, split)
    indexes = {}
    for page, labels in entries.items():
        index = defaultdict(list)
        for locus, tokens in labels.items():
            for word in sorted(set(tokens)):
                if re.fullmatch('[a-z]+',word):
                    index[word].append(locus)
        indexes[page] = index
    counts = {p:{'etiquettes':len(entries[p]), 'avec_forme_lisible':len({l for loci in indexes[p].values() for l in loci}), 'formes_distinctes':len(indexes[p])} for p in PAGES}
    max_training = max(map(len,indexes['f99r'].values()))
    def locate(words):
        return {w:{p:indexes[p].get(w,[]) for p in PAGES} for w in sorted(words)}
    candidates = locate(w for w,loci in indexes['f99r'].items() if len(loci)==max_training)
    overlap = locate(indexes['f99r'].keys() & indexes['f99v'].keys())
    return {'effectifs':counts,'maximum_apprentissage':max_training, 'premiers_ex_aequo':candidates,
            'intersection_deux_faces':overlap, 'etiquettes':entries}

def further_occurrences(path, split, reference):
    groups = {}
    comparable = defaultdict(list)
    pattern = re.compile(r'^<((?:f(\d+)[rv]\d*)\.[^,>]+),.([A-Za-z0-9]{2})>\s*(.*)')
    for line in path.read_text().splitlines():
        match = pattern.match(line)
        if not match:
            continue
        locus, folio, kind, raw = match.groups()
        if int(folio) in {99,102}:
            continue
        counts = groups.setdefault(kind, {'loci':0, 'mots_simples':0, 'occurrences':[]})
        counts['loci'] += 1
        for i, word in enumerate(split_tokens(raw,split),1):
            if re.fullmatch('[a-z]+',word):
                counts['mots_simples'] += 1
            if kind == 'Lf' and word in reference:
                comparable[word].append([locus,i])
            if word == 'otoldy':
                counts['occurrences'].append([locus,i])
    return groups, dict(sorted(comparable.items()))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--donnees',type=Path,default=HERE.parents[2]/'voynich_20261028/data')
    parser.add_argument('--sortie',type=Path,default=HERE/'RESULTATS.json')
    args=parser.parse_args()
    result={}
    for edition,filename in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        path=args.donnees/filename
        result[edition]={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        for mode in ['joint','separe']:
            result[edition][mode]=inspect_labels(path,mode=='separe')
            run = result[edition][mode]
            reference = {word for words in run['etiquettes']['f99r'].values() for word in words
                         if re.fullmatch('[a-z]+',word)}
            occurrences, comparable = further_occurrences(path,mode=='separe',reference)
            run['verification_otoldy'] = occurrences
            run['comparaison_exploratoire_transfert_des_autres_formes_de_f99r'] = comparable
    args.sortie.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
