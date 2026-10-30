"""Rule-only candidate propagation; upstream glossary used only after prediction."""
import re,json,hashlib,collections,functools
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
SEEDS=dict(zip('chedy shedy chol shol cheol sheol chor shor chey shey cheos shy daiin okaiin qokol okal oly kol'.split(),
 'DEUS HEUS DAT HABET DEDIT HERBA DEA HORAM DES HEC DEOS HIC OLEUM FOCUM NOCET FACIT FLOS GRATIA'.split()))
DIGRAPHS=('cth','cph','cfh','ckh','sh','ch','ii','ee')
GALLOWS={'cth','ckh','cph','cfh'}
PREFIXES={'original':['d','l','ol','p','op','ch'],
 'extended':['o','d','l','p','ol','op','ch','sh','s','k','qo']}
def tokens(s):
 result=[];i=0
 while i<len(s):
  t=next((x for x in DIGRAPHS if s.startswith(x,i)),s[i]);result.append(t);i+=len(t)
 return tuple(result)
def strip(s):return ''.join(x for x in tokens(s) if x not in GALLOWS)
def decoder(seeds,prefixes):
 """Build a decoder that has no access to the upstream full glossary."""
 initials=tuple(tokens(p) for p in prefixes)
 @functools.lru_cache(None)
 def descend(state):
  word=''.join(state); readings=set()
  if word in seeds:readings.add((word,seeds[word]))
  next_states=set()
  for prefix in initials:
   if len(state)>len(prefix) and state[:len(prefix)]==prefix:next_states.add(state[len(prefix):])
  for i,t in enumerate(state):
   if 0<i<len(state)-1 and t in ('ch','f'):next_states.add(state[:i]+state[i+1:])
  if len(state)>1 and state[-1] in ('t','g','p'):next_states.add(state[:-1])
  for nxt in next_states:readings.update(descend(nxt))
  return frozenset(readings)
 def decode(word):return descend(tuple(t for t in tokens(word) if t not in GALLOWS))
 return decode
def corpus():
 rows=[];counts=collections.Counter()
 text=(ROOT/'tmp/vendor/scott/tools/eva-data/eva_takahashi.txt').read_text()
 for line in text.splitlines():
  m=re.match(r'^<(f\d+[rv]\d?)\.(\d+),([^>]+)>\s+(.+)',line)
  if not m:continue
  folio,ln,kind,body=m.groups()
  if len(kind)<2 or kind[1]!='P':continue
  counts['prose_lines']+=1
  body=body.replace('<->','.');body=re.sub(r'<[^>]*>','',body);body=re.sub(r'\{[^}]*\}','',body)
  for index,raw in enumerate(body.split('.')):
   w=raw.strip()
   if not w:continue
   counts['raw_prose_tokens']+=1
   if not re.fullmatch('[a-z]+',w):counts['excluded_uncertain_or_other']+=1;continue
   rows.append({'folio':folio,'locus':f'{folio}.{ln}', 'position':index+1,'word':w})
 counts['retained_tokens']=len(rows);counts['retained_types']=len({x['word'] for x in rows})
 return rows,dict(counts)
def metrics(rows,predict,gloss):
 c=collections.Counter(total=len(rows));ambig=[];mismatches=[]
 for row in rows:
  w=row['word'];pairs=predict(w);values={v for k,v in pairs}
  if not values:c['no_candidate']+=1;continue
  c['has_candidate']+=1
  c['unique_candidate' if len(values)==1 else 'ambiguous_candidates']+=1
  if w in SEEDS:c['direct_seed_tokens']+=1
  else:c['new_surface_tokens']+=1
  author=gloss.get(w) or gloss.get(strip(w))
  if author:
   c['author_comparable']+=1
   if author in values:c['author_reading_in_candidates']+=1
   else:c['author_reading_absent']+=1;mismatches.append(row)
   if len(values)==1:
    c['unique_comparable']+=1
    c['unique_agree' if author in values else 'unique_disagree']+=1
  if len(values)>1:ambig.append(row)
 return dict(c)
def main():
 raw=json.loads((ROOT/'tmp/upstream_private.json').read_text());gloss=raw['gloss']
 rows,counts=corpus();freq=collections.Counter(r['word'] for r in rows)
 for w,d in raw['entries'].items():assert strip(w)==d['stripped'],w
 direct=[(w,d) for w,d in raw['entries'].items() if d['stripped']!=w]
 comparable=[(w,d) for w,d in direct if d['after']]
 conflicts=[(w,d) for w,d in comparable if d['decoded']!=d['after']]
 changed_existing=sum(freq[w] for w,d in conflicts)
 retained_sg=[r for r in rows if strip(r['word'])!=r['word']]
 mapped_sg=[r for r in retained_sg if gloss.get(r['word']) or gloss.get(strip(r['word']))]
 rule_missing=[r for r in mapped_sg if not gloss.get(strip(r['word']))]
 null_result={'all_dictionary_entries':len(gloss),'entries_with_gallows':len(direct),
  'entries_both_readings_defined':len(comparable),'entries_conflicting':len(conflicts),
  'retained_prose_gallows_tokens':len(retained_sg),'originally_mapped_gallows_tokens':len(mapped_sg),
  'tokens_lost_by_strip_first':len(rule_missing),'comparable_gallows_tokens':len(mapped_sg)-len(rule_missing),
  'tokens_with_changed_reading':changed_existing,
  'conflicting_observed_types':sum(freq[w]>0 for w,d in conflicts),
  'examples':[{'eva':w,'stripped':d['stripped'],'before':d['decoded'],'after':d['after'],'occurrences':freq[w]}
   for w,d in sorted(conflicts,key=lambda x:(-freq[x[0]],x[0]))[:5]]}
 results={'source_commit':'71f2f3c91e9113d285ab21e024f1dd70c1f43c44','parser':counts,
  'original_parser':raw['original_parser'],'null_rule':null_result,'reconstructions':{}}
 private={}
 for name,prefixes in PREFIXES.items():
  predict=decoder(SEEDS,prefixes)
  result={'prefixes':prefixes,'all_prose':metrics(rows,predict,gloss),
   'folios':{f:metrics([r for r in rows if r['folio']==f],predict,gloss) for f in ['f1r','f75r','f103r']}}
  result['seed_reading_ambiguities']=[{'eva':w,'candidate_count':len({v for k,v in predict(w)})} for w in SEEDS if len({v for k,v in predict(w)})>1]
  # Preserve all surface predictions internally, not as validated translations.
  private[name]={w:sorted(predict(w)) for w in freq}
  result['prediction_sha256']=hashlib.sha256(json.dumps(private[name],sort_keys=True).encode()).hexdigest()
  results['reconstructions'][name]=result
 (ROOT/'tmp/candidates_private.json').write_text(json.dumps(private,indent=2))
 (ROOT/'results/rule_audit.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
