"""Transfert des six tables de la double rencontre dans le reste de l’herbier."""
from collections import Counter,defaultdict
from functools import reduce
from operator import and_
import json
import re
from chercher import HERE, corpus, macer, runs, save, segment

SEEDS={'chol':'radix','cthy':'eius','daiin':'foliis'}
LEAVES = (11,15)

def grams(sequence,n):
    return zip(*(sequence[i:] for i in range(n)))

def field_summary(hits):
    return {'types':len(hits),'occurrences':sum(hits.values())}

def books():
    chapters=macer();fragments={n:defaultdict(list) for n in range(1,4)};nextwords=[]
    for title,lines in chapters.items():
        for n,verse in lines.items():
            for a,b,c in grams(verse,3):
                if (a,b)==('foliis','eius'):
                    nextwords.append({'notice':title,'vers':n,'mot':c})
        full=[w for ws in lines.values() for w in ws]
        for n,index in fragments.items():
            for g in set(grams(full,n)):
                index[g].append(title)
    other=Counter(w for title,ls in chapters.items() if title!='Chelidonia' for words in ls.values() for w in words)
    return fragments,other,nextwords

def manuscript():
    editions,sections=corpus()
    inventory={k:Counter() for k in range(1,4)}
    places={k:defaultdict(list) for k in range(1,4)}
    totals=defaultdict(Counter);pages=set()
    for loc,(p,kind,_,_) in editions['ZL'].items():
        if kind!='P0' or sections.get(p)!='H' or int(re.match(r'f(\d+)',p)[1]) in LEAVES:
            continue
        if loc not in editions['H'] or editions['H'][loc][1]!='P0':
            continue
        pages.add(p);versions=[]
        for ed,rows in editions.items():
            raw=re.sub(r'\{[^}]*\}','?',rows[loc][3])
            for cut in ('joints','separes'):
                version={n:Counter() for n in inventory}
                for span in runs(raw,cut):
                    words=[w for i,w in span]
                    for n,cnt in version.items():
                        cnt.update(grams(words,n))
                words=version[1]
                total=totals[ed+'/'+cut];total['mots']+=sum(words.values())
                total['lignes']+=1
                for w in SEEDS:total[w]+=words[w,]
                versions.append(version)
        for n,overall in inventory.items():
            shared=reduce(and_,(v[n] for v in versions))
            overall.update(shared)
            for words in shared: places[n][words].append(loc)
    return inventory,places,totals,pages

def main():
    pre=json.loads((HERE/'voynich.json').read_bytes())['modeles']['2']['details']
    tables=[r['tables_possibles'] for r in pre if r['B']=='daiin' and r['A']=='chol' and r['M']=='cthy']
    assert len(tables)==2 and len(tables[0])==6 and tables[0]==tables[1]
    latin,other,nextwords=books()
    inventory,places,totals,pages=manuscript()
    anchor={'formes_edition_sans_chelidoine':{w:other[w] for w in SEEDS.values()},
            'mots_edition_sans_chelidoine':sum(other.values()),'faces_voynich':len(pages),'versions':totals,
            'minimum_stable':{w:inventory[1][w,] for w in SEEDS},'mots_communs':sum(inventory[1].values())}
    tested=[]
    for key in tables[0]:
        dy=''.join(key[s] for s in segment('dy'))
        decoder={w:''.join(key[s] for s in segment(w)) for (w,) in inventory[1] if len(segment(w))>=2 and all(s in key for s in segment(w))}
        res={}
        for n in (2,3):
            readable=Counter({ws:m for ws,m in inventory[n].items() if all(w in decoder for w in ws)})
            matches=[]
            for ws,m in readable.items():
                clear=tuple(decoder[w] for w in ws)
                if clear in latin[n]:
                    matches.append({'eva':ws,'lecture':clear,'nombre':m,'lignes':places[n][ws],
                                    'notices_du_macer':latin[n][clear]})
            res[n]={'lisibles':field_summary(readable),'types_dans_macer':len(matches),
                    'occurrences_dans_macer_somme_cote_voynich':sum(r['nombre'] for r in matches),'details':matches}
        tested.append({'cle':key,'dy':dy,'dy_present_macer':(dy,) in latin[1],
                       'dy_apres_foliis_eius':dy in [r['mot'] for r in nextwords],'transfert':res})
    keys=tables[0]
    assert {key['cth'] for key in keys}=={'ei'} and {key['y'] for key in keys}=={'us'}
    examples={loc:verse for ls in macer().values() for loc,verse in ls.items() if 'ei' in verse}
    short={'toutes_lectures_cth':['ei'],'toutes_lectures_cthy':['eius'],
           'formes_foliis_ei_dans_le_macer':latin[2].get(('foliis','ei'),[]),'vers_du_macer_avec_ei':examples,
           'lieux_communs_cth':places[1].get(('cth',),[]),
           'lieux_communs_daiin_cth':places[2].get(('daiin','cth'),[])}
    out={'variante_f10r':short,'comparaison_frequences':anchor,'mots_apres_foliis_eius_edition':nextwords,'tables':tested}
    save('suite.json',out)
    print(anchor,nextwords)
    for r in tested:
        print(r['dy'],r['dy_present_macer'],[(n,v['lisibles'],v['types_dans_macer'],v['occurrences_dans_macer_somme_cote_voynich']) for n,v in r['transfert'].items()])

if __name__=='__main__':main()
