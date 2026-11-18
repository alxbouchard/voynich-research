"""Chercher une table commune à deux encadrements, puis évaluer cinq voisins réservés."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]/'phrase'))
from lecture import adjacent, code, extend, load, read_books, save, texts
from croiser import corpus, MODES as SPACE_MODES
from corpus_dam import parse

FORMS = ('qokol','daiin','qokchol','dar')
MODES = ('EVA','ii','aiin')
LANG = {'Macer':'latin','Celse':'latin','Mayence1485':'allemand','RIDGES':'allemand',
        'regime':'français','viandier':'français','martino':'italien'}


def index(books):
    """Ranger les encadrements et les continuations à leur place dans chaque ouvrage."""
    patterns = []
    tails = defaultdict(list)
    for name, body in books.items():
        for loc, line in body.items():
            for i,(a,b,c) in enumerate(zip(line,line[1:],line[2:])):
                if a==b:
                    continue
                if a!=c:
                    tails[name,a,b].append([loc,i+1,c])
                    continue
                patterns.append(dict(ouvrage=name,lieu=loc,rang=i+1,exterieur=a,centre=b,
                                     gauche=line[i-1] if i else None,
                                     droite=line[i+3] if i+3<len(line) else None))
    return patterns,tails


@lru_cache(maxsize=None)
def maps(shape, word, mute):
    spoken = tuple(u for u in shape if u!=mute)
    return tuple(extend(spoken,word,2,{}))


def candidates(shapes, patterns, muet):
    a,b=shapes
    results=[]
    for i,r in enumerate(patterns):
        for ka in maps(a,r['exterieur'],muet):
            core=tuple(x for x in b if x!=muet)
            for key in extend(core,r['centre'],2,ka):
                results.append((i,key))
    return results


def combine(left,right):
    new={**left,**right}
    return new if (len(set(new.values()))==len(new)
                   and all(new[k]==v for k,v in left.items())) else None


def search(patterns, tails, forms=FORMS, languages=LANG):
    metrics={}
    results=[]
    for mode in MODES:
        shapes=[code(w,mode) for w in forms]
        signs=set(sum(shapes,()))
        for mute in [None,*sorted(signs)]:
            left = candidates(shapes[:2],patterns,mute)
            right = candidates(shapes[2:],patterns,mute)
            how=mode+'/'+(mute or 'aucun')
            book_counts={b:{'lieux_gauche':0,'tables_gauche':0,'lieux_droite':0,'tables_droite':0,
                            'couples_meme_ouvrage':0,'tables_meme_ouvrage':0}
                         for b in languages}
            for side, hits in [('gauche',left),('droite',right)]:
                counts=Counter(patterns[i]['ouvrage'] for i,_ in hits)
                places=Counter(patterns[i]['ouvrage'] for i in {i for i,_ in hits})
                for name in counts:
                    book_counts[name]['lieux_'+side]=places[name]
                    book_counts[name]['tables_'+side]=counts[name]
            shared=sorted((set(shapes[0]+shapes[1])&set(shapes[2]+shapes[3]))-{mute})
            bucket=defaultdict(list)
            for j,kr in right:
                bucket[tuple(kr[s] for s in shared)].append((j,kr))
            pairs=defaultdict(set)
            cross=0
            for i,kl in left:
                left_book=patterns[i]['ouvrage']
                for j,kr in bucket[tuple(kl[s] for s in shared)]:
                    right_book=patterns[j]['ouvrage']
                    if i==j or languages[left_book]!=languages[right_book]:
                        continue
                    key=combine(kl,kr)
                    if key is None:
                        continue
                    if mute:
                        key[mute]=''
                    if left_book==right_book:
                        book_counts[left_book]['tables_meme_ouvrage']+=1
                        pairs[left_book].add((i,j))
                    else:
                        cross+=1
                    places=[patterns[i],patterns[j]]
                    words=[p[s] for p in places for s in ('gauche','droite')]
                    extra=tails[right_book,patterns[j]['exterieur'],patterns[j]['centre']]
                    results.append(dict(mode=mode,muet=mute,lettres_max=max(map(len,key.values())),
                                        indice_gauche=i,indice_droite=j,table=key,voisins_annonces=words,
                                        suites_hors_encadrement=extra,ouvrages_distincts=left_book!=right_book))
            for name,seen in pairs.items():
                book_counts[name]['couples_meme_ouvrage']=len(seen)
            metrics[how]=dict(ouvrages=book_counts,tables_entre_ouvrages=cross)
    return dict(conventions=metrics,candidats=patterns,solutions=results)


def opened():
    plants=texts('plantes',True)
    neighbors=[]
    for page,loc,head,center in [('f18v','f18v.7',*FORMS[:2]),('f23r','f23r.7',*FORMS[2:])]:
        line=[r for r in plants[page] if r[1]==loc]
        found=[j for j in range(len(line)-2) if [x[0] for x in line[j:j+3]]==[head,center,head]
               and adjacent(line[j],line[j+1]) and adjacent(line[j+1],line[j+2])]
        i,=found
        neighbors.extend([line[i-1][0] if i and adjacent(line[i-1],line[i]) else None,
                          line[i+3][0] if i+3<len(line) and adjacent(line[i+2],line[i+3]) else None])
    line=[r for r in plants['f14r'] if r[1]=='f14r.5']
    i,=[j for j in range(len(line)-1) if [line[j][0],line[j+1][0]]==list(FORMS[2:])
        and adjacent(line[j],line[j+1])]
    third=line[i+2][0] if i+2<len(line) and adjacent(line[i+1],line[i+2]) else None
    readings={}
    editions,_=corpus()
    for edition,spaces in SPACE_MODES:
        _,parts=parse(editions[edition]['f14r.5'][3],spaces)
        candidates=[block[j+2] for block in parts for j in range(len(block)-2)
                    if tuple(block[j:j+2])==FORMS[2:]]
        candidate,=candidates
        readings[edition+'/'+spaces]=candidate
    return neighbors,third,readings



def check(cipher,word,mode,key):
    if cipher is None or word is None:
        return 'hors_limite'
    parts=code(cipher,mode)
    if not all(p in key for p in parts):
        return 'signes_sans_valeur'
    return 'exact' if ''.join(key[p] for p in parts)==word else 'différent'


def verify(ann,neighbors,third,readings=None):
    tests=[]
    for i,sol in enumerate(ann['solutions']):
        mode,key=sol['mode'],sol['table']
        sides=[check(g,w,mode,key) for g,w in zip(neighbors,sol['voisins_annonces'])]
        extras=[dict(lieu=loc,rang=pos,suite=w,etat=check(third,w,mode,key),
                    editions={e:check(v,w,mode,key) for e,v in (readings or {}).items()})
                for loc,pos,w in sol['suites_hors_encadrement']]
        tests.append(dict(solution=i,voisins=sides,troisieme=extras))
    return dict(groupes_reserves=neighbors,suite_f14r=third,lectures_f14r=readings,tests=tests)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('annoncer','ouvrir'))
    parser.add_argument('sources',nargs='*',type=Path)
    args=parser.parse_args()
    predictions=HERE/'TABLES.json.gz'
    if args.action=='annoncer':
        if len(args.sources)!=3:
            parser.error('Fournir le XML de Celse, le HTML du Viandier et celui de Martino.')
        external={p.name:sha256(p.read_bytes()).hexdigest() for p in args.sources}
        old=load(HERE.parents[1]/'phrase/INTERPRETATIONS.json.gz')['sha256']
        assert sorted(external.values())==sorted(old.values())
        books=read_books(*args.sources)
        pats,tails=index(books)
        ann=search(pats,tails)
        ann['sha256_sources_externes']=external
        ann['effectifs']={n:dict(passages=len(body),mots=sum(map(len,body.values())),
                      fenetres=sum(max(0,len(line)-2) for line in body.values()),
                      encadrements=sum(p['ouvrage']==n for p in pats)) for n,body in books.items()}
        save(predictions,ann)
    else:
        save(HERE/'OUVERTURE.json.gz',verify(load(predictions),*opened()))
