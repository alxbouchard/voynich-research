"""Montrer la scène et les deux passages de prose sur les photographies originales."""
from pathlib import Path
from hashlib import sha256
import sys,json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def main(path84,path48):
    src={v['label']:v for v in json.loads((ROOT/'voynich_resources/yale/image_index.json').read_text())}
    sources={}
    for f,p in [('84r',path84),('48v',path48)]:
        assert sha256(p.read_bytes()).hexdigest()==src[f]['sha256']
        sources[f]=Image.open(p).convert('RGB')
    canvas=Image.new('RGB',(1150,935),'#f4f0e6')
    draw=ImageDraw.Draw(canvas)
    try:font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
    except OSError:font=ImageFont.truetype('DejaVuSans.ttf',25)
    panels=[
      ('84r',(1490,280,2600,795),10,40,'f84r, trois inscriptions au-dessus du bain'),
      ('84r',(222,948,1335,1051),10,615,'f84r.15, du début de la ligne au sixième mot'),
      ('48v',(1790,1005,2480,1160),10,775,'f48v.8, à droite de la tige : otoly chey')]
    keys=[]
    for face,box,x,y,label in panels:
        draw.text((x,y-34),label,font=font,fill='#292e28')
        crop=sources[face].crop(box)
        canvas.paste(crop,(x,y))
        l,t,r,b=box
        keys.append({'face':face,'source':src[face]['url'].replace('/full/full/',f'/{l},{t},{r-l},{b-t}/full/'),'cadre':box})
    draw.text((162,557),'okolshy',font=font,fill='#292e28')
    draw.text((407,557),'otoly',font=font,fill='#292e28')
    draw.text((777,557),'dshedy',font=font,fill='#292e28')
    canvas.save(HERE/'scene-et-prose.jpg',quality=94,subsampling=0,optimize=True)
    (HERE/'CADRAGES.json').write_text(json.dumps(keys,indent=1,ensure_ascii=False)+'\n')
if __name__=='__main__':main(*(Path(s) for s in sys.argv[1:]))
