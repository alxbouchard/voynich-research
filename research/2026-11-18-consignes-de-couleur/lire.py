"""Test littéral des trois correspondances proposées à partir de la feuille de f2r."""
import argparse
from bisect import bisect_left
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HEAD = re.compile(r'^<((?:f\d+[rv]\d*|fRos))>\s*<!\s*(.*?)>')
LOC = re.compile(r'^<(((?:f\d+[rv]\d*|fRos))\.[^,>]+),.([A-Za-z0-9]{2})>\s*(.*)')
SIMPLE = re.compile('[a-z]+')
COMPOUNDS = re.compile('ckh|cth|cph|cfh|ch|sh')
CODES = {'g':'ios','r':'an','n':'on'}
PATTERNS = [*CODES.values(),'iosan','iosanon']
SYMBOLS = {k:chr(0xe000+i) for i,k in enumerate(['ckh','cth','cph','cfh','ch','sh'])}
BARRIER = '|'

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def parse(path, separated):
    pages, rows = {}, {}
    for line in path.read_text().splitlines():
        head = HEAD.match(line)
        if head:
            pages[head[1]]=dict(re.findall(r'\$(\w)=(\S+)',head[2]))
            continue
        entry=LOC.match(line)
        if entry:
            locus, page, kind, raw = entry.groups()
            raw = re.sub(r'<![^>]*>|<@[^>]+>|<[%$]>', '', raw).replace('!', '')
            raw = re.sub(r'<[-~]>', '.', raw).replace(',', '.' if separated else '')
            fields = [w for w in raw.split('.') if w]
            rows[locus]=(page,kind,fields)
    return pages,rows

def units(w, compounds):
    if not SIMPLE.fullmatch(w):
        return BARRIER
    return COMPOUNDS.sub(lambda m:SYMBOLS[m[0]],w) if compounds else w

def find_all(haystack, needle):
    pos=haystack.find(needle)
    while pos>=0:
        yield pos
        pos=haystack.find(needle,pos+1)

def inventory(pages,rows,compounds):
    totals={}
    witnesses=defaultdict(lambda:defaultdict(list))
    paper=defaultdict(list)
    for loc,(p,typ,fields) in rows.items():
        if pages[p]['Q']=='A':
            continue
        category='prose_herbier' if pages[p].get('I')=='H' and typ.startswith('P') else 'fragment' if typ=='Lf' else 'autres'
        values=[units(w,compounds) for w in fields]
        joined=''.join(values)
        if category=='prose_herbier':
            paper[p].append(joined)
        if category not in totals:
            totals[category]={'pages':set(),'lignes':0,'positions':0,'incertaines':0,'unites_lisibles':0,
                              'motifs':{s:Counter() for s in PATTERNS}}
        total=totals[category]
        total['pages'].add(p)
        total['lignes']+=1
        total['positions']+=len(values)
        total['incertaines']+=values.count(BARRIER)
        total['unites_lisibles']+=sum(len(v) for v in values if v!=BARRIER)
        for motif in PATTERNS:
            counts=total['motifs'][motif]
            whole=values.count(motif)
            inside=sum(sum(1 for _ in find_all(w,motif)) for w in values)
            anyplace=sum(1 for _ in find_all(joined,motif))
            counts.update({'groupes_entiers':whole,'interieur_occurrences':inside,'ligne_jointe_occurrences':anyplace})
            if anyplace:
                counts['lignes_avec_motif']+=1
                if motif.startswith('ios'):
                    witnesses[category][motif].append({'locus':loc,'positions_dans_ligne_jointe':[x+1 for x in find_all(joined,motif)],'interieur':inside,'entier':whole})
    for total in totals.values():
        total['pages']=len(total['pages'])
    return totals,witnesses,{page:''.join(lines) for page,lines in paper.items()}

def sources():
    macer=REPO/'research/2026-11-18-noms-dans-les-notices/historique/corpus.jsonl'
    gart=REPO/'research/2026-11-17-plantes-repetees/historique/corpus.json'
    documents={}
    for line in macer.read_text().splitlines():
        ref=json.loads(line); words=ref['tokens'][:20]
        documents[ref['id']]=('macer',words,len(words))
    for ref in json.loads(gart.read_text())['items']:
        fields=ref['body'].split()[:20]
        excluded=set(ref['uncertain_word_positions'])|set(ref['missing_initial'])
        words=[w.lower() for i,w in enumerate(fields,1) if i not in excluded]
        documents[ref['id']]=('gart',words,len(fields))
    return documents,{file.name:hashlib.sha256(file.read_bytes()).hexdigest() for file in [macer,gart]}

def letter_order(words):
    return ''.join(ch for w in words for ch in w.lower() if ch in CODES)

def index_codes(pages):
    return {page:{letter:list(find_all(raw,code)) for letter,code in CODES.items()} for page,raw in pages.items()}

def contains(order,starts):
    stop=0
    for ch in order:
        positions=starts[ch]
        i=bisect_left(positions,stop)
        if i==len(positions):
            return False
        stop=positions[i]+len(CODES[ch])
    return True

def passage_search(documents,pages):
    indexed=index_codes(pages)
    results={}
    rng=random.Random(2408)
    for key,(book,words,n) in documents.items():
        order=letter_order(words)
        # In this positive control every other letter has one neutral character.
        enc=''.join(CODES.get(ch,'k') for w in words for ch in w)
        assert contains(order,index_codes({'controle':enc})['controle'])
        matches=sorted(page for page,index in indexed.items() if contains(order,index))
        counts=[]
        for _ in range(100):
            shuffled=list(order)
            rng.shuffle(shuffled)
            counts.append(sum(contains(shuffled,index) for index in indexed.values()))
        result={'source':book,'positions':n,'mots_retenus':len(words),'signature':order,'effectifs':dict(Counter(order)),
                'controle_positif':True,'faces_compatibles':matches,
                'permutations_nombre_de_faces':dict(sorted(Counter(counts).items()))}
        results[key]=result
    return results

def literal_fits(plain,code,may_omit):
    if BARRIER in code:
        return False
    @lru_cache(None)
    def fit(i,j):
        if i==len(plain):
            return j==len(code)
        token=CODES.get(plain[i])
        if token:
            return code.startswith(token,j) and fit(i+1,j+len(token))
        return any(fit(i+1,k) for k in range(j+(not may_omit),len(code)+1))
    return fit(0,0)

def name_tests(rows,compounds):
    cases={'f2v.1':['nenufar'],'f35v.1':['edera','nigra'],'f99v.2':['veratrum']}
    result={}
    for loc,names in cases.items():
        fields=rows[loc][2]
        vals=[units(w,compounds) for w in fields]
        strict=[]
        loose=[]
        for i in range(len(vals)):
            if i+len(names)<=len(vals) and all(literal_fits(n,w,False) for n,w in zip(names,vals[i:i+len(names)])):
                strict.append(i+1)
            for end in range(i+1,len(vals)+1):
                if literal_fits(''.join(names),''.join(vals[i:end]),True):
                    loose.append([i+1,end])
        result[loc]={'termes':names,'signature':letter_order(names),'groupes':fields,
                     'debuts_stricts':strict,'intervalles_assouplis':loose}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sortie',type=Path,default=HERE/'RESULTATS.json')
    args=p.parse_args()
    docs,hashes=sources()
    result={'editions':{},'sources_sha256':hashes,'convention':CODES}
    for ed,file in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        path=REPO/'voynich_20261028/data'/file
        result['sources_sha256'][file]=hashlib.sha256(path.read_bytes()).hexdigest()
        e=result['editions'][ed]={}
        for sep in [True,False]:
            pages,rows=parse(path,sep)
            for compounds in [True,False]:
                k=('separes' if sep else 'joints')+('_EVA' if compounds else '_ascii')
                totals,witnesses,paper=inventory(pages,rows,compounds)
                e[k]={'inventaire':totals,'temoins_rares':witnesses,
                      'passages':passage_search(docs,paper),'noms':name_tests(rows,compounds),
                      'locus_formation':rows.get('f2r.15')}
    dump(args.sortie,result)

if __name__=='__main__':
    main()
