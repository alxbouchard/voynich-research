"""Independent numerical consistency checks; does not assert semantic correctness."""
import json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def read(n):return json.loads((ROOT/'results'/n).read_text())
s=read('scott_audit.json');b=s['baseline']
assert (b['total'],b['decoded'],b['glossary_keys'])==(37886,33785,4063)
assert sum(v['total'] for v in b['sections'].values())==b['total']
assert sum(v['decoded'] for v in b['sections'].values())==b['decoded']
assert len(s['trials'])==100
for t in s['trials']:
 assert t['total']==b['total'] and t['decoded']==b['decoded']
 assert t['changed_decoded_tokens']==b['decoded']
 assert t['output_vocabulary_set_unchanged'] and t['sorted_frequency_profile_unchanged']
 assert t['section_coverage_unchanged']
r=read('zfd_v3_reproduction.json');assert not r['published_differences']
assert len(r['configs'])==2
for c in r['configs'].values():
 assert c['discriminating_folios']==5 and c['hierarchy_holds']
 assert c['iterations_per_baseline']==30
v=read('zfd_v3_semantic.json'); n=0
for c in v.values():
 assert len(c['trials'])==20
 for t in c['trials']:
  for f,a in t['folios'].items():
   b=c['baseline'][f]
   assert a['changed_glosses']>0
   for k in ['total_tokens','known_stems','known_ratio','average_confidence','coherence']:
    assert a[k]==b[k],(f,k)
   formula=round(.30*a['known_ratio']+.25*min(len(a['operator_counts'])/5,1)+.25*min(len(a['category_counts'])/5,1)+.20*a['average_confidence'],4)
   assert formula==a['coherence']
   n+=1
assert n==200
c=read('zfd_canonical_semantic.json');assert len(c['trials'])==20
assert sum(v['stats']['total_words'] for v in c['baseline'].values())==1946
for f,b in c['baseline'].items():
 assert sum(b['stats'][k] for k in ['fully_resolved','partially_resolved','unknown'])==b['stats']['total_words']
 assert len(b['word_confidences'])==b['stats']['total_words']
 assert sum(x>=.7 for x in b['word_confidences'])==b['stats']['fully_resolved']
 assert sum(.3<=x<.7 for x in b['word_confidences'])==b['stats']['partially_resolved']
for t in c['trials']:
 assert len(t['folios'])==8
 for f,a in t['folios'].items():
  assert a['metrics_unchanged'] and 0<a['changed_glosses']<=a['total_tokens']
  assert a['total_tokens']==c['baseline'][f]['stats']['total_words']
manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
verified=0
for f in manifest:
 p=ROOT/f['local_path']
 if p.exists():
  data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==f['sha256'];verified+=1
summary={'scott_permutations_checked':100,'zfd_v3_semantic_folio_checks':200,
 'zfd_canonical_folio_checks':160,'canonical_tokens':1946,
 'upstream_files_hash_checked':verified,'status':'PASS'}
(ROOT/'results/verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
