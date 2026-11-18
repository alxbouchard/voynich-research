"""Reprises exactes sur plusieurs feuillets ou notices, de deux à huit mots."""
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus

EXPECTED = tuple('de foliis ejus tritis factum cataplasma'.split())
LENGTHS = range(2,9)

def entries(chunks):
    """La fenêtre conserve la ligne de chaque mot, sans imposer le rang à l'intérieur de la ligne."""
    counter=Counter()
    for run in chunks:
        for end in range(2,len(run)+1):
            for n in range(2,min(8,end)+1):
                piece=run[end-n:end]
                words,loci=zip(*piece)
                counter[(words,loci)]+=1
    return counter

def voynich_chunks(data, sections, cut):
    chunks=[]; run=[]; previous=None
    for loc,(page,kind,pos,raw) in data.items():
        if kind!='P0' or sections.get(page)!='H':
            if run: chunks.append(run);run=[]
            previous=None
            continue
        number=int(loc.split('.')[1])
        if previous!=(page,number-1) or pos not in ('+','*'):
            if run: chunks.append(run);run=[]
        previous=(page,number)
        # Une note attachée au tracé, alternative ou ligature marquée suffit
        # à exclure le mot concerné. Un saut physique et la fin/début du
        # paragraphe interrompent le flux tout en gardant les mots complets.
        raw=re.sub(r'<![^>]*(?:gap|space|jump|through plant|next line intrudes)[^>]*>','.|.',raw,flags=re.I)
        raw=re.sub(r'<![^>]*>|\[[^\]]*\]|\{[^}]*\}','?',raw)
        raw=re.sub(r'<[-~%$]>','.|.',raw)
        raw=raw.replace('!','').replace(',','.' if cut=='separes' else '')
        for s in raw.split('.'):
            if not s:continue
            if re.fullmatch('[a-z]+',s):
                run.append((s,loc))
            elif run:
                chunks.append(run);run=[]
    if run:chunks.append(run)
    return chunks

def latin_chunks():
    root=RESEARCH/'2026-11-18-opcheor-paralleles/latin'
    books=json.loads((root/'corpus.json').read_bytes())
    chapters=defaultdict(list)
    for row in csv.DictReader((root/'vers.tsv').open(),delimiter='\t'):
        name=row['titre'];line=row['rang_du_vers']
        start=int(row['premier_mot_notice'])-1
        end=int(row['dernier_mot_notice'])
        chapters[name].extend((word,name+'#'+line) for word in books[name][start:end])
    return list(chapters.values())

def folio(loc):
    return loc.split('#')[0] if '#' in loc else re.match(r'^f(\d+)',loc)[1]

def summarise(data,include_cross):
    events=Counter(); groups=defaultdict(list)
    for (words,locs),n in data.items():
        if not include_cross and locs[0]!=locs[-1]:continue
        groups[words].append((locs,n));events[len(words)]+=n
    distribution=defaultdict(Counter)
    selected=defaultdict(list)
    for words,rec in groups.items():
        ids={folio(locs[0]) for locs,n in rec}
        count=len(ids);k=len(words)
        distribution[k][count]+=1
        if count>=2:
            selected[k].append({'mots':' '.join(words),'unites':count,'occurrences':sum(n for _,n in rec),
                                 'lieux':[[locs[0],locs[-1],n] for locs,n in rec]})
    stats=[]
    for n in LENGTHS:
        counts=distribution[n]
        stats.append({'longueur':n,'occurrences':events[n],'formes':sum(counts.values()),
                      'deux_unites':sum(v for k,v in counts.items() if k>=2),
                      'trois_unites':sum(v for k,v in counts.items() if k>=3)})
    tops={}
    for threshold in (2,3):
        longest=max((r['longueur'] for r in stats if r['deux_unites' if threshold==2 else 'trois_unites']),default=0)
        out=sorted((r for r in selected[longest] if r['unites']>=threshold),key=lambda r:(-r['unites'],r['mots']))
        tops[str(threshold)]={'longueur':longest,'reprises':out}
    return {'effectifs':stats,'maxima':tops},selected

def equal_volume(counts, n):
    # Préserver l'unité d'origine même si une formule reparaît dans une notice.
    rows=[(w,folio(locs[0])) for (w,locs),ct in counts.items() if len(w)==6 for _ in range(ct)]
    N=len(rows)
    recurrences=defaultdict(set)
    for w,chapter in rows:
        recurrences[w].add(chapter)
    ids={w:i for i,w in enumerate(w for w in recurrences if len(recurrences[w])>=2)}
    candidates=[(ids[w],chap) if w in ids else None for w,chap in rows]
    rng=random.Random(681847);out=Counter()
    for _ in range(1999):
        found=defaultdict(set)
        for i in rng.sample(range(N), n):
            event=candidates[i]
            if event:
                word,chapter=event
                found[word].add(chapter)
        nb2=sum(len(chapters)>=2 for chapters in found.values())
        nb3=sum(len(chapters)>=3 for chapters in found.values())
        out['une_suite_deux_notices']+=nb2>0
        out['une_suite_trois_notices']+=nb3>0
        out['formule_feuilles_trois_notices']+=len(found.get(ids[EXPECTED],()))>=3
    return {'source':N,'echantillon':n,'repetitions':1999,'graine':681847,'reussites':dict(out),
            'proba_formule_trois_exacte':n*(n-1)*(n-2)/(N*(N-1)*(N-2))}


def main():
    editions,sections=corpus()
    names=(e+'/'+cut for e in editions for cut in ('joints','separes'))
    all_stats={};shared=None
    for name in names:
        e,cut=name.split('/')
        counts=entries(voynich_chunks(editions[e],sections,cut))
        all_stats[name]={mode:summarise(counts,allow)[0]['effectifs'] for mode,allow in [('ligne',False),('paragraphe',True)]}
        shared=counts if shared is None else shared & counts
    consensus={};latin={}
    words_latin=entries(latin_chunks())
    for mode,cross in [('ligne',False),('paragraphe',True)]:
        consensus[mode],_=summarise(shared,cross)
        latin[mode],lat=summarise(words_latin,cross)
        phrase=[r for r in lat[6] if r['mots']==' '.join(EXPECTED)]
        assert len(phrase)==1 and phrase[0]['unites']==3
        latin[mode]['formule']=phrase[0]
    r={'lignes_H_P0':{e:sum(v[1]=='P0' and sections.get(v[0])=='H' for v in rs.values()) for e,rs in editions.items()},
       'unites_voynich':len({folio(loc) for rs in editions.values() for loc,v in rs.items() if v[1]=='P0' and sections.get(v[0])=='H'}),
       'panneaux_voynich':len({v[0] for rs in editions.values() for v in rs.values() if v[1]=='P0' and sections.get(v[0])=='H'}),
       'couches':all_stats,'consensus':consensus,'latin':latin}
    r['controle_volume']=equal_volume(words_latin,consensus['paragraphe']['effectifs'][4]['occurrences'])
    (HERE/'resultats.json').write_text(json.dumps(r,indent=1,ensure_ascii=False)+'\n')
    for obj in ('consensus','latin'):
        for mode in ('ligne','paragraphe'):
            s=r[obj][mode]
            print(obj,mode,[(v['longueur'],v['deux_unites'],v['trois_unites']) for v in s['effectifs']])
            for m,top in s['maxima'].items():
                print('max',m,top['longueur'],len(top['reprises']),top['reprises'][0] if top['reprises'] else '-')
    print('feuillets',r['unites_voynich'],r['panneaux_voynich'])
if __name__=='__main__': main()
