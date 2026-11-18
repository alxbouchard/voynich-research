"""Comparaison conditionnelle exacte des deux groupes, par face et longueur."""
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]/'2026-11-18-mots-et-dessins'))
from etiquettes import DATA, FILES, corpus

TARGETS = ('otoldy','okol')
TYPES = ('Lf','Lc')
KNOWN = {88,89,99,101}
HEADER = re.compile(r'^<(f\d+[rv]\d*)>\s+<!\s*(.*?)>')
LOCUS = re.compile(r'^<((f\d+[rv]\d*)\.\d+),[^!](L[fc])>\s*(.+)')


def sources():
    faces = {}
    literals = {}
    for ed,file in FILES.items():
        faces[ed] = set()
        literals[ed] = {}
        for ln in (DATA/file).read_text().splitlines():
            h = HEADER.match(ln)
            if h and '$I=P' in h[2].split():
                faces[ed].add(h[1])
            l = LOCUS.match(ln)
            if l and l[2] in faces[ed]:
                literals[ed][l[1]] = re.sub(r'<![^>]*>','',l[4]).strip()
    assert faces['H'] == faces['ZL']
    return faces['H'], literals


def exact_randomization(readable, targets, length_exact):
    strata = defaultdict(list)
    for locus, (face,leaf,kind,words) in readable.items():
        strata[face, len(words) if length_exact else 0].append((kind,bool(set(words) & targets)))
    dist,observed = Counter({0:Fraction(1)}),0
    for stratum in strata.values():
        n,f,h = len(stratum),sum(k=='Lf' for k,_ in stratum),sum(hit for _,hit in stratum)
        observed += sum(k=='Lf' and hit for k,hit in stratum)
        if not h:
            continue
        local = {j:Fraction(comb(f,j)*comb(n-f,h-j),comb(n,h)) for j in range(max(0,h-(n-f)),min(f,h)+1)}
        next_dist = Counter()
        for i,prob in dist.items():
            for j,part in local.items():
                next_dist[i+j] += prob*part
        dist = next_dist
    assert sum(dist.values()) == 1
    expected = sum(j*p for j,p in dist.items())
    upper = sum(v for j,v in dist.items() if j>=observed)
    return {'observed_fragment_hits':observed,'expected':float(expected),'expected_exact':str(expected),
            'upper_tail':float(upper),'upper_tail_exact':str(upper),'informative':len(dist)>1,
            'distribution':{j:str(v) for j,v in sorted(dist.items())}}


def summary(rows):
    n = len(rows)
    read = {loc:r for loc,r in rows.items() if r[3]}
    return {'annotated':n,'readable_loci':len(read),'readable_words':sum(len(r[3]) for r in read.values()),
            'hits':{w:sorted(loc for loc,r in read.items() if w in r[3]) for w in TARGETS}}


def condition(faces,ed,split):
    folios = {int(re.match(r'f(\d+)',face)[1]) for face in faces}
    table = {key:row for key,row in corpus(ed,folios,split).items() if row[0] in faces and row[2] in TYPES}
    per_face = {}; comparable = set()
    for face in sorted(faces):
        mapped = {k:summary({loc:r for loc,r in table.items() if r[0] == face and r[2] == k}) for k in TYPES}
        annotated_mix = all(mapped[k]['annotated'] for k in TYPES)
        read_mix = all(mapped[k]['readable_loci'] for k in TYPES)
        if read_mix:
            comparable.add(face)
        per_face[face] = dict(mapped,annotated_mix=annotated_mix,readable_mix=read_mix)
    cohorts = {}
    for name, criterion in [('hors_origine',lambda n:n not in KNOWN),('origine',lambda n:n in KNOWN),('ensemble',lambda n:True)]:
        val = {loc:r for loc,r in table.items() if r[0] in comparable and criterion(r[1])}
        read = {loc:r for loc,r in val.items() if r[3]}
        cohorts[name] = {'faces':sorted({r[0] for r in read.values()}),
                         'by_class':{k:summary({loc:r for loc,r in val.items() if r[2]==k}) for k in TYPES},
                         'permutations':{}}
        for words in [TARGETS,(TARGETS[0],),(TARGETS[1],)]:
            cohorts[name]['permutations']['|'.join(words)] = {
                strat:exact_randomization(read,set(words),is_len)
                for strat,is_len in [('face',False),('face_et_nombre_de_mots',True)]}
    return per_face,cohorts,table


def finite(raw,split):
    raw = raw.replace(',','.' if split else '')
    m = re.search(r'\[([a-z]*):([a-z]*)\]',raw)
    if not m:
        return [raw.split('.')] if re.fullmatch('[a-z]+(?:\\.[a-z]+)*',raw) else []
    return [ws for a in m.groups() for ws in finite(raw[:m.start()] + a + raw[m.end():],split)]


def main():
    faces, raw = sources()
    result = {'protocole_sha256':hashlib.sha256((HERE/'PROTOCOLE.md').read_bytes()).hexdigest(),
              'transcriptions_sha256':{e:hashlib.sha256((DATA/f).read_bytes()).hexdigest() for e,f in FILES.items()},
              'variants':{},'possible_readings':{}}
    with (HERE/'loci.tsv').open('w') as output:
        writer=csv.writer(output,delimiter='\t',lineterminator='\n')
        writer.writerow(['edition','espaces','face','locus','category','lisible','words','otoldy','okol'])
        for ed in ('accord','H','ZL'):
            for split in (False,True):
                spaces = 'separes' if split else 'joints'
                label = ed+'_'+spaces
                per_face,cohorts,table = condition(faces,ed,split)
                result['variants'][label]={'faces':per_face, 'cohorts':cohorts}
                for loc,(face,leaf,kind,words) in sorted(table.items()):
                    writer.writerow([ed,spaces,face,loc,kind,1 if words else 0,len(words or []),
                                     *[int(w in (words or [])) for w in TARGETS]])
                if ed != 'accord':
                    maybe = []
                    for loc,r in raw[ed].items():
                        if '[' not in r:
                            continue
                        readings=finite(r,split)
                        if any(w in ws for w in TARGETS for ws in readings):
                            maybe.append({'locus':loc,'code':table[loc][2],'raw':r,'readings':readings})
                    result['possible_readings'][label] = maybe
    (HERE/'resultats.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
