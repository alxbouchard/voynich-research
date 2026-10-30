#!/usr/bin/env python3
"""Paired-transcription audit and independent recomputation of published ink-gap data."""
import collections,csv,json,math,sys
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import research as h
def read(p):return json.loads(p.read_text())
def main():
 data=read(ROOT/'data/inputs.json');paired=[];cells=collections.Counter()
 # Only complete single-span lines, with exactly equal letter stream, can be aligned without guessing.
 z=collections.defaultdict(list);it=collections.defaultdict(list)
 for r in data['ZL']:z[r['locus']].append(r)
 for r in data['IT']:it[r['locus']].append(r)
 for loc,rr in z.items():
  if len(rr)!=1 or len(it.get(loc,[]))!=1:continue
  a,b=rr[0],it[loc][0]
  if a['text']!=b['text']:continue
  for i,(x,y) in enumerate(zip(a['labels'],b['labels'])):cells[(x,y)]+=1
  paired.append({'locus':loc,'page':a['page'],'group':a['group'],'characters':len(a['text'])})
 h.save(ROOT/'results/paired_transcriptions.json',{'matched_lines':len(paired),'matching_rule':'One surviving span per locus, exactly equal letter stream. This may be a fragment if both transcriptions contain the same excluded edge. It is not a claim that all source lines are complete.','confusion_counts':{f'{x}->{y}':n for (x,y),n in sorted(cells.items())},'lines':paired})
 rows=list(csv.DictReader((ROOT/'data/published_ink_gaps.csv').open()));accepted=[r for r in rows if r['include']=='True'];sure=[float(r['gap_px']) for r in accepted if r['label']=='.'];weak=[float(r['gap_px']) for r in accepted if r['label']==',']
 per=[]
 for folio in sorted({r['folio'] for r in accepted}):
  a=[float(r['gap_px']) for r in accepted if r['folio']==folio and r['label']=='.'];b=[float(r['gap_px']) for r in accepted if r['folio']==folio and r['label']==',']
  per.append({'folio':folio,'certain_n':len(a),'uncertain_n':len(b),'mean_certain':float(np.mean(a)) if a else None,'mean_uncertain':float(np.mean(b)) if b else None,'difference':float(np.mean(a)-np.mean(b)) if a and b else None})
 labels=[r['label']=='.' for r in accepted];gaps=[float(r['gap_px']) for r in accepted]
 out={'source':'Rozanova and Temerev arXiv:2608.17096v1, published direct_pixel/results_unblinded.csv, not new image measurements','source_rows':len(rows),'accepted':len(accepted),'excluded':len(rows)-len(accepted),'certain_n':len(sure),'uncertain_n':len(weak),'mean_certain':float(np.mean(sure)),'mean_uncertain':float(np.mean(weak)),'median_certain':float(np.median(sure)),'median_uncertain':float(np.median(weak)),'difference':float(np.mean(sure)-np.mean(weak)),'ink_gap_auc':float(roc_auc_score(labels,gaps)),'by_folio':per,'limits':'Only six folios, 21 accepted uncertain gaps. Existing author measurements and exclusions, not an independent blind audit. Pixels refer to 700-pixel image derivatives.'}
 assert len(sure)==265 and len(weak)==21 and round(out['difference'],2)==1.84
 h.save(ROOT/'results/published_ink_gap_reanalysis.json',out)
 # Quire-clustered intervals for space-recovery precision and recall, no refitting.
 reports={}
 for name in ['ZL','IT']:
  pred=read(ROOT/'results'/f'{name}_predictions.json');group=collections.defaultdict(lambda:np.zeros(3,dtype=int));candidates=[]
  for r in pred:
   labels=np.array(r['labels']);p=np.array(r['four']);known=labels!=2;yy=labels[known];hat=p[known]>=.5
   group[r['group']]+=np.array([((yy==1)&hat).sum(),hat.sum(),yy.sum()])
   if name=='ZL':
    for i,(y,v) in enumerate(zip(r['labels'],r['four'])):
     if y==2:
      candidates.append({'locus':r['locus'],'page':r['page'],'group':r['group'],'span':r['span'],'offset':i+1,'left_context':r['text'][max(0,i-14):i+1],'right_context':r['text'][i+1:i+16],'predicted_space_probability':v})
  arr=np.array(list(group.values()));rng=np.random.default_rng(h.SEED);draw=[]
  for _ in range(2000):
   a=arr[rng.integers(len(arr),size=len(arr))].sum(axis=0);draw.append([a[0]/a[1],a[0]/a[2]])
  reports[name]={'clusters':len(arr),'precision_ci':np.quantile(np.array(draw)[:,0],[.025,.975]).tolist(),'recall_ci':np.quantile(np.array(draw)[:,1],[.025,.975]).tolist(),'type':'Cluster bootstrap of out-of-fold predictions, no refitting; overlapping training folds limit inferential independence.'}
  if candidates:
   candidates.sort(key=lambda x:(x['predicted_space_probability'],x['locus'],x['offset']));h.save(ROOT/'results/uncertain_review_queue.json',{'warning':'Model suggestions only; not corrected readings. Low probability means graphically internal-like, not proof that a space is absent. Post-hoc queue, requires image reading.','lowest20':candidates[:20],'highest20':candidates[-20:]})
 h.save(ROOT/'results/prediction_intervals.json',reports)
 print(json.dumps({'paired_lines':len(paired),'confusion':{f'{a}->{b}':v for (a,b),v in cells.items()},'ink':{k:out[k] for k in ['certain_n','uncertain_n','mean_certain','mean_uncertain','difference','ink_gap_auc']},'prediction_intervals':reports},indent=2))
if __name__=='__main__':main()
