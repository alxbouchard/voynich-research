"""Recherche de reprises de noms dans leur propre notice et dans les pages témoins."""
import argparse
from collections import defaultdict
from functools import lru_cache
from itertools import permutations, product
import json
from math import factorial, lcm, prod
from pathlib import Path
import random
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'voynich_20261028' / 'data'
HEADER = re.compile(r'^<(f\d+[rv]\d*)>\s*<!\s*(.*?)>')
LOCUS = re.compile(r'^<((f\d+[rv]\d*)\.[^,>]+),.([A-Za-z0-9]{2})>\s*(.*)')
EVA = re.compile(r'ckh|cth|cph|cfh|ch|sh|[a-z]')
SIMPLE = re.compile(r'[a-z]+')

def load_edition(path, split):
    pages, labels = {}, {}
    for line in path.read_text().splitlines():
        head = HEADER.match(line)
        if head:
            currier = re.search(r'\$L=(\S+)',head[2])
            pages[head[1]] = {'classe':currier[1] if currier else '?','positions':[]}
            continue
        loc = LOCUS.match(line)
        if not loc:
            continue
        key, page, kind, raw = loc.groups()
        raw = re.sub(r'<![^>]*>|<[%$]>', '', raw)
        raw = re.sub(r'<[-~]>', '.', raw).replace('!', '').replace(',', '.' if split else '')
        words = [word for word in raw.split('.') if word]
        if kind == 'Lf':
            labels[key] = words
        if kind in ('P0','Pt'):
            positions = pages[page]['positions']
            positions.extend((key,i,w) for i,w in enumerate(words,1))
    for page in pages.values():
        page['positions'] = page['positions'][:100]
    return pages, labels

def select_records(inventory, editions):
    selected, log = [], []
    occupied = {}
    for row in sorted(inventory['fragments'],key=lambda item:(item['quire'],item['fragment'])):
        decision = dict(fragment=row['fragment'],qui=row['quire'],loci=row['loci'],cibles=row['targets'],
                        attache=row['attachment'],accord=row['double_agreement'])
        log.append(decision)
        if len(row['loci']) != 1 or len(row['targets']) != 1 or row['attachment'] in ('multiple','absente'):
            decision['decision'] = 'inscription ou cible absente ou multiple'
            continue
        locus, page = row['loci'][0], row['targets'][0]
        readings = {key: value[1].get(locus) for key,value in editions.items()}
        decision['lectures'] = readings
        words = next(iter(readings.values()))
        if not (words and len(words)==1 and SIMPLE.fullmatch(words[0]) and all(v == words for v in readings.values())):
            decision['decision'] = 'groupe simple concordant absent'
            continue
        if not all(value[0].get(page,{}).get('positions') for value in editions.values()):
            decision['decision'] = 'texte de la face cible indisponible'
            continue
        physical = int(re.match(r'f(\d+)',page)[1])
        if physical in occupied:
            decision['decision'] = 'feuillet cible déjà utilisé'
            decision['fragment_prioritaire'] = occupied[physical]
            continue
        occupied[physical] = row['fragment']
        decision['decision'] = 'retenu'
        selected.append(dict(id=f"F{row['fragment']}",fragment=row['fragment'],split='train' if row['quire']==15 else 'validation',
                             label=words[0],page=page,strict=row['attachment']=='sure' and row['double_agreement'] is True))
    return selected,log

@lru_cache(None)
def units(word, latin):
    return tuple(word) if latin else tuple(EVA.findall(word))

def endings(left,right):
    shared=0
    for a,b in zip(left,right):
        if a!=b:
            break
        shared+=1
    if shared<4 or max(len(left),len(right))-shared>2:
        return None
    return left[shared:],right[shared:]

def compare(label,positions,latin):
    left=units(label,latin)
    hits=[]
    for rank,(locus,in_line,word) in enumerate(positions,1):
        if not SIMPLE.fullmatch(word):
            continue
        exact=word==label
        change=None if exact else endings(left,units(word,latin))
        if exact or change:
            hits.append(dict(score=2 if exact else 1,locus=locus,rang=rank,dans_ligne=in_line,mot=word,
                             terminaison=change))
    return {'score':max((h['score'] for h in hits),default=0),'lectures':hits}

def possible_output(label, rule, latin):
    start, end = rule
    letters=units(label,latin)
    prefix_length=len(letters)-len(start)
    if prefix_length<4 or letters[prefix_length:] != start:
        return None
    return ''.join(letters[:prefix_length]+end)

def learn_rule(rows,pages,latin):
    supports=defaultdict(set)
    for row in rows:
        for hit in compare(row['label'],pages[row['page']]['positions'],latin)['lectures']:
            if hit['terminaison']:
                supports[hit['terminaison']].add(row['id'])
    candidates=[]
    for rule,support in sorted(supports.items()):
        if len(support)<2:
            continue
        false_pairs=0
        for row in rows:
            prediction=possible_output(row['label'],rule,latin)
            if prediction:
                for other in rows:
                    other_page=pages[other['page']]
                    if other['page'] != row['page'] and other_page['classe']==pages[row['page']]['classe']:
                        false_pairs+=any(w==prediction for _,_,w in other_page['positions'])
        candidates.append(dict(rule=rule,support=sorted(support),fausses_pages=false_pairs))
    candidates.sort(key=lambda c:(-len(c['support']),c['fausses_pages'],c['rule']))
    return {'regle':candidates[0]['rule'] if candidates else None, 'candidates':candidates,
            'soutiens_observes':[{'regle':r,'couples':sorted(s)} for r,s in sorted(supports.items())]}

def evaluate_rule(rule, rows, pages, latin):
    if rule is None:
        return None
    results=[]
    for row in rows:
        prediction=possible_output(row['label'],rule,latin)
        found={}
        if prediction:
            for peer in rows:
                page=peer['page']
                if pages[page]['classe']==pages[row['page']]['classe']:
                    found[page]=[(loc,i) for loc,i,w in pages[page]['positions'] if w==prediction]
        results.append(dict(id=row['id'],etiquette=row['label'],page=row['page'],prediction=prediction,occurrences=found))
    return results

def evaluate(rows,pages,latin):
    matches={}
    rows_by_class=defaultdict(list)
    for row in rows:
        rows_by_class[pages[row['page']]['classe']].append(row)
    ranking_groups=[]
    ranks={}
    for cls,group in rows_by_class.items():
        cell_values=[]
        for row in group:
            cells={peer['page']:compare(row['label'],pages[peer['page']]['positions'],latin) for peer in group}
            matches[row['id']]=cells
            scores=[c['score'] for c in cells.values()]
            n=len(scores)
            eligible=n>1
            own=cells[row['page']]['score']
            best=max(scores)
            ranks[row['id']]=dict(page=row['page'],classe=cls,etiquette=row['label'],positions=len(pages[row['page']]['positions']),
                                  exact_ou_partiel=own,pages_au_maximum=scores.count(best),
                                  cible_au_maximum=own==best,comparables=n-1)
            if eligible:
                # Twice the wins plus ties against all other pages. Remove the self-tie.
                cell_values.append([sum((2 if x>y else (1 if x==y else 0)) for y in scores)-1 for x in scores])
        if cell_values:
            ranking_groups.append(cell_values)
    # Integer weights express half-ties exactly across unequal stratum sizes.
    sizes=[len(group) for group in ranking_groups]
    n=sum(sizes)
    null=None
    if n:
        denom=lcm(*(s-1 for s in sizes))
        weights=[denom//(s-1) for s in sizes]
        def rank_total(assignment):
            return sum(w*sum(g[i][j] for i,j in enumerate(perm))
                       for w,g,perm in zip(weights,ranking_groups,assignment))
        obs=rank_total([range(s) for s in sizes])
        count=prod(factorial(s) for s in sizes)
        exact=count<=100000
        rng=random.Random(40819)
        assignments=(product(*(permutations(range(s)) for s in sizes)) if exact else
                     ([rng.sample(range(s),s) for s in sizes] for _ in range(20000)))
        tail=total=0
        for assignment in assignments:
            tail+=rank_total(assignment)>=obs
            total+=1
        null=dict(n_comparables=n,tailles_strates=sizes,score=obs/(2*n*denom),permutations=total,exact=exact,
                  au_moins_aussi_bon=tail,p=(tail+(not exact))/(total+(not exact)))
    return dict(rangs=ranks,comparaisons=matches,permutation=null)

def analysis(rows,pages,latin):
    train=[r for r in rows if r['split']=='train']
    val=[r for r in rows if r['split']=='validation']
    rule=learn_rule(train,pages,latin)
    return {'apprentissage':evaluate(train,pages,latin),'validation':evaluate(val,pages,latin),
            'choix_terminaison':rule,'prediction_terminaison':evaluate_rule(rule['regle'],val,pages,latin)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--donnees',type=Path,default=DATA)
    ap.add_argument('--sortie',type=Path,default=HERE/'RESULTATS.json')
    args=ap.parse_args()
    data=[json.loads(line) for line in (HERE/'historique/corpus.jsonl').read_text().splitlines()]
    latin_rows=[dict(id=r['id'],page=r['id'],label=r['label'],split=r['split']) for r in data]
    latin_pages={r['id']:{'classe':'latin','positions':[(r['id'],i,w) for i,w in enumerate(r['tokens'],1)]} for r in data}
    editions={}
    for name,filename in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        for mode in ['separe','joint']:
            editions[name+'_'+mode]=load_edition(args.donnees/filename,mode=='separe')
    register=json.loads((HERE/'registre/registre.json').read_text())
    rows,log=select_records(register,editions)
    result={'latin':analysis(latin_rows,latin_pages,True),'selection':log,'couples':rows,'voynich':{}}
    for key,(pages,_) in editions.items():
        result['voynich'][key]=analysis(rows,pages,False)
    args.sortie.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    main()
