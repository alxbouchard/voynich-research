#!/usr/bin/env python3
import collections,hashlib,json,sys
from pathlib import Path
import numpy as np
import run_syllabic as h
def readlines(name,part):return [[int(x) for x in s.split()] for s in (h.DATA/f'{name}_{part}.txt').read_text().splitlines()]
def join_diagnostics(decoded,inventory):
 pairs={s for s in inventory if len(s)==2};bad=0;total=0;badsegments=0
 for line in decoded:
  errors=sum(len(inventory[a])==len(inventory[b])==1 and inventory[a]+inventory[b] in pairs for a,b in zip(line,line[1:]))
  bad+=errors;total+=len(line)-1;badsegments+=errors>0
 return {'illegal_singleton_joins':int(bad),'boundaries':total,'illegal_join_rate':bad/total,'noncanonical_segments':int(badsegments),'two_letter_unit_fraction':sum(len(inventory[x])==2 for line in decoded for x in line)/sum(map(len,decoded))}
def main():
 controls=json.loads((h.OUT/'controls_summary.json').read_text());rows=json.loads((h.OUT/'real_summary.json').read_text());gate=json.loads((h.OUT/'validation_gate.json').read_text())
 assert len(controls)==8 and len(rows)==64 and len(gate['allowed_models'])==4
 assert len({r['case'] for r in rows})==64
 assert h.prev.units_from_raw('ch.[a:o]iin.<->sh.@123;','COMPOSED')==['ch','?','iin','?','sh','?']
 assert h.prev.units_from_raw('c,h.ch','COMPOSED')==['c','h','ch']
 models={}
 for lang in ['latin','italian']:
  for kind in ['CV','VC']:
   model=json.loads((h.DATA/f'{lang}_{kind}_dictionary.json').read_text());inv=model['inventory'];models[lang+'_'+kind]=model
   assert len(inv)==32 and len(set(inv))==32 and all(1<=len(x)<=2 for x in inv)
   for part in ['train','target']:
    source=(h.P4/'data'/f'{lang}_{part}.txt').read_text();assert hashlib.sha256(source.encode()).hexdigest()==model[part+'_sha256']
    tokenized=h.tokenize(source,inv);assert ''.join(inv[x] for x in tokenized)==source
    assert join_diagnostics([tokenized],inv)['illegal_singleton_joins']==0
 for r in controls+rows:
  inv=models[r['language']+'_'+r['kind']]['inventory']
  for part,label in [('train','train_metrics'),('test','test_metrics')]:
   lines=readlines(r['case'],part);m,decoded,text=h.metrics(lines,r['key'],r['language'],r['kind'])
   for k,v in m.items():assert abs(v-r[label][k])<1e-10
   if part=='train':
    obj=-m['quadgrams']*m['bits_per_four_units']-r['lambda']*m['units']*m['kl_to_model_bits'];assert abs(obj-r['training_objective'])<1e-6*m['units']
  diagnostic=join_diagnostics(decoded,inv)
  assert diagnostic['noncanonical_segments']==m['segments']-m['canonical_segments']
  assert abs(diagnostic['two_letter_unit_fraction']-(m['characters_per_unit']-1))<1e-12
  r['segmentation_diagnostics']=diagnostic
  if r['control']:
   truth=json.loads((h.DATA/f'{r["case"]}_truth.json').read_text());expected=truth['truth_test']
   assert all(h.tokenize(''.join(inv[x] for x in s),inv)==s for s in expected)
   error=sum(a!=b for e,d in zip(expected,decoded) for a,b in zip(e,d));n=sum(map(len,expected));assert [len(s) for s in decoded]==[len(s) for s in expected]
   assert error==r['heldout_unit_errors'] and abs(1-error/n-r['heldout_unit_accuracy'])<1e-12
   assert r['heldout_unit_accuracy']>=.95
   r['confusions']={inv[int(x)]:sorted({inv[r['key'][i]] for i in codes}) for x,codes in truth['encryption_homophones'].items() if any(r['key'][i]!=int(x) for i in codes)}
  elif not r['shuffled']:
   assert not set(r['fit_leaf_pool'])&set(r['test_leaves'])
   assert {x for s in readlines(r['case'],'train') for x in s}==set(range(r['symbols']))
   assert r['symbols']==len(r['symbols_ordered'])
   r['decoding_map']={u:inv[t] for u,t in zip(r['symbols_ordered'],r['key'])}
   (h.OUT/f'{r["case"]}_candidate_NOT_A_TRANSLATION.txt').write_text('CANDIDAT AUTOMATIQUE. AUCUNE TRADUCTION VALIDEE.\n'+ '\n'.join(text)+'\n')
   null=next(x for x in rows if x['case']==r['case'].replace('voynich_','null_',1));r['matched_null_bits']=null['test_metrics']['bits_per_four_units'];r['null_minus_real']=r['matched_null_bits']-r['test_metrics']['bits_per_four_units']
   for part in ['train','test']:
    a=readlines(r['case'],part);b=readlines(null['case'],part)
    assert len(a)==len(b) and all(collections.Counter(x)==collections.Counter(y) for x,y in zip(a,b))
 real=[r for r in rows if not r['shuffled']]
 best={lang+'_'+kind:min([r for r in real if r['language']==lang and r['kind']==kind],key=lambda r:r['test_metrics']['bits_per_four_units']) for lang in ['latin','italian'] for kind in ['CV','VC']}
 summary={'date':'2026-10-28','verdict':'Aucune traduction validée. Test exploratoire de quatre inventaires limités, non une réfutation des chiffres syllabiques.','controls':controls,'real':real,'best_post_hoc_within_inventory':best,'models':models,'calibration_changes':[],'verification':'PASS','real_count':len(real),'null_count':32,'all_beat_matched_null':all(r['null_minus_real']>0 for r in real),'real_full_canonical_count':sum(r['test_metrics']['canonical_segment_fraction']==1 for r in real),'real_two_letter_fraction_min':min(r['segmentation_diagnostics']['two_letter_unit_fraction'] for r in real),'real_two_letter_fraction_max':max(r['segmentation_diagnostics']['two_letter_unit_fraction'] for r in real)}
 h.save(h.OUT/'summary.json',summary)
 h.save(h.OUT/'verification.json',{'status':'PASS','checked':['72 C++ objectives independently recomputed in Python','8 control unit accuracies and exact plaintext flags','4 dictionaries; complete source tokenization roundtrips; source hashes','32 null histograms paired with identical segment lengths','32 keys fit on disjoint physical leaf pools','2 independent canonical segmentation checks agree on all 72 tests','ambiguous readings and rare signs cause stream breaks'],'not_verified':['meaning of any Voynich candidate','general completeness of a syllabic cipher search','new image-based transcription']})
 print(json.dumps({k:summary[k] for k in ['verification','real_count','null_count','all_beat_matched_null','real_full_canonical_count','real_two_letter_fraction_min','real_two_letter_fraction_max']}|{'best':{k:{'case':v['case'],'two_letter_fraction':v['segmentation_diagnostics']['two_letter_unit_fraction'],'canonical':v['test_metrics']['canonical_segment_fraction'],'bits':v['test_metrics']['bits_per_four_units']} for k,v in best.items()}},indent=2))
if __name__=='__main__':main()
