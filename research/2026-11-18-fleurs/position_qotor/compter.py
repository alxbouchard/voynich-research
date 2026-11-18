"""Tester la position de qotor, conditionnellement aux occurrences de chaque ligne."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import re

def evaluate(path, split, single_hand):
    counts = Counter()
    occurrences = []
    dist = [Fraction(1)]
    face = None
    for line in path.read_text().splitlines():
        header = re.match(r'^<(f(\d+)[rv]\d*)>\s*(.*)',line)
        if header:
            name,leaf,attrs = header.groups()
            meta = dict(re.findall(r'\$(\w)=(\w+)',attrs))
            valid = int(leaf)>=25 and meta.get('I')=='H' and (not single_hand or (meta.get('H'),meta.get('L'))==('1','A'))
            face = name if valid else None
            rank = 0
            continue
        row = re.match(r'^<([^,.]+)\.([^,>]+),[^!]P0>\s*(.*)',line)
        if not face or not row:
            continue
        assert row[1]==face
        rank += 1
        body = re.sub(r'<![^>]*>|<[%$]>|!','',row[3])
        slots = [s for s in re.sub(r'<[-~]>','.',body).strip().replace(',','.' if split else '').split('.') if s]
        if not slots: continue
        first = bool(re.fullmatch('[a-z]+',slots[0]))
        eligible = sum(bool(re.fullmatch('[a-z]+',s)) for s in slots)
        hits = [i+1 for i,s in enumerate(slots) if s=='qotor']
        counts['lignes']+=1
        counts['initiales_lisibles']+=first
        counts['cases_lisibles']+=eligible
        counts['qotor']+=len(hits)
        counts['qotor_initial']+=(1 in hits)
        counts['qotor_initial_point4']+=(1 in hits and row[2]=='4')
        counts['qotor_initial_quatrieme_P0']+=(1 in hits and rank==4)
        if not hits:continue
        p = Fraction(len(hits),eligible) if first else Fraction()
        occurrences.append({'locus':face+'.'+row[2],'rang_P0':rank,'emplacements':hits,'lisibles':eligible,'p_initial':str(p)})
        new=[Fraction(0)]*(len(dist)+1)
        for i,value in enumerate(dist):
            new[i]+=value*(1-p)
            new[i+1]+=value*p
        dist=new
    assert sum(dist)==1
    prob=sum(dist[counts['qotor_initial']:])
    return {'comptes':dict(counts),'attente_initiale':sum(i*float(v) for i,v in enumerate(dist)),
            'probabilite_queue':float(prob),'fraction_exacte':str(prob),'occurrences':occurrences}

if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('donnees',type=Path)
    args=cli.parse_args()
    result = {f'{edition}_{mode}_{scope}':evaluate(args.donnees/name,split,hand)
              for edition,name in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]
              for mode,split in [('joint',False),('separe',True)]
              for scope,hand in [('tous',False),('main1A',True)]}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
