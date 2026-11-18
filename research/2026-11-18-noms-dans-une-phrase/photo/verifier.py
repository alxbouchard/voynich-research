"""Relecture des deux contextes et de l'épreuve géométrique à partir des deux éditions IVTFF."""
from pathlib import Path
from hashlib import sha256
import json
import re

ICI=Path(__file__).resolve().parent
DEPOT=ICI.parents[2]
RANGEES=DEPOT/'research/2026-11-18-ordre-des-noms/panneaux/RANGEES.json'
CIBLES={'f89r2.22':('opcheor','opcheol'),'f100v.16':('okeor','okeol')}

def groupes(raw,sep):
    a=re.sub(r'<[-~]>|<![^>]*(?:gap|jump|space)[^>]*>','.|.',raw,flags=re.I)
    a=re.sub(r'<![^>]*>|<[%$]>|!', '',a)
    return [w for w in a.strip().replace(',', '.' if sep else '').split('.') if w]


def lire(path):
    rows={}
    for l in path.read_text().splitlines():
        k=re.match(r'^<([^.,>]+)\.([0-9]+),(.)([^>]+)>\s*(.*?)\s*$',l)
        if not k or k[3]=='!':continue
        rows[k[1]+'.'+k[2]]=(k[3],k[4],k[5])
    return rows


def unites(w):
    return re.findall(r'c[ktpf]h|[cs]h|.',w)


def extraire():
    paths={'H':DEPOT/'voynich_20261028/data/IT2a-n.txt','ZL':DEPOT/'voynich_20261028/data/ZL3b-n.txt'}
    d={ed:lire(p) for ed,p in paths.items()}
    rows=json.loads(RANGEES.read_text())
    familles={'sources':[],'cible':[],'autres_places_cible':[],'complement':[]}
    for row in rows:
        page=row['page'];rang=row['rang'];places=[s for s in row['positions'] if len(s['loci'])==1]
        if len(places)<4:continue
        last=places[-1];n=last['loci'][0];suite=f'{page}.{n+1}'
        if not all(v.get(suite,('',))[:2] in [('@','P0'),('*','P0')] for v in d.values()):continue
        num=int(re.search(r'\d+',page)[0]);kind=None
        if rang==3:kind='sources' if num in (89,100) else 'cible'
        elif rang in (1,2) and num not in (89,100,102):kind='complement'
        if kind is None:continue
        familles[kind].append((f'{page}.{n}',last['fragment']))
        if kind=='cible':
            familles['autres_places_cible']=[(f"{page}.{s['loci'][0]}",s['fragment']) for s in places[:-1]]
    assert familles['cible']==[('f102v2.29',233)] and len(familles['complement'])==4
    r={}
    attendu=['ch','o','s']
    for k,defis in familles.items():
        group=[]
        for lieu,id_frag in defis:
            valeurs={}
            for ed,lines in d.items():
                for sp in (False,True):
                    g=groupes(lines[lieu][2],sp)
                    phrase=[u for w in g for u in unites(w)]
                    valeurs[ed+('-separes' if sp else '-joints')]={'g':g,'bord':phrase[:3]==attendu or phrase[-3:]==attendu,'mot':'chos' in g,'net':all(re.fullmatch('[a-z]+',w) for w in g)}
            group.append({'locus':lieu,'fragment':id_frag,'lectures':valeurs,'bord_quatre':all(v['bord'] for v in valeurs.values()),'mot_quatre':all(v['mot'] for v in valeurs.values()),'tous_identiques':len({tuple(v['g']) for v in valeurs.values()})==1 and all(v['net'] for v in valeurs.values())})
        r[k]=group
    flancs={}
    for l,paire in CIBLES.items():
        flancs[l]={}
        for ed,lines in d.items():
            for sp in (False,True):
                line=groupes(lines[l][2],sp)
                pos,=[j for j in range(len(line)-1) if tuple(line[j:j+2])==paire]
                droite=line[pos+2:pos+4];gauche=line[pos-2:pos]
                f,n=l.split('.')
                suivant=groupes(lines[f+'.'+str(int(n)+1)][2],sp)[0]
                flancs[l][ed+('-separes' if sp else '-joints')]={'gauche':gauche,'paire':paire,'droite':droite,'premier_ligne_suivante':suivant}
    return {'empreintes':{'rangees':sha256(RANGEES.read_bytes()).hexdigest(),**{k:sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}},'lectures':r,'flancs':flancs}

if __name__=='__main__':print(json.dumps(extraire(),indent=1,ensure_ascii=False))
