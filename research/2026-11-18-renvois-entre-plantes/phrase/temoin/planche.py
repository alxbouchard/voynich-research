"""Composer les quatre extraits de la Library of Congress avec Pillow."""
from hashlib import sha256
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import json

HERE = Path(__file__).resolve().parent
VUES = (
    (47, "22r", "Bouillon de pois chiches", (90, 379, 400, 445)),
    (62, "29v", "Sauce au fenouil", (222, 310, 551, 390)),
    (91, "44r", "Beignets aux herbes amères", (80, 511, 421, 571)),
    (95, "46r", "Beignets soufflés", (82, 230, 389, 291)),
)


def compose(dossier):
    planche = Image.new("RGB", (1160, 1260), "white")
    dessin = ImageDraw.Draw(planche)
    try:
        police = ImageFont.truetype("Arial.ttf", 30)
    except OSError:
        police = ImageFont.load_default(size=30)
    y = 12
    sources = []
    for vue, folio, titre, cadre in VUES:
        nom = f"{vue:04d}.jp2"
        fichier = dossier / nom
        url = f"https://tile.loc.gov/storage-services/service/rbc/rbc0001/2017/2017medren60856/{nom}"
        with Image.open(fichier) as original:
            rectangle = tuple(round(i * original.height / 900) for i in cadre)
            sources.append(dict(folio=folio, url=url, dimensions=original.size,
                                coupe=rectangle, sha256=sha256(fichier.read_bytes()).hexdigest()))
            detail = original.crop(rectangle).convert("RGB")
        detail.thumbnail((1100, 310), Image.Resampling.LANCZOS)
        dessin.text((20, y), f"f. {folio}   {titre}", fill="black", font=police)
        y += 45
        planche.paste(detail, (20, y))
        y += detail.height + 25
    planche.crop((0, 0, 1160, y)).save(HERE / "martino-quatre-contextes.jpg", quality=93)
    (HERE / "SOURCES.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("originaux", type=Path)
    compose(parser.parse_args().originaux)
