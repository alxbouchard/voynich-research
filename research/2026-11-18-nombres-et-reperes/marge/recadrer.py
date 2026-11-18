"""Recrée la planche à partir du JPEG Yale et des coordonnées en pixels du TSV."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv
import hashlib

folder = Path(__file__).resolve().parent
source = folder / "f49v-yale-1006171.jpg"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "3c03e0e8b3d3e75f93ba7a7619a029b7ffbe33d7243f32222ad59ac7555dfd96"
page = Image.open(source)
assert page.size == (2935, 3769)
with (folder / "positions-f49v.tsv").open() as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
assert len(rows) == 26

def font(size, bold=False):
    for family in (("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
                   ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
                    "/System/Library/Fonts/Supplemental/Arial.ttf")):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)

canvas = Image.new("RGB", (1140, 924), "#f9f7f0")
draw = ImageDraw.Draw(canvas)
black, muted, blue = "#171d20", "#475457", "#005d77"

def label(x, y, s, size=18, color=black, bold=False, anchor=None):
    draw.text((x, y), s, fill=color, font=font(size, bold), anchor=anchor)

label(30, 18, "Les cinq chiffres de la marge du folio 49v", 35, bold=True)
label(30, 68, "Beinecke MS 408   ·   Les rangées se comptent depuis le premier signe isolé.", 20, muted)
left, top, right, bottom = 620, 395, 1200, 1085
ox, oy = 143, 153
canvas.paste(page.crop((left, top, right, bottom)), (ox, oy))
for (xx, txt) in ((710, "Chiffres"), (880, "Signes"), (1060, "Début du texte")):
    label(ox + xx-left, 127, txt, 15, blue, True, "mm")
label(30, 127, "Rangée", 15, blue, True, "lm")
for row in rows[:7]:
    n = int(row["rangee_physique"])
    y = int(row["y_chiffre_px"] or row["y_signe_px"]) + oy - top
    label(37, y, f"L{n}", 23, blue, True, "lm")
    draw.line((83, y, ox-1, y), fill=blue, width=2)
label(755, 129, "Le deuxième signe de trois séries", 18, blue, True)
label(755, 159, "Détails à la même échelle (× 2).", 16, muted)
for j, n in enumerate((3, 11, 18)):
    row = rows[n-1]
    x, y = int(row["x_signe_px"]), int(row["y_signe_px"])
    tx, ty = 755, 210 + 178*j
    crop = page.crop((x-38, y-34, x+38, y+34)).resize((152,136), Image.Resampling.NEAREST)
    canvas.paste(crop, (tx, ty))
    label(929, ty+24, f"Rangée {n}", 20, bold=True)
    label(929, ty+64, "EVA " + row["ZL3b"], 17, blue)
label(755, 765, "La courbure change entre L3 et L11.", 16)
label(755, 792, "ZL distingue les deux formes.", 16)
label(30, 876, "Yale University Library, image 1006171  ·  Recadrage principal à la taille native  ·  Repères bleus ajoutés dans la marge de la planche.", 15, muted)
canvas.save(folder / "f49v-cinq-chiffres.png", optimize=True)
