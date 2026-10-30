#!/usr/bin/env python3
"""Post-hoc source sensitivity: freeze ZL keys and apply to matched IT loci."""
import json
import run_syllabic as h
def main():
 summary=json.loads((h.OUT/'summary.json').read_text())
 zl=h.prev.parse('ZL3b-n.txt')[0];it=h.prev.parse('IT2a-n.txt')[0]
 itd={}
 for r in it:
  if not r['type'].startswith('P'):continue
  loc=r['locus'].split(',')[0];assert loc not in itd;itd[loc]=r
 results=[]
 for label,best in summary['best_post_hoc_within_inventory'].items():
  mapping={u:i for i,u in enumerate(best['symbols_ordered'])};mode=best['units'];direction=best['direction']
  chosen=[r for r in zl if r['type'].startswith('P') and r['metadata'].get('L')==best['subset'] and r['leaf'] in set(best['test_leaves'])]
  pairs=[(r,itd[r['locus'].split(',')[0]]) for r in chosen if r['locus'].split(',')[0] in itd]
  def encode(r):
   units=h.prev.units_from_raw(r['raw'],mode);seq=[mapping.get(u,-1) for u in units];lines=[];span=[]
   for x in seq:
    if x>=0:span.append(x)
    else:
     if len(span)>=4:lines.append(span)
     span=[]
   if len(span)>=4:lines.append(span)
   if direction=='reverse':lines=[s[::-1] for s in lines]
   return seq,lines
  srcz=[];srci=[];same=0;diffs=[]
  for a,b in pairs:
   az,za=encode(a);ai,ia=encode(b);srcz.extend(za);srci.extend(ia);same+=az==ai
   if az!=ai:diffs.append(a['locus'].split(',')[0])
  zm,_,_=h.metrics(srcz,best['key'],best['language'],best['kind']);im,_,_=h.metrics(srci,best['key'],best['language'],best['kind'])
  results.append({'model':label,'frozen_case':best['case'],'matched_loci':len(pairs),'zl_loci_without_IT':len(chosen)-len(pairs),'equal_encoded_unit_sequences':same,'differing_loci':diffs,'ZL_metrics_matched_loci':zm,'IT_metrics_matched_loci':im,'key_refitted':False})
 h.save(h.OUT/'transcription_sensitivity.json',{'status':'Post-hoc diagnostic, not an independent decipherment confirmation. ZL metadata defines selection. Source uncertainty can change scored spans and lengths. Equal processed unit sequences may contain unknown breaks. No new image reading certified.','cases':results})
 print(json.dumps([{'model':r['model'],'loci':r['matched_loci'],'equal':r['equal_encoded_unit_sequences'],'ZL_bits':r['ZL_metrics_matched_loci']['bits_per_four_units'],'IT_bits':r['IT_metrics_matched_loci']['bits_per_four_units']} for r in results],indent=2))
if __name__=='__main__':main()
