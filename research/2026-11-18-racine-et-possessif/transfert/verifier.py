"""Comparer deux expressions à distance de ligne fixe, après exclusion de f11 et f15."""
import csv
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-opcheor-paralleles/variantes'))
from compter import corpus, runs

MOTIFS = {'depart': ('chol','cthy'), 'arrivee': ('daiin','cthy'),
          'depart_dy':('chol','cthy','dy'), 'arrivee_dy':('daiin','cthy','dy')}
MODES = [(e,c) for e in ('H','ZL') for c in ('joints','separes')]

def positions(raw,cut):
    result={k:[] for k in MOTIFS}
    for run in runs(re.sub(r'\{[^}]*\}', '?',raw),cut):
        words=tuple(w for _,w in run)
        for k,expression in MOTIFS.items():
            result[k].extend(rank for i,(rank,_) in enumerate(run) if words[i:i+len(expression)]==expression)
    return result

def line_key(s):
    page,rank=s.split('.')
    match=re.match(r'f(\d+)([rv])(\d*)$',page)
    if not match:
        return (999,page,0,int(rank))
    return (int(match[1]),match[2],int(match[3] or 0),int(rank))

def paragraph_ok(start,dist,books,p0):
    page,num=start.split('.')
    for offset in range(dist+1):
        l=f'{page}.{int(num)+offset}'
        if l not in p0:
            return False
        for book in books.values():
            raw=book[l][3]
            if (offset<dist and '<$>' in raw) or (offset and '<%>' in raw):
                return False
    return True

def relative(locus,delta):
    page,i=locus.split('.')
    return f'{page}.{int(i)+delta}'

def domain(page, sections):
    if re.fullmatch(r'f(?:11|15)[rv]\d*', page):
        return 'selection'
    return 'herbier' if sections[page]=='H' else 'autres'

def measure(pool, signs, books, start, target, delta):
    bases=sorted(pool & signs[start],key=line_key)
    exposed=[l for l in bases if relative(l,delta) in pool]
    possible=[l for l in pool if relative(l,delta) in pool]
    others=set(possible)-set(bases)
    hits=[l for l in exposed if relative(l,delta) in signs[target]]
    return {'departs':len(bases),'cible_evaluable':len(exposed),'avec_motif':hits,
            'sans_ligne_cible':[l for l in bases if l not in exposed],
            'meme_paragraphe':sum(paragraph_ok(l,delta,books,pool) for l in exposed),
            'succes_meme_paragraphe':[l for l in hits if paragraph_ok(l,delta,books,pool)],
            'autres_fenetres':len(others),'avec_cible_autres_fenetres':sum(relative(l,delta) in signs[target] for l in others)}

def main():
    books,sections=corpus()
    places={l for l in set.intersection(*(set(v) for v in books.values())) if all(b[l][1]=='P0' for b in books.values())}
    signs={k:set() for k in MOTIFS}
    details={}
    for l in sorted(places,key=line_key):
        modes={e+'/'+c:positions(books[e][l][3],c) for e,c in MODES}
        if not any(any(q.values()) for q in modes.values()):
            continue
        agreed=[]
        for k in MOTIFS:
            if all(v[k] for v in modes.values()):
                signs[k].add(l);agreed.append(k)
        details[l]={'accord':agreed,'positions':modes,'lignes':{e:b[l][3] for e,b in books.items()}}
    assert positions('chol<->cthy.daiin.?.cthy.chol,{cthy}','joints')['depart']==[]
    assert positions('chol.cthy.dy','separes')['depart_dy']==[1]
    summary={}
    index=[]
    for group in ('selection','herbier','autres'):
        pool={l for l in places if domain(l.split('.')[0],sections)==group}
        by_mode={}
        for e,c in MODES:
            by_mode[e+'/'+c]={k:sum(bool(r['positions'][e+'/'+c][k]) for l,r in details.items() if l in pool) for k in MOTIFS}
        stat={'lieux_P0':len(pool),'panneaux':len({l.split('.')[0] for l in pool}),
              'signatures_par_lecture':by_mode,
              'motifs':{k:sorted(pool&s,key=line_key) for k,s in signs.items()},
              'distances':{},'inversion_plus_deux':measure(pool,signs,books,'arrivee','depart',2)}
        for delta in range(1,7):
            stat['distances'][delta]=measure(pool,signs,books,'depart','arrivee',delta)
        for l in stat['motifs']['depart']:
            target=relative(l,2)
            index.append([group,l,target,int(target in pool),int(target in signs['arrivee']),int(l in signs['depart_dy']),
                          int(target in signs['arrivee_dy']),','.join(str(d) for d in range(1,7) if relative(l,d) in signs['arrivee']),
                          int(paragraph_ok(l,2,books,pool))])
        summary[group]=stat
    with (HERE/'departs.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n')
        w.writerow(['groupe','depart','cible_plus_deux','P0_aux_deux_editions','arrivee_confirmee','dy_apres_depart',
                   'dy_apres_arrivee_a_plus_deux','distances_arrivees_de_1_a_6','meme_paragraphe_plus_deux']);w.writerows(index)
    (HERE/'resultats.json').write_text(json.dumps({'resume':summary,'lignes_au_moins_une_lecture':details},ensure_ascii=False,indent=1)+'\n')
    for group,r in summary.items():
        print(group,r['lieux_P0'],r['panneaux'],{k:len(v) for k,v in r['motifs'].items()})
        for d,m in r['distances'].items():
            print(d,m['cible_evaluable'],m['avec_motif'],m['autres_fenetres'],m['avec_cible_autres_fenetres'])
        print('inverse', r['inversion_plus_deux'])
if __name__=='__main__':main()
