"""Comparer les formes avec ou sans y aux repères matériels des deux transcriptions."""
from collections import Counter, defaultdict
import csv
from functools import lru_cache
import json
from math import comb
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-opcheor-paralleles/variantes'))
from compter import corpus, segment, tokens

CUT=re.compile(r'(<[-~]>)')
WORD=re.compile(r'[a-z]+')
MODES=(('H','joints'),('H','separes'),('ZL','joints'),('ZL','separes'))
EXCLUDE={10,11,15,96}
CATEGORIES=('avant','apres','fin')
FIELDS=('page','lieu','section','feuillet','troncon','rang_troncon_IT','rangs_quatre','mot','positions','famille','forme')

def parse(raw,mode):
    # Une note, une lecture alternative ou un caractère exceptionnel invalide le jeton.
    raw=re.sub(r'<![^>]*>|\{[^}]*\}|\[[^\]]*\]', '?',raw)
    bits=CUT.split(raw)
    return tuple(bits[1::2]),[tokens(part,mode) for part in bits[::2]]

def positions(part,nparts,i,n):
    labels=set()
    if i==0:
        labels.add('debut' if part==0 else 'apres')
    if i+1==n:
        labels.add('fin' if part+1==nparts else 'avant')
    return labels or {'interieur'}

def lcs_table(a,b):
    mat=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i,v in enumerate(a):
        for j,w in enumerate(b):
            if v==w and WORD.fullmatch(v):
                mat[i+1][j+1]=mat[i][j]+1
            else:
                mat[i+1][j+1]=max(mat[i+1][j],mat[i][j+1])
    return mat

@lru_cache(maxsize=60000)
def forced(a,b):
    """La paire est nécessaire si elle est seule possible à son rang dans une LCS."""
    if a==b:
        return {i:i for i,w in enumerate(a) if WORD.fullmatch(w)}
    left=lcs_table(a,b)
    right=lcs_table(a[::-1],b[::-1])
    best=left[-1][-1]
    options=defaultdict(list)
    for i,v in enumerate(a):
        for j,w in enumerate(b):
            if v!=w or not WORD.fullmatch(v):continue
            rank=left[i][j]+1
            if rank+right[len(a)-i-1][len(b)-j-1]==best:
                options[rank].append((i,j))
    return dict(v[0] for v in options.values() if len(v)==1)

def aligned(rows,loc,page,section,folio,coverage,identical=False):
    views=[parse(rows[ed][loc][3],mode) for ed,mode in MODES]
    marks,ref=views[0]
    coverage['lignes_P0_communes']+=1
    coverage['marques_IT_toutes']+=len(marks)
    coverage['marques_ZL_toutes']+=len(views[-1][0])
    if not all(v[0]==marks for v in views):
        coverage['lignes_marques_divergentes']+=1
        return
    if identical and not all(v[1]==ref for v in views):
        coverage['lignes_non_identiques']+=1
        return
    coverage['lignes_admises']+=1
    coverage['marques_de_lignes_admises']+=len(marks)
    for part,a in enumerate(ref):
        others=[v[1][part] for v in views[1:]]
        maps=[forced(a,b) for b in others]
        for i,w in enumerate(a):
            coverage['jetons_IT_joints_troncons_admis']+=1
            if not WORD.fullmatch(w):
                coverage['jetons_illisibles_IT']+=1
                continue
            if not all(i in m for m in maps):
                coverage['jetons_sans_alignement_impose']+=1
                continue
            roles=positions(part,len(ref),i,len(a))
            indices=[i,*[m[i] for m in maps]]
            if any(positions(part,len(ref),j,len(b))!=roles for j,b in zip(indices[1:],others)):
                coverage['jetons_statut_de_bord_divergent']+=1
                continue
            coverage['jetons_accords']+=1
            yield {'page':page,'lieu':loc,'section':section,'feuillet':folio,'troncon':part+1,
                   'rang_troncon_IT':i+1,'rangs_quatre':'/'.join(str(j+1) for j in indices),
                   'mot':w,'positions':tuple(sorted(roles))}

def family(word,one=False):
    base=word.removesuffix('y')
    if base=='cth' or base.endswith('y') or not base:
        return None
    if (len(segment(base))==1) != one:
        return None
    return base

def inventory(identical=False):
    editions,sections=corpus()
    rows=[];cover=defaultdict(Counter)
    for loc in editions['ZL']:
        if not all(loc in ds and ds[loc][1]=='P0' for ds in editions.values()):continue
        page=editions['ZL'][loc][0]
        m=re.match(r'f(\d+)',page)
        if not m:continue
        folio=int(m[1])
        if folio in EXCLUDE:continue
        section=sections[page]
        rows.extend(aligned(editions,loc,page,section,folio,cover['H' if section=='H' else 'autres'],identical))
    return rows,cover

def paired(rows,one=False):
    vocab={r['mot'] for r in rows}
    families={x for x in vocab if family(x,one)==x and x+'y' in vocab}
    return [r|{'famille':base,'forme':'longue' if r['mot'].endswith('y') else 'courte'}
            for r in rows if (base:=family(r['mot'],one)) in families]

def counts(rows):
    return Counter((role,r['forme']) for r in rows for role in r['positions'])

def table(rows):
    return {role:[sum(role in r['positions'] and r['forme']==form for r in rows) for form in ('courte','longue')]
            for role in ('avant','apres','fin','debut','interieur')}

def margins(groups,power=False):
    # Distribution exacte du total de formes courtes aux bords à marges fixes.
    ways=[1];denom=1;matched=Counter();observed=0;expected=0.;informs=0
    for (ns,nl,cs,cl) in groups:
        edge=ns+nl;control=cs+cl;short=ns+cs;n=edge+control
        if not edge or not control or short in (0,n):continue
        informs+=1
        matched.update({'courts_bord':ns,'longs_bord':nl,'courts_interieurs':cs,'longs_interieurs':cl})
        freq=[comb(short,k)*comb(n-short,edge-k) for k in range(min(edge,short)+1)]
        # comb(n,k) vaut zéro si k>n pour les entiers non négatifs.
        new=[0]*(len(ways)+len(freq)-1)
        for i,a in enumerate(ways):
            for j,b in enumerate(freq):new[i+j]+=a*b
        ways=new;denom*=comb(n,edge)
        observed+=ns;expected+=edge*short/n
    assert sum(ways)==denom
    result={'strates_informatives':informs,'marges_informatives':dict(matched),'courts_bord_observes':observed,
            'courts_bord_attendus':expected,'difference':observed-expected,
            'p_superieur_ou_egal':sum(ways[observed:])/denom if informs else None}

    if power and informs:
        possible=[k for k,v in enumerate(ways) if v]
        threshold=next((k for k in possible if 20*sum(ways[k:])<=denom),None)
        def detect(odds):
            weights=[v*odds**k for k,v in enumerate(ways)]
            return sum(weights[threshold:])/sum(weights) if threshold is not None else 0
        result['sensibilite_a_marges_fixes']={'support':possible,'distribution_positions_echangeables':
                [v/denom for v in ways], 'seuil_nombre_de_courts':threshold,'p_si_tous_courts_possibles_au_bord':
                ways[max(possible)]/denom,'puissance':{odds:detect(odds) for odds in (1,2,5)}}
    return result

def tests(rows,role='avant',unit='page',unique=False,power=False):
    grouped=defaultdict(lambda:[0,0,0,0])
    for r in rows:
        pos=r['positions']
        if role not in pos and 'interieur' not in pos:continue
        if (unique or role=='fin') and len(pos)>1:continue
        idx=(0 if role in pos else 2)+(r['forme']=='longue')
        grouped[r['famille'],r[unit]][idx]+=1
    return margins(grouped.values(),power)

def report(rows):
    eligible=paired(rows)
    by=defaultdict(list)
    for r in eligible:by[r['famille']].append(r)
    info={'jetons_stables':len(rows),'jetons_de_familles':len(eligible),'familles':len(by),
          'marges_brutes':table(eligible),'par_famille':{fam:table(rs) for fam,rs in sorted(by.items())},
          'tests':{role:tests(eligible,role) for role in CATEGORIES},
          'avant_sans_mots_seuls':tests(eligible,unique=True),
          'avant_stratification_par_ligne':tests(eligible,unit='lieu')}
    return info,eligible

def write_tsv(rows):
    with (HERE/'occurrences.tsv').open('w') as f:
        writer=csv.DictWriter(f,list(FIELDS),delimiter='\t',lineterminator='\n')
        writer.writeheader()
        for r in rows:
            writer.writerow(r|{'positions':'+'.join(r['positions'])})

def main():
    assert forced(('a','a'),('a',))=={}
    assert forced(('a','b'),('b','a'))=={}
    assert forced(('a','b','a'),('a','b','c','a'))=={0:0,1:1,2:3}
    assert forced(('a','?','a'),('a','?','a'))=={0:0,2:2}
    assert family('cth') is None and family('sholy')=='shol' and family('sholyy') is None
    assert abs(margins([(1,0,0,1),(1,0,0,1)])['p_superieur_ou_egal']-0.25)<1e-14
    rows,cover=inventory()
    result={'couverture':cover}
    all_eligible=[]
    for group,subset in [('H',[r for r in rows if r['section']=='H']),
                         ('autres',[r for r in rows if r['section']!='H'])]:
        summary,eligible=report(subset)
        all_eligible.extend(eligible)
        for parity,id in [(0,'pairs'),(1,'impairs')]:
            part=[r for r in eligible if r['feuillet']%2==parity]
            summary[id]={'marges_brutes':table(part),'test_avant':tests(part)}
        result[group]=summary
    herbal=[r for r in rows if r['section']=='H']
    short_bases=paired(herbal,True)
    groups=defaultdict(list)
    for r in short_bases:groups[r['famille']].append(r)
    strict,cover_strict=inventory(True)
    identical_rows=[r for r in strict if r['section']=='H']
    stricter=paired(identical_rows)
    result['sensibilites_H']={'marges_principales':tests(paired(herbal),power=True),
        'base_une_unite':{'familles':{f:table(vals) for f,vals in sorted(groups.items())},
                           'marges':table(short_bases),'avant':tests(short_bases)},
        'lignes_identiques':{'couverture':cover_strict['H'],'marges':table(stricter),'avant':tests(stricter)}}
    write_tsv(all_eligible)
    (HERE/'resultats.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')
    for group in ('H','autres'):
        d=result[group]
        print(group,d['jetons_stables'],d['familles'],d['marges_brutes'],d['tests']['avant'],d['pairs']['test_avant'],d['impairs']['test_avant'])

if __name__=='__main__':main()
