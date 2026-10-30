import json,statistics
from pathlib import Path
P=Path(__file__).resolve().parent/'results'
rows=json.loads((P/'real_permutation_summary.json').read_text());out=[]
for r in rows:
 if r['null_index'] is not None:continue
 ns=[s['gain_bits'] for s in rows if s['name'].startswith(r['name']+'_null')];row=dict(r)
 if ns:row['null']={'n':len(ns),'mean':statistics.mean(ns),'min':min(ns),'max':max(ns),'at_least_observed':sum(x>=r['gain_bits'] for x in ns),'note':'Descriptive counts only; no p-value or claim of calibrated significance.'}
 out.append(row)
(P/'report_summary.json').write_text(json.dumps(out,indent=2)+'\n')
