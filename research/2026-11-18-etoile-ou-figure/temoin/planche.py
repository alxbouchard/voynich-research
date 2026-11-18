"""Assembler les détails de l'exemplaire de Munich, sans retouche des tracés."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DIGESTS = {
    60: "0f28e8a4d20c8cc55ac3aa583242f8a71b77b1f696a226f623acc182d213411f",
    61: "10d600c3f42e571ba404a91d3a20806f3df731664091faf38af6ec9a2c167024",
    62: "5596d764ec579da47c64442dce9579439e6c0d1ca4dee4fc211f3c3271b8ef5e",
    63: "6a4ec1885bd5232dfc59aea2e0449a6e805af4f410ddde88d2687b846d41bb47",
}


def read_pages(cache):
    pages = {}
    for view, digest in DIGESTS.items():
        path = cache / f"voy-hygin-1482-{view}.jpg"
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Photographie différente pour la vue {view}")
        pages[view] = Image.open(path).convert("RGB")
    return pages


def panel(page, bounds, width):
    crop = page.crop(bounds)
    return crop.resize((width, round(crop.height * width / crop.width)), Image.Resampling.LANCZOS)


def caption(canvas, xy, label):
    ImageDraw.Draw(canvas).text(xy, label, font=ImageFont.load_default(size=23), fill="#222222")


def build(cache):
    pages = read_pages(cache)
    full = Image.new("RGB", (1600, 860), "white")
    for column, (num, name, bounds) in enumerate([
        (60, "27v - Cassiopeia", (383, 126, 1285, 1488)),
        (61, "28r - Andromeda", (190, 120, 1080, 1475)),
        (62, "28v - Perseus", (365, 137, 1292, 1420)),
    ]):
        x = 10 + 530 * column
        caption(full, (x, 5), name)
        full.paste(panel(pages[num], bounds, 510), (x, 40))
    full.save(HERE / "trois-figures.jpg", quality=90)
    detail = Image.new("RGB", (1300, 1070), "white")
    caption(detail, (18, 6), "28v - Perseus et la Gorgone")
    detail.paste(panel(pages[62], (510, 580, 1265, 1185), 790), (16, 44))
    caption(detail, (830, 6), "28v - Les cheveux")
    detail.paste(panel(pages[62], (1070, 820, 1260, 1178), 330), (830, 44))
    caption(detail, (18, 704), "29r - Suite de la notice (lignes 4-7)")
    detail.paste(panel(pages[63], (184, 332, 1079, 508), 1258), (16, 746))
    detail.save(HERE / "quatre-etoiles.jpg", quality=93)


if __name__ == "__main__":
    build(Path(sys.argv[1]))
