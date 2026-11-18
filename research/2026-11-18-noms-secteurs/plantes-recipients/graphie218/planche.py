"""Recadrages de Beinecke MS 408, image 1006252. Coordonnées natives, origine en haut à gauche."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
im=Image.open(HERE/"f102v2-haut.jpg")
assert im.size==(2981,1450)

# Boîtes (gauche, haut, droite, bas), dans l'image Yale non redimensionnée.
boxes={
    "K":(1274,968,1332,1055),  # milieu de f102v2.12, après le o initial
    "T":(2211,469,2281,562),  # f102v2.8, après le o initial
    "A":(1342,453,1400,545),  # f102v2.6, après le o initial
    "B":(1795,453,1882,544),  # f102v2.7, après le o initial
    "C":(873,1110,935,1207), # f102v2.17, mot 2, signe haut
}
font=ImageFont.load_default(size=20)
board=Image.new("RGB",(580,440),"white")
draw=ImageDraw.Draw(board)
cards=(("K",70,6),("T",315,6),("A",6,220),("B",200,220),("C",390,220))
for code,x,y in cards:
    crop=im.crop(boxes[code])
    crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST)
    board.paste(crop,(x+10,y+30))
    draw.text((x+8,y),("Reference "+code) if code in "KT" else code,fill="black",font=font)
board.save(HERE/"planche.png")

# Bande indépendante pour contrôler le rang des dessins ; aucun cadre ne recouvre l'encre.
region=(230,355,2850,880)
overview=im.crop(region)
pen=ImageDraw.Draw(overview)
for n,(x,y) in enumerate([(676,665),(924,628),(1145,580),(1337,637),
                         (1627,595),(2040,663),(2450,613)],214):
    pen.text((x-region[0],y-region[1]),str(n),fill="#7e192c",font=ImageFont.load_default(size=34),
             stroke_width=2,stroke_fill="#fff9ea")
for n,(x,y) in enumerate([(560,455),(808,459),(1020,449),(1350,408),
                          (1810,410),(2220,420),(2680,418)],3):
    pen.text((x-region[0],y-region[1]),"."+str(n),fill="#163b75",font=ImageFont.load_default(size=28),
             stroke_width=2,stroke_fill="#fff9ea")
overview.thumbnail((1450,530))
overview.save(HERE/"rangee.jpg",quality=93)
