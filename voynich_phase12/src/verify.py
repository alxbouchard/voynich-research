"""Independent breadth-first verification of all rule-only predictions."""
from pathlib import Path
import json,re,hashlib,collections
from analyse import ROOT,SEEDS,PREFIXES,corpus
def tok(word):return tuple(re.findall('cth|cph|cfh|ckh|sh|ch|ii|ee|.',word))
def independently_predict(word,prefixes):
 start=tuple(x for x in tok(word) if x not in ('cth','ckh','cph','cfh'))
 todo=collections.deque([start]);seen={start};found=set()
 while todo:
  state=todo.popleft();spelling=''.join(state)
  if spelling in SEEDS:found.add((spelling,SEEDS[spelling]))
  successors=[]
  for p in prefixes:
   prefix=tok(p)
   if state[:len(prefix)]==prefix and len(state)>len(prefix):successors.append(state[len(prefix):])
  successors.extend(state[:i]+state[i+1:] for i in range(1,len(state)-1) if state[i] in ('ch','f'))
  if state and state[-1] in ('t','g','p') and len(state)>1:successors.append(state[:-1])
  for s in successors:
   if s not in seen:seen.add(s);todo.append(s)
 return sorted(found)
def main():
 private=json.loads((ROOT/'tmp/candidates_private.json').read_text());result=json.loads((ROOT/'results/rule_audit.json').read_text())
 n=0
 for mode,preds in private.items():
  for word,pairs in preds.items():
   assert independently_predict(word,PREFIXES[mode])==[tuple(p) for p in pairs],(mode,word)
   n+=1
  stats=result['reconstructions'][mode]['all_prose']
  assert stats['has_candidate']+stats['no_candidate']==stats['total']
  assert stats['unique_candidate']+stats.get('ambiguous_candidates',0)==stats['has_candidate']
  assert stats['direct_seed_tokens']+stats['new_surface_tokens']==stats['has_candidate']
  assert stats['author_reading_in_candidates']+stats['author_reading_absent']==stats['author_comparable']
 manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
 for f in manifest:
  b=(ROOT/f['local_path']).read_bytes();assert len(b)==f['expected_bytes']
  assert hashlib.sha256(b).hexdigest()==f['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['blob_sha']
 out={'status':'PASS','predictions_independently_verified':n,'sources_hash_verified':len(manifest),
  'algorithm':'Breadth-first state enumeration, independently coded from recursive implementation.'}
 (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
