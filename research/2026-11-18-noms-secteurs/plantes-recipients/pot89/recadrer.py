"""Reproduce the crops from Yale image 1006233, full native JPG."""
import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE_HASH = "3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e"
CONTEXT = (5130, 185, 7300, 1810)
WORDS = [
    ("f89r2.9", (5480, 1172, 5690, 1290)),
    ("f89r2.1", (5520, 462, 5710, 577)),
    ("f89r2.2", (5775, 498, 5938, 642)),
    ("f89r2.10", (6585, 1238, 6679, 1337)),
]


def main(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SOURCE_HASH:
        raise ValueError("Yale image 1006233 expected at native resolution")
    with Image.open(path) as source:
        assert source.size == (9078, 3777)
        context = source.crop(CONTEXT)
        context.thumbnail((1085, 813))
        context.save(HERE / "deux-rangees.jpg", quality=92)
        source.crop(WORDS[0][1]).save(HERE / "f89r2-9-natif.png")
        sheet = Image.new("RGB", (820, 395), "white")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default(size=18)
        for index,(locus, bounds) in enumerate(WORDS):
            crop = source.crop(bounds)
            crop = crop.resize((round(crop.width*1.4), round(crop.height*1.4)), Image.Resampling.NEAREST)
            left = (index % 2) * 410 + 10
            top = 4 if index < 2 else 177
            draw.text((left,top), locus, font=font, fill="black")
            sheet.paste(crop, (left+96,top+6))
        sheet.save(HERE / "quatre-finales.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    main(parser.parse_args().image)
