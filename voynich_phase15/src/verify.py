"""Rebuild observed fits, audit strict matches, and recompute exact p values."""
import json,re
import numpy as np
from threadpoolctl import threadpool_limits
from experiment import ROOT,make_data,rule_universe,features,evaluate,metadata,IDENTITY,read_rows

def q_diagnostic():
 out={}
 for code in ['ZL','IT']:
  d=make_data(code,'strict');h=features(d,[IDENTITY,('P',(),('q',))]);li,_=metadata(d)
  table={}
  for name,mat in [('identity',h[0]),('identity_or_q_prefix',h[0]|h[1])]:
   table[name]=dict(any_leaf_hits=int(mat.any(axis=1).sum()),own_leaf_hits=int(mat[np.arange(len(li)),li].sum()),
    mean_own_fraction=float(np.mean([mat[li==j,j].mean() for j in range(6)])),
    mean_other_fraction=float(np.mean([mat[np.ix_(li==j,[k for k in range(6) if k!=j])].mean() for j in range(6)])))
  out[code]=table
 (ROOT/'results/q_prefix_descriptive.json').write_text(json.dumps(out,indent=2))
 return out

def main():
 checks=[];audited=0
 with threadpool_limits(limits=1):
  for code in ['ZL','IT']:
   for cond in ['strict','lattice']:
    r=json.loads((ROOT/'results'/f'{code}_{cond}.json').read_text())
    d=make_data(code,cond);rules=rule_universe(d);H=features(d,rules)
    obs=evaluate(d,rules,H,tuple(range(6)),True)
    assert obs==r['observed']
    for key in ['score','gain']:
     p=sum(n[key]>=obs[key]-1e-12 for n in r['permutations'])/720
     assert p==r['full_null'][key]['p_exact']
     blocked=[n for n in r['permutations'] if all(r['panel_counts'][i]==r['panel_counts'][j] for i,j in enumerate(n['permutation']))]
     assert len(blocked)==48
     assert sum(n[key]>=obs[key]-1e-12 for n in blocked)/48==r['panel_count_null'][key]['p_exact']
    if cond=='strict':
     for fold in obs['folds']:
      for hit in fold['matches']:
       for m in hit['matches']:
        src=m['label_surface'];dst=m['prose_surface'];rule=m['rule']
        if rule=='identity':assert src==dst
        else:
         side,rr=rule.split(':');old,new=rr.split('>');old=old.replace('∅','');new=new.replace('∅','')
         if side=='P':assert src.startswith(old) and new+src[len(old):]==dst
         else:assert src.endswith(old) and (src[:-len(old)] if old else src)+new==dst
        for occurrence in m['occurrences']:
         # Independent character-string check, without atomization or features().
         raw=occurrence['raw_line'].replace('<->','.').replace('<~>','.')
         tokens=re.sub(r'<[^>]*>','',raw).split('.')
         assert dst in tokens and occurrence['n_words']==1
         audited+=1
    checks.append(dict(code=code,condition=cond,observed_refit='identical',exact_p_recomputed=True))
 q=q_diagnostic()
 controls=json.loads((ROOT/'results/controls.json').read_text())
 positive=sum(f['own_hits'] for f in controls['positive']['folds'])
 negative=sum(f['own_hits'] for f in controls['negative']['folds'])
 assert positive==120 and negative==0
 out=dict(checks=checks,strict_prose_occurrences_independently_verified=audited,
          positive_control_recovered=positive,negative_control_matches=negative,
          drawing_separator_note='Phase 14 omitted a separator for <~>. Six ZL loci contain this marker, none are pharmaceutical; phase-14 pharmaceutical test unaffected. This parser treats both drawing markers as hard barriers.')
 (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
