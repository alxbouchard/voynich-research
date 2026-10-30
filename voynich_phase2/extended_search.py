#!/usr/bin/env python3
"""Exploratory language/unit/direction sensitivity and independent controls."""
import json,re,sys,random,collections
from pathlib import Path
import numpy as np
from search_keys import ROOT,BASE,DATA,OUT,SEED,clean,grams,run_case,lm_build
from analyse import parse

def build(s):
 c=np.bincount(grams(s),minlength=26**4)
 lm=np.log2((c+.01)/(c.sum()+.01*26**4));lm.tofile(DATA/'latin_lm.bin')
 rank=''.join(sorted('abcdefghijklmnopqrstuvwxyz',key=lambda ch:(-s.count(ch),ch)))
 return lm,rank

def main():
 raw=(DATA/'dante.txt').read_text()
 assert '\nPARADISO\n' in raw
 # The published input contains the poem twice. Use only its first complete
 # occurrence, so later Inferno/Purgatorio copies cannot leak into test data.
 starts=list(re.finditer(r'INFERNO\nInferno\nCanto I\n',raw))
 unique=raw[:starts[1].start()] if len(starts)>1 else raw
 if len(starts)>1:assert raw[starts[1].start():].strip()==unique.strip(),'Duplicate differs; inspect source'
 before,paradiso=unique.split('\nPARADISO\n',1)
 def poem(t):return clean('\n'.join(l for l in t.splitlines() if l.strip() and not re.match(r'^(INFERNO|PURGATORIO|PARADISO|Inferno|Purgatorio|Paradiso|Canto\b)',l)))
 italian_train=poem(before);italian_test=poem(paradiso)
 (DATA/'italian_train.txt').write_text(italian_train)
 latin_train=clean((DATA/'latin_train.txt').read_text())
 results=[]
 recs=parse('ZL3b-n.txt')[0]
 eligible=[r for r in recs if r['type'].startswith('P')]
 leaves=sorted({r['leaf'] for r in eligible});testleaves=set(leaves[::5])
 unit_re=r'ckh|cth|cph|cfh|ch|sh|iiiin|iiin|iin|in|.'
 freq=collections.Counter(u for r in eligible if r['leaf'] not in testleaves for w in r['tokens'] for u in re.findall(unit_re,w) if '?' not in u)
 unitmap={u:chr(97+i) for i,(u,n) in enumerate(freq.most_common(26))}
 (OUT/'composed_unit_mapping.json').write_text(json.dumps({'rule':unit_re,'units':unitmap,'selection':'26 most frequent training units only; unknown/rare units break spans, never concatenate across them'},indent=2))
 def encode(r,units):
  seq=''.join(r['tokens']) # uncertain characters remain as hard breaks
  if units=='EVA':return re.findall('[a-z]+',seq)
  coded=''.join(''.join(unitmap.get(u,'?') for u in re.findall(unit_re,w)) for w in r['tokens']);return re.findall('[a-z]+',coded)
 for language,training in [('latin',latin_train),('italian',italian_train)]:
  if '--control-only' in sys.argv and language=='latin':continue
  lm,rank=build(training)
  if language=='italian':
   alphabet=list('abcdefghijklmnopqrstuvwxyz');random.Random(SEED+1).shuffle(alphabet)
   encrypted=italian_test.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz',''.join(alphabet)))
   ctl=run_case('italian_hidden_key_control',[encrypted[:24000]],[encrypted[24000:]],lm,rank,truth=[italian_test[24000:]])
   assert ctl['heldout_character_accuracy']>=.95,'Italian control failed'
  if '--control-only' in sys.argv:continue
  for subset in ['all','A','B']:
   selected=[r for r in eligible if subset=='all' or r['metadata'].get('L')==subset]
   for units in ['EVA','COMPOSED']:
    training_segs=[s for r in selected if r['leaf'] not in testleaves for s in encode(r,units)]
    testing_segs=[s for r in selected if r['leaf'] in testleaves for s in encode(r,units)]
    used=[];size=0
    for s in training_segs:
     if size+len(s)>24000:break
     if len(s)>=4:used.append(s);size+=len(s)
    for direction in ['forward','reverse']:
     train=used if direction=='forward' else [s[::-1] for s in used]
     test=testing_segs if direction=='forward' else [s[::-1] for s in testing_segs]
     name=f'extended_{language}_{subset}_{units}_{direction}'
     results.append(run_case(name,train,test,lm,rank,restarts=8,steps=40000))
  # Shuffled null with identical per-line character composition, same solver.
  train=[s for r in eligible if r['leaf'] not in testleaves for s in encode(r,'EVA')]
  test=[s for r in eligible if r['leaf'] in testleaves for s in encode(r,'EVA')]
  used=[];n=0
  for s in train:
   if n+len(s)>24000:break
   used.append(s);n+=len(s)
  rng=random.Random(SEED)
  def shuf(segs):
   out=[]
   for s in segs:
    a=list(s);rng.shuffle(a);out.append(''.join(a))
   return out
  results.append(run_case('shuffled_null_'+language,shuf(used),shuf(test),lm,rank))
 if '--control-only' not in sys.argv:(OUT/'extended_summary.json').write_text(json.dumps(results,indent=2)+'\n')
 # Restore Latin model for all future base experiments.
 lm_build()
 print('EXTENDED SEARCH COMPLETE',flush=True)

if __name__=='__main__':main()
