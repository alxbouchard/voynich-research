"""Dérouler le deuxième anneau d'après le JPEG pleine résolution de Yale 1006187."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
META = json.loads((HERE / "RESULTATS.json").read_text())
SECTORS = [(304, 404), (404, 494.5), (494.5, 579.5), (579.5, 664)]


def font(size):
    for name in ("DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jpeg_yale", type=Path)
    parser.add_argument("sortie", type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.jpeg_yale.read_bytes()).hexdigest() != META["sha256_image"]:
        raise ValueError("Le JPEG doit correspondre au fac-similé pleine taille référencé.")
    photo = np.asarray(Image.open(args.jpeg_yale).convert("RGB"))
    with (HERE / "POSITIONS.tsv").open() as infile:
        positions = list(csv.DictReader(infile, delimiter="\t"))
    page = Image.new("RGB", (1832, 1025), "#FAF8F4")
    draw = ImageDraw.Draw(page)
    title_font, body_font, tick_font = font(30), font(19), font(17)
    ink, accent = "#272521", "#19586A"
    draw.text((24, 14), "Folio 57v  ·  Les quatre tours de la deuxième couronne", font=title_font, fill=ink)
    draw.text((24, 62), "Sens horaire depuis le nord-ouest. Les numéros sous la bande désignent les groupes graphiques.", font=body_font, fill=ink)
    cx, cy = META["centre_image_xy_px"]
    row_top = 116
    left = 95
    for i, (start, end) in enumerate(SECTORS, 1):
        width = round((end - start) * 17)
        angles = np.deg2rad(np.linspace(start, end, width, endpoint=False))
        radii = np.arange(1008, 841, -1)[:, None]
        x = np.rint(cx + radii * np.sin(angles)).astype(int)
        y = np.rint(cy - radii * np.cos(angles)).astype(int)
        strip = Image.fromarray(photo[y, x])
        page.paste(strip, (left, row_top))
        draw.text((16, row_top + 67), f"Tour {i}", font=body_font, fill=ink)
        for row in positions:
            if int(row["cycle"]) != i:
                continue
            angle = float(row["angle_horaire_approx_deg_nord"])
            while angle < start:
                angle += 360
            xpos = left + (angle - start) * width / (end - start)
            ypos = row_top + strip.height
            draw.line((xpos, ypos, xpos, ypos + 6), fill=accent, width=1)
            draw.text((xpos, ypos + 8), row["position_17"], font=tick_font, anchor="mt", fill=accent)
        row_top += 213
    draw.text((24, 982), "Yale, Beinecke Rare Book and Manuscript Library, MS 408, f. 57v, image 1006187. Coordonnées dans POSITIONS.tsv.", font=body_font, fill=ink)
    page.save(args.sortie, quality=91, optimize=True)


if __name__ == "__main__":
    main()
