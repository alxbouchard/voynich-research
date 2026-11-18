"""Énumérer les lectures sans ouvrir d'image ni de résultat iconographique."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import re
import sys

D = Path(__file__).resolve().parent
sys.path.insert(0,str(D.parents[1]/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import corpus, sequence, MODES

ORIGINES = {'f89r1.3','f89r1.25','f99v.31'}
FORMES = [base+fin for base in ('olda','salda','dolda') for fin in ('r','l','iin')]

def lecture(raw, mode):
    return [w for _,w in sequence(raw,mode)]

def alternatives(raw):
    pieces = re.split(r'(\[[^\[\]]+\])',raw)
    subs = [p[1:-1].split(':') if p.startswith('[') and p.endswith(']') else [p] for p in pieces]
    return {''.join(s) for s in product(*subs)}

def emplacements(words):
    return [{'mot':w,'rang':i+1,'position':'seul' if len(words)==1 else
             'premier' if i==0 else 'dernier' if i==len(words)-1 else 'interieur'}
             for i,w in enumerate(words) if w in FORMES]

def regrouper(table):
    labels={}
    for loc,(_,kind,pos,raw) in table.items():
        if kind!='Lf': continue
        base = 'f99r.6' if loc=='f99r.7' and pos=='+' else loc
        labels.setdefault(base,[]).append((loc,raw))
    return labels

def main():
    editions,_=corpus();tables={ed:regrouper(t) for ed,t in editions.items()}
    ids=dict.fromkeys(i for t in tables.values() for i in t if i not in ORIGINES)
    counts={};hits=[];sensitivity=[]
    for ed,t in tables.items():
        counts[ed]={'lignes_Lf':sum(len(rows) for k,rows in t.items() if k not in ORIGINES),
                    'inscriptions_Lf':sum(k not in ORIGINES for k in t)}
    for loc in ids:
        views={};altes={};originals={}
        for ed,table in tables.items():
            rows=table.get(loc,[]); originals[ed]=rows
            for cut in MODES:
                raw='.'.join(r for _,r in rows)
                ws=lecture(raw,cut)
                # Les séquences entre crochets ne prennent le statut certain dans aucune lecture.
                views[ed+' '+cut]={'texte':ws,'cibles':emplacements(ws)}
                variants=sorted({tuple(lecture(s,cut)) for s in alternatives(raw)}-{tuple(ws)})
                possibles=[list(x) for x in variants if emplacements(x)]
                if possibles: altes[ed+' '+cut]=possibles
        has=any(v['cibles'] for v in views.values())
        if has:
            common=set.intersection(*[{h['mot'] for h in v['cibles']} for v in views.values()])
            hits.append({'lieu':loc,'origine':originals,'vues':views,'communs':sorted(common)})
        if altes: sensitivity.append({'lieu':loc,'lectures_possibles':altes})
    out={'formes':FORMES,'exclus':sorted(ORIGINES),'couverture':counts,'union_inscriptions':len(ids),
         'cibles':hits,'alternatives':sensitivity}
    (D/'CIBLES.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
    print(counts,len(ids),[(h['lieu'],h['communs']) for h in hits],sensitivity)
if __name__=='__main__':main()
