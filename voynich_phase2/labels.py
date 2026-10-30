#!/usr/bin/env python3
"""Anchor inventory, with no invented names for depicted objects."""
import sys,csv,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent/'voynich_20261028';sys.path.insert(0,str(BASE))
from analyse import parse

def main():
 zl=parse('ZL3b-n.txt')[0];it=parse('IT2a-n.txt')[0]
 # Match locus page.number despite differences in type/locator.
 other={r['locus'].split(',')[0]:r for r in it}
 paragraphs=collections.defaultdict(list)
 for r in zl:
  if r['type'].startswith('P'):
   for word in set(r['clean']):paragraphs[word].append(r['locus'])
 rows=[]
 for r in zl:
  if r['type'] not in {'Lp','Lf','Lc','Ls','Lz','Ln','Lt','La'}:continue
  x=other.get(r['locus'].split(',')[0]);reading=' '.join(r['tokens'])
  agreed=x is not None and x['tokens']==r['tokens'] and '?' not in reading
  occurrence=paragraphs.get(reading,[]) if ' ' not in reading and '?' not in reading else []
  rows.append(dict(locus=r['locus'],page=r['page'],label_type=r['type'],ZL=reading,IT=' '.join(x['tokens']) if x else '',exact_agreement=agreed,paragraph_occurrences=len(occurrence),paragraph_loci=';'.join(occurrence),meaning='UNKNOWN'))
 out=ROOT/'results'
 with (out/'illustration_anchors.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 zodiac=[r for r in rows if r['label_type']=='Lz'];freq=collections.Counter(r['ZL'] for r in zodiac if '?' not in r['ZL'])
 stats=dict(illustration_labels=len(rows),by_type=dict(collections.Counter(r['label_type'] for r in rows)),
            exact_agreement_all=sum(r['exact_agreement'] for r in rows),zodiac_labels=len(zodiac),zodiac_agree=sum(r['exact_agreement'] for r in zodiac),zodiac_complete=sum('?' not in r['ZL'] for r in zodiac),
            zodiac_singletons=sum(n==1 for n in freq.values()),zodiac_distinct=len(freq),
            agreeing_labels_with_running_text=sum(r['exact_agreement'] and r['paragraph_occurrences']>0 for r in rows),
            caution='Agreement is only between transcriptions of one object. Labels may be names, adjectives, numbers or operations. No automatic plant or star identifications have been made.',
            month_names='Readable month names are later writing in the Latin alphabet; not a bilingual alignment to the 299 zodiac labels.',
            priorities=sorted([r for r in rows if r['exact_agreement'] and 1<=r['paragraph_occurrences']<=10],key=lambda r:(r['paragraph_occurrences'],r['locus']))[:20])
 (out/'anchors_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in stats.items() if k!='priorities'},ensure_ascii=False))

if __name__=='__main__':main()
