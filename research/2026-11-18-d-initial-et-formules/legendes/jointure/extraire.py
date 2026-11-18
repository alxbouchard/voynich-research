"""Cadrer six jonctions y/t de même main et les présenter à un grossissement commun."""
from hashlib import sha256
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
CASES={
  'B7':('f84r',13,969,899,'dytedy','interne'),
  'U4':('f84r',16,547,1045,'shedy.tedy / shedytedy','cible'),
  'H8':('f84r',17,1762,1125,'keedy.tey','espace'),
  'P3':('f84r',32,509,2383,'ytedy','interne'),
  'A6':('f84r',32,648,2383,'ytedy.tedy','espace'),
  'N5':('f43v',13,1012,1124,'dshedy.tedy','espace')}
def main(paths):
    root=HERE.parents[3]
    sources={x['label']:x for x in json.loads((root/'voynich_resources/yale/image_index.json').read_text())}
    images={}
    for f,p in zip(('f84r','f43v'),paths):
        assert sha256(p.read_bytes()).hexdigest()==sources[f[1:]]['sha256']
        images[f]=Image.open(p)
    key={}
    for code,(face,n,x,y,word,role) in CASES.items():
        box=(x-100,y-61,x+100,y+54)
        crop=images[face].crop(box).resize((400,230),Image.Resampling.LANCZOS)
        sheet=Image.new('RGB',(400,256),'#f6f6f3')
        sheet.paste(crop,(0,13))
        pen=ImageDraw.Draw(sheet)
        pen.polygon([(194,0),(206,0),(200,12)],fill='#4a6690')
        pen.polygon([(194,255),(206,255),(200,244)],fill='#4a6690')
        sheet.save(HERE/'cartes'/(code+'.jpg'),quality=94,subsampling=0,optimize=True)
        src=sources[face[1:]]['url'].replace('/full/full/',f'/{box[0]},{box[1]},200,115/full/')
        key[code]={'locus':f'{face}.{n}','centre':[x,y],'mots':word,'type':role,'detail_natif':src}
    (HERE/'CLE.json').write_text(json.dumps(key,indent=1,ensure_ascii=False)+'\n')
if __name__=='__main__':main([Path(v) for v in sys.argv[1:]])
