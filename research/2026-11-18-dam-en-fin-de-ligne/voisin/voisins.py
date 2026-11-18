"""python3 voisins.py annoncer | verifier"""
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import json
import re
import sys

ICI = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0,str(ICI.parent))
from corpus_dam import corpus, metadata, aligned, parse, WORD, MODES, segment

NOP = ('m','r','l','iin')
MODELES = NOP + ('fond',)

def meilleur(compte):
    return min(compte, key=lambda mot: (-compte[mot],mot)) if compte else None

def fini_m(w):
    return WORD.fullmatch(w) and len(segment(w)) >= 2 and segment(w)[-1] == 'm'

def cle(w, fin, sortie):
    return w[:-1] + sortie if fin and fini_m(w) else w

def candidats(editions,loc):
    vues=[parse(editions[e][loc][3], mode) for e,mode in MODES]
    if any(v[0]!=vues[0][0] for v in vues):
        return None
    troncons=[v[1][-1] for v in vues]
    if any(len(tr)<2 for tr in troncons):
        return None
    derniers=[tr[-1] for tr in troncons]
    if len(set(derniers))!=1 or not fini_m(derniers[0]):
        return None
    return derniers[0],troncons

def archive(nom, data):
    obj=json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n'
    (ICI/nom).write_bytes(gzip.compress(obj,mtime=0))

def ouvrir(nom):
    return json.loads(gzip.decompress((ICI/nom).read_bytes()))

def apprendre():
    ed,_=corpus()
    meta=metadata()
    votes={s:defaultdict(Counter) for s in NOP}
    fond=Counter()
    exemples={}
    refs=[]
    appris=Counter()
    couv=Counter()
    for lieu, (page, genre, _,raw) in ed['H'].items():
        q=meta.get(page,{}).get('Q')
        if not q or genre!='P0' or lieu not in ed['ZL'] or ed['ZL'][lieu][1]!='P0':
            continue
        if q=='T':
            masques=candidats(ed,lieu)
            if masques:
                refs.append([lieu,masques[0]])
            continue
        precedent=None
        for w in aligned(ed,lieu,page,meta[page].get('I'),page,couv):
            rangs=tuple(map(int,w['rangs_quatre'].split('/')))
            droite=w['mot']
            if precedent:
                tranche,anciens,gauche=precedent
                if tranche==w['troncon'] and all(a+1==b for a,b in zip(anciens,rangs)):
                    fin='fin' in w['positions']
                    for s in NOP:
                        votes[s][cle(droite,fin,s)][gauche]+=1
                    k=(gauche,droite)
                    if k not in exemples:
                        exemples[k]=[lieu,tranche,rangs[0]-1,rangs[0],fin]
                    if fin:
                        fond[gauche]+=1
                    appris['paires']+=1
                    if fin: appris['paires_terminales']+=1
            precedent=(w['troncon'],rangs,droite)
    previsions=[]
    for lieu,fin in refs:
        d={s:meilleur(votes[s].get(cle(fin,True,s))) for s in NOP}
        d['fond']=meilleur(fond)
        supports = {}
        for s in NOP:
            v=votes[s].get(cle(fin,True,s),{})
            prev=d[s]
            supports[s]={'voisins':sum(v.values()),'pour_premier':v.get(prev,0),'exemple_variante':exemples.get((prev,cle(fin,True,s)))}
        previsions.append({'locus':lieu,'fin':fin,'previsions':d,'appuis':supports})
    archive('ANNONCES.json.gz',{'apprentissage':appris,'fond':fond.most_common(10),'lignes':previsions})
    print('Cartes :',len(previsions),'; bigrammes :',appris)

def total(cas):
    d={}
    for s in MODELES:
        e=[a for a in cas if a['previsions'][s] is not None]
        oui=sum(a['previsions'][s]==a['reponse'] for a in e)
        d[s]={'exacts':oui,'faux':len(e)-oui,'abstentions':len(cas)-len(e),'couverts':len(e)}
    return d

def verifier():
    marques=ouvrir('ANNONCES.json.gz')
    ed,_=corpus()
    l=[]
    for a in marques['lignes']:
        fin,troncons=candidats(ed,a['locus'])
        assert a['fin']==fin
        formes=[t[-2] for t in troncons]
        a['reponse']=formes[0] if len(set(formes))==1 and WORD.fullmatch(formes[0]) else None
        l.append(a)
    vrais=[a for a in l if a['reponse'] is not None]
    commun=[a for a in vrais if all(a['previsions'][s] is not None for s in NOP)]
    d={'toutes':total(vrais),'commun':total(commun),'dam':total([a for a in vrais if a['fin'].endswith('dam')]),'dam_seul':total([a for a in vrais if a['fin']=='dam'])}
    for nom,ss in [('tous',vrais),('communs',commun)]:
        changes={}
        for s in ['r','l','iin']:
            diff=[a for a in ss if a['previsions']['m']!=a['previsions'][s]]
            changes[s]={'differentes':len(diff),
                        'gains':[a['locus'] for a in diff if a['reponse']==a['previsions'][s]],
                        'pertes':[a['locus'] for a in diff if a['reponse']==a['previsions']['m']]}
        d['comparaison_'+nom]=changes
    choix=[]
    for a in vrais:
        for s in ['r','l','iin']:
            p=a['previsions'][s]
            ex=a['appuis'][s]['exemple_variante']
            if ex and p==a['reponse'] and p!=a['previsions']['m'] and p not in ('kedy','qoky'):
                choix.append({'cible':a['locus'],'predit':p,'fin':a['fin'],'remplacement':s,'source':ex})
    d.update({'candidats':len(l),'cotables':len(vrais),'commun_n':len(commun),'exemples_eligibles':choix})
    archive('VERIFICATION.json.gz',{'scores':d,'lignes':l})
    print(json.dumps(d,ensure_ascii=False,indent=1))

if __name__=='__main__':
    {'annoncer':apprendre,'verifier':verifier}[sys.argv[1]]()
