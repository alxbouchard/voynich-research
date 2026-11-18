"""Recadrer l'autre occurrence de qokchol dar, avec contrôle d'identité du cliché de Yale."""
from hashlib import sha256
from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE = "https://collections.library.yale.edu/iiif/2/1006100/full/full/0/default.jpg"
DIGEST = "1c2b3a255fc01cb6db6f1c2e971ee93e6911ef1acc2ef0800a6a7eae2572945c"
CONTEXT = (365, 395, 1930, 1095)
LINE = (430, 750, 1340, 895)
FIRST = (445, 781, 705, 892)
THIRD = (878, 778, 1051, 873)


def main(path):
    if sha256(path.read_bytes()).hexdigest() != DIGEST:
        raise ValueError("Le fichier diffère du cliché source.")
    im = Image.open(path).convert("RGB")
    board = Image.new("RGB", (985, 668), "white")
    ink = ImageDraw.Draw(board)
    font = ImageFont.load_default(size=18)
    ink.text((12, 6), "f14r - Ligne 5 du premier paragraphe", fill="black", font=font)
    overview = im.crop(CONTEXT)
    draw = ImageDraw.Draw(overview)
    for xa, ya, xb, yb in [FIRST, THIRD]:
        draw.rectangle((xa-CONTEXT[0], ya-CONTEXT[1], xb-CONTEXT[0], yb-CONTEXT[1]), outline="#96223c", width=4)
    overview.thumbnail((940, 425), Image.Resampling.LANCZOS)
    board.paste(overview, (12, 36))
    ink.text((12, 482), "qokchol      dar      dala / dalo      qotolo", fill="black", font=font)
    board.paste(im.crop(LINE), (12, 515))
    board.save(HERE / "f14r-5.jpg", quality=94)
    coords = {"url": SOURCE, "sha256": DIGEST, "largeur_hauteur": im.size, "repere": "xyxy, origine en haut à gauche, bout exclu",
              "contexte": CONTEXT, "ligne": LINE, "premier_groupe": FIRST, "troisieme_groupe": THIRD}
    (HERE / "f14r-coordonnees.json").write_text(json.dumps(coords, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
