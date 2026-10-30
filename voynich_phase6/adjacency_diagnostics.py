#!/usr/bin/env python3
"""Exploratory local structure, with page-preserving randomization controls."""
import collections,functools,hashlib,itertools,json,re,sys,unicodedata
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;P5=ROOT.parent/'voynich_phase5';sys.path.insert(0,str(P5));import run_syllabic as p5
BASE=ROOT.parent/'voynich_20261028';SEED=20261031;PERMS=100
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def strict_words(raw):
 raw=raw.replace('<->','.? .').replace('<~>','.? .')
 raw=re.sub(r'<[^>]*>','',raw);raw=re.sub(r'\[[^\]]*\]','?',raw)
 raw=re.sub(r'@\d+;','?',raw).replace('{','').replace('}','').lower()
 return [w if re.fullmatch('[a-z]+',w) else None for w in re.split(r'[.\s]+',raw) if w]
def plainwords(raw):
 return [p5.prev.clean(w) for w in re.findall(r'[^\W\d_]+',raw,flags=re.UNICODE) if p5.prev.clean(w)]
def inputs():
 cases=[];allzl=[]
 for name in ['ZL3b-n.txt','IT2a-n.txt']:
  recs=p5.prev.parse(name)[0];eligible=[r for r in recs if r['type'].startswith('P')]
  if name.startswith('ZL'):allzl=eligible
  for lang in ['A','B']:
   lines=[{'page':r['page'],'locus':r['locus'],'section':r['metadata'].get('I','?'),'hand':r['metadata'].get('H','?'),'words':strict_words(r['raw'])} for r in eligible if r['metadata'].get('L')==lang]
   cases.append((name[:2]+'_'+lang,lines,'original manuscript line/page layout'))
 template=[r for r in allzl if r['metadata'].get('L') in ['A','B']]
 def layout(words):
  out=[];pos=0
  for r in template:
   n=len(strict_words(r['raw']));take=words[pos:pos+n]
   if not take:break
   out.append({'page':r['page'],'locus':r['locus'],'section':'control','hand':'control','words':take});pos+=len(take)
  return out
 pliny=(BASE/'controls/input/nathist_book16.txt').read_text();pliny='\n'.join(l for l in pliny.splitlines() if not re.fullmatch(r'[IVXLCDM\d\s]+',l))
 raw=(ROOT.parent/'voynich_phase2/data/dante.txt').read_text();starts=list(re.finditer(r'INFERNO\nInferno\nCanto I\n',raw));unique=raw[:starts[1].start()];assert raw[starts[1].start():].strip()==unique.strip()
 para=unique.split('\nPARADISO\n',1)[1];para='\n'.join(l for l in para.splitlines() if not re.match(r'^(PARADISO|Paradiso|Canto\b)',l))
 naibbe=(BASE/'controls/generated/naibbe_ciphertext.txt').read_text().split()
 timm=[l for l in (ROOT/'data/timm_generated_text.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
 timmwords=' '.join(timm[1:]).split() # drop the single published VMS-derived seed line
 control_counts={}
 for name,words in [('Latin_Pliny',plainwords(pliny)),('Italian_Paradiso',plainwords(para)),('Naibbe_Pliny',naibbe),('Timm_generated',timmwords)]:
  control_counts[name]=len(words)
  cases.append((name,layout(words),'artificial ZL line/page template; different lengths; descriptive control, not a corpus-matched classifier'))
 save(ROOT/'data/adjacency_inputs.json',[{'case':n,'layout':note,'source_word_count_before_template':control_counts.get(n),'retained_word_count':sum(w is not None for r in lines for w in r['words']),'lines':lines} for n,lines,note in cases]);return cases
def near_matrix(words,composed=False):
 units=[tuple(re.findall(p5.prev.UNITS,w)) if composed else tuple(w) for w in words];idx={u:i for i,u in enumerate(units)};assert len(idx)==len(units)
 n=len(words);out=np.zeros((n,n),dtype=bool);patterns=collections.defaultdict(list)
 for i,u in enumerate(units):
  for j in range(len(u)):
   deletion=u[:j]+u[j+1:]
   if deletion in idx:k=idx[deletion];out[i,k]=out[k,i]=True
   patterns[u[:j]+('\x00',)+u[j+1:]].append(i)
 for group in patterns.values():
  g=sorted(set(group))
  for a,b in itertools.combinations(g,2):out[a,b]=out[b,a]=True
 np.fill_diagonal(out,False);return out
def analyze(name,lines,note):
 vocabulary=sorted({w for r in lines for w in r['words'] if w is not None});mp={w:i for i,w in enumerate(vocabulary)}
 slots=[];pages=collections.defaultdict(list);interior=collections.defaultdict(list);a=[];b=[];edge_strata=collections.defaultdict(list)
 for r in lines:
  offset=len(slots);seq=[mp.get(w,-1) for w in r['words']];slots.extend(seq)
  known=[offset+i for i,x in enumerate(seq) if x>=0];pages[r['page']].extend(known);interior[r['page']].extend(known[1:-1])
  for j in range(1,len(seq)):
   if seq[j-1]>=0 and seq[j]>=0:
    edge_strata[r['section']+'|'+r['hand']].append(len(a));a.append(offset+j-1);b.append(offset+j)
 slots=np.array(slots,dtype=np.int32);a=np.array(a);b=np.array(b);assert len(a)>0
 rawnear=near_matrix(vocabulary);compnear=near_matrix(vocabulary,True)
 first=np.array([ord(w[0])-97 for w in vocabulary]);last=np.array([ord(w[-1])-97 for w in vocabulary]);assert first.min()>=0 and first.max()<26 and last.min()>=0 and last.max()<26
 def measure(s,indices=None):
  x=s[a];y=s[b]
  if indices is not None:x=x[indices];y=y[indices]
  hist=np.bincount(last[x]*26+first[y],minlength=26*26).reshape(26,26).astype(float);p=hist/hist.sum();den=p.sum(axis=1)[:,None]*p.sum(axis=0)[None,:];mask=p>0
  return np.array([(x==y).mean(),rawnear[x,y].mean(),compnear[x,y].mean(),float((p[mask]*np.log2(p[mask]/den[mask])).sum())])
 obs=measure(slots);nulls={};keys=['identical_adjacent','distinct_edit1_EVA','distinct_edit1_composed','last_first_mutual_information_bits']
 for mode,groups in [('all_page_slots',pages),('line_ends_fixed',interior)]:
  rng=np.random.default_rng(SEED);draws=[];arrays=[np.array(v,dtype=int) for v in groups.values() if len(v)>1]
  for i in range(PERMS):
   shuffled=slots.copy()
   for ix in arrays:shuffled[ix]=rng.permutation(slots[ix])
   if i==0:
    for ix in pages.values():assert collections.Counter(slots[ix])==collections.Counter(shuffled[ix])
    assert np.array_equal(shuffled[slots<0],slots[slots<0])
   draws.append(measure(shuffled))
  z=np.array(draws);nulls[mode]={k:{'mean':float(z[:,j].mean()),'p025':float(np.quantile(z[:,j],.025)),'p975':float(np.quantile(z[:,j],.975)),'observed_minus_mean':float(obs[j]-z[:,j].mean()),'exploratory_upper_tail_p':float((1+(z[:,j]>=obs[j]).sum())/(PERMS+1))} for j,k in enumerate(keys)}
  save(ROOT/'results'/f'adjacency_{name}_{mode}_draws.json',z.tolist())
 strata={k:{'pairs':len(ix),'observed':dict(zip(keys,map(float,measure(slots,np.array(ix)))))} for k,ix in edge_strata.items() if len(ix)>=500}
 result={'case':name,'layout':note,'words':int((slots>=0).sum()),'uncertain_slots':int((slots<0).sum()),'types':len(vocabulary),'pages':len(pages),'adjacent_pairs':len(a),'observed':dict(zip(keys,map(float,obs))),'nulls':nulls,'strata_section_hand_min500pairs':strata,'permutations_each':PERMS,'seed':SEED,'warning':'Exploratory, no multiple-testing correction. Raw/composed measures on natural-language controls are orthographic comparisons, not linguistic syllabification. Different lengths and artificial control layout preclude a universal language classifier.'}
 save(ROOT/'results'/f'adjacency_{name}.json',result);print(json.dumps({'case':name,'words':result['words'],'pairs':len(a),'observed':result['observed'],'excess_fixed_ends':{k:v['observed_minus_mean'] for k,v in nulls['line_ends_fixed'].items()}}),flush=True);return result
def main():
 assert strict_words('aa.[x:y].bb.cc,dd.ee<->ff')==['aa',None,'bb',None,'ee',None,'ff']
 a=near_matrix(['ab','ac','a','abc','zz']);assert a[0,1] and a[0,2] and a[0,3] and not a[0,4] and not a[0,0]
 out=[analyze(*case) for case in inputs()];save(ROOT/'results/adjacency_summary.json',out)
if __name__=='__main__':main()
