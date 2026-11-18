"""Assembler les rubriques et les deux figures précédentes de l'exemplaire de Munich."""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROWS = json.loads((HERE / "IMAGES.json").read_bytes())


def panels(rows, destination, drawings=False):
    images = []
    for row in rows:
        path = Path(sys.argv[1]) / row["nom"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        with Image.open(path) as source:
            im = source.crop(row["decoupe"])
        if drawings:
            im.thumbnail((450, 490), Image.Resampling.LANCZOS)
        images.append(im)
    if drawings:
        out = Image.new("RGB", (sum(i.width + 36 for i in images), max(i.height for i in images) + 66), "white")
    else:
        out = Image.new("RGB", (max(i.width for i in images) + 36, sum(i.height + 57 for i in images) + 8), "white")
    x, y = 18, 9
    draw = ImageDraw.Draw(out)
    for row, im in zip(rows, images, strict=True):
        title = f"Munich, vue {row['vue']}  |  Ch. {row['chapitre']}"
        draw.text((x, y), title, font=ImageFont.load_default(size=22), fill="#1c2833")
        out.paste(im, (x, y+32))
        if drawings:
            x += im.width + 36
        else:
            y += im.height + 57
    out.save(HERE / destination, quality=92)


panels(ROWS[:3], "trois-rubriques.jpg")
panels(ROWS[3:], "deux-dessins.jpg", drawings=True)
