"""Montrer le premier mot des deux plantes dans son contexte et à plus grande échelle."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

base=Path(__file__).resolve().parent
font=ImageFont.truetype('Arial.ttf',21)
header=ImageFont.truetype('Arial.ttf',26)
plate=Image.new("RGB",(1100,933),"white")
pen=ImageDraw.Draw(plate)
for i,(file,face,rect,title) in enumerate(zip(sys.argv[1:],("f39v","f40r"),
                   ((302,170,540,265),(145,403,391,497)),("pdair  ·  chdy","pchey  ·  keodar / k,eodar"))):
    im=Image.open(file).convert("RGB")
    assert im.width==1500
    preview=im.copy()
    preview.thumbnail((525,650))
    x=10+i*550
    ratio=preview.width/im.width
    plate.paste(preview,(x,44))
    pen.rectangle((x+rect[0]*ratio,44+rect[1]*ratio,x+rect[2]*ratio,44+rect[3]*ratio),
                  outline="#A22238",width=2)
    pen.text((x,8),f"Beinecke MS 408, {face}",font=header,fill="#162633")
    crop=im.crop(rect)
    crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.LANCZOS)
    plate.paste(crop,(x,705))
    pen.text((x,902),title,font=font,fill="#162633")
plate.save(base/"premiers-mots.jpg",quality=92)
