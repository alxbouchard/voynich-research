"""Recherche conditionnelle et révélation séparée. Le résultat TEXTES ne sert pas à sélectionner."""
from pathlib import Path
import json, re, sys
from collections import defaultdict, Counter
D = Path(__file__).resolve().parent
sys.path.insert(0,str(D.parents[1]/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import corpus, sequence, units

def order(loc):
    number, side, panel, line = re.fullmatch(r'f(\d+)([rv])(\d*)\.(\d+)',loc).groups()
    return int(number),side,int(panel or 0),int(line)

def parse(table, cut='joints'):
    rows={}
    for loc, row in table.items():
        if row[1]!='P0' or not re.fullmatch(r'f\d+[rv]\d*\.\d+',loc): continue
        seq=sequence(row[3],cut)
        rows[loc]=seq
    return rows

def options(seq):
    left=[]
    for i,(group,w) in enumerate(seq):
        if i and seq[i-1][0]!=group: left=[]
        if re.fullmatch('[a-z]+',w):
            u=units(w,False)
            if len(u)>=2:
                base=''.join(u[:-1])
                if base=='daii' or base.endswith('da'):
                    yield i,base,u[-1],tuple(left)
            left.append(w)
        else: left=[]

def shared(a,b):
    n=0
    for s,t in zip(reversed(a),reversed(b)):
        if s!=t: break
        n+=1
    return n

def save(name,value):
    (D/name).write_text(json.dumps(value,ensure_ascii=False,indent=1)+'\n')

def make(rows):
    inside=defaultdict(list)
    margins=[]
    for loc,seq in rows.items():
        if order(loc)[0]>74 or loc.startswith('f55r.'): continue
        for i,base,last,left in options(seq):
            if not left: continue
            x=(loc,i,left)
            if i<len(seq)-1 and last==('n' if base=='daii' else 'r'):
                inside[base,left[-1]].append(x)
            elif i==len(seq)-1 and last=='m':
                margins.append((base,x))
    pairs=[]
    for base,(eloc,ei,el) in margins:
        for iloc,ii,il in inside[base,el[-1]]:
            if iloc==eloc and ii==ei: continue
            length=shared(el,il)
            pairs.append((base!='daii',-length,eloc.split('.')[0]!=iloc.split('.')[0],
                          abs(order(eloc)[0]-order(iloc)[0]),order(eloc),order(iloc),
                          {'base':base,'fin':[eloc,ei+1],'interieur':[iloc,ii+1],'contexte':el[-length:]}))
    pairs.sort(key=lambda p:p[:-1])
    if pairs: print('Paire de découverte',pairs[0][-1])
    predicted=[]
    for loc,seq in rows.items():
        if order(loc)[0]<75: continue
        for i,base,_hidden,left in options(seq):
            if i!=len(seq)-1 or not left: continue
            c=sorted([(-shared(left,il),order(iloc),ii,iloc) for iloc,ii,il in inside[base,left[-1]]])
            if not c: continue
            negn,_,ii,loc0=c[0]
            predicted.append({'lieu':loc,'base':base,'contexte':left[negn:],
                              'source_interieure':[loc0,ii+1],'attendu':'m','temoin':'n' if base=='daii' else 'r'})
    predicted.sort(key=lambda p:(p['base']!='daii',-len(p['contexte']),order(p['lieu'])))
    out={'paire':pairs[0][-1] if pairs else None,'nb_paires_daii':sum(not p[0] for p in pairs),
         'nb_paires_da':sum(p[0] for p in pairs),'predictions':predicted}
    save('ANNONCES.json',out); print('Première cible',predicted[:1],'Nombre',len(predicted))

def reveal(editions):
    data=json.loads((D/'ANNONCES.json').read_text())
    results=[]
    for p in data['predictions']:
        views={}
        strict=[]
        for ed, table in editions.items():
            raw=table.get(p['lieu'])
            views[ed]=[]
            for cut in ('joints','separes'):
                seq=sequence(raw[3],cut) if raw else []
                src=table.get(p['source_interieure'][0])
                interior=sequence(src[3],cut) if src else []
                w=seq[-1][1] if seq else None
                views[ed].append(w)
                # La base et les mots précédents doivent eux aussi survivre à l'édition.
                hits=[(i,b,l,list(cx)) for i,b,l,cx in options(seq) if i==len(seq)-1 and b==p['base']
                      and list(cx[-len(p['contexte']):])==p['contexte']]
                src_hits=[i for i,b,l,cx in options(interior) if i<len(interior)-1 and b==p['base']
                          and l==p['temoin'] and list(cx[-len(p['contexte']):])==p['contexte']]
                strict.append(bool(hits and src_hits))
        results.append({**p,'lectures_derniere':views,'contexte_et_base_dans_les_4_lectures':all(strict)})
    comparisons={}
    for ed,table in editions.items():
        entries=[]
        for loc,seq in parse(table).items():
            for i,base,last,left in options(seq):
                if base=='olkarda': entries.append([loc,i+1,left[-2:],base+last,i==len(seq)-1])
        comparisons[ed]=entries
    save('LECTURES.json',{'reserve':results,'autres_olkarda':comparisons})
    for ed in editions:
        print(ed, Counter((r['lectures_derniere'][ed][0] or '?')[-1] for r in results))
    print('f55',comparisons)

if __name__=='__main__':
    editions,_=corpus()
    if sys.argv[1]=='annoncer': make(parse(next(iter(editions.values()))))
    elif sys.argv[1]=='reveler': reveal(editions)
