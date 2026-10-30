#!/usr/bin/env python3
"""Compare true keys with initial fitted keys, using verifier's independent scorer."""
import collections,json,math
from pathlib import Path
from verify import recover,lmread,scoregram
P=Path(__file__).resolve().parent;D=P/'data';R=P/'results'
out=[]
for c in json.loads((D/'controls.json').read_text()):
 name=c['name'];t=json.loads((D/(name+'_truth.json')).read_text());fit=json.loads((R/(name+'_context.json')).read_text())
 inv=[{b:a for a,b in t[k].items()} for k in ['base_encryption','after_y_encryption']]
 seqs=recover(c['train'],False);plain=[''.join(inv[x[1]][x[0]] for x in s) for s in seqs]
 lm,q=lmread(c['language'],False);cnt=collections.Counter(''.join(plain));n=sum(cnt.values())
 gc=collections.Counter(s[i:i+4] for s in plain for i in range(len(s)-3));g=sum(gc.values())
 ll=math.fsum(k*scoregram(s,26,lm) for s,k in gc.items());kl=math.fsum(k/n*math.log2(k/n/q[ord(ch)-97]) for ch,k in cnt.items())
 true={'characters':n,'quadgrams':g,'bits_per_quadgram':-ll/g,'kl_bits':kl,'objective':ll-4*n*kl}
 wrong=[dict(x,true_output=inv[x['after_y']][x['cipher']]) for x in fit['key_mapping'] if x['output']!=inv[x['after_y']][x['cipher']]]
 assert fit['training_objective']>true['objective']
 out.append({'name':name,'true_training':true,'found_training':fit['train'],'wrong_mappings':wrong})
(R/'calibration_diagnostic.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('All four initial fitted wrong keys have higher objective than true key.')
