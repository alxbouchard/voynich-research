"""Reconstituer deux planches depuis les trois JPEG de Yale en résolution native."""
import argparse
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCES = {
    "f89r2": "3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e",
    "f100v": "72637b9770f40f7a8ff6b96a551e64775e88994ae69bafec0b43d48974364c33",
    "f18r": "01659aa94a6176b56c621f50c9cbe8c467836d6265a03d8edb1e97e236126e78",
}

# Les deux bornes hautes de chaque rectangle sont exclues.
BANDS = [
    ("f89r2", (6540, 2370, 8550, 2545), "f89r2.22  |  Les deux doublets, puis le blanc",
     "sheey    opcheor    opcheol    shody    sholdy       [blanc]       qokol / qokal    chey    oldy    sheodal    ytoldy"),
    ("f100v", (1845, 2615, 2730, 2748), "f100v.16  |  Fin de la ligne, rang inférieur",
     "okeol     ches     okeor     okeol     dy"),
    ("f18r", (315, 860, 1630, 978), "f18r.7  |  Trois groupes avec un l intérieur",
     "oshor    shaiin    cthy    sholdy    doldy       [bouton de plante]       doldaiin"),
]
# Tous les détails ont la même taille native. Chaque rectangle est défini par son centre.
SIGNS = [
    ("f89r2", (6954, 2452), "opcheor", "r final"),
    ("f89r2", (7181, 2464), "opcheol", "l final"),
    ("f89r2", (7444, 2462), "sholdy", "l intérieur proposé"),
    ("f89r2", (7992, 2470), "oldy", "l intérieur"),
    ("f100v", (2386, 2689), "okeor", "r final"),
    ("f100v", (2595, 2698), "okeol", "l final"),
    ("f18r", (932, 926), "sholdy", "l intérieur"),
    ("f18r", (1108, 922), "doldy", "l intérieur"),
]


def font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.truetype("Arial.ttf", size)


def show_bands(scans):
    page = Image.new("RGB", (1320, 610), "white")
    draw = ImageDraw.Draw(page)
    for i, (source, bounds, title, caption) in enumerate(BANDS):
        top = 14 + 194 * i
        draw.text((16, top), title, font=font(22), fill="black")
        image = scans[source].crop(bounds)
        size = min(1, 1288 / image.width)
        image = image.resize((round(image.width * size), round(image.height * size)), Image.Resampling.LANCZOS)
        page.paste(image, (16, top + 33))
        draw.text((16, top + 38 + image.height), caption, font=font(16), fill="black")
    page.save(HERE / "lignes.png", optimize=True)


def show_signs(scans):
    page = Image.new("RGB", (1000, 555), "white")
    draw = ImageDraw.Draw(page)
    for i, (source, (x, y), word, role) in enumerate(SIGNS):
        source_crop = (x - 30, y - 26, x + 30, y + 26)
        image = scans[source].crop(source_crop).resize((210, 182), Image.Resampling.NEAREST)
        left, top = 13 + (i % 4) * 247, 10 + (i // 4) * 276
        draw.text((left, top), f"{source}   {word}", font=font(18), fill="black")
        page.paste(image, (left, top + 28))
        draw.text((left, top + 218), role, font=font(18), fill="black")
    page.save(HERE / "signes.png", optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in SOURCES:
        parser.add_argument(name, type=Path)
    files = vars(parser.parse_args())
    scans = {}
    for source, path in files.items():
        if sha256(path.read_bytes()).hexdigest() != SOURCES[source]:
            raise ValueError(f"Le JPEG fourni diffère de l'original vérifié de {source}")
        scans[source] = Image.open(path).convert("RGB")
    show_bands(scans)
    show_signs(scans)


if __name__ == "__main__":
    main()
