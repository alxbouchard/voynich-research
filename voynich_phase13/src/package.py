import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def main():
 paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in {'tmp','output','__pycache__','.venv'} for x in p.relative_to(ROOT).parts) and p.name!='MANIFEST.json')
 paths.append(ROOT/'output/Voynich_phase13_lexiques.pdf')
 manifest=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
 (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
 out=ROOT/'output/Voynich_phase13_reproduction.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in paths+[ROOT/'MANIFEST.json']:z.write(p,'voynich_phase13/'+str(p.relative_to(ROOT)))
 print(json.dumps({'zip':str(out),'files':len(paths)+1,'bytes':out.stat().st_size}))
if __name__=='__main__':main()
