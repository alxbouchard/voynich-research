"""Shared edge-rewrite experiment with leaf-level cross-fitting and exact nulls."""
from pathlib import Path
from collections import defaultdict, Counter
import itertools, json, re, time, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
ATOMS=re.compile('cth|ckh|cph|cfh|ch|sh|[a-z]')
IDENTITY=('I',(),())

def atomize(s): return tuple(ATOMS.findall(s))
def surface(t): return ''.join(t)
def rule_name(r):
    return 'identity' if r==IDENTITY else f'{r[0]}:{surface(r[1]) or "∅"}>{surface(r[2]) or "∅"}'

def variants(chunk):
    """Finite explicit IVTFF alternatives only. Unknown signs never match anything."""
    chunk=re.sub(r'\{([a-z]+)\}',r'\1',chunk)
    stack=[chunk]
    while any('[' in s for s in stack):
        nxt=[]
        for s in stack:
            m=re.search(r'\[([^\[\]]+)\]',s)
            if not m:
                if '[' not in s:nxt.append(s)
                continue
            for opt in m[1].split(':'):nxt.append(s[:m.start()]+opt+s[m.end():])
        stack=nxt
        if len(stack)>16:return []
    out=set()
    for s in stack:
        n=s.count(',')
        if n>4:continue
        for decisions in itertools.product(['','.'],repeat=n):
            parts=s.split(',');st=parts[0]
            for sep,part in zip(decisions,parts[1:]):st+=sep+part
            words=tuple(st.split('.'))
            if 1<=len(words)<=2 and all(re.fullmatch('[a-z]+',w) for w in words):out.add(words)
            if len(out)>16:return []
    return sorted(out)

def read_rows(file):
    rows=[];meta={}
    for line in file.read_text().splitlines():
        h=re.match(r'^<(f[^.>]+)>\s+<! (.+)>',line)
        if h:meta[h[1]]=dict(re.findall(r'\$(\w)=(\S+)',h[2]))
        m=re.match(r'^<(f[^.>]+)\.(\d+),([^>]+)>\s+(.+)',line)
        if m:
            page,num,kind,raw=m.groups()
            if kind[0]=='!':continue
            if not re.match(r'f\d+',page):continue
            # Keep a hard barrier: never merge across a drawing interruption.
            clean=re.sub(r'<[^>]*>','',raw.replace('<->','|').replace('<~>','|'))
            rows.append(dict(page=page,leaf=re.match(r'f\d+',page)[0],locus=f'{page}.{num}',
                             kind=kind,raw=raw,clean=clean,meta=meta[page]))
    return rows

def make_data(code,condition):
    rows=read_rows(ROOT/'data'/('ZL3b-n.txt' if code=='ZL' else 'IT2a-n.txt'))
    leaves=sorted({r['leaf'] for r in rows if r['meta'].get('I')=='P'},key=lambda x:int(x[1:]))
    labels=[];prose=[defaultdict(list) for _ in leaves];pages=[set() for _ in leaves]
    for r in rows:
        if r['meta'].get('I')!='P':continue
        j=leaves.index(r['leaf'])
        if r['kind'][1:] in ('Lf','Lc'):
            if condition=='strict':
                vv=[(r['clean'],)] if re.fullmatch('[a-z]{3,}',r['clean']) else []
            else:vv=variants(r['clean'])
            vv=[v for v in vv if len(''.join(v))>=3]
            forms=sorted({atomize(''.join(v)) for v in vv})
            if forms:labels.append(dict(leaf_index=j,locus=r['locus'],raw=r['raw'],variants=[list(v) for v in vv],forms=forms,kind=r['kind']))
        elif r['kind'][1:2]=='P':
            pages[j].add(r['page'])
            for segment in r['clean'].split('|'):
                chunks=segment.split('.')
                parsed=[]
                for chunk in chunks:
                    vv=variants(chunk) if condition=='lattice' else ([(chunk,)] if re.fullmatch('[a-z]+',chunk) else [])
                    parsed.append(vv)
                for ci,vv in enumerate(parsed):
                    found=[]
                    for v in vv:
                        for a,w in enumerate(v):found.append((w,1,ci,ci))
                        if len(v)==2:found.append((''.join(v),2,ci,ci))
                    if condition=='lattice' and ci+1<len(parsed):
                        for a in vv:
                            for b in parsed[ci+1]:
                                if len(a)==len(b)==1:found.append((a[0]+b[0],2,ci,ci+1))
                    for text,n,start,end in found:
                        key=atomize(text)
                        info=dict(locus=r['locus'],surface=text,n_words=n,chunk_start=start,chunk_end=end,raw_line=r['raw'])
                        if info not in prose[j][key]:prose[j][key].append(info)
    assert len(leaves)==6 and all(any(x['leaf_index']==j for x in labels) for j in range(6))
    return dict(code=code,condition=condition,leaves=leaves,labels=labels,prose=prose,pages=[sorted(p) for p in pages])

def apply_rule(src,rule):
    side,old,new=rule
    if side=='I':return src
    if len(src)-len(old)<3:return None
    if side=='P':
        if src[:len(old)]!=old:return None
        return new+src[len(old):]
    if old and src[-len(old):]!=old:return None
    stem=src[:-len(old)] if old else src
    return stem+new

def rule_universe(data,excluded_leaf=None,excluded_text=None):
    # Exhaustively induce all members of the predeclared family that can match.
    # Eligibility during fitting uses training pairs only; held-out-only rules
    # can never be selected. A train-only universe check verifies equivalence.
    left=defaultdict(set);right=defaultdict(set)
    for j,text in enumerate(data['prose']):
        if j==excluded_text:continue
        for dst in text:
            for k in range(3):
                if len(dst)-k<3:continue
                left[dst[k:]].add(dst[:k])
                right[dst[:-k] if k else dst].add(dst[-k:] if k else ())
    rules={IDENTITY}
    for label in data['labels']:
        if label['leaf_index']==excluded_leaf:continue
        for src in label['forms']:
            for k in range(3):
                if len(src)-k<3:continue
                old=src[:k]
                rules.update(('P',old,new) for new in left[src[k:]] if new!=old)
                old=src[-k:] if k else ()
                rules.update(('S',old,new) for new in right[src[:-k] if k else src] if new!=old)
    return [IDENTITY]+sorted(rules-{IDENTITY},key=rule_name)

def features(data,rules):
    H=np.zeros((len(rules),len(data['labels']),6),dtype=bool)
    for ri,rule in enumerate(rules):
        for li,label in enumerate(data['labels']):
            outputs={apply_rule(src,rule) for src in label['forms']}-{None}
            for j,text in enumerate(data['prose']):H[ri,li,j]=any(dst in text for dst in outputs)
    return H

def metadata(data):
    li=np.array([l['leaf_index'] for l in data['labels']])
    groups={}
    for n,l in enumerate(data['labels']):
        key=tuple(l['forms'])
        groups.setdefault(key,[]).append(n)
    return li,list(groups.values())

def train(H,li,groups,perm,hold):
    n=len(li);trainrows=np.flatnonzero(li!=hold);trainleaves=[j for j in range(6) if j!=hold]
    traincols=[perm[j] for j in trainleaves]
    own=H[:,trainrows,np.asarray(perm)[li[trainrows]]]
    leafsupport=np.zeros(H.shape[0],int)
    for leaf in trainleaves:leafsupport+=own[:,li[trainrows]==leaf].any(axis=1)
    hits=np.zeros((H.shape[0],n),dtype=bool);hits[:,trainrows]=own
    unique=np.zeros(H.shape[0],int)
    for group in groups:unique+=hits[:,group].any(axis=1)
    eligible=(leafsupport>=2)&(unique>=3);eligible[0]=False
    W=np.zeros((n,6),float)
    for leaf in trainleaves:
        rr=np.flatnonzero(li==leaf);den=len(rr)*5
        W[np.ix_(rr,traincols)]=-1/(den*4)
        W[rr,perm[leaf]]=1/den
    selected=[0];base=H[0].copy();scores=[]
    # Flatten once so all possible gains are one dense matrix-vector product.
    FH=H.reshape(H.shape[0],-1)
    for _ in range(3):
        gains=FH @ (W*(~base)).ravel()
        gains[~eligible]=-np.inf
        ri=int(np.argmax(gains))
        if gains[ri] <= .01+1e-12:break
        selected.append(ri);scores.append(float(gains[ri]));base|=H[ri];eligible[ri]=False
    return selected,base,scores

def evaluate(data,rules,H,perm,details=False):
    li,groups=metadata(data);ownmeans=[];bgmeans=[];identityscores=[];folds=[]
    for hold in range(6):
        selected,base,gains=train(H,li,groups,perm,hold)
        rows=np.flatnonzero(li==hold);col=perm[hold];others=[c for c in range(6) if c!=col]
        own=base[rows,col];bg=base[np.ix_(rows,others)].mean(axis=1)
        ownmeans.append(float(own.mean()));bgmeans.append(float(bg.mean()))
        identityscores.append(float(H[0,rows,col].mean()-H[0][np.ix_(rows,others)].mean()))
        if details:
            trainingforms={v for k,l in enumerate(data['labels']) if li[k]!=hold for v in l['forms']}
            unseen=[k for k in rows if not trainingforms.intersection(data['labels'][k]['forms'])]
            fold=dict(held_out=data['leaves'][hold],target_leaf=data['leaves'][col],
                rules=[rule_name(rules[r]) for r in selected],training_gains=gains,
                n_labels=len(rows),own_hits=int(own.sum()),background_mean_fraction=float(bg.mean()),
                unseen_label_count=len(unseen),unseen_hits=int(base[unseen,col].sum()),matches=[])
            for k in rows:
                if not base[k,col]:continue
                l=data['labels'][k];matches=[]
                for ri in selected:
                    for src in l['forms']:
                        dst=apply_rule(src,rules[ri])
                        if dst in data['prose'][col]:matches.append(dict(rule=rule_name(rules[ri]),label_surface=surface(src),prose_surface=surface(dst),occurrences=data['prose'][col][dst]))
                assert matches
                fold['matches'].append(dict(label_locus=l['locus'],raw=l['raw'],matches=matches))
            folds.append(fold)
    score=float(np.mean(ownmeans)-np.mean(bgmeans));identity=float(np.mean(identityscores))
    return dict(score=score,identity_score=identity,gain=score-identity,
                own_fraction=float(np.mean(ownmeans)),background_fraction=float(np.mean(bgmeans)),folds=folds)

def run_case(code,condition):
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1):
        start=time.monotonic();data=make_data(code,condition);rules=rule_universe(data);H=features(data,rules)
        print(f'{code}/{condition}: {len(data["labels"])} labels, {len(rules)} rules',flush=True)
        perm0=tuple(range(6));observed=evaluate(data,rules,H,perm0,True)
        permutations=list(itertools.permutations(range(6)));null=[]
        for p in permutations:
            e=evaluate(data,rules,H,p)
            null.append(dict(permutation=list(p),score=e['score'],gain=e['gain']))
        def summarize(nn):
            return {key:dict(observed=observed[key],null_mean=float(np.mean([r[key] for r in nn])),
               p_exact=float(np.mean([r[key]>=observed[key]-1e-12 for r in nn])),n_permutations=len(nn)) for key in ['score','gain']}
        lengths=[len(x) for x in data['pages']]
        blocked=[r for r in null if all(lengths[i]==lengths[j] for i,j in enumerate(r['permutation']))]
        result=dict(code=code,condition=condition,n_rules=len(rules),labels=len(data['labels']),
                    leaves=data['leaves'],panel_counts=lengths,n_prose_forms=[len(t) for t in data['prose']],
                    observed=observed,full_null=summarize(null),panel_count_null=summarize(blocked),permutations=null,
                    elapsed_seconds=time.monotonic()-start)
        (ROOT/'results'/f'{code}_{condition}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        # Verify absence of candidate-generation leakage using independently
        # reconstructed training-only rule inventories for all observed folds.
        li,groups=metadata(data)
        for hold in range(6):
            tr=rule_universe(data,hold,hold);th=features(data,tr)
            ss,_,_=train(th,li,groups,perm0,hold)
            assert [rule_name(tr[k]) for k in ss]==observed['folds'][hold]['rules']
        print(f'{code}/{condition}: done, score {observed["score"]:.6f}, exact p {result["full_null"]["score"]["p_exact"]:.6f}, {result["elapsed_seconds"]:.1f}s',flush=True)
        return {k:result[k] for k in ['code','condition','n_rules','labels','full_null','panel_count_null','elapsed_seconds']}

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--case',nargs=2);ap.add_argument('--inventory',action='store_true');args=ap.parse_args()
    if args.inventory:
        for code in ['ZL','IT']:
            for cond in ['strict','lattice']:
                d=make_data(code,cond);r=rule_universe(d)
                print(json.dumps(dict(code=code,condition=cond,labels=len(d['labels']),rules=len(r),leaves=d['leaves'],panels=[len(x) for x in d['pages']],prose_forms=[len(x) for x in d['prose']])))
    elif args.case:run_case(*args.case)
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=4) as ex:
            jobs=[ex.submit(run_case,k,c) for k in ['ZL','IT'] for c in ['strict','lattice']]
            summary=[j.result() for j in jobs]
        (ROOT/'results/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
