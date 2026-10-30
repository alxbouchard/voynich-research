#!/usr/bin/env python3
import collections,concurrent.futures,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P5=ROOT.parent/'voynich_phase5'
sys.path.insert(0,str(P5));import run_syllabic as p5
sys.path.insert(0,str(P5))
from verify_and_summarize import join_diagnostics
OUT=ROOT/'results';DATA=ROOT/'data';SEED=20261030
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def lines(name,part):return [[int(x) for x in l.split()] for l in (P5/'data'/f'{name}_{part}.txt').read_text().splitlines()]
def prepare():
 if not all((P5/'data'/f'{l}_{k}_lm.bin').exists() for l in ['latin','italian'] for k in ['CV','VC']):p5.models()
 for l in ['latin','italian']:
  for k in ['CV','VC']:
   d=json.loads((P5/'data'/f'{l}_{k}_dictionary.json').read_text());(DATA/f'{l}_{k}_vocabulary.txt').write_text('\n'.join(d['inventory'])+'\n')
def run_case(base,restarts=8,steps=60000,temp=.002,tag='initial'):
 name=base['case'];lang=base['language'];kind=base['kind'];out=OUT/f'{tag}_{name}.json'
 if out.exists() and '--force' not in sys.argv:return json.loads(out.read_text())
 cmd=[str(ROOT/'src/constrained'),str(P5/'data'/f'{lang}_{kind}_lm.bin'),str(P5/'data'/f'{lang}_{kind}_freq.txt'),str(P5/'data'/f'{name}_train.txt'),str(restarts),str(steps),str(SEED),'4',str(temp),str(DATA/f'{lang}_{kind}_vocabulary.txt')]
 if tag=='warm':
  initial=DATA/f'{name}_phase5_learned_key.txt';initial.write_text(' '.join(map(str,base['key']))+'\n')
  cmd[0]=str(ROOT/'src/constrained_warm');cmd.append(str(initial))
 start=time.time();proc=subprocess.run(cmd,capture_output=True,text=True,check=True);r=json.loads(proc.stdout)
 inv=json.loads((P5/'data'/f'{lang}_{kind}_dictionary.json').read_text())['inventory']
 tm,td,_=p5.metrics(lines(name,'train'),r['key'],lang,kind);vm,vd,vt=p5.metrics(lines(name,'test'),r['key'],lang,kind)
 diag=join_diagnostics(vd,inv);assert tm['canonical_segment_fraction']==1 and join_diagnostics(td,inv)['illegal_singleton_joins']==0
 obj=-tm['quadgrams']*tm['bits_per_four_units']-4*tm['units']*tm['kl_to_model_bits'];assert abs(obj-r['training_objective'])<1e-6*tm['units']
 r.update(case=name,run_tag=tag,language=lang,kind=kind,seconds=round(time.time()-start,2),settings={'restarts':restarts,'steps':steps,'temperature':temp,'seed':SEED,'lambda':4},train_metrics=tm,test_metrics=vm,test_segmentation=diag,baseline_phase5_test_metrics=base['test_metrics'],control=base['control'],candidate_preview_NOT_A_TRANSLATION='\n'.join(vt)[:900])
 r['training_units']=r.pop('training_chars')
 if base['control']:
  truth=json.loads((P5/'data'/f'{name}_truth.json').read_text())['truth_test'];a=[x for s in vd for x in s];b=[x for s in truth for x in s];assert len(a)==len(b)
  r['heldout_unit_errors']=sum(x!=y for x,y in zip(a,b));r['heldout_unit_accuracy']=1-r['heldout_unit_errors']/len(a)
  r['full_plaintext_exact']=''.join(vt)==''.join(inv[x] for x in b)
 else:
  r.update({k:base[k] for k in ['subset','units','direction','symbols_ordered','fit_leaf_pool','test_leaves','shuffled']})
  assert not set(r['fit_leaf_pool'])&set(r['test_leaves'])
  if not r['shuffled']:
   (OUT/f'{tag}_{name}_candidate_NOT_A_TRANSLATION.txt').write_text('CANDIDAT AUTOMATIQUE, AUCUNE TRADUCTION VALIDEE.\n'+'\n'.join(vt)+'\n')
   r['decoding_map']={u:inv[x] for u,x in zip(r['symbols_ordered'],r['key'])}
 save(out,r);print(json.dumps({'case':name,'tag':tag,'seconds':r['seconds'],'accuracy':r.get('heldout_unit_accuracy'),'train_feasible':True,'test_canonical':vm['canonical_segment_fraction'],'bits':vm['bits_per_four_units']}),flush=True);return r
def main():
 prepare();base=json.loads((P5/'results/controls_summary.json').read_text())
 if '--controls' in sys.argv:
  temp=.002;tag='initial';steps=60000;restarts=8
  if '--hot' in sys.argv:temp=.02;tag='hot';steps=120000;restarts=12
  if '--warm' in sys.argv:temp=.002;tag='warm';steps=60000;restarts=8
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(lambda b:run_case(b,temp=temp,tag=tag,steps=steps,restarts=restarts),base))
  save(OUT/f'{tag}_controls_summary.json',res)
 elif '--real' in sys.argv:
  chosen=json.loads((DATA/'selected_settings.json').read_text());tag=chosen['tag'];ctl=json.loads((OUT/f'{tag}_controls_summary.json').read_text())
  allowed={(l,k) for l in ['latin','italian'] for k in ['CV','VC'] if all(r['heldout_unit_accuracy']>=.95 for r in ctl if r['language']==l and r['kind']==k)}
  assert len(ctl)==8
  save(OUT/'validation_gate.json',{'allowed_models':sorted(allowed),'threshold':.95,'test_segmentation_not_a_gate':'reported separately; never used to impose fitting constraints'})
  rows=[r for r in json.loads((P5/'results/real_summary.json').read_text()) if (r['language'],r['kind']) in allowed]
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(lambda b:run_case(b,tag=tag,restarts=chosen['restarts'],steps=chosen['steps'],temp=chosen['temperature']),rows))
  save(OUT/'constrained_real_summary.json',res)
if __name__=='__main__':main()
