"""python3 planche.py dossier-images ; entrées formule-gart-53.jpg etc., IIIF largeur 2000."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1])
ROWS = [
 ('XXIII · f. 27r · Nom de la plante en tête', 57, (605, 3100, 2600, 3260)),
 ('XXIII · f. 27v · La racine du romarin', 58, (850, 1236, 2875, 1370)),
 ('XXI · f. 25v · Un déterminant entre von et le nom', 54, (901, 591, 2933, 715)),
 ('XXI · f. 25v · Le nom précède aussi la racine', 54, (927, 2755, 2925, 2865)),
 ('XXIII · f. 27v · Le jus du romarin', 58, (851, 944, 2870, 1083)),
 ('XXIV · f. 29r · Racine du persil, ingrédient ajouté', 61, (594, 968, 2602, 1072)),
 ('XXIV · f. 29r · Le jus du sujet de la notice', 61, (593, 1190, 2601, 1297)),
]

def get_font():
    for file in ('Arial.ttf','DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(file, 21)
        except OSError:
            continue
    return ImageFont.load_default()

cuts = []
for title, page, box in ROWS:
    with Image.open(SOURCE / f'formule-gart-{page}.jpg') as img:
        scale = img.width / (3504 if page % 2 else 3434)
        crop = img.crop(tuple(round(v*scale) for v in box))
        crop.thumbnail((1080, 140))
        cuts.append((title,crop))
board = Image.new('RGB',(1110, 12+sum(46+im.height for _,im in cuts)), 'white')
draw=ImageDraw.Draw(board)
y=8
for title,crop in cuts:
    draw.text((15,y),title,font=get_font(),fill='#183e4b')
    board.paste(crop,(15,y+29))
    y += 46+crop.height
board.save(HERE/'formules-sur-pages.jpg',quality=91)
