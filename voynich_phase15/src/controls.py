from pathlib import Path
import json,random
from collections import defaultdict
import numpy as np
from threadpoolctl import threadpool_limits
from experiment import atomize,variants,rule_universe,features,evaluate,rule_name,IDENTITY,apply_rule,ROOT

def make_control(positive=True):
 rng=random.Random(2152026);seen=set();labels=[];texts=[defaultdict(list) for _ in range(6)]
 for leaf in range(6):
  for n in range(20):
   while True:
    s=''.join(rng.choice('abcdinrx') for _ in range(9))
    # No shared 5-character end can generate a false short-edge correspondence.
    if not any(s[:5]==t[:5] or s[-5:]==t[-5:] for t in seen):break
   seen.add(s);labels.append(dict(leaf_index=leaf,locus=f'control{leaf}.{n}',raw=s,forms=[atomize(s)],variants=[[s]]))
   dst='q'+s if positive else 'zzzzzzzzzz'
   texts[leaf][atomize(dst)].append(dict(locus=f'text{leaf}.{n}',surface=dst,n_words=1))
 return dict(code='positive' if positive else 'negative',condition='synthetic',labels=labels,prose=texts,leaves=[f'c{i}' for i in range(6)],pages=[[f'c{i}r',f'c{i}v'] for i in range(6)])

def main():
 assert set(variants('otor,am'))=={('otoram',),('otor','am')}
 assert set(variants('ok[a:o]l'))=={('okal',),('okol',)}
 assert variants('a?b')==[] and variants('a@194;b')==[]
 assert variants('{ck}ey')==[('ckey',)]
 assert atomize('qockhey')==('q','o','ckh','e','y')
 assert apply_rule(atomize('okol'),('P',(),('q',)))==atomize('qokol')
 assert apply_rule(atomize('ol'),('P',(),('q',))) is None
 out={}
 with threadpool_limits(limits=1):
  for positive in [True,False]:
   d=make_control(positive);rules=rule_universe(d);H=features(d,rules)
   r=evaluate(d,rules,H,tuple(range(6)),True)
   if positive:
    assert abs(r['score']-1)<1e-12
    assert all(f['own_hits']==20 and f['unseen_hits']==20 and 'P:∅>q' in f['rules'] for f in r['folds'])
   else:
    assert r['score']==0 and all(f['rules']==['identity'] for f in r['folds'])
   out[d['code']]=r
 (ROOT/'results/controls.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print(json.dumps({k:dict(score=v['score'],held_out_hits=sum(f['own_hits'] for f in v['folds']),rules=[f['rules'] for f in v['folds']]) for k,v in out.items()},ensure_ascii=False))

if __name__=='__main__':main()
