from pathlib import Path
import json,re,hashlib,subprocess,sys
R=Path(__file__).resolve().parent.parent
before=(R/'results/analysis.json').read_bytes()
subprocess.run([sys.executable,str(R/'src/analyse.py')],check=True,stdout=subprocess.DEVNULL)
assert before==(R/'results/analysis.json').read_bytes()
x=json.loads(before);assert x['software_checks']=='passed'
checks=[]
for code,f in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]:
 text=(R/'data'/f).read_text()
 target=[l for l in text.splitlines() if l.startswith('<f116v.')]
 assert len(target)==(1 if code=='ZL' else 0)
 # Independent literal scan of joined spelling after accepting optional comma.
 hits=[l for l in text.splitlines() if l.startswith('<f') and re.search(r'aror,?sheey',l)]
 assert len(hits)==1 and hits[0].startswith('<f104r.28,')
 for mode,a in x['corpora'][code]['concordance'].items():
  for q,matches in a['matches'].items():
   assert a['counts'][q]==len(matches)
   for m in matches:
    assert m['locus']!='f116v.1'
    assert any(l.startswith('<'+m['locus']+',') and l.endswith(m['raw']) for l in text.splitlines())
 counts=x['corpora'][code]['coverage'];assert len({a['fully_mapped_occurrences'] for a in counts.values()})==1
 checks.append(dict(corpus=code,joined_literal_hits=hits,target_locus_count=len(target)))
for a in json.loads((R/'results/image_audit.json').read_text()):
 from PIL import Image,ImageOps
 src=R/a['source'];cut=R/a['crop']
 assert hashlib.sha256(src.read_bytes()).hexdigest()==a['source_sha256']
 assert hashlib.sha256(cut.read_bytes()).hexdigest()==a['sha256']
 assert Image.open(cut).tobytes()==ImageOps.exif_transpose(Image.open(src)).crop(a['crop_xyxy_after_exif']).tobytes()
out=dict(status='passed',identical_recompute=True,literal_scan=checks,pixel_crops_verified=6,
         limitations='Software and source-consistency checks, not independent palaeographic or semantic validation.')
(R/'results/verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
