"""Régénère deux planches à partir du JPEG IIIF Yale identifié par son empreinte."""
from hashlib import sha256
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA256 = "4ce0750cd5118df63ca35fe955dcf3add4160d2ddb5e2770e47bb9930e992fc3"
CONTEXT = (655, 1145, 1390, 1420)

# Coordonnées absolues dans le JPEG Yale. Boîtes [gauche, haut, droite, bas).
ROWS = [
    [
        ("f23v.12  cible", (705, 1301, 942, 1405)),
        ("f23v.12  oloro, r interne", (935, 1297, 1114, 1391)),
    ],
    [
        ("f23v.1  s", (2354, 448, 2411, 544)),
        ("f23v.3  eees", (1201, 609, 1321, 695)),
        ("f23v.9  chees", (2218, 1049, 2371, 1128)),
        ("f23v.11  olols", (1230, 1220, 1422, 1311)),
        ("f23v.11  ols", (2282, 1181, 2424, 1284)),
    ],
    [
        ("f23v.5  dor", (703, 753, 813, 833)),
        ("f23v.6  shor", (896, 829, 1049, 932)),
        ("f23v.7  otor", (721, 926, 862, 1008)),
        ("f23v.9  or", (1537, 1079, 1625, 1150)),
        ("f23v.10  dor", (728, 1150, 842, 1231)),
    ],
]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("python recadrer.py /chemin/1006119.jpg")
    source = Path(sys.argv[1])
    if sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("Le JPEG ne correspond pas à l’empreinte Yale enregistrée.")
    out = Path(__file__).resolve().parent
    image = Image.open(source).convert("RGB")
    image.crop(CONTEXT).save(out / "derniere-ligne.png")
    background = "#f8f7f3"
    board = Image.new("RGB", (1270, 515), background)
    draw = ImageDraw.Draw(board)
    title = ImageFont.load_default(size=21)
    label = ImageFont.load_default(size=16)
    headings = [
        "Ligne 12  |  premier groupe et comparaison dans le groupe suivant",
        "Cinq finales s  |  accord entre H et ZL",
        "Cinq finales or  |  accord entre H et ZL",
    ]
    for i, row in enumerate(ROWS):
        y = 8 + 172 * i
        draw.text((14, y), headings[i], font=title, fill="#24282a")
        for j, (name, box) in enumerate(row):
            x = 14 + 252 * j
            draw.text((x, y + 32), name, font=label, fill="#24282a")
            board.paste(image.crop(box), (x, y + 55))
    board.save(out / "comparaisons.png")


if __name__ == "__main__":
    main()
