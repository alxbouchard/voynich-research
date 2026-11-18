"""Recomposer les détails des deux faces du feuillet 46 de Martino, Library of Congress."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
SCANS=[
 ('0095','acc3df8898e662feeb90f5c8761e7d81be1a9475e3207a17992abe78b5c13785',
  (410,1460,1670,1740),'46r   pâte à frire','... bucata in niun loco ...'),
 ('0096','0f77d5c4da6ed5bf0eff94a723152b43ce91b680b39ffa9aab993cf2822091c4',
  (1050,2165,2360,2485),'46v   omelette aux herbes','... in un bon botiro ...')]
def main(cache):
    board=Image.new('RGB',(1060,680),'#f7f5ee')
    draw=ImageDraw.Draw(board)
    try:font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24)
    except OSError:font=ImageFont.load_default(size=24)
    top=7
    for n,check,box,title,caption in SCANS:
        src=cache/f'voy-d-martino-{n}.jp2'
        assert sha256(src.read_bytes()).hexdigest()==check
        draw.text((18,top),title+'     '+caption,font=font,fill='#332b23')
        with Image.open(src) as whole:
            im=whole.crop(box)
            im.thumbnail((1022,280),Image.Resampling.LANCZOS)
        board.paste(im,(18,top+42));top+=335
    board.save(HERE/'martino-f46.jpg',quality=94,subsampling=0,optimize=True)

def planche_voynich(cache):
    scan=cache/'voy-d-f75r-n.jpg'
    assert sha256(scan.read_bytes()).hexdigest()=='6fd33917722a97ef0c93f905885963332645c1a1c81f60f03a165b12007a7fc3'
    board=Image.new('RGB',(670,370),'#f7f5ee')
    draw=ImageDraw.Draw(board)
    try:font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',19)
    except OSError:font=ImageFont.load_default(size=19)
    frames=[((2025,935,2535,1055),'f75r.11     shedy  dor  chekam'),
            ((365,949,880,1070),'f75r.12     ssheckhy  qokal')]
    with Image.open(scan) as whole:
        for j,(box,title) in enumerate(frames):
            offset=8+180*j
            draw.text((15,offset),title,font=font,fill='#332b23')
            board.paste(whole.crop(box),(15,offset+32))
    board.save(HERE/'f75r-suite.jpg',quality=94,subsampling=0,optimize=True)

if __name__=='__main__':
    cache=Path(sys.argv[1])
    main(cache)
    planche_voynich(cache)
