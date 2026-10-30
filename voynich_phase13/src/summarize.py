import json,platform,sys
from pathlib import Path
import numpy,scipy
from engine import ROOT
def main():
 ds=[json.loads(p.read_text()) for p in sorted((ROOT/'results').glob('*_s*_k*.json'))]
 lookup={(d['name'],d['seed'],d['steps']):d for d in ds};rows=[]
 for name in sorted(d['name'] for d in ds if d['kind']=='voynich' and not d['null'] and '_DEFAULT' in d['name'] and d['seed']==13010):
  a=lookup[(name,13010,5000)];b=lookup[(name+'_null',13010,5000)];r=lookup[(name,13011,5000)]
  mapping_agree=sum(set(a['mapping'][s])==set(r['mapping'][s]) for s in a['mapping'])
  inter=sum(len(set(a['mapping'][s])&set(r['mapping'][s])) for s in a['mapping'])
  union=sum(len(set(a['mapping'][s])|set(r['mapping'][s])) for s in a['mapping'])
  rows.append({'case':name,'test_types':a['test_scored_types'],'distance':a['heldout_mean_distance'],
   'null_distance':b['heldout_mean_distance'],'improvement':b['heldout_mean_distance']-a['heldout_mean_distance'],
   'repeat_distance':r['heldout_mean_distance'],'mapping_signs_agree':mapping_agree,'mapping_signs_total':len(a['mapping']),
   'mapping_jaccard':inter/union,'exact_lexicon_matches':round(a['heldout_exact_fraction']*a['test_scored_types']),
   'ambiguous_signs':sum(len(v)>1 for v in a['mapping'].values())})
 controls=[{k:d[k] for k in ['name','steps','seed','energy','test_scored_types','heldout_unique_correct','heldout_accuracy'] if k in d} for d in ds if d['kind']=='control']
 bench=next(d for d in ds if d['kind']=='benchmark')
 summary={'real_fit_runs':sum(d['kind']=='voynich' for d in ds),'all_fit_runs':len(ds),'energy_evaluations':sum(d['evaluations'] for d in ds),
  'cpu_fit_seconds_sum':sum(d['seconds'] for d in ds),'controls':controls,'benchmark':{k:bench[k] for k in ['benchmark_cognate_correct','benchmark_cognate_total','benchmark_accuracy','steps']},
  'default_cases':rows,'no_validated_translation':True,'not_run':['image clustering','joint phonetic segmentation'],
  'conclusion':'Lexicon proximity can generalize versus within-word permutations; no semantic validation. Key stability and limited historical lexica preclude decipherment claims.'}
 (ROOT/'results/summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
 (ROOT/'data/environment.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'scipy':scipy.__version__},indent=2))
 print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
