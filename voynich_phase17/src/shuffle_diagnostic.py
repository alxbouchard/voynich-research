from pathlib import Path
import json,numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from crib_scan import blocks,rows,PLAIN

ROOT=Path(__file__).resolve().parents[1]
segments=[np.array([ord(c)-97 for w in b for c in w['text']],dtype=np.uint8)
          for b in blocks(rows(ROOT/'data/ZL3b-n.txt'),'split')]
separator=np.full(len(PLAIN),255,dtype=np.uint8)

def count(parts):
    stream=np.concatenate([a for part in parts for a in [part,separator]])
    view=sliding_window_view(stream,len(PLAIN))
    allowed=(view!=255).all(axis=1)
    ans={}
    for direction,plain in [('forward',PLAIN),('reverse',PLAIN[::-1])]:
        ok=allowed.copy()
        for i in range(len(plain)):
            for j in range(i):
                if plain[i]!=plain[j]:ok &= view[:,i]!=view[:,j]
        ans[direction]=int(ok.sum())
    ans['total']=ans['forward']+ans['reverse']
    return ans

observed=count(segments)
prior=json.loads((ROOT/'results/crib_scan.json').read_text())['runs'][0]['counts']
assert observed['forward']==prior['unspaced_forward_homophonic']
assert observed['reverse']==prior['unspaced_reverse_homophonic']
rng=np.random.default_rng(2026103017)
controls=[count([rng.permutation(a) for a in segments]) for _ in range(32)]
out={'post_hoc':True,'seed':2026103017,'replicates':32,'observed':observed,'controls':controls,
     'null_summary':{k:{'min':min(r[k] for r in controls),'max':max(r[k] for r in controls),
                       'mean':float(np.mean([r[k] for r in controls]))} for k in observed},
     'interpretation_limit':'Descriptive check of constraint matches in shuffled data, not a test of meaning or language.'}
(ROOT/'results/shuffle_diagnostic.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='controls'},indent=2))
