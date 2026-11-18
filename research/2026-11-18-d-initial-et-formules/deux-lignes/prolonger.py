"""Tester la continuité d'un début de ligne sur des feuillets physiques distincts."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import json
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from suites import aligned, corpus, metadata, segment

SOURCE,CIBLE="f108r.20","f116r.17"
def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=1,sort_keys=True,ensure_ascii=False)+'\n')

def line(ed,meta,loc):
    page=loc.split('.')[0]
    words=[]
    for r in aligned(ed,loc,page,meta[page].get("I"),page,Counter()):
        n=len(words)+1
        if r['troncon']!=1 or any(int(x)!=n for x in r['rangs_quatre'].split('/')):break
        words.append(r['mot'])
        if len(words)==5:break
    return words

def delta(a,b):
    u,v=map(segment,(a,b))
    if u==v:return "identiques"
    if len(u)>len(v):u,v=v,u
    if len(v)==len(u)+1 and any(k=='d' and v[:i]+v[i+1:]==u for i,k in enumerate(v)):
        return "un_d"
    return "autre"

def announce():
    ed,_=corpus();meta=metadata()
    a=line(ed,meta,SOURCE)
    assert a[:3]==['dain','chey','qokeedy']
    write('ANNONCE.json',{'source':SOURCE,'cible':CIBLE,'debut_source':a,'positions':{'4':a[3] if len(a)>3 else None,'5':a[4] if len(a)>4 else None}})

def verify():
    ed,_=corpus();meta=metadata()
    announced=json.loads((HERE/'ANNONCE.json').read_bytes())
    seen=defaultdict(list); stats=defaultdict(Counter); rare=[]
    for loc,(page,kind,_,_) in ed['H'].items():
        if kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0':continue
        words=line(ed,meta,loc)
        if len(words)>=3:
            seen[tuple(words[:2])].append((loc,re.match(r'f\d+',page)[0],meta[page].get('Q'),words))
    for group in seen.values():
        for (li,lf,lq,l),(ri,rf,rq,r) in combinations(group,2):
            if lf==rf:continue
            typ=delta(l[2],r[2])
            for pool,keep in [('tout',True),('dernier',lq==rq=='T'),('tout_sans_paire',set((li,ri))!={SOURCE,CIBLE}),
                              ('dernier_sans_paire',lq==rq=='T' and set((li,ri))!={SOURCE,CIBLE})]:
                if not keep:continue
                s=stats[pool+'/'+typ];s['couples']+=1
                if min(len(l),len(r))>=4:
                    s['quatriemes_lisibles']+=1;s['quatriemes_identiques']+=l[3]==r[3]
            if typ=='un_d':rare.append([li,ri,l,r])
    target=line(ed,meta,CIBLE)
    assert target[:3]==['dain','chey','qokeey']
    write('VERIFICATION.json',{'annonce':announced,'cible':target,'couples':stats,'cas_un_d':rare})
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['annoncer','verifier'])
    announce() if p.parse_args().mode=='annoncer' else verify()
