#!/usr/bin/env python3
import collections, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent

def rd(p):return json.loads(p.read_text())
def verify():
 raw=rd(ROOT/'data/source_inputs.json');z=collections.defaultdict(list);it=collections.defaultdict(list)
 for item in raw['ZL']:z[item['locus']].append(item)
 for item in raw['IT']:it[item['locus']].append(item)
 pred={(r['locus'],r['span']):r for r in rd(ROOT/'data/source_predictions.json')}
 expected={}
 for loc,a in z.items():
  if len(a)!=1 or len(it[loc])!=1 or a[0]['text']!=it[loc][0]['text']:continue
  for j,label in enumerate(a[0]['labels']):
   if label==2:expected[(loc,a[0]['span'],j+1)]=(it[loc][0]['labels'][j],pred[loc,a[0]['span']]['four'][j])
 pairs=rd(ROOT/'data/paired_uncertain.json');observed={(r['locus'],r['span'],r['offset']):(r['IT_label'],r['p4']) for r in pairs}
 assert len(expected)==1089 and observed==expected
 ct=collections.Counter((int(p>=.5),y) for y,p in expected.values());assert ct=={(0,0):280,(0,1):264,(1,0):109,(1,1):436}
 pos=[p for y,p in expected.values() if y];neg=[p for y,p in expected.values() if not y]
 auc=sum((a>b)+.5*(a==b) for a in pos for b in neg)/(len(pos)*len(neg))
 s=rd(ROOT/'results/transfer_summary.json')['all'];assert abs(s['auc']-auc)<1e-12;assert abs(s['agreement']-716/1089)<1e-12
 extreme=[(y,p) for y,p in expected.values() if p<=.1 or p>=.9];assert len(extreme)==319 and sum((p>=.5)!=y for y,p in extreme)==67
 audit=rd(ROOT/'results/image_audit.json')['items'];assert len(audit)==7
 for a in audit:
  source=ROOT/'data'/f"{a['oid']}.jpg";assert hashlib.sha256(source.read_bytes()).hexdigest()==a['source_sha256']
  x0,y0,x1,y1=a['bbox_xyxy'];im=Image.open(source);assert 0<=x0<x1<=im.width and 0<=y0<y1<=im.height
  assert x0<a['boundary_x_approx']<x1
  assert np.array_equal(np.array(im.crop(a['bbox_xyxy'])),np.array(Image.open(ROOT/a['crop_file'])))
  p=pred[a['locus'],a['span']];assert p['labels'][a['offset']-1]==2 and p['four'][a['offset']-1]==a['p4']
 ledger=[];attached={(r['locus'],r['span'],r['offset']):r for r in audit}
 for r in pred.values():
  for i,y in enumerate(r['labels']):
   if y!=2:continue
   key=(r['locus'],r['span'],i+1);t=observed.get(key);a=attached.get(key)
   ledger.append({'locus':key[0],'span':key[1],'offset_in_retained_stream':key[2],'original_separator':',','text':r['text'],'p4_frozen_phase7':r['four'][i],'IT_label_strict_matched_span':t[0] if t else None,'image_audit_id':a['id'] if a else None,'IT_label_local_assisted_review':int(a['IT_target_split']) if a else None,'status':'UNCERTAIN_PRESERVED','automatic_correction':False})
 assert len(ledger)==2394 and sum(r['image_audit_id'] is not None for r in ledger)==7
 (ROOT/'results/transcription_variant_ledger.json').write_text(json.dumps({'warning':'No corrected or translated text. Scores do not measure semantic truth. Offsets refer to retained phase7 glyph streams, not full raw loci. IT strict pairing and local visual-assisted review are separate evidence channels.','count':len(ledger),'items':ledger},indent=2)+'\n')
 out={'status':'PASS','exact_pairs':1089,'independent_pairwise_auc_comparisons':len(pos)*len(neg),'auc':auc,'correct_predictions_against_IT':716,'high_certainty_disagreements_with_IT':67,'exact_pixel_crops_verified':7,'source_image_hashes_verified':4,'uncertain_boundaries_preserved':2394,'automatic_corrections':0,'limits':'Verifies data, calculations, cropping and provenance, not correctness of manual glyph identification.'}
 (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':verify()
