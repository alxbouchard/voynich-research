"""Régénérer la planche à partir des cinq JPEG de sources.json, nommés par numéro de vue."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent


def font(size):
    for filename in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(filename).is_file():
            return ImageFont.truetype(filename, size)
    return ImageFont.load_default(size=size)


def main(folder):
    sources = json.loads((HERE / "sources.json").read_text())
    blocks = []
    for row in sources["photos"]:
        source = folder / f"{row['vue']}.jpg"
        if sha256(source.read_bytes()).hexdigest() != row["sha256_source"]:
            raise ValueError(f"Image source différente pour la vue {row['vue']}")
        crop = Image.open(source).crop(row["recadrage_dans_source_xyxy"])
        crop.thumbnail((1390, 215), Image.Resampling.LANCZOS)
        blocks.append((row, crop))
    board = Image.new("RGB", (1440, 120+sum(im.height+66 for _,im in blocks)), "white")
    text = ImageDraw.Draw(board)
    text.text((23,12),"Celse, De medicina · Florence, 1478", font=font(35), fill="#23251c")
    y = 85
    for row,im in blocks:
        name = f"{row['passage']} · f. {row['folio']} · {row['titre']}"
        text.text((24,y),name,font=font(23),fill="#23251c")
        board.paste(im,(24,y+36))
        y += im.height+66
    text.text((23,y-6),"Munich, Bayerische Staatsbibliothek · bsb00050602", font=font(17), fill="#45473e")
    board.save(HERE/"celse-florence-1478.jpg",quality=94)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
