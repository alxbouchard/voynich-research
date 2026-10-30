#!/usr/bin/env python3
"""Independent score/accuracy/holdout checks and complete non-translation outputs."""
import collections, hashlib, json, math
from pathlib import Path
import numpy as np
import run_homophonic as h

def main():
 controls=json.loads((h.OUT/'controls_summary.json').read_text())
 rows=json.loads((h.OUT/'real_summary.json').read_text())
 assert len(controls)==4 and len(rows)==32
 assert len({r['case'] for r in rows})==32
 assert h.units_from_raw('aaa.[ch:sh]eee.ccc','EVA')==list('aaa?eeeccc')
 assert h.units_from_raw('ch.iin.[a:o]d.<->sh.@123;','COMPOSED')==['ch','iin','?','d','?','sh','?']
 assert h.units_from_raw('c,h.ch','COMPOSED')==['c','h','ch']
 assert h.units_from_raw("abcd?efgh'ijkl",'EVA')==list('abcd?efgh?ijkl')
 def readlines(name,part):return [[int(x) for x in s.split()] for s in (h.DATA/(name+'_'+part+'.txt')).read_text().splitlines()]
 for r in controls+rows:
  lm=np.fromfile(h.DATA/(r['language']+'_lm.bin'));q=np.loadtxt(h.DATA/(r['language']+'_freq.txt'))
  for part,record in [('train','train_metrics'),('test','test_metrics')]:
   lines=readlines(r['case'],part);m,decoded=h.metrics(lines,r['key'],lm,q)
   for k,v in m.items():assert abs(v-r[record][k])<1e-10
   if part=='train':
    obj=-m['quadgrams']*m['bits_per_quadgram']-r['lambda']*m['chars']*m['kl_to_model_bits']
    assert abs(obj-r['training_objective'])<1e-6*m['chars']
  if r['control']:
   truth=json.loads((h.DATA/(r['case']+'_truth.json')).read_text());expected=''.join(truth['truth_test']);actual=''.join(decoded)
   assert len(expected)==len(actual)
   err=sum(x!=y for x,y in zip(expected,actual));assert err==r['heldout_errors']
   assert abs((1-err/len(expected))-r['heldout_character_accuracy'])<1e-12
   assert r['heldout_character_accuracy']>=.95
   r['confusions']={a:sorted({r['key'][i] for i in ids}) for a,ids in truth['encryption_homophones'].items() if any(r['key'][i]!=a for i in ids)}
  elif not r['shuffled']:
   assert not set(r['train_leaf_pool'])&set(r['test_leaves'])
   assert r['symbols']==len(r['symbols_ordered'])
   assert {x for line in readlines(r['case'],'train') for x in line}==set(range(r['symbols']))
   r['decoded_symbol_groups']={a:[s for s,t in zip(r['symbols_ordered'],r['key']) if t==a] for a in sorted(set(r['key']))}
   (h.OUT/(r['case']+'_candidate_NOT_A_TRANSLATION.txt')).write_text('CANDIDATE AUTOMATIQUE. AUCUNE TRADUCTION VALIDEE.\n'+ '\n'.join(decoded)+'\n')
   null=next(n for n in rows if n['case']==r['case'].replace('voynich_','null_',1))
   for part in ['train','test']:
    a=readlines(r['case'],part);b=readlines(null['case'],part)
    assert len(a)==len(b)
    assert all(collections.Counter(x)==collections.Counter(y) for x,y in zip(a,b))
   r['matched_null_bits']=null['test_metrics']['bits_per_quadgram']
   r['null_minus_real_bits']=r['matched_null_bits']-r['test_metrics']['bits_per_quadgram']
 real=[r for r in rows if not r['shuffled']]
 best={lang:min([r for r in real if r['language']==lang],key=lambda r:r['test_metrics']['bits_per_quadgram']) for lang in ['latin','italian']}
 summary={'date':'2026-10-28','verdict':'Aucune traduction validée. Comparaison exploratoire limitée à une clé homophonique fixe et deux modèles de langue.','controls':controls,'real':real,'best_post_hoc':best,'verification':'PASS','matched_nulls':16,'all_16_real_better_than_matched_null':all(r['null_minus_real_bits']>0 for r in real),'calibration_changes':[],'assumptions':'Currier A/B separate keys; 24k fit cap; grouped leaf test; unknown glyph variants hard breaks; reverse means each retained span reversed, not manuscript page order.'}
 h.save(h.OUT/'summary.json',summary)
 h.save(h.OUT/'verification.json',{'status':'PASS','checks':['4 control accuracies independently recalculated','36 solver objectives recomputed in Python','all train/test statistics recomputed','16 within-line null histograms match train and test','16 real cases have disjoint leaf pools','parser does not choose explicit alternatives','all key symbols present in fit and output index valid'],'not_verified':['meaning of any Voynich candidate','independent paleographic reading of all glyphs','general impossibility of homophonic or other ciphers']})
 sourcepaths=[h.BASE/'data/ZL3b-n.txt',h.BASE/'data/IT2a-n.txt',h.BASE/'controls/input/nathist_book16.txt',h.P2/'data/caesar.xml',h.P2/'data/dante.txt']
 h.save(h.ROOT/'SOURCES.json',{'date':'2026-10-28','sha256':{str(p.relative_to(h.ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},'source_metadata':'Original descriptions retained in voynich_20261028/SOURCES.json and voynich_phase2/SOURCES_AND_LIMITS.json','background_references':[{'author':'Nils Kopal','year':2019,'title':'Cryptanalysis of Homophonic Substitution Ciphers Using Simulated Annealing with Fixed Temperature','url':'https://ep.liu.se/en/conference-article.aspx?Article_No=12&issue=158&series=','role':'Background; our implementation uses cooling and a unigram penalty, not an exact replication.'},{'authors':'Kambhatla, Born, Sarkar','year':2023,'title':'Decipherment as Regression: Solving Historical Substitution Ciphers by Learning Symbol Recurrence Relations','url':'https://aclanthology.org/2023.findings-eacl.160/','role':'Possible future comparison; neural method NOT implemented here.'}],'licenses':'Caesar XML and derived normalized Latin model corpus: CC BY-SA 4.0, Perseus Digital Library. Greshko input corpora license and mandatory article citation retained. Manuscript transcription credits retained in original headers.'})
 print(json.dumps({'verification':'PASS','best_cases':{k:{'case':v['case'],'bits':v['test_metrics']['bits_per_quadgram'],'letters':v['test_metrics']['output_distinct_letters'],'null':v['matched_null_bits']} for k,v in best.items()},'controls':[{k:r[k] for k in ['case','heldout_character_accuracy','heldout_errors','confusions']} for r in controls]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
