import collections,hashlib,json,math,random,re,shutil
from pathlib import Path
from engine import ROOT
BASE=ROOT.parent
def norm(w):return w.lower().replace('v','u').replace('j','i')
def atomic(w):
 for i,s in enumerate(['cth','ckh','cph','cfh','ch','sh']):w=w.replace(s,chr(0xe000+i))
 return w
def top(ws,n):return [w for w,c in sorted(collections.Counter(ws).items(),key=lambda x:(-x[1],x[0])) if 2<=len(w)<=10][:n]
def main():
 source_files=['voynich_phase10/data/real.json','voynich_phase10/data/latin_train_boundary.txt','voynich_phase10/data/italian_train_boundary.txt']
 hashes=[{'source':p,'sha256':hashlib.sha256((BASE/p).read_bytes()).hexdigest()} for p in source_files]
 refs={lang:top([norm(w) for w in (BASE/f'voynich_phase10/data/{lang}_train_boundary.txt').read_text().split()],256) for lang in ['latin','italian']}
 data=json.loads((BASE/source_files[0]).read_text());cases=[]
 for d in data:
  if d['name'].startswith('IT'):continue
  train_words=[w for l in d['train'] for w in l['words'] if w]
  test_words=[w for l in d['test'] for w in l['words'] if w]
  for mode,convert in [('EVA',lambda w:w),('COMPOSED',atomic)]:
   train=[convert(w) for w in train_words];test=[convert(w) for w in test_words]
   selected=top(train,96);alphabet=sorted(set(''.join(selected)))
   seen=set(train);held=[w for w in test if w not in seen and 2<=len(w)<=10 and set(w)<=set(alphabet)]
   # Source order is canonical lexicographic, never an implied cognate pairing.
   selected=sorted(selected)
   for lang,target in refs.items():
    cases.append({'name':d['name']+'_'+mode+'_'+lang,'kind':'voynich','mode':mode,'language':lang,
     'source':[[w] for w in selected],'target':[[w] for w in sorted(target)],'test':sorted(set(held)),
     'alphabet':alphabet,'N':math.ceil(len(set(''.join(target)))/len(alphabet)),'M':2,
     'train_pages':sorted(set(l['page'] for l in d['train'])),'test_pages':sorted(set(l['page'] for l in d['test'])),
     'train_leaf_ids':sorted(set(l['physical_leaf'] for l in d['train'])),'test_leaf_ids':sorted(set(l['physical_leaf'] for l in d['test'])),
     'counts':{'train_tokens':len(train),'test_tokens':len(test),'unseen_test_retained_tokens':len(held),'unseen_test_types':len(set(held))}})
 for typ in ['mono','null','homophonic']:
  rng=random.Random(13002);target=sorted(refs['latin']);alphabet=sorted(set(''.join(target)))
  # Hide all target spellings with a random symbol permutation.
  shuffled=list(alphabet);rng.shuffle(shuffled);enc=dict(zip(alphabet,shuffled))
  candidates=list(target);rng.shuffle(candidates);plain_train=candidates[:96];plain_test=candidates[96:160]
  def encode(w):
   out=''
   for i,c in enumerate(w):
    out+=('X' if typ=='homophonic' and c=='e' and i%2 else enc[c])
   return out+('Z' if typ=='null' else '')
  source=sorted(encode(w) for w in plain_train);held=sorted(encode(w) for w in plain_test)
  truth={encode(w):w for w in plain_train+plain_test}
  cases.append({'name':'control_'+typ,'kind':'control','source':[[w] for w in source],
   'target':[[w] for w in target],'test':held,'truth':truth,'N':1,'M':2 if typ=='homophonic' else 1})
 # The paired benchmark annotations are saved only for evaluation, not passed as alignments.
 path=ROOT/'vendor/CSA_OptMatcher/data/StarlingDB_Ph-Ug.cog'
 pairs=[l.split() for l in path.read_text().splitlines()[1:]]
 source=[a.split('|') for a,b in pairs if a!='_'];target=[b.split('|') for a,b in pairs if b!='_']
 rng=random.Random(13003);rng.shuffle(source);rng.shuffle(target)
 cases.append({'name':'benchmark_Phoenician_Ugaritic','kind':'benchmark','source':source,'target':target,'test':[],
  'gold_pairs':[[a.split('|'),b.split('|')] for a,b in pairs if a!='_' and b!='_'],'N':2,'M':1})
 for c in cases:
  if 'train_leaf_ids' in c:assert not set(c['train_leaf_ids'])&set(c['test_leaf_ids'])
 (ROOT/'data/cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
 (ROOT/'data/input_sources.json').write_text(json.dumps(hashes,indent=2))
 protocol={'created':'2026-10-28 America/Toronto','objective':'Pilot global lexicon matching with corrected CPU CSA adaptation',
  'training_source_types':96,'target_lexicon_types':256,'glyph_encodings':['EVA','cth/ckh/cph/cfh/ch/sh as atomic units'],
  'train_test_split':'reused physical-leaf split from phase10; heldout evaluation restricted to word types absent from ALL training pages',
  'validation_warning':'These pages were used in prior project phases. Algorithmic holdout, not a project-wide untouched discovery set.',
  'language_warning':'Latin and Italian are convenience baselines, neither historically exhaustive nor language identification.',
  'initial_calibration_steps':5000,'annealers':8,'penalty':4,'max_calibrated_steps':20000,
  'gate':'Report known-answer recovery before interpreting Voynich; if insufficient, real scores only computational diagnostics.',
  'null':'Permutation inside each distinct source word, fixed across occurrences; same type lengths and glyph counts; duplicates allowed as source groups.',
  'score':'Mean minimum generalized edit distance to reference lexicon on unseen heldout types. Lower is closer; not translation accuracy.',
  'corrections':['serial candidate copying','independent initial states','best visited state retention','GED(empty,nonempty)=1'],
  'not_implemented':['joint phonetic segmentation model','automatic semantic translation','full historical-language lexica','image-driven glyph reclassification']}
 (ROOT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False))
 print(json.dumps([{'name':c['name'],'types':len(c['source']),'targets':len(c['target']),'test':len(c['test']),'N':c['N'],'M':c['M']} for c in cases],indent=2))
if __name__=='__main__':main()
