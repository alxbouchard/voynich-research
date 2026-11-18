from pathlib import Path
import hashlib
import json
import random
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

D=Path(__file__).resolve().parent
data=json.loads((D.parent/'RESULTATS.json').read_text())
key={v['face']:v for v in json.loads((D.parent/'cle-reserve.json').read_text()).values()}
faces=[]
for target in ('f38v','f54r'):
    faces.append(target)
    for vote in ('O','N'):
        candidates=[f for f,s in data['reserve_primaire'].items() if s==vote and key[f]['cahier']==key[target]['cahier']]
        faces.append(min(candidates,key=lambda f:(f[-1]!=target[-1],abs(int(f[1:-1])-int(target[1:-1])),int(f[1:-1]),f)))
assert len(set(faces))==6
random.Random(443).shuffle(faces)
dest=D/'cartes'
dest.mkdir(exist_ok=True)
ids={}
for i,face in enumerate(faces,1):
    code=f'X{i}'
    path=Path(sys.argv[1])/(face+'.jpg')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==key[face]['sha256_original']
    with Image.open(path) as im:
        w,h=im.size
        whole=ImageOps.contain(im.convert('RGB'),(320,790))
        lower=ImageOps.contain(im.crop((0,round(.45*h),w,h)).convert('RGB'),(1080,790))
    card=Image.new('RGB',(1420,830),'#ece7dc')
    card.paste(whole,(5,(830-whole.height)//2))
    card.paste(lower,(330+(1080-lower.width)//2,25+(790-lower.height)//2))
    ImageDraw.Draw(card).text((12,5),code,fill='black',font=ImageFont.load_default(size=26))
    card.save(dest/(code+'.jpg'),quality=91)
    ids[code]=key[face]
(D/'cle.json').write_text(json.dumps(ids,ensure_ascii=False,indent=1)+'\n')
