#!/usr/bin/env python3
import json,hashlib,sys,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent

def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 sys.path.insert(0,str(BASE/'voynich_20261028'));from analyse import parse
 meta={};pageinfo={}
 for prefix,filename in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]:
  bypage={}
  for r in parse(filename)[0]:
   if r['type']!='P0' or r['metadata'].get('L') not in ['A','B']:continue
   bypage.setdefault(r['page'],[]).append(r)
  for page,rows in bypage.items():
   paras=[];cur=[]
   for r in rows:
    if '<%>' in r['raw'] and cur:paras.append(cur);cur=[]
    cur.append(r)
    if '<$>' in r['raw']:paras.append(cur);cur=[]
   if cur:paras.append(cur)
   for pid,para in enumerate(paras):
    for j,r in enumerate(para):
     meta[prefix,r['locus']]={'group':r['metadata']['Q'],'physical_leaf':r['leaf'],'paragraph':pid,'line_in_paragraph':j,'paragraph_lines':len(para),'vertical':min(3,4*j//len(para)) if len(para)>1 else 4}
   pageinfo[page]=rows[0]['metadata']['Q']
 cases=read(BASE/'voynich_phase6/data/adjacency_inputs.json');out=[]
 for case in cases:
  name=case['case'];lines=[];pages=list(dict.fromkeys(r['page'] for r in case['lines']));groups={p:str(min(7,8*i//len(pages))) for i,p in enumerate(pages)}
  for r in case['lines']:
   if name[:2] in ['ZL','IT']:
    if (name[:2],r['locus']) not in meta:continue
    m=meta[name[:2],r['locus']]
   else:
    # Template paragraph position is purely artificial for controls.
    m=dict(meta.get(('ZL',r['locus']),{'paragraph':-1,'line_in_paragraph':0,'paragraph_lines':1,'vertical':4}),group=groups[r['page']],physical_leaf=r['page'])
   lines.append(dict(r,**m))
  out.append({'case':name,'layout':case['layout'],'lines':lines})
 save(ROOT/'data/inputs.json',out)
 sources=[BASE/'voynich_phase6/data/adjacency_inputs.json',BASE/'voynich_20261028/data/ZL3b-n.txt',BASE/'voynich_20261028/data/IT2a-n.txt',ROOT/'PROTOCOL.json']
 save(ROOT/'data/lineage.json',{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
 for p in [BASE/'voynich_phase6/data/LICENSE_TIMM.txt',BASE/'voynich_20261028/controls/LICENSE_GRESHKO',BASE/'voynich_phase6/SOURCES.json',BASE/'voynich_phase2/SOURCES_AND_LIMITS.json']:
  if p.exists():shutil.copy2(p,ROOT/'data'/('source_'+p.name))
 print([(d['case'],len(d['lines']),len(set(r['group'] for r in d['lines']))) for d in out])
if __name__=='__main__':main()
