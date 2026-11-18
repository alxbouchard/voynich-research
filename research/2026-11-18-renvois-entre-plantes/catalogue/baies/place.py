"""Vérifier la place d'une forme qui ouvre deux lignes sur des plantes apparentées."""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'2026-11-18-dam-en-fin-de-ligne'))
from corpus_dam import aligned,corpus,metadata,segment,MODES,parse
SOURCE='f17v.2'; PAIR='f96v.8'; W='ycheey'

def adjacent(a,b):
    return a['troncon']==b['troncon'] and all(int(y)==int(x)+1 for x,y in zip(a['rangs_quatre'].split('/'),b['rangs_quatre'].split('/')))

def announce(ed,meta):
    page=SOURCE.split('.')[0]
    arr=list(aligned(ed,SOURCE,page,meta[page].get('I'),17,Counter()))
    a,b=arr[:2]
    assert a['mot']==W and 'debut' in a['positions'] and adjacent(a,b)
    return {'source':SOURCE,'ancre':W,'suite_annoncee':b['mot'],'place_annoncee':'debut'}

def test(ed,meta,forecast):
    records=[];ctrl=defaultdict(Counter)
    individual=defaultdict(Counter)
    for code,cut in MODES:
        for loc,(page,kind,_,raw) in ed[code].items():
            if kind!='P0':continue
            n=int(re.match(r'f(\d+)',page)[1])
            if n in (17,35,37,96):continue
            _,blocks=parse(raw,cut)
            for part,words in enumerate(blocks):
                for pos,w in enumerate(words):
                    if w==W:
                        stratum='herbier' if meta[page].get('I')=='H' else 'autres'
                        counter=individual[code+'/'+cut+'/'+stratum]
                        counter['total']+=1
                        counter['debut']+=part==0 and pos==0
    for loc,(page,k,*_) in ed['H'].items():
        if k!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!=k:continue
        n=int(re.match(r'f(\d+)',page)[1])
        if n in (17,35,37,96) and loc!=PAIR:continue
        rows=list(aligned(ed,loc,page,meta[page].get('I'),n,Counter()))
        for i,r in enumerate(rows):
            w=r['mot'];start='debut' in r['positions']
            if w==W:
                after=rows[i+1]['mot'] if i+1<len(rows) and adjacent(r,rows[i+1]) else None
                records.append(dict(page=page,lieu=loc,rangs=r['rangs_quatre'],suite=after,debut=start,
                                    lot='paire' if loc==PAIR else 'herbier' if meta[page].get('I')=='H' else 'autres'))
            elif segment(w)[0]=='y' and len(segment(w))>=2:
                ctrl[page]['total']+=1; ctrl[page]['debut']+=start
    for r in records:
        r['autres_en_y']=dict(ctrl[r['page']]) if r['lot']!='paire' else None
    held_out=[r for r in records if r['lot']!='paire']
    summary={}
    for group in ('herbier','autres','ensemble'):
        subset=[r for r in held_out if group=='ensemble' or r['lot']==group]
        summary[group]=dict(
            positions=len(subset),
            debuts=sum(r['debut'] for r in subset),
            debuts_attendus_selon_autres_mots_en_y=sum(r['autres_en_y']['debut']/r['autres_en_y']['total'] for r in subset),
            voisins_lisibles=sum(r['suite'] is not None for r in subset),
            voisins_identiques=sum(r['suite']==forecast['suite_annoncee'] for r in subset))
    return dict(annonce=forecast,lieux=records,lectures_individuelles=individual,bilan_hors_apprentissage=summary)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=('annoncer','ouvrir'));mode=parser.parse_args().mode
    ed,_=corpus();meta=metadata()
    f=HERE/'SUITE-ANNONCEE.json'
    if mode=='annoncer':result=announce(ed,meta)
    else:
        result=test(ed,meta,json.loads(f.read_bytes()));f=HERE/'PLACES.json'
    f.write_text(json.dumps(result,indent=1,ensure_ascii=False,sort_keys=True)+'\n')
