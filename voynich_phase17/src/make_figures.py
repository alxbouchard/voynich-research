from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import io,os
ROOT=Path(__file__).resolve().parents[1];F=ROOT/'figures'
BOX=(62,662,582,942)

def save(im,path):
    b=io.BytesIO();im.save(b,format='PNG');temp=Path(str(path)+'.writing')
    with temp.open('wb') as out:out.write(b.getvalue());out.flush();os.fsync(out.fileno())
    temp.replace(path)
    with Image.open(path) as check:check.load()

font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
selected=[('band_06_contrast.png','006 : lumière rouge'),('band_13_contrast.png','013 : fluorescence UV'),
          ('pca_all_2.png','ACP 22 bandes : composante 2'),('pca_fluorescence_2.png','ACP fluorescence : composante 2')]
out=Image.new('RGB',(1060,640),'white');d=ImageDraw.Draw(out)
for i,(name,title) in enumerate(selected):
    x=(i%2)*530;y=(i//2)*320;d.text((x+4,y+5),title,fill='black',font=font);out.paste(Image.open(F/name).crop(BOX),(x+4,y+35))
save(out,F/'report_comparison.png')
out=Image.new('RGB',(1080,1032),'white');d=ImageDraw.Draw(out)
for i in range(22):
    x=(i%4)*270;y=(i//4)*172;d.text((x+3,y+3),f'Capture {i+1:03d}',fill='black',font=font)
    im=Image.open(F/f'band_{i+1:02d}_contrast.png').crop(BOX);im.thumbnail((260,140));out.paste(im,(x+3,y+29))
save(out,F/'all_bands_pair.png')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
items=[('band_06_contrast.png','006 : rouge, contraste local'),('band_07_contrast.png','007 : UV, contraste local'),
       ('band_13_contrast.png','013 : fluorescence'),('band_17_contrast.png','017 : fluorescence'),
       ('pca_all_1.png','ACP 22 bandes : composante 1'),('pca_all_2.png','ACP 22 bandes : composante 2'),
       ('pca_fluorescence_1.png','ACP fluorescence : composante 1'),('pca_fluorescence_2.png','ACP fluorescence : composante 2')]
out=Image.new('RGB',(1060,1280),'white');d=ImageDraw.Draw(out)
for i,(name,label) in enumerate(items):
    x=(i%2)*530;y=(i//2)*320;d.text((x+4,y+5),label,fill='black',font=font);out.paste(Image.open(F/name).crop(BOX),(x+4,y+35))
save(out,F/'f116v_pair_comparison.png')
