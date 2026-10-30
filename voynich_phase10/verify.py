#!/usr/bin/env python3
"""Independent reconstruction without importing the fitting implementation."""
import array,collections,json,math,random,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent;D=ROOT/'data';R=ROOT/'results'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def recover(lines,spaces):
 out=[]
 for line in lines:
  block=[];previous=''
  for j,word in enumerate(line['words']):
   if word is None:
    if len(block)>=4:out.append(block)
    block=[];previous='';continue
   if spaces and previous:block.append((' ',0,' '))
   truth=line.get('truth_words',line['words'])[j]
   block.extend((ch,int(i==0 and previous.endswith('y')),truth[i]) for i,ch in enumerate(word))
   previous=word
  if len(block)>=4:out.append(block)
 return out
def randomize(c,n):
 rng=random.Random(20261110+1000+n);d=dict(c)
 for split in ['train','test']:
  rows=[]
  for line in c[split]:
   old=line['words'];new=list(old);positions=[j for j in range(len(old)) if 0<j<len(old)-1 and old[j] is not None]
   contents=[new[j] for j in positions];rng.shuffle(contents)
   for j,w in zip(positions,contents):new[j]=w
   assert collections.Counter(x for x in old if x)==collections.Counter(x for x in new if x)
   assert [i for i,x in enumerate(old) if x is None]==[i for i,x in enumerate(new) if x is None]
   if old:assert new[0]==old[0] and new[-1]==old[-1]
   rows.append(dict(line,words=new))
  d[split]=rows
 return d
def lmread(lang,spaces):
 a=array.array('d');suffix='_boundary' if spaces else ''
 with open(D/(lang+'_lm'+suffix+'.bin'),'rb') as f:a.fromfile(f,(27 if spaces else 26)**4)
 q=list(map(float,(D/(lang+'_freq'+suffix+'.txt')).read_text().split()))
 return a,q
def scoregram(g,base,lm):
 v=0
 for ch in g:v=v*base+(26 if ch==' ' else ord(ch)-97)
 return lm[v]
def main():
 controls={c['name']:c for c in read(D/'controls8.json')};real={c['name']:c for c in read(D/'real.json')}
 # Independent encryption/decryption roundtrip, including state changes.
 cryptchars=0
 for name,c in controls.items():
  truth=read(D/(name+'_truth.json'))
  for split in ['train','test']:
   for line in c[split]:
    prev=''
    for w,t in zip(line['words'],line['truth_words']):
     enc=''.join(truth['after_y_encryption' if i==0 and prev.endswith('y') else 'base_encryption'][ch] for i,ch in enumerate(t))
     assert enc==w;prev=w;cryptchars+=len(w)
 for c in real.values():
  assert not {r['physical_leaf'] for r in c['train']} & {r['physical_leaf'] for r in c['test']}
  assert sum(len(w) for r in c['train'] for w in r['words'] if w)<=24000
 models={};checks=0;positions=0;maxerr=0.;pairs=0
 for path in sorted(R.glob('*.json')):
  result=read(path)
  if not isinstance(result,dict) or 'key_mapping' not in result:continue
  name=result['name'];spaces=result.get('boundary',False);base=27 if spaces else 26
  if name.startswith('control_'):
   m=re.match(r'(control_(?:latin|italian)_\d+)',name);c=controls[m[1]]
  else:
   m=re.fullmatch(r'((?:ZL|IT)_[AB])_wb_perm_(latin|italian)(?:_null(\d+))?_(blind|context)',name);assert m,name
   c=real[m[1]]
   if m[3]:c=randomize(c,int(m[3]))
  contextual=result['model']=='context'
  labels=[(x['cipher'],x['after_y']) for x in result['key_mapping']];mp={x:i for i,x in enumerate(labels)}
  key={x:result['key'][i] for i,x in enumerate(labels)}
  if spaces:assert key[(' ',0)]==' '
  if result.get('permutation'):
   for st in range(2 if contextual else 1):assert set(key[(chr(97+i),st)] for i in range(26))==set('abcdefghijklmnopqrstuvwxyz')
  tr=recover(c['train'],spaces);te=recover(c['test'],spaces)
  def label(x):return (x[0],x[1] if contextual else 0)
  count=collections.Counter(label(x) for s in tr for x in s)
  for v in result['key_mapping']:assert count[(v['cipher'],v['after_y'])]==v['training_occurrences']
  actual_input=[[int(t) for t in line.split()] for line in (D/(name+'_train.txt')).read_text().splitlines()]
  assert actual_input==[[mp[label(x)] for x in s] for s in tr]
  decoded=[''.join(key.get(label(x),'?') for x in s) for s in te];assert decoded==result['test_decoded_NOT_TRANSLATION']
  lm,q=lmread(result['language'],spaces)
  traindec=[''.join(key[label(x)] for x in s) for s in tr];counts=collections.Counter(''.join(traindec));n=sum(counts.values())
  gc=collections.Counter(s[i:i+4] for s in traindec for i in range(len(s)-3))
  ll=math.fsum(k*scoregram(g,base,lm) for g,k in gc.items())
  penalty=math.fsum(nc*math.log2(nc/(n*q[26 if ch==' ' else ord(ch)-97])) for ch,nc in counts.items())
  error=abs(ll-4*penalty-result['training_objective']);assert error<1e-6*n;maxerr=max(maxerr,error)
  allchars=[(x,ch) for s,ds in zip(te,decoded) for x,ch in zip(s,ds) if x[0]!=' ']
  assert len(allchars)==result['test_characters'];positions+=len(allchars)
  if result['control']:
   errors=sum(x[2]!=ch for x,ch in allchars);context=[(x,ch) for x,ch in allchars if x[1]];ce=sum(x[2]!=ch for x,ch in context)
   assert errors==result['heldout_errors'] and ce==result['context_errors'] and len(context)==result['context_characters']
   assert abs(1-errors/len(allchars)-result['heldout_accuracy'])<1e-15
  models[name]=result;checks+=1
 for path in sorted(R.glob('*_comparison.json')):
  row=read(path);a=models[row['name']+'_blind'];b=models[row['name']+'_context'];spaces=a.get('boundary',False);lm,_=lmread(row['language'],spaces);base=27 if spaces else 26
  count=[collections.Counter(),collections.Counter()];total=0
  for sa,sb in zip(a['test_decoded_NOT_TRANSLATION'],b['test_decoded_NOT_TRANSLATION']):
   assert len(sa)==len(sb)
   for i in range(len(sa)-3):
    total+=1;ga=sa[i:i+4];gb=sb[i:i+4]
    if '?' not in ga+gb:count[0][ga]+=1;count[1][gb]+=1
  n=sum(count[0].values());assert n==row['heldout_quadgrams'] and total==row['all_heldout_quadgrams']
  means=[math.fsum(k*scoregram(g,base,lm) for g,k in ct.items())/n for ct in count]
  assert abs(means[1]-means[0]-row['gain_bits'])<1e-11;pairs+=1
 assert not all(x['gate_passed'] for x in read(R/'controls_summary.json'))
 assert not all(x['gate_passed'] for x in read(R/'controls_boundary_summary.json'))
 assert all(x['gate_passed'] for x in read(R/'controls_permutation_summary.json'))
 assert not (R/'real_summary.json').exists() and not (R/'real_boundary_summary.json').exists()
 summary={'status':'PASS','independent_model_reconstructions':checks,'heldout_letter_predictions_checked':positions,'comparison_pairs_checked':pairs,'control_cipher_characters_roundtrip':cryptchars,'max_training_objective_absolute_error':maxerr,'physical_leaf_separation':'PASS','space_anchors_and_permutations':'PASS','failed_gates_respected':'PASS','limitations':'Computational checks, not independent linguistic validation or external replication. Shares frozen data and LM arrays with main analysis.'}
 write(R/'verification.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
