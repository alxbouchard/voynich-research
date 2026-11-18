"""python3 -B tester.py /chemin/vers/phi1011.phi001.lascivaroma-lat1.xml"""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import gzip
import json
import re
import sys
from lxml import etree

ICI=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ICI.parent))
from corpus_dam import aligned, corpus, segment

SIGNES='oldams'
ANCRES={'oldam','saldam','doldam'}
TEI={'t':'http://www.tei-c.org/ns/1.0'}

def fenetres(suite):
    for n in (1,2,3):
        for i in range(len(suite)-n+1):
            yield i,tuple(suite[i:i+n])

def xml_texte(p):
    morceaux=[p.text or '']
    for el in p:
        typ=etree.QName(el).localname
        morceaux.append(' ' if typ in {'lb','pb'} else '¤')
        morceaux.append(el.tail or '')
    return ''.join(morceaux)

def latin(source):
    root=etree.parse(str(source),etree.XMLParser(resolve_entities=True,no_network=True))
    refs=defaultdict(list)
    positions=Counter()
    paragraphes=0
    for div in root.xpath('//t:body/t:div/t:div',namespaces=TEI):
        for ip,p in enumerate(div.xpath('t:p',namespaces=TEI),1):
            paragraphes+=1
            blocs=[]
            bloc=[]
            for t in re.findall(r"[\w¤]+(?:['’ʻ\-‐][\w¤]+)*|[^\w\s]",xml_texte(p)):
                if re.fullmatch('[a-zA-Z]+',t) and not re.fullmatch('[IVXLCDM]+',t):
                    bloc.append(t.lower())
                elif bloc:
                    blocs.append(bloc)
                    bloc=[]
            if bloc: blocs.append(bloc)
            for ib,bl in enumerate(blocs,1):
                for i,w in fenetres(bl):
                    refs[w].append((div.get('n'),ip,ib,i+1))
                    positions[len(w)]+=1
    return refs,positions,paragraphes

def voynich():
    ed,sections=corpus()
    cov=Counter()
    avant=Counter()
    fen=defaultdict(list)
    runs=[]
    def garder(loc,bloc):
        if not bloc:return
        mots=[w for _,w in bloc]
        runs.append((loc,len(mots),mots))
        for i,f in fenetres(mots):
            fen[f].append((loc,bloc[i][0]))
    for loc,(page,kind,_,_) in ed['H'].items():
        if kind!='P0' or loc not in ed['ZL'] or ed['ZL'][loc][1]!='P0': continue
        last=None
        bloc=[]
        for row in aligned(ed,loc,page,sections.get(page),page,cov):
            mot=row['mot']
            rangs=tuple(map(int,row['rangs_quatre'].split('/')))
            contigu=last and last[0]==row['troncon'] and all(a+1==b for a,b in zip(last[1],rangs))
            valide=set(segment(mot))<=set(SIGNES)
            if valide: avant[mot]+=1
            if not contigu or not valide or mot in ANCRES:
                garder(loc,bloc)
                bloc=[]
            if valide and mot not in ANCRES:
                bloc.append((f"{row['troncon']}/{row['rang_troncon_IT']}",mot))
            last=row['troncon'],rangs
        garder(loc,bloc)
    return fen,avant,cov,runs

def decoder(mot,table):
    return ''.join(table[c] for c in segment(mot))

def marques(table,fens,refs):
    lectures={w[0]:decoder(w[0],table) for w in fens if len(w)==1}
    nb=Counter()
    distincts=Counter()
    matches=[]
    for fen,lieux in fens.items():
        lu=tuple(lectures[x] for x in fen)
        if lu in refs:
            n=len(fen)
            nb[n]+=len(lieux)
            distincts[n]+=1
            matches.append((n,fen,lu,lieux,refs[lu]))
    return tuple(nb[n] for n in (1,2,3)),tuple(distincts[n] for n in (1,2,3)),matches

def positif(refs):
    for trigramme in refs:
        if len(trigramme)!=3 or len(set(trigramme))!=3 or min(map(len,trigramme))<2: continue
        lettres=sorted(set(''.join(trigramme)))
        if len(lettres)>6:continue
        table=dict(zip(SIGNES,lettres))
        enc={l:s for s,l in table.items()}
        fictif=[''.join(enc[l] for l in mot) for mot in trigramme]
        if set(fictif)&ANCRES:continue
        def cases(troncons):
            f=defaultdict(list)
            for ib,troncon in enumerate(troncons):
                for i,k in fenetres(troncon):f[k].append((ib,i))
            return f
        f=cases([fictif])
        exact=marques(table,f,refs)
        separe=marques(table,cases([fictif[:2],fictif[2:]]),refs)
        assert exact[0]==(3,2,1) and separe[0][2]==0
        assert any(n==3 and lu==trigramme for n,_,lu,_,_ in exact[2])
        return dict(latin=trigramme,recodage=fictif,lieu=refs[trigramme][0],table=table,sans_coupure=exact[0],avec_coupure=separe[0])
    raise ValueError('Aucun témoin positif admissible')

def essais_meme_cle(table, refs):
    # Diagnostic après le test principal : quelles suites le texte latin offre-t-il
    # à cette clé si chaque mot mesure au moins deux lettres ?
    @lru_cache(maxsize=None)
    def encoder(w):
        if not w:return ''
        for signe in SIGNES:
            lettre=table[signe]
            if w.startswith(lettre):
                fin=encoder(w[len(lettre):])
                if fin is not None:return signe+fin
        return None

    possibles=[]
    for k,lieux in refs.items():
        if len(k)<2 or min(map(len,k))<2: continue
        eva=tuple(encoder(w) for w in k)
        if None in eva or set(eva)&ANCRES: continue
        mini={f:[(1,i+1)] for i,f in fenetres(eva)}
        nb,_,matches=marques(table,mini,refs)
        assert any(n==len(k) and lu==k for n,_,lu,_,_ in matches)
        possibles.append(dict(latin=k,eva=eva,lieu=lieux[0]))
    return possibles

def main(source):
    modeles_path=ICI.parent/'lecture/MODELES.json.gz'
    modeles=[d for d in json.loads(gzip.decompress(modeles_path.read_bytes())) if d['corpus']=='Celse' and d['largeur']==2 and d['injective']]
    assert len(modeles)==2
    refs,lat_n,paragraphes=latin(source)
    fens,avant,cov,runs=voynich()
    sortkey={f:i for i,f in enumerate(fens)}
    lieux_n=Counter()
    for f,v in fens.items():lieux_n[len(f)]+=len(v)
    controles=positif(refs)
    res=dict(empreinte_xml=sha256(source.read_bytes()).hexdigest(),empreinte_modeles=sha256(modeles_path.read_bytes()).hexdigest(),
             latin=dict(positions=lat_n,distincts=Counter(map(len,refs)),paragraphes=paragraphes),
             voynich=dict(couverture=cov,positions=lieux_n,distincts=Counter(map(len,fens)),avant_exclusion=sum(avant.values()),ancres={a:avant[a] for a in sorted(ANCRES)},longueur_maximale=max(x[1] for x in runs)),
             positif=controles,modeles=[],permutations=[])
    familles=[]
    for m in modeles:
        table=m['cle']
        assert set(table)==set(SIGNES) and len(set(table.values()))==6
        vals=tuple(table[s] for s in SIGNES)
        n,distincts,matches=marques(table,fens,refs)
        distribution=Counter()
        combinaisons=set(permutations(vals))
        for perm in sorted(combinaisons):
            k=dict(zip(SIGNES,perm))
            score,_,_=marques(k,fens,refs)
            distribution[score[1:]]+=1
        familles.append(combinaisons)
        exemples=[]
        for taille,fen,lu,lieux,latins in sorted(matches,key=lambda x:(-x[0],sortkey[x[1]])):
            exemples.append(dict(n=taille,eva=fen,latin=lu,lieux=lieux,texte=latins))
        res['modeles'].append(dict(ancres=m['mots'],cle=table,occurrences=n,types_eva=distincts,correspondances=exemples,diagnostic_recodage_meme_cle=essais_meme_cle(table,refs),meilleur=exemples[0] if exemples else None))
        res['permutations'].append(dict(n=len(combinaisons),scores=[[a,b,c] for (a,b),c in sorted(distribution.items())],egales_ou_meilleures=[sum(v for k,v in distribution.items() if k[j]>=n[j+1]) for j in range(2)]))
    res['union_tables']=len(familles[0]|familles[1])
    res['intersection_tables']=len(familles[0]&familles[1])
    all_data={'resultats':res,'fenetres_eva':[[f,lieux] for f,lieux in fens.items()]}
    (ICI/'RESULTATS.json.gz').write_bytes(gzip.compress(json.dumps(all_data,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
    for m in res['modeles']:
        print(m['ancres'],m['occurrences'],m['types_eva'],[(x['n'],x['eva'],x['latin'],x['lieux'][0],x['texte'][0]) for x in m['correspondances'][:4]])
    print(res['voynich'],res['latin'],controles)
    print(res['permutations'])

if __name__=='__main__':main(Path(sys.argv[1]))
