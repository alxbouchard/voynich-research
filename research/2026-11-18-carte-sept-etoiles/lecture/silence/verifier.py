"""Recherche des paires avec un seul signe muet, puis transfert des clés figées."""
import csv
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE.parent))
from essai import tokenize, variants, tables

RULE=HERE/'01-regles.json'
HASH='43228b5b6a717c776d9d34b00cbe9e0e2685eacefc3a2fd9aa204356522338b1'
assert hashlib.sha256(RULE.read_bytes()).hexdigest()==HASH
SPEC=json.loads(RULE.read_text())
ROOT=HERE.parents[3]


def partitions_for(signs, target, muted):
    """Contre-calcul par partitions de la sortie, indépendant de la récursion de essai.py."""
    source=tuple(s for s in signs if s!=muted)
    if ' ' in source or not source or len(source)>len(target):return []
    maps=[]
    for cuts in itertools.combinations(range(1,len(target)),len(source)-1):
        starts=(0,)+cuts; ends=cuts+(len(target),); mapping={muted:''}
        for sign,a,b in zip(source,starts,ends):
            segment=target[a:b]
            if mapping.setdefault(sign,segment)!=segment:break
        else:maps.append(mapping)
    return maps


def calibration():
    rows=[]; catalog={}
    for lang,(t1,t3) in SPEC['paires'].items():
        for reader,(r1,r3) in SPEC['lectures_X1_X3'].items():
            for space,text3 in variants(r3):
                for compound,reverse in itertools.product((True,False),(False,True)):
                    s1=tokenize(r1,compound,reverse);s3=tokenize(text3,compound,reverse)
                    for silent in sorted((set(s1)|set(s3))-{' '}):
                        x1=tuple(s for s in s1 if s!=silent);x3=tuple(s for s in s3 if s!=silent)
                        joint=[]
                        for m in tables(x1,t1.lower(),None):
                            for n in tables(x3,t3.lower(),None,m):
                                n[silent]=''
                                assert ''.join(' ' if s==' ' else n[s] for s in s1)==t1.lower()
                                assert ''.join(' ' if s==' ' else n[s] for s in s3)==t3.lower()
                                key=lang,compound,reverse,tuple(sorted(n.items()))
                                if key not in catalog:catalog[key]=len(catalog)+1
                                joint.append(catalog[key])
                        left=partitions_for(s1,t1.lower(),silent);right=partitions_for(s3,t3.lower(),silent)
                        shared=set(s1)&set(s3)-{' '}
                        count=sum(all(m[k]==n[k] for k in shared) for m in left for n in right)
                        assert count==len(joint)
                        rows.append({'ajustements_X1':len(left),'ajustements_X3':len(right),'tradition':lang,'transcription':reader,'frontiere':space,'ch_compose':compound,'inverse':reverse,'vide':silent,'n_cles':len(joint),'cles':joint})
    return rows,catalog


def expand_word(group):
    options=re.search(r'\[([^\[\]]+)\]',group)
    if not options:
        return [group]
    return [w for val in options[1].split(':') for w in expand_word(group[:options.start()]+val+group[options.end():])]


def corpus(version):
    data=ROOT/'voynich_20261028/data'/version
    assert hashlib.sha256(data.read_bytes()).hexdigest()==SPEC['versions'][version]
    entries=[]
    for line in data.read_text().splitlines():
        match=re.match(r'^<(f68r[12]\.\d+),.(\w\w)>\s+(.*)',line)
        if not match:continue
        locus,kind,raw=match.groups();region=SPEC['disques'].get(locus,'etoile')
        if region=='etoile' and kind!='Ls':continue
        clean=re.sub(r'<[^>]*>','',raw).strip();assert ' ' not in clean
        for j,word in enumerate(clean.split('.'),1):
            if not word:continue
            scenarios=[('principale',word.split(','))]
            if ',' in word:scenarios.append(('soudure', [word.replace(',','')]))
            for branch,words in scenarios:
                for k,part in enumerate(words,1):
                    for vv in expand_word(part):
                        entries.append({'locus':locus,'region':region,'branche':branch,'position':f'{j}.{k}',
                                        'source':part,'variante':vv,'incertain':'[' in part or '?' in part or ',' in word})
    assert set(SPEC['disques'])=={e['locus'] for e in entries if e['region']!='etoile'}
    return entries


def decode(group,compound,reverse,mapping):
    # Les codes @...; restent chacun un signe illisible pour cette table.
    atoms=[]
    for part in re.split(r'(@\d+;|\{[^}]*\})',group):
        if part.startswith(('@','{')):atoms.append(part)
        else:atoms.extend(tokenize(part,compound,False))
    if reverse:atoms.reverse()
    result=''.join(mapping.get(s,'['+s+']') for s in atoms)
    return result,all(s in mapping for s in atoms),sum(s in mapping for s in atoms),len(atoms)


def main():
    assert hashlib.sha256((ROOT/'research/2026-11-18-sept-astres/sources/LUMINAIRES.md').read_bytes()).hexdigest()==SPEC['inventaire_sha256']
    assert list(tables(('d','d'),'aa',None))==[{'d':'a'}]
    c1=partitions_for(('d','ch','d'),'aa','ch');c2=partitions_for(('ch','d'),'a','ch')
    assert c1==c2==[{'ch':'','d':'a'}]
    rows,catalog=calibration();results=[];summary=[]
    contents={name:corpus(name) for name in SPEC['versions']} if catalog else {}
    for (lang,compound,reverse,pairs),i in catalog.items():
        m=dict(pairs)
        for version,entries in contents.items():
            counts=Counter();hits=set();wrong=set()
            for e in entries:
                prediction,complete,ns,nt=decode(e['variante'],compound,reverse,m)
                expected=SPEC['cibles_transfert'].get(e['region'])
                if not complete:category='partielle'
                elif prediction not in {'sol','luna'}:category='entière_autre'
                elif expected is None:category='faux_positif_étoile'
                elif prediction==expected:category='identité_correcte';hits.add(e['region'])
                else:category='identité_inverse';wrong.add(e['region'])
                counts[(e['region'],category)]+=1
                results.append(dict(cle=i,tradition=lang,version=version,**e,sortie=prediction,signes_connus=ns,signes=nt,categorie=category))
            summary.append({'cle':i,'version':version,'disques_corrects':sorted(hits),'disques_inverses':sorted(wrong),
                            'comptages':{'/'.join(k):n for k,n in sorted(counts.items())}})
    keys=[{'id':i,'tradition':l,'ch_compose':c,'inverse':r,'table':dict(m)} for (l,c,r,m),i in catalog.items()]
    (HERE/'resultats.json').write_text(json.dumps({'regles_sha256':HASH,'configurations':rows,'tables':keys,'transfert':summary},ensure_ascii=False,indent=2)+'\n')
    if results:
        with (HERE/'sorties.tsv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=results[0],delimiter='\t');w.writeheader();w.writerows(results)
    print('configurations',len(rows),'ajustements',sum(r['n_cles'] for r in rows),'tables distinctes',len(keys),'groupes et variantes examinés',len(results))
    print(Counter((r['tradition'],r['vide']) for r in rows if r['n_cles']))
    print(Counter(r['categorie'] for r in results))
    print('sources', {n:len(entries) for n,entries in contents.items()})

if __name__=='__main__':main()
