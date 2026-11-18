"""Compare generic whole-word recurrence near catalogued root/leaf drawings."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path


def catalogue(path):
    entries = []
    description = re.compile(r'^#\s*(root|leaf)\s+\[([^\]]+)\]', re.I)
    locus = re.compile(r'^<((f(?:\d+)[rv]\d*)\.\d+),.Lf;[^>]+>')
    lines = path.read_text(encoding='latin-1').splitlines()
    for n, line in enumerate(lines):
        hit = description.match(line)
        if not hit:
            continue
        j = n + 1
        while j < len(lines) and lines[j].startswith('#'):
            comment = lines[j][1:].strip()
            if (re.match(r'^(?:above |below )?(?:root|plant|leaf|item|container|label)\s+(?:f[\drv]+)?\s*\[',comment,re.I) or comment.startswith(('[','#','<'))):
                break
            j += 1
        record = locus.match(lines[j])
        if record and int(re.match(r'f(\d+)',record[2])[1]) >= 87:
            entries.append(dict(locus=record[1], face=record[2], kind=hit[1].lower(), element=hit[2], description=line, source_line=n+1))
    assert len({r['locus'] for r in entries}) == len(entries)
    return entries


def load_transcription(path):
    records = {}
    for line in path.read_text().splitlines():
        m = re.match(r'^<([^,]+),.Lf>(.*)$', line)
        if m:
            records[m[1]]=re.sub(r'<![^>]*>', '', m[2]).strip()
    return records


def words(raw, split):
    clean=raw.replace('!', '').replace('<$>','').replace('<%>','').replace('<->','.').replace('<~>','.')
    if split:
        clean=clean.replace(',', '.')
    else:
        clean=clean.replace(',', '')
    return sorted({w for w in clean.split('.') if re.fullmatch('[a-z]+',w)})


def metrics(records, name):
    types={'root_recto':[], 'root_verso':[], 'root_ailleurs':[], 'feuilles':[]}
    for row in records:
        key=({'f99r':'root_recto','f99v':'root_verso'}.get(row['face'],'root_ailleurs') if row['kind']=='root' else 'feuilles')
        types[key].append(row[name])
    counts={k:collections.Counter(w for group in groups for w in group) for k,groups in types.items()}
    pooled=counts['root_recto'] + counts['root_verso'] + counts['root_ailleurs']
    return {
        'groupes':{k:{'loci':len(groups),'lisibles':sum(bool(z) for z in groups),'distincts':len(counts[k]),'max_loci_meme_forme':max(counts[k].values(),default=0)} for k,groups in types.items()},
        'racines_toutes':{'maximum':max(pooled.values()),'formes_au_maximum':sorted(w for w,v in pooled.items() if v==max(pooled.values()))},
        'candidats_recto':{w:{k:c[w] for k,c in counts.items()} for w,v in counts['root_recto'].items() if v>=2},
        'intersection_recto_verso':{w:[counts['root_recto'][w],counts['root_verso'][w]] for w in sorted(counts['root_recto'].keys() & counts['root_verso'].keys())},
        'intersection_racines_feuilles':sorted(pooled.keys() & counts['feuilles'].keys())
    }

def main():
    parser=argparse.ArgumentParser();parser.add_argument('depot',type=Path);args=parser.parse_args()
    root=args.depot
    data=root/'voynich_20261028/data'
    paths={'LSI':root/'voynich_phase48/sources/upstream/input/LSI_ivtff_0d_original.txt','H':data/'IT2a-n.txt','ZL':data/'ZL3b-n.txt'}
    corpus={k:load_transcription(p) for k,p in paths.items() if k!='LSI'}
    records=catalogue(paths['LSI'])
    omitted=[r for r in records if any(r['locus'] not in d for d in corpus.values())]
    records=[r for r in records if r not in omitted]
    keys=[]
    for k,d in corpus.items():
        for split in [False,True]:
            name=k+('_separe' if split else '_joint')
            keys.append(name)
            for row in records:
                row[name]=words(d[row['locus']],split)
    print(json.dumps({'empreintes':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'hors_corpus':omitted,'bilan':{k:metrics(records,k) for k in keys},'loci':records},indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
