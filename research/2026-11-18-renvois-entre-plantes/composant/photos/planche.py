"""Recréer le relevé des trois dar à partir du cliché Yale 1006118."""
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE = "https://collections.library.yale.edu/iiif/2/1006118/full/full/0/default.jpg"
DIGEST = "accaf5bdc2bcbbb97171d591f8352258329671eb68d095f4fe3f556979ff2e07"
CONTEXT = (230, 330, 2160, 1220)
OCCURRENCES = [
    ("f23r.6", (982, 756, 1086, 835), (831, 748, 1310, 855), "yky   dar   okol"),
    ("f23r.7", (1158, 825, 1262, 907), (862, 821, 1520, 930), "qokchol   dar   qokchol"),
    ("f23r.10", (1802, 1021, 1905, 1112), (1422, 1013, 2078, 1137), "fleur   dar   ykain"),
]


def main(source):
    if hashlib.sha256(source.read_bytes()).hexdigest() != DIGEST:
        raise ValueError("Le JPEG ne correspond pas à la source indexée.")
    im = Image.open(source).convert("RGB")
    board = Image.new("RGB", (1130, 1016), "white")
    panel = im.crop(CONTEXT)
    draw = ImageDraw.Draw(panel)
    for _, (x0, y0, x1, y1), _, _ in OCCURRENCES:
        draw.rectangle((x0-CONTEXT[0], y0-CONTEXT[1], x1-CONTEXT[0], y1-CONTEXT[1]), outline="#96223c", width=5)
    panel.thumbnail((1100, 510), Image.Resampling.LANCZOS)
    board.paste(panel, (15, 37))
    d = ImageDraw.Draw(board)
    font = ImageFont.load_default(size=18)
    d.text((15, 7), "Beinecke MS 408, f23r. Les cadres indiquent les trois groupes.", fill="black", font=font)
    y = 555
    for loc, _, box, reading in OCCURRENCES:
        d.text((18, y), loc+"    "+reading, fill="black", font=font)
        board.paste(im.crop(box), (17, y+25))
        y += 151
    board.save(HERE / "dar-f23r.jpg", quality=94)
    coords = {"source": SOURCE, "sha256": DIGEST, "dimensions": im.size, "contexte_xyxy": CONTEXT,
              "repere": "Pixels depuis le coin supérieur gauche. Fin de cadrage exclue.",
              "lectures": [{"ligne": locus, "cadre_dar_xyxy": box, "extrait_xyxy": crop, "legende": label}
                           for locus, box, crop, label in OCCURRENCES]}
    (HERE / "coordonnees.json").write_text(json.dumps(coords, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
