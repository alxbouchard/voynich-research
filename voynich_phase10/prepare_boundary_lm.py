#!/usr/bin/env python3
"""Rebuild space-aware LMs. No target plaintext is used in model training."""
import hashlib,json,re,unicodedata
from pathlib import Path
from lxml import etree
import numpy as np
ROOT=Path(__file__).resolve().parent;DATA=ROOT/'data'
def clean(s):return re.sub('[^a-z]','',unicodedata.normalize('NFKD',s).lower()).replace('j','i').replace('k','c').replace('w','uu')
def words(s):return [w for t in re.findall(r'[^\W\d_]+',s,flags=re.UNICODE) if (w:=clean(t))]
def main():
 tree=etree.parse(str(DATA/'caesar.xml'));body=tree.xpath('//*[local-name()="body"]')[0]
 for e in body.xpath('.//*[local-name()="note" or local-name()="head"]'):e.getparent().remove(e)
 latin=words(''.join(body.itertext()))
 raw=(DATA/'dante.txt').read_text();starts=list(re.finditer(r'INFERNO\nInferno\nCanto I\n',raw));assert len(starts)==2
 unique=raw[:starts[1].start()];assert unique.strip()==raw[starts[1].start():].strip()
 before=unique.split('\nPARADISO\n',1)[0]
 italian=words('\n'.join(l for l in before.splitlines() if l.strip() and not re.match(r'^(INFERNO|PURGATORIO|PARADISO|Inferno|Purgatorio|Paradiso|Canto\b)',l)))
 audit={}
 for lang,ws in [('latin',latin),('italian',italian)]:
  assert ''.join(ws)==(DATA/(lang+'_train.txt')).read_text().strip()
  text=' '.join(ws);a=np.array([26 if c==' ' else ord(c)-97 for c in text],dtype=np.int32)
  ids=((a[:-3]*27+a[1:-2])*27+a[2:-1])*27+a[3:]
  counts=np.bincount(ids,minlength=27**4);lm=np.log2((counts+.01)/(counts.sum()+.01*27**4));lm.tofile(DATA/(lang+'_lm_boundary.bin'))
  q=np.bincount(a,minlength=27)+.5;q=q/q.sum();(DATA/(lang+'_freq_boundary.txt')).write_text(' '.join(map(str,q)))
  (DATA/(lang+'_train_boundary.txt')).write_text(text)
  audit[lang]={'words':len(ws),'letters':len(text)-text.count(' '),'spaces':text.count(' '),'matches_previous_letter_stream':True,'sha256':hashlib.sha256(text.encode()).hexdigest()}
 (DATA/'boundary_lm_audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(audit)
if __name__=='__main__':main()
