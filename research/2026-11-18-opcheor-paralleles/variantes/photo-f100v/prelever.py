"""Produit le recadrage natif et les repères sur le verso de 100, depuis le JPEG Yale."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE_HASH = '72637b9770f40f7a8ff6b96a551e64775e88994ae69bafec0b43d48974364c33'
source = Path(sys.argv[1])
if sha256(source.read_bytes()).hexdigest()!=SOURCE_HASH:
    raise ValueError('Le fichier fourni diffère du JPEG Yale 1006249 utilisé ici.')
page = Image.open(source)
assert page.size == (7486,3715)
detail = (2040,2617,2720,2728)
paragraph = (750,2335,2770,3130)
words = [(2237,2631,2419,2714), (2451,2637,2614,2718)]
page.crop(detail).save(HERE/'deux-finales.png')
page.crop((605,1340,1285,2370)).save(HERE/'fragment140.jpg',quality=93)
page.crop((982,2146,1218,2246)).save(HERE/'legende140.png')
resize_to_width = lambda im, w: im.resize((w,round(im.height*w/im.width)), Image.Resampling.LANCZOS)
context = page.crop((120,0,2960,3640))
left = resize_to_width(context,480)
right = resize_to_width(page.crop(paragraph),1160)
board = Image.new('RGB',(1740,710),'white')
left_origin, right_origin = (22,57), (553,120)
board.paste(left,left_origin)
board.paste(right,right_origin)
draw = ImageDraw.Draw(board)
try:
    font = ImageFont.truetype('DejaVuSans.ttf',22)
except OSError:
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
draw.text((20,18),'Feuillet 100 verso',font=font,fill='#202020')
draw.text((553,55),'Les neuf lignes de prose sous les fragments végétaux',font=font,fill='#202020')

def frame(src_box, origin, src_origin, scale, color, width):
    def px(i): return round(origin[i%2]+(src_box[i]-src_origin[i%2])*scale)
    draw.rectangle(tuple(px(i) for i in range(4)),outline=color,width=width)

frame(paragraph,left_origin,(120,0),480/2840,'#17679a',3)
for box in words:
    frame(box,right_origin,paragraph[:2],1160/(paragraph[2]-paragraph[0]),'#9d2e18',2)
for tag,y in [('15',2547),('16',2609),('17',2695)]:
    draw.text((510,round(right_origin[1]+(y-paragraph[1])*1160/(paragraph[2]-paragraph[0]))-10),tag,font=font,fill='#204b62')
draw.text((553,613),'Les cadres désignent les deux groupes comparés sur la troisième ligne.',font=font,fill='#202020')
board.save(HERE/'page-et-paragraphe.jpg',quality=92)
