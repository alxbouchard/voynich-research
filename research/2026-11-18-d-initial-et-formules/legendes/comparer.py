"""Confronter l'ordre des inscriptions du bain à la prose concordante."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from random import Random
import argparse
import json
import re
import sys

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-dam-en-fin-de-ligne'))
from corpus_dam import ROOT, aligned, corpus, metadata

ROWS={'f84r':[[10],[11],[12]],'f80r':[[i] for i in range(1,10)],
      'f82r':[[i] for i in range(40,46)],'f75v':[[i,i+1] for i in range(18,38,2)]}
SCOPES=('sous_image','reste_84r','autres_bains','autres_pages')
FILES=('IT2a-n.txt','ZL3b-n.txt')


def save(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=1,ensure_ascii=False,sort_keys=True)+'\n')


def dump_labels():
    tables=defaultdict(list)
    for filename in FILES:
        for line in (ROOT/'voynich_20261028/data'/filename).read_text().splitlines():
            m=re.match(r'^<(f\d+[rv]\d*)\.(\d+),.Ln>\s*(.*)',line)
            if not m or m[1] not in ROWS:
                continue
            raw=re.sub(r'<![^>]*>|<[%$]>|!','',m[3]).strip('.')
            for split in ('','.'):
                v=raw.replace(',',split).split('.')
                tables[m[1],int(m[2])].append(v if all(re.fullmatch('[a-z]+',w) for w in v) else None)
    out={}
    for page,row in ROWS.items():
        objects=[]
        for ids in row:
            editions=[tables[page,n] for n in ids]
            agree=all(len(v)==4 and v[0] and all(r==v[0] for r in v) for v in editions)
            words=[w for v in editions for w in v[0]] if agree else None
            objects.append({'lieux':[f'{page}.{n}' for n in ids],'lectures':editions,'mots':words})
        out[page]=objects
    save('ANNONCES.json',out)


def normal(words):
    return tuple('shedy' if w=='dshedy' else w for w in words)


def prose():
    ed,_=corpus()
    meta=metadata()
    out=defaultdict(list)
    for loc,(face,kind,_,_) in ed['H'].items():
        if kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0':
            continue
        section=meta.get(face,{}).get('I')
        if face=='f84r':
            scope='sous_image' if 13<=int(loc.split('.')[1])<=16 else 'reste_84r'
        else:
            scope='autres_bains' if section=='B' else 'autres_pages'
        previous=None
        for r in aligned(ed,loc,face,section,face,Counter()):
            ranks=tuple(map(int,r['rangs_quatre'].split('/')))
            block=r['troncon']
            if previous is None or previous[0]!=block or any(y!=x+1 for x,y in zip(previous[1],ranks)):
                out[scope].append([])
            out[scope][-1].append((f"{loc}/{block}/{ranks[0]}",r['mot'],'debut' in r['positions']))
            previous=(block,ranks)
    return out


def index_runs(runs,convert,max_length):
    hist=Counter()
    sites=defaultdict(list)
    sequences=[]
    for run in runs:
        seq=tuple('shedy' if convert and first and w=='dshedy' else w for _,w,first in run)
        loci=[k for k,_,_ in run]
        sequences.append((seq,loci))
        for i in range(len(seq)):
            for n in range(1,min(max_length,len(seq)-i)+1):
                gram=seq[i:i+n]
                hist[gram]+=1
                sites[gram].append((len(sequences)-1,i))
    return hist,sites,sequences


def alignment(phrase,index):
    _,sites,seqs=index
    return [seqs[r][1][i] for r,i in sites.get(phrase,[])]


def predict(left,right,index):
    _,sites,seqs=index
    rows=[]
    for r,i in sites.get(left,[]):
        seq,loc=seqs[r]
        j=i+len(left)
        if j+len(right)>len(seq):
            actual=None
        else:
            actual=list(seq[j:j+len(right)])
        rows.append({'depart':loc[i],'suite_lue':actual})
    return {'ancre':list(left),'annonce':list(right),'occurrences':len(rows),
            'suites_evaluables':sum(r['suite_lue'] is not None for r in rows),
            'exactes':sum(r['suite_lue']==list(right) for r in rows),'ouvertures':rows}


def within_gap(words,index):
    _,sites,seqs=index
    hits=[]
    for r,i in sites.get((words[0],),[]):
        seq,loc=seqs[r]
        for j in range(i+1,min(i+6,len(seq))):
            if seq[j]!=words[1]:continue
            if len(words)==2:
                hits.append([loc[i],loc[j]])
                continue
            for k in range(j+1,min(j+6,len(seq))):
                if seq[k]==words[2]:hits.append([loc[i],loc[j],loc[k]])
    return hits


def ordered_counts(objs,hist):
    value=Counter()
    for n in (2,3):
        occ=0
        for i in range(len(objs)-n+1):
            window=objs[i:i+n]
            if all(window):
                occ+=hist[sum(window,())]
        value[str(n)]=occ
    return value


def control(objs,hist,rng):
    direct=ordered_counts(objs,hist)
    reverse=ordered_counts(objs[::-1],hist)
    simulated=Counter()
    for _ in range(999):
        trial=rng.sample(objs,len(objs))
        score=ordered_counts(trial,hist)
        simulated[score['2'],score['3']]+=1
    return {'direct':direct,'inverse':reverse,'distribution_999':[[a,b,v] for (a,b),v in sorted(simulated.items())]}


def verify():
    labels=json.loads((HERE/'ANNONCES.json').read_text())
    groups=prose()
    out={}
    for convert in (False,True):
        how='d_initial' if convert else 'exact'
        for scope in SCOPES:
            o={}
            index=index_runs(groups[scope],convert,8)
            hist,sites,seqs=index
            o['denominateurs']={'mots':sum(map(len,groups[scope])),'troncons_concordants':len(seqs),
                                'paires':sum(n for k,n in hist.items() if len(k)==2),
                                'triplets':sum(n for k,n in hist.items() if len(k)==3)}
            o['rangees']={}
            for page,items in labels.items():
                objs=[(normal(x['mots']) if convert else tuple(x['mots'])) if x['mots'] else None for x in items]
                row=control(objs,hist,Random(8412))
                row['annonces_de_la_troisieme']=[]
                row['paires_retrouvees']=[]
                row['inscriptions_composees']=[]
                for i,word in enumerate(objs):
                    if word and len(word)>1:
                        row['inscriptions_composees'].append({'mots':list(word),'lieux':alignment(word,index)})
                    if i and word and objs[i-1]:
                        pair=objs[i-1]+word
                        if hist[pair]:
                            row['paires_retrouvees'].append({'mots':list(pair),'lieux':alignment(pair,index)})
                    if i>=2 and all(objs[i-2:i+1]):
                        row['annonces_de_la_troisieme'].append(predict(objs[i-2]+objs[i-1],word,index))
                o['rangees'][page]=row
            words=tuple(normal(['okolshy','otoly','dshedy']) if convert else ('okolshy','otoly','dshedy'))
            o['trois_mots']={word:alignment((word,),index) for word in words}
            o['ordres']={}
            for order in permutations(words):
                o['ordres'][' '.join(order)]={'triplet':alignment(order,index),'paires':[
                    alignment(order[:2],index),alignment(order[1:],index)],'espacement_0a4':{
                    'premiere_paire':within_gap(order[:2],index),'seconde_paire':within_gap(order[1:],index),
                    'trois':within_gap(order,index)}}
            o['mot_suivant']=[predict(words[:1],words[1:2],index),predict(words[1:2],words[2:],index)]
            out[how+'/'+scope]=o
    save('RESULTATS.json',out)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['annoncer','verifier'])
    if p.parse_args().mode=='annoncer':dump_labels()
    else:verify()
