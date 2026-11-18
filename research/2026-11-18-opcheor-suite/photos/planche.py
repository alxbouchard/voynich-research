"""Reproduire les planches depuis six vues originales du Beinecke MS 408."""
from hashlib import sha256
from itertools import groupby
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCES = {
    "f52v": ("52v", "q07/f052v"),
    "f93r": ("93r", "q17/f093r"),
    "f89r2": ("88v and 89r", "q15/f089r2"),
    "f100v": ("100v and 101r", "q19/f100v"),
    "f81v": ("81v", "q13/f081v"),
    "f107v": ("107v", "q20/f107v"),
}
# Les rectangles sont mesurés dans le JPEG natif, depuis son coin supérieur gauche.
CROPS = {
    "f52v.4": (850, 607, 2300, 759),
    "f52v.4-detail": (1070, 614, 1825, 741),
    "f93r.7": (345, 789, 1220, 940),
    "f93r.7-detail": (373, 814, 819, 932),
    "f89r2.22": (6680, 2362, 7550, 2515),
    "f100v.16": (2186, 2594, 2760, 2740),
    "f100v.17": (830, 2610, 1155, 2765),
    "f81v.19": (1920, 1473, 2530, 1599),
    "f107v.14": (1060, 882, 1845, 1029),
}
GAPS = {
    "qokar | qokal": (2147, 1542),
    "qokal | dol": (2320, 1528),
    "dol | chy": (2420, 1529),
    "interieur du second qokal": (2249, 1530),
}
PAPER = "#fbfaf6"
INK = "#242a2b"


def font(n):
    for name in ("DejaVuSans.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, n)
        except OSError:
            continue
    return ImageFont.load_default()


def texte(image, xy, words, size):
    ImageDraw.Draw(image).text(xy, words, font=font(size), fill=INK)


def paste(page, img, xy, maxw, maxh):
    scale = min(maxw / img.width, maxh / img.height)
    w, h = round(img.width * scale), round(img.height * scale)
    resized = img.resize((w, h), Image.Resampling.LANCZOS)
    page.paste(resized, xy)
    return scale


def source_images(cache):
    index = json.loads((ROOT / "voynich_resources/yale/image_index.json").read_bytes())
    records = {}
    images = {}
    for page, (label, inter) in SOURCES.items():
        info = next(r for r in index if r["label"] == label)
        src = cache / (page + "-n.jpg")
        digest = sha256(src.read_bytes()).hexdigest()
        assert digest == info["sha256"], page
        images[page] = Image.open(src).convert("RGB")
        records[page] = {"vue_yale": info["url"], "sha256": digest, "dimensions": images[page].size,
                         "anciennes_lectures": f"https://www.voynich.nu/{inter}_tr.txt"}
    return records, images


def herbal(images):
    out = Image.new("RGB", (1580, 1115), PAPER)
    for i, (page, locus, reading, caption) in enumerate([
        ("f52v", "f52v.4", "tchor   ctheor   ctheol   cheeor   cheol   chckheey   sody",
         "ctheor  ctheol  cheeor  cheol"),
        ("f93r", "f93r.7", "shor   shol   ody   cheodaiin   s", "shor  shol  ody")
    ]):
        y = 553 * i
        source = images[page]
        texte(out, (15, y + 9), locus, 28)
        scale = paste(out, source, (14, y + 55), 386, 470)
        box = CROPS[locus]
        coords = [int((14 if j % 2 == 0 else y + 55) + b * scale) for j, b in enumerate(box)]
        ImageDraw.Draw(out).rectangle(coords, outline="#a33c24", width=3)
        texte(out, (409, y + 24), "Ligne entière", 22)
        paste(out, source.crop(box), (409, y + 65), 1148, 169)
        texte(out, (409, y + 239), reading, 23)
        texte(out, (409, y + 291), "Détail de la suite", 22)
        paste(out, source.crop(CROPS[locus + "-detail"]), (409, y + 331), 1145, 155)
        texte(out, (409, y + 497), caption, 24)
    out.save(HERE / "deux-grandes-plantes.jpg", quality=92, subsampling=0)


def strips(images, filename, rows):
    out = Image.new("RGB", (1350, 320 * len(rows)), PAPER)
    for i, (locus, caption) in enumerate(rows):
        y = i * 320
        src = images[locus.split(".")[0]].crop(CROPS[locus])
        texte(out, (15, y + 7), locus, 26)
        paste(out, src, (15, y + 52), 1320, 194)
        texte(out, (15, y + 262), caption, 23)
    out.save(HERE / filename, quality=93, subsampling=0)


def widths(image):
    gray = image.convert("L")
    out = {}
    for label, (x, y) in GAPS.items():
        samples = {}
        for threshold in (105, 125, 145):
            def clear(col):
                return all(gray.getpixel((col, row)) >= threshold for row in range(y, y + 12))
            for status, group in groupby(range(x - 85, x + 86), key=clear):
                cols = list(group)
                if cols[0] <= x <= cols[-1]:
                    assert status
                    samples[threshold] = [cols[0], cols[-1], len(cols)]
                    break
        out[label] = {"x": x, "y": y, "hauteur": 12, "seuils_xmin_xmax_largeur": samples}
    return out


def main(cache):
    sources, images = source_images(cache)
    herbal(images)
    strips(images, "deux-lignes-de-depart.jpg", [
        ("f89r2.22", "opcheor  opcheol  shody  sholdy"),
        ("f100v.16", "okeor  okeol  dy, fin de ligne"),
        ("f100v.17", "chockhey, premier groupe de la ligne suivante"),
    ])
    strips(images, "deux-qokar-qokal.jpg", [
        ("f107v.14", "qokar  qokal  qokal  cheody"),
        ("f81v.19", "qokar  qokal  dol  chy, avec une coupure discutée entre les deux derniers groupes"),
    ])
    record = {"sources": sources, "cadres_x1_y1_x2_y2": CROPS, "espaces_f81v": widths(images["f81v"])}
    (HERE / "SOURCES.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
