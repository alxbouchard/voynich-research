"""Essayer deux noms d’organe avec une seule table et chercher les groupes en prose."""
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH/'2026-11-18-carte-sept-etoiles/lecture'))
from essai import tables
sys.path.insert(0, str(RESEARCH/'2026-11-18-formes-souterraines/nom/second'))
from transfert import corpus, tokens

A,B,C = 'otoky','otaly','oky'
WORDS = (A,B,C)
REQUIRED = (A,B)

def fits(forms, allow_silent):
    results=[]
    nulls=sorted(set(A+B)) if allow_silent else [None]
    for null in nulls:
        x=tuple(s for s in A if s!=null)
        y=tuple(s for s in B if s!=null)
        for first in sorted(forms):
            for table in tables(x,first,None):
                for second in sorted(forms):
                    for key in tables(y,second,None,table):
                        if null:
                            key[null]=''
                        assert [''.join(key[s] for s in seq) for seq in (A,B)]==[first,second]
                        probe=''.join(key[s] for s in C)
                        results.append(dict(mot1=first,mot2=second,autre_organe=forms[first]!=forms[second],
                                            muet=null,cle=key,mot3=probe,atteste=probe in forms))
    return results

def run_lookup():
    # Contrôle avec les mêmes motifs de signes, valeurs connues en une ou deux lettres.
    hidden={'o':'al','t':'m','a':'r','k':'v','l':'i','y':'s'}
    clear=lambda seq: ''.join(hidden[s] for s in seq)
    artificial={clear(w):w for w in WORDS}
    assert any(row['cle']==hidden and row['mot3']==clear(C) and row['atteste'] for row in fits(artificial,False))
    hidden['t']=''
    artificial={clear(w):w for w in WORDS}
    assert any(row['cle']==hidden and row['atteste'] for row in fits(artificial,True))
    with (HERE.parent/'temoin/occurrences.tsv').open() as f:
        forms={row['forme']:row['lemme'] for row in csv.DictReader(f,delimiter='\t')}
    pools={'lemmes':{s:s for s in ('radix','folium','flos')}, 'formes_du_poeme':forms}
    results={}
    for name,pool in pools.items():
        modes={}
        for null in (False,True):
            rows=fits(pool,null)
            modes['un_signe_muet' if null else 'sans_muet']=dict(
                total=len(rows),paires_distinctes=len({(r['mot1'],r['mot2']) for r in rows}),
                graphies_differentes=sum(r['mot1']!=r['mot2'] for r in rows),
                organes_differents=sum(r['autre_organe'] for r in rows),
                predictions_attestees=sum(r['atteste'] for r in rows),tables=rows)
        results[name]={'lexique':pool,'modes':modes}
    return results

def paragraphs(book, sections, spacing):
    paras=[];active=None
    for locus,(page,kind,position,raw) in book.items():
        if kind not in ('P0','Pc') or sections.get(page)!='P':
            continue
        if active is None or active['page']!=page or '<%>' in raw:
            active={'page':page,'premiere':locus,'derniere':locus,'debut_marque':'<%>' in raw,
                    'fin_marquee':False,'occurrences':[],'lignes':0,'mots_lisibles':0}
            paras.append(active)
        active['lignes']+=1;active['derniere']=locus
        # Les signes spéciaux sont exclus, on conserve la position de chaque groupe.
        line=tokens(re.sub(r'\{[^}]*\}','?',raw),spacing)
        for i,word in enumerate(line,1):
            if re.fullmatch('[a-z]+',word):
                active['mots_lisibles']+=1
            if word in WORDS:
                active['occurrences'].append([locus,i,word])
        if '<$>' in raw:
            active['fin_marquee']=True
            active=None
    total=Counter(w for para in paras for loc,i,w in para['occurrences'])
    both=[p['premiere'] for p in paras if set(REQUIRED)<={w for loc,i,w in p['occurrences']}]
    return {'panneaux':len({p['page'] for p in paras}),'paragraphes':len(paras),
            'limites_marquees':sum(p['debut_marque'] and p['fin_marquee'] for p in paras),
            'mots_lisibles':sum(p['mots_lisibles'] for p in paras),'occurrences':dict(total),'deux_mots':both,
            'detail':paras}

def consecutive(results,books):
    for entries in books.values():
        raw=entries['f82v.31'][3]
        for spacing in ('joints','separes'):
            words=tokens(re.sub(r'\{[^}]*\}','?',raw),spacing)
            assert (C,B) in zip(words,words[1:])
    rows=results['formes_du_poeme']['modes']['un_signe_muet']['tables']
    pairs={(row['mot3'],row['mot2']) for row in rows}
    assert len(pairs)==143
    lookup=json.loads((RESEARCH/'2026-11-18-opcheor-paralleles/latin/corpus.json').read_bytes())
    out={}
    for rev in (False,True):
        candidates={(b,a) if rev else (a,b) for a,b in pairs}
        hits=[]
        for title,words in lookup.items():
            for i,ab in enumerate(zip(words,words[1:])):
                if ab in candidates:
                    hits.append({'notice':title,'premier_mot':i+1,'paire':ab,
                                 'contexte':words[max(0,i-4):i+6]})
        out['inverse' if rev else 'direct']=hits
    out['paires_a_rechercher']=sorted(pairs)
    out['nombre_de_bigrams']=sum(len(ws)-1 for ws in lookup.values())
    out['nombre_de_notices']=len(lookup)
    return out

def main():
    results=run_lookup();books,sections=corpus()
    runs={edition+'/'+spacing:paragraphs(book,sections,spacing) for edition,book in books.items()
          for spacing in ('joints','separes')}
    for mode,report in runs.items():
        assert {p['premiere'] for p in report['detail']} >= {'f88r.7','f99v.10'}
    out={'lecture_organe':results,'prose_pharmaceutique':runs,'passage_f82v_31':consecutive(results,books)}
    (HERE/'resultats.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
    for name,d in results.items():
        print(name,len(d['lexique']),[(n,{k:v for k,v in e.items() if k!='tables'}) for n,e in d['modes'].items()])
    for mode,d in runs.items():
        print(mode,{k:v for k,v in d.items() if k!='detail'})
        print([(p['premiere'],p['occurrences']) for p in d['detail'] if p['occurrences']])
if __name__=='__main__':main()
