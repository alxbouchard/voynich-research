"""Deux JPEG Yale réduits à 2400 px (f89v2) et 1800 px (f48r), dans cet ordre."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

small, large = (Image.open(p).convert('RGB') for p in sys.argv[1:])
assert small.size==(2400,2175) and large.size==(1800,2341)
canvas = Image.new('RGB',(1100,1030),'white')
draw = ImageDraw.Draw(canvas)
try:
    font=ImageFont.truetype("Arial.ttf",21)
except OSError:
    font=ImageFont.load_default(size=21)
view=small.resize((690,625),Image.Resampling.LANCZOS)
canvas.paste(view,(10,42))
draw.text((15,9),'f89v2  |  Douze fragments, quatre inscriptions étudiées',font=font,fill='#26373d')
boxes={'50':(615,505,795,606),'54':(1595,475,1785,566),'56':(1100,923,1285,986),
       '61':(1415,1762,1610,1868)}
for obj,box in boxes.items():
    x,y,u,v=box
    coord=(10+x*690/2400,42+y*625/2175,10+u*690/2400,42+v*625/2175)
    draw.rectangle(coord,outline='#a92934',width=2)
    draw.text((coord[0],coord[3]+1),obj,font=font,fill='#a92934',stroke_width=1,stroke_fill='white')
for idx,(obj,box) in enumerate(boxes.items()):
    y=65+idx*138
    draw.text((735,y),'Fragment '+obj,font=font,fill='#26373d')
    canvas.paste(small.crop(box),(735,y+31))
draw.text((15,684),'f48r  |  La septième ligne de prose se termine par le groupe lu « okam ».',font=font,fill='#26373d')
canvas.paste(large.crop((700,355,1460,545)),(28,725))
draw.rectangle((28+576,725+69,28+680,725+120),outline='#a92934',width=2)
canvas.crop((0,0,1100,944)).save(Path(__file__).parent/'lectures.jpg',quality=90)
