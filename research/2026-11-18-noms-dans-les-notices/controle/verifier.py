"""Contre-calcul des matrices directement à partir des trois sources primaires d'entrée."""
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction
from itertools import permutations, product, takewhile
import gzip
import json
from math import factorial, lcm, prod
from pathlib import Path
from random import Random
import re
import sys
import unicodedata

WORK = Path(__file__).parent
ROOT = Path(sys.argv[1]) if len(sys.argv)>1 else WORK.resolve().parents[2]
HIST = Path(sys.argv[2]) if len(sys.argv)>2 else WORK.parent / 'historique'
REG = Path(sys.argv[3]) if len(sys.argv)>3 else WORK.parent / 'registre/registre.json'
INPUT = ROOT / 'voynich_20261028/data'
BUNDLED = ROOT / 'research/2026-11-18-noms-dans-les-notices'
TAGS = ('ckh','cth','cfh','cph','ch','sh')
def cuts(s, mode):
    s=re.sub(r'<!.*?>|<[%$]>', '', s)
    s=s.replace('<->','.').replace('<~>','.').replace('!','')
    if mode=='joint':
        s=s.replace(',','')
    else:
        s=s.replace(',','.')
    return list(filter(len,s.split('.')))
def parse(file,mode):
    pages={}; labels={}; classes={}
    for line in file.read_text().splitlines():
        if not line.startswith('<'): continue
        loc,body=line[1:].split('>',1)
        body=body.strip()
        if ',' not in loc:
            page=loc
            pages[page]=[]
            classes[page]=next((k[3:] for k in body.rstrip('>').split() if k.startswith('$L=')),'?')
            continue
        anchor,locus=loc.split(',')
        words=cuts(body,mode)
        if locus[1:]=='Lf':
            labels[anchor]=words
        elif locus[1:] in ('P0','Pt'):
            for word in words:
                if len(pages[page])<100:
                    pages[page].append((word,anchor))
    return pages,labels,classes
def latin():
    def plain(string):
        return re.findall('[a-z]+',''.join(c for c in unicodedata.normalize('NFD',string.lower()) if not unicodedata.combining(c)))
    corpus=[json.loads(line) for line in (HIST/'corpus.jsonl').read_text().splitlines()]
    chapters=re.split(r'(?m)^==', gzip.decompress((HIST/'source.wiki.gz').read_bytes()).decode('utf-8'))[1:41]
    pages={}; rows=[]
    assert len(chapters)==len(corpus)==40
    for i,(ch,record) in enumerate(zip(chapters,corpus),1):
        heading,paragraph=ch.split('<poem>')
        label=plain(heading.split('.',1)[1])[0]
        words=plain(re.sub(r'\{\{[^{}]+\}\}','',paragraph.split('</poem>')[0]))
        assert label==record['label'] and words[:100]==record['tokens'] and len(words)==record['full_body_token_count']
        page=record['id']; pages[page]=[(w,page) for w in words[:100]]
        rows.append((page,label,page,'train' if i<=20 else 'validation',False))
    return rows,pages,dict.fromkeys(pages,'latin')
@lru_cache(None)
def characters(word,islatin):
    if islatin: return tuple(word)
    chars=[]
    while word:
        token=next((t for t in TAGS if word.startswith(t)),word[0])
        chars.append(token)
        word=word[len(token):]
    return tuple(chars)
@lru_cache(None)
def change(x,y,islatin):
    if not re.fullmatch('[a-z]+',y):
        return (0,None)
    if x==y: return (2,None)
    a,b=characters(x,islatin),characters(y,islatin)
    prefix=sum(1 for pair in takewhile(lambda pair:pair[0]==pair[1],zip(a,b)))
    if prefix>=4 and len(a)-prefix<=2 and len(b)-prefix<=2:
        return 1, (a[prefix:],b[prefix:])
    return 0,None
def compute(rows,pages,classes,islatin):
    groups=defaultdict(list); scores={}; details={}; hitpairs=[]
    for id,_,page,_,_ in rows: groups[classes[page]].append(id)
    mapping={r[0]:r for r in rows}
    for id,label,page,_,_ in rows:
        scores[id]={}; details[id]={}
        for peer in groups[classes[page]]:
            p=mapping[peer][2]
            hits=[(value,i,word,at,rule) for i,(word,at) in enumerate(pages[p],1) for value,rule in [change(label,word,islatin)] if value]
            scores[id][peer]=max([x[0] for x in hits],default=0)
            details[id][p]=[(i,w,a,s) for s,i,w,a,_ in hits]
            if peer==id:
                hitpairs.extend((id,rule) for _,_,_,_,rule in hits if rule)
    rules=defaultdict(set)
    for id,rule in hitpairs: rules[rule].add(id)
    def apply(label,rule):
        bef,aft=rule; sym=characters(label,islatin); base=sym[:len(sym)-len(bef)]
        if len(base)>=4 and base+bef==sym: return ''.join(base+aft)
    def rule_eval(rule):
        targets={}; wrong={}
        for id,label,target,_,_ in rows:
            word=apply(label,rule)
            if not word: continue
            for peer in groups[classes[target]]:
                page=mapping[peer][2]
                occ=[j for j,(w,_) in enumerate(pages[page],1) if w==word]
                if occ:
                    (targets if id==peer else wrong)[id+' '+word+' '+page]=occ
        return targets,wrong
    repeat=sorted(((-len(s),len(rule_eval(r)[1]),r) for r,s in rules.items() if len(s)>=2))
    ordered=[g for g in groups.values() if len(g)>1]
    denom=lcm(*(len(g)-1 for g in ordered))
    matrices=[]; obs=0
    for group in ordered:
        matrix=[]
        for i in group:
            vec=[]
            for j in group:
                v=scores[i][j]
                doubled=sum((2*(v>scores[i][k])+(v==scores[i][k])) for k in group if k!=j)
                vec.append(doubled*denom//(len(group)-1))
            matrix.append(vec)
        obs+=sum(matrix[k][k] for k in range(len(group)))
        matrices.append(matrix)
    N=sum(map(len,ordered))
    total=prod(factorial(len(g)) for g in ordered)
    rng=Random(40819)
    sample=(product(*(permutations(range(len(g))) for g in ordered)) if total<=100000 else
            (tuple(rng.sample(range(len(g)),len(g)) for g in ordered) for _ in range(20000)))
    more=0; count=0
    for perms in sample:
        v=sum(sum(row[col] for row,col in zip(mat,perm)) for mat,perm in zip(matrices,perms))
        more+=int(v>=obs); count+=1
    ranks={}
    for id,label,page,_,strict in rows:
        own=scores[id][id]; others=[s for j,s in scores[id].items() if j!=id]
        ranks[id]=dict(label=label,page=page,classe=classes[page],n=len(pages[page]),clean=sum(bool(re.fullmatch('[a-z]+',w)) for w,_ in pages[page]),own=own,
                       win_loss_tie=[sum(own>s for s in others),sum(own<s for s in others),sum(own==s for s in others)],
                       top=all(own>=s for s in others),unique=bool(others) and all(own>s for s in others),strict=strict)
    actual=Fraction(obs,2*denom*N) if N else None
    result={'groups':dict(groups),'n':N,'p_tail':more, 'p_count':count,'p':(more+(total>100000))/(count+(total>100000)) if N else None,'score':str(actual) if N else None,'score_value':float(actual) if N else None,'own':dict(Counter(v['own'] for v in ranks.values())),'unique':sum(v['unique'] for v in ranks.values()),'ranks':ranks,'details':details,'rules':[(r,sorted(s)) for r,s in rules.items()],'chosen':repeat[0][2] if repeat else None}
    return result,rule_eval
def analyse(rows,pages,classes,islatin):
    train,_=compute([r for r in rows if r[3]=='train'],pages,classes,islatin)
    val,apply=compute([r for r in rows if r[3]=='validation'],pages,classes,islatin)
    return {'train':train,'validation':val,'prediction':apply(train['chosen']) if train['chosen'] else None}
def choose(reg, versions,skip_alternatives=False):
    admitted=[]; reasons={}; occupied=set()
    for row in sorted(reg['fragments'],key=lambda r:(r['quire'],r['fragment'])):
        n=row['fragment']; id='F'+str(n)
        if skip_alternatives and row['alternatives']: reasons[id]='alternative'; continue
        if len(row['targets'])!=1 or len(row['loci'])!=1 or row['attachment'] in ('absente','multiple'): continue
        target,=row['targets']; locus,=row['loci']; physical=re.findall('[0-9]+',target)[0]
        if not all(p.get(target) for p,_,_ in versions.values()): continue
        forms=[l.get(locus,[]) for _,l,_ in versions.values()]
        if any(len(form)!=1 for form in forms):continue
        word=forms[0][0]
        if not re.fullmatch('[a-z]+',word) or any(f[0]!=word for f in forms):continue
        if physical in occupied: reasons[id]='doublon';continue
        occupied.add(physical)
        admitted.append((id,word,target,'train' if row['quire']==15 else 'validation',row['attachment']=='sure' and row['double_agreement'] is True))
    return admitted,reasons
def main():
    lr,lp,lc=latin()
    results={'latin':analyse(lr,lp,lc,True)}
    callout=lambda part:{s:{k:part[s][k] for k in ('own','unique','score','p_tail','p','chosen')} for s in ('train','validation')}
    print('Latin',callout(results['latin']),results['latin']['prediction'],flush=True)
    versions={e+'_'+m:parse(INPUT/f,m) for e,f in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')] for m in ['separe','joint']}
    reg=json.loads(REG.read_text()); chosen,reasons=choose(reg,versions)
    results['selection']=chosen; results['voynich']={}
    print('Selection',chosen,reasons,flush=True)
    for edition,(pages,_,classes) in versions.items():
        result=analyse(chosen,pages,classes,False)
        print(edition,callout(result),flush=True)
        results['voynich'][edition]=result
    reduced,_=choose(reg,versions,True)
    print('Excluding ambiguous montage attributions', [r for r in chosen if r not in reduced],flush=True)
    (WORK/'audit_independant.json').write_text(json.dumps(results,ensure_ascii=False,indent=1)+'\n')
if __name__=='__main__': main()
