import sys,json,copy,random,hashlib,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
V=ROOT/'tmp/vendor/zfd'
sys.path.insert(0,str(V/'validation/blind_decode_test'))
import run_test_v3 as v3
from decoder import decode_eva_text
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def hashobj(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def permute_fields(table,fields,rng,typed=False):
 if typed:
  groups={}
  for k,v in table.items():
   signature=tuple((f in v,type(v.get(f)).__name__) for f in fields)
   groups.setdefault(signature,[]).append(k)
  changed=0
  for keys in groups.values():
   group={k:table[k] for k in keys}
   changed+=permute_fields(group,fields,rng)
  return changed
 keys=list(table); order=list(range(len(keys))); rng.shuffle(order)
 old=copy.deepcopy(table)
 for i,k in enumerate(keys):
  for f in fields:
   if f in old[keys[order[i]]]: table[k][f]=old[keys[order[i]]][f]
   else: table[k].pop(f,None)
 return sum(any(table[k].get(f)!=old[k].get(f) for f in fields) for k in keys)
def strip_private(r): return {k:v for k,v in r.items() if k not in ('tokens','unknown_stem_list')}

# Reproduce published v3 functions without overwriting the pinned report.
repro={name:v3.run_config(name,cfg,30) for name,cfg in v3.CONFIGS.items()}
published=json.loads((V/'validation/blind_decode_test/results_v3/v3_dual_config_results.json').read_text())['configs']
differences=[]
def compare(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b: differences.append([p+'/'+k,'missing'])
   else: compare(a[k],b[k],p+'/'+k)
 elif a!=b: differences.append([p,a,b])
compare(repro,published)
save('zfd_v3_reproduction.json',{'configs':repro,'published_differences':differences})
print('v3 reproduction complete; differences',len(differences),flush=True)

# Semantic perturbations of the older statistical-validation pipeline.
semantic={}
for name,cfg in v3.CONFIGS.items():
 base_pipe=v3.build_pipeline(cfg)
 texts={f:(V/'voynich_data/raw_eva'/f'{f}.txt').read_text() for f in v3.FOLIOS}
 baseline={f:decode_eva_text(t,f,pipeline=base_pipe) for f,t in texts.items()}
 trials=[]
 for i in range(20):
  seed=310000+i; rng=random.Random(seed); pipe=copy.deepcopy(base_pipe)
  changed=permute_fields(pipe.lexicon.stems,['gloss','latin','croatian'],rng)
  comp=permute_fields(pipe.compound.morphemes,['gloss'],rng) if pipe.compound else 0
  folios={}
  for f,t in texts.items():
   r=decode_eva_text(t,f,pipeline=pipe); b=baseline[f]
   assert len(r['tokens'])==len(b['tokens'])
   folios[f]={**strip_private(r),'changed_glosses':sum(x.get('stem_gloss')!=y.get('stem_gloss') for x,y in zip(r['tokens'],b['tokens']))}
  trials.append({'seed':seed,'changed_lexicon_entries':changed,'changed_compound_entries':comp,'lexicon_hash':hashobj(pipe.lexicon.stems),'folios':folios})
 semantic[name]={'baseline':{f:strip_private(r) for f,r in baseline.items()},'trials':trials}
save('zfd_v3_semantic.json',semantic)
print('v3 semantic perturbations complete',flush=True)

# Current canonical decoder, separate from the older validation pipeline.
spec=importlib.util.spec_from_file_location('zfd_canonical',V/'06_Pipelines/zfd_decoder_v2.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
base=module.ZFDDecoder()
folios=v3.FOLIOS+['f1r','f75r','f103r']
texts={f:(V/'voynich_data/raw_eva'/f'{f}.txt').read_text() for f in folios}
baseline={f:base.decode_folio(t,f) for f,t in texts.items()}
def metrics(r):
 return {'stats':r['stats'],'folio_confidence':r['folio_confidence'],
  'line_confidences':[l['line_confidence'] for l in r['lines']],
  'word_confidences':[w['confidence'] if w else 0 for l in r['lines'] for w in l['words']]}
def glosses(dec,r): return [dec.gloss_word(w) for l in r['lines'] for w in l['words']]
trials=[]
sections={'operators':['meaning_en','meaning_hr','latin'], 'state_markers':['meaning_en'],
 'stems':['meaning_en','meaning_hr','latin'], 'suffixes':['meaning_en','grammatical_function'],
 'latin_terms':['meaning_en','latin_full']}
for i in range(20):
 seed=210000+i; rng=random.Random(seed); dec=copy.deepcopy(base)
 changed={s:permute_fields(dec.lexicon[s],fields,rng,typed=True) for s,fields in sections.items()}
 rows={}
 for f,t in texts.items():
  r=dec.decode_folio(t,f); a=glosses(dec,r); b=glosses(base,baseline[f])
  assert len(a)==len(b)
  rows[f]={'metrics_unchanged':metrics(r)==metrics(baseline[f]),
   'total_tokens':len(a),'changed_glosses':sum(x!=y for x,y in zip(a,b))}
 trials.append({'seed':seed,'changed_entries':changed,'lexicon_sha256':hashobj(dec.lexicon),'folios':rows})
save('zfd_canonical_semantic.json',{'baseline':{f:metrics(r) for f,r in baseline.items()},'trials':trials})
# Private full outputs, excluded from delivered archive (translation rights).
(ROOT/'tmp/zfd_canonical_private.json').write_text(json.dumps(baseline,ensure_ascii=False))
print('canonical complete',json.dumps({f:r['stats'] for f,r in baseline.items()}),flush=True)
