"""Rassembler pour comparaison les fac-similés publics de l'Herbarius de Passau."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

HERE = Path(__file__).resolve().parent
BASE = 'https://iiif.archive.org/image/iiif/3/herbarius00petr%2Fherbarius00petr_jp2.zip%2Fherbarius00petr_jp2%2Fherbarius00petr_'
PAGES = (10,13,48,49,50,51,201,202,203,204,205,206,207,209)


def url(n):
    return BASE+f'{n:04d}.jp2/full/900,/0/default.jpg'


def make(src):
    size = (1560,740)
    sheet = Image.new('RGB',size,'white')
    label = ImageDraw.Draw(sheet)
    for i,n in enumerate((201,203,205,207)):
        im = Image.open(src/f'boston-{n}.jpg').convert('RGB')
        im.thumbnail((385,647))
        x=390*i+(390-im.width)//2
        sheet.paste(im,(x,33))
        label.text((390*i+10,10), f'Boston, Q.405.115 / vue {n:04d}', fill='black')
    label.text((10,679),'Herbarius, Passau, Johann Petri, 1485. Boston Public Library, Rare Books Department. Domaine public.',fill='black')
    sheet.crop((0,0,1560,703)).save(HERE/'quatre-feuillets.jpg',quality=87)
    proof=Image.new('RGB',(1600,1120),'white')
    draw=ImageDraw.Draw(proof)
    font_path = next((path for path in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') if Path(path).exists()), None)
    font = ImageFont.truetype(font_path,17) if font_path else ImageFont.load_default(size=17)
    def place(n,box,at,size,title):
        im=Image.open(src/f'boston-{n}.jpg').convert('RGB').crop(box)
        im.thumbnail(size)
        x,y=at
        draw.text((x,y),title,fill='black',font=font)
        proof.paste(im,(x,y+31))
    place(10,(430,165,840,450),(10,5),(640,285),'Table imprimée, vue 0010')
    place(203,(190,24,420,161),(500,5),(280,145),'Folio du cresson des jardins')
    place(205,(10,690,875,905),(780,5),(805,212),'Cresson aquatique, vue 0205')
    place(205,(0,1001,875,1148),(800,250),(795,185),'Fin du recto XCVI')
    place(206,(50,28,885,218),(800,447),(795,185),'Suite au verso XCVI, page gauche devant la nigelle')
    place(49,(45,145,865,1215),(10,362),(360,520),'Vue 0049')
    place(51,(0,0,850,1320),(394,362),(360,520),'Même feuillet, vue 0051')
    place(209,(10,692,885,962),(780,710),(800,310),'Nénuphar, vue 0209')
    draw.text((12,1040),'Boston Public Library, Rare Books Department, Q.405.115. Reproduction du domaine public.',fill='black',font=font)
    proof.crop((0,0,1600,1090)).save(HERE/'reperes.jpg',quality=87)
    files={}
    for n in PAGES:
        p=src/f'boston-{n}.jpg'
        files[str(n)]={'url':url(n),'sha256':sha256(p.read_bytes()).hexdigest()}
    (HERE/'IMAGES.json').write_text(json.dumps(files,indent=1)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    args=parser.parse_args()
    make(args.source)
