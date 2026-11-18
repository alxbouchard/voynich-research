"""Mesurer les expressions d’organe de la chélidoine dans les 76 autres notices."""
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
BASE = RESEARCH / '2026-11-18-opcheor-paralleles/latin'
OLD = RESEARCH / '2026-11-18-legendes-repetitions/temoin'
# Lancer le script directement ou l'importer sous un nom propre ne dépend pas
# du module 'compter.py' de l'étude antérieure.
import importlib.util
spec = importlib.util.spec_from_file_location('ancien_macer', OLD/'compter.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
ORGANS = {w:k for w,k in old.MATCH.items() if k in ('radix','folium')}
EXACT = {'radix':'radix','folium':'foliis'}
SOURCE = 'Chelidonia'

def write_tsv(name, header, rows):
    with (HERE/name).open('w') as stream:
        writer=csv.writer(stream,delimiter='\t',lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)

def normalized(word):
    return 'ejus' if word=='eius' else word

def main():
    corpus=json.loads((BASE/'corpus.json').read_bytes())
    verses=list(csv.DictReader((BASE/'vers.tsv').open(), delimiter='\t'))
    lex={k:[normalized(w) for w in ws] for k,ws in corpus.items()}
    verses_by_chapter=defaultdict(list)
    locations={}
    for r in verses:
        title=r['titre']
        line=int(r['rang_du_vers'])
        start=int(r['premier_mot_notice'])-1
        end=int(r['dernier_mot_notice'])
        verses_by_chapter[title].append(lex[title][start:end])
        for i in range(start,end):
            assert (title,i) not in locations
            locations[title,i]=line
    hits=[]
    headings=[]
    contextual={int(r['rang_du_vers']):r['texte_edite'] for r in verses}
    for chapter,(title,words) in enumerate(lex.items(),1):
        portion=('source' if title==SOURCE else ('pair' if chapter%2==0 else 'impair'))
        headings.append((chapter,title,portion,len(words),len(verses_by_chapter[title])))
        for i,word in enumerate(words):
            if word not in ORGANS: continue
            for j in range(max(0,i-3),min(len(words),i+4)):
                if words[j] not in ('ejus','illius'): continue
                line=locations[title,i]; other=locations[title,j]
                direction='apres' if i<j else 'avant'
                hits.append(dict(notice=chapter,titre=title,jeu=portion,organe=ORGANS[word],
                                 forme=word,pronom=words[j],ordre=direction,intervalle=abs(i-j)-1,
                                 vers=line,vers_pronom=other,position_organe=i+1,position_pronom=j+1,
                                 contexte=' / '.join(contextual[v] for v in range(min(line,other),max(line,other)+1))))
    write_tsv('concordance.tsv',list(hits[0]),(h.values() for h in hits))
    counts=defaultdict(Counter)
    for h in hits:
        typ='exacte' if EXACT[h['organe']]==h['forme'] else 'autre'
        zone='meme_vers' if h['vers']==h['vers_pronom'] else 'vers_adjacent'
        key=(h['jeu'],h['organe'],h['pronom'],h['ordre'],typ,zone,h['intervalle'])
        counts[key][h['titre']]+=1
    rows=[[ *k, sum(cnt.values()),len(cnt),', '.join(sorted(cnt))] for k,cnt in sorted(counts.items())]
    write_tsv('comptes.tsv',['jeu','organe','pronom','ordre','graphie','vers','mots_intercales','occurrences','notices','titres'],rows)
    index=[]
    for h in headings:
        direct=[v for v in hits if v['titre']==h[1] and v['ordre']=='apres' and v['pronom']=='ejus'
                and v['vers']==v['vers_pronom'] and v['intervalle']==0]
        index.append([*h,*[sum(v['forme']==s for v in direct) for s in ('radix','foliis')],
                      *[sum(v['organe']==s for v in direct) for s in ('radix','folium')]])
    write_tsv('notices.tsv',['notice','titre','jeu','mots','vers','radix_ejus','foliis_ejus','racine_flechie_ejus','feuille_flechie_ejus'],index)
    comparison={}
    rng=random.Random(4583101)
    for pron in ('ejus','illius'):
        lines=[words for title,book in verses_by_chapter.items() if title!=SOURCE
               for words in book if pron in words and any(w in ORGANS for w in words)]
        observed=Counter()
        simulations=defaultdict(list)
        def pairs(lines):
            c=Counter()
            for ws in lines:
                for a,b in zip(ws,ws[1:]):
                    if b==pron and a in ORGANS:
                        c[ORGANS[a]+'_flechi']+=1
                        if a==EXACT[ORGANS[a]]:c[ORGANS[a]+'_exact']+=1
            return c
        observed=pairs(lines)
        for _ in range(999):
            shuffled=[]
            for line in lines:
                copy=line.copy()
                rng.shuffle(copy)
                shuffled.append(copy)
            s=pairs(shuffled)
            for k in ['radix_exact','folium_exact','radix_flechi','folium_flechi']:
                simulations[k].append(s[k])
        comparison[pron]={k:{'observe':observed[k],'distribution':dict(sorted(Counter(s).items())),
                             'moyenne':sum(s)/len(s),'au_moins_observe':sum(n>=observed[k] for n in s)}
                          for k,s in simulations.items()}
    (HERE/'permutations.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=1)+'\n')
    for portion in ('impair','pair','source'):
        print(portion,len([r for r in index if r[2]==portion]),
              [(sum(r[i] for r in index if r[2]==portion),sum(r[i]>0 for r in index if r[2]==portion)) for i in range(5,9)])
    print({p:{k:(v['observe'],round(v['moyenne'],2),v['au_moins_observe']) for k,v in obj.items()} for p,obj in comparison.items()})
if __name__=='__main__':main()
