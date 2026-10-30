"""Additional positive control for N=2,M=2, added before interpreting real scores."""
import json,random
from engine import ROOT
from run import run
cases=json.loads((ROOT/'data/cases.json').read_text())
base=next(c for c in cases if c['name']=='control_mono')
target=[g[0] for g in base['target']];rng=random.Random(13002)
alphabet=sorted(set(''.join(target)));symbols=list(alphabet);rng.shuffle(symbols);enc=dict(zip(alphabet,symbols));enc['e']=enc['i']
candidates=list(target);rng.shuffle(candidates)
def encode(w):return ''.join(enc[c] for c in w)
train=candidates[:96];test=candidates[96:160]
groups={}
for w in target:groups.setdefault(encode(w),[]).append(w)
# Score only invertible ciphertext words not seen in the training source.
used={encode(w) for w in train};test=[w for w in test if len(groups[encode(w)])==1 and encode(w) not in used]
case={'name':'control_polyphonic','kind':'control','source':[[encode(w)] for w in train],
 'target':base['target'],'test':[encode(w) for w in test],'truth':{encode(w):w for w in train+test},'N':2,'M':2,
 'note':'e and i collapse to the same cipher sign; exclude intrinsically ambiguous test words'}
(ROOT/'data/polyphonic_control.json').write_text(json.dumps(case,indent=2))
run(case,13010,5000,8)
