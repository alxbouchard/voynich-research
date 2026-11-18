"""Concordance indépendante du patron à un seul emplacement libre."""
from collections import Counter,defaultdict
import hashlib,json,re
from pathlib import Path
from itertools import combinations

ICI=Path(__file__).resolve().parent
DEPOT=ICI.parents[3]
RECHERCHE=('o','*','ch','d','y')
ORIGINE={'olchdy','okchdy'}


def pieces(mot):
    return tuple(re.findall(r'c[ktpf]h|[cs]h|.',mot))


def patron(mot,k):
    e=pieces(mot)
    if len(e)==5:return e[:k]+('*',)+e[k+1:]


def vue(body,separe):
    s=re.sub(r'<![^>]*>|<[%$]>|!', '',body)
    s=re.sub(r'\[[^\]]*\]|\{[^}]*\}', '?',s)
    s=re.sub(r'<[-~]>','.',s).replace(',','.' if separe else '')
    return Counter(w for w in s.strip().split('.') if re.fullmatch('[a-z]+',w))


def regrouper():
    donnees=defaultdict(dict);metas={};empreintes={}
    for ed,nom in [('H','IT2a-n'),('ZL','ZL3b-n')]:
        p=DEPOT/'voynich_20261028/data'/(nom+'.txt')
        empreintes[ed]=hashlib.sha256(p.read_bytes()).hexdigest()
        for line in p.read_text().splitlines():
            k=re.match(r'<([^.,>]+)\.(\w+),(.)([LP]\w)>\s*(.+)$',line)
            if not k or k[3]=='!':continue
            f,n,_,typ,body=k.groups();l=f+'.'+n;metas[l]=typ
            for s in [False,True]:donnees[l][ed+('-separes' if s else '-joints')]=vue(body,s)
    return donnees,metas,empreintes


def main():
    donnees,types,empreintes=regrouper();total=defaultdict(Counter);par_famille=defaultdict(Counter)
    occurrences=[];familles={'L':set(),'P':set()};proches=[];roues=defaultdict(Counter)
    for l,views in donnees.items():
        fam=types[l][0];a=list(views.values());agree=Counter()
        if len(a)==4:
            agree=a[0].copy()
            for v in a[1:]:agree &= v
        if agree:familles[fam].add(l)
        total[fam].update(agree)
        for w in sorted(set().union(*views.values())):
            if patron(w,1)!=RECHERCHE:continue
            counted={s:vals.get(w,0) for s,vals in views.items()}
            record={'locus':l,'type':types[l],'mot':w,'origine':w in ORIGINE,'par_vue':counted,'accord':agree.get(w,0)}
            occurrences.append(record)
        if fam=='L':
            for w,n in agree.items():
                if len(pieces(w))!=5:continue
                for k in range(5):par_famille[k][patron(w,k)]+=n
    etudes=[json.loads((ICI.parent/'PREDICTION.json').read_text()),json.loads((ICI.parent/'RESULTATS.json').read_text())]
    cas=[z for q in etudes for z in q['cas'] if z['mot']]
    for r in cas:
        for k in range(5):
            v=patron(r['mot'],k)
            if v:roues[k,v][r['geste']]+=1
    vrais=par_famille[1][RECHERCHE];vues={}
    for ks,cat in [([1],'deuxieme'),(range(5),'toutes_positions')]:
        group=[(k,v,f) for k in ks for v,f in par_famille[k].items()]
        eq=[(k,v) for k,v,n in group if n==vrais]
        vus=[{'patron':' '.join(v),'position_libre':k+1,'C':roues[k,v]['C'],'N':roues[k,v]['N']} for k,v in eq]
        vues[cat]={'n_patrons':len(group),'n_frequents_au_moins':sum(n>=vrais for _,_,n in group),'meme_frequence':len(eq),
            'au_moins_autant_de_contacts':sum(r['C']>=roues[1,RECHERCHE]['C'] for r in vus),'patrons_de_meme_frequence':vus}
    r=[q for q in occurrences if q['accord'] and q['type'].startswith('L')]
    e=[p for p in occurrences if p['accord'] and p['type'].startswith('P')]
    return {'empreintes':empreintes,'total':{f:{'loci_avec_mot':len(familles[f]),'occurrences_mots':sum(c.values()),'types_mots':len(c)} for f,c in total.items()},
        'inventaire':occurrences,
        'patron':{f:{'loci':len({r['locus'] for r in rows}),'mots': dict(sorted(Counter({w:sum(r['accord'] for r in rows if r['mot']==w) for w in {r['mot'] for r in rows}}).items()))} for f,rows in [('L',r),('P',e)]},
        'contacts_deja_cotes':[{'objet':r['objet'],'mot':r['mot'],'geste':r['geste']} for r in cas if patron(r['mot'],1)==RECHERCHE],
        'comparaison':vues}

if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=1))
