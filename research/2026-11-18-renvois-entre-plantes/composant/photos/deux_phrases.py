"""Assembler uniquement des extraits des trois JPEG Yale authentifiés. Pillow est requis."""
from hashlib import sha256
from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BIB = {
    "f18v": ("1006109", "a0f14ccc11f76d832def734e32e33dccea82222e0b198ac3d73c93e8d1fcc47f"),
    "f23r": ("1006118", "accaf5bdc2bcbbb97171d591f8352258329671eb68d095f4fe3f556979ff2e07"),
    "f102r2": ("1006251", "30fd529fc6bf8999d5be48024ee6a1676af55e8d66dc0a4f77993fe2565e9d94"),
}
LINES = {
    "f18v": (1427, 923, 2685, 1046), "f23r": (310, 817, 2097, 926),
}
WORDS = {
    "f18v": [("qokol", (1913, 927, 2127, 1030)), ("daiin", (2128, 925, 2307, 1028)),
             ("qokol", (2308, 926, 2477, 1029))],
    "f23r": [("qokchol", (886, 820, 1156, 923)), ("dar", (1156, 820, 1271, 923)),
             ("qokchol", (1277, 820, 1516, 923))],
}
ROOTS = {
    "grande_f18v": ("f18v", (780, 2535, 2640, 3690)), "212": ("f102r2", (5250, 2500, 6825, 3485)),
    "grande_f23r": ("f23r", (340, 2750, 2530, 3410)), "213": ("f102r2", (6830, 2570, 7900, 3350)),
}


def font(size, bold=False):
    name = "Arial Bold" if bold else "Arial"
    for path in [Path("/System/Library/Fonts/Supplemental") / (name + ".ttf"),
                 Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def main(directory):
    images, provenance = {}, {}
    for page, (identifier, digest) in BIB.items():
        path = directory / (page + ".jpg")
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("Original différent du JPEG indexé de Yale : " + page)
        images[page] = Image.open(path).convert("RGB")
        provenance[page] = {"sha256": digest, "dimensions": images[page].size,
                            "url": f"https://collections.library.yale.edu/iiif/2/{identifier}/full/full/0/default.jpg"}

    board = Image.new("RGB", (1500, 1568), "#ffffff")
    pen = ImageDraw.Draw(board)
    dark, grey = "#20221e", "#50554c"
    def words_at(pos, value, size, bold=False, color=dark, anchor=None):
        pen.text(pos, value, font=font(size, bold), fill=color, anchor=anchor)
    def picture_center(page, box, x, y, w, h, upscale=False):
        im = images[page].crop(box)
        scale = min(w/im.width, h/im.height)
        if not upscale:
            scale = min(1, scale)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        board.paste(im, (int(x+(w-im.width)/2), int(y+(h-im.height)/2)))

    words_at((42, 24), "Les septièmes lignes de f18v et f23r", 40, True)
    for idx, (page, box) in enumerate(LINES.items()):
        y = 94 + 121*idx
        words_at((43, y+39), page+".7", 30, True)
        picture_center(page, box, 175, y, 1280, 112)
    pen.line((42, 345, 1458, 345), fill="#c4c7bf", width=2)
    words_at((42, 366), "Les mots 4 à 6, alignés par position", 31, True)
    centers = [418, 822, 1226]
    for idx,x in enumerate(centers):
        words_at((x, 419), "Mot "+str(idx+4), 23, color=grey, anchor="mt")
    for row, (page, items) in enumerate(WORDS.items()):
        y = 456 + 140*row
        words_at((45, y+34), page+".7", 27, True)
        for center,(word, box) in zip(centers, items):
            picture_center(page, box, center-165, y, 330, 96)
            words_at((center, y+102), word, 22, anchor="mt")
    pen.line((42, 744, 1458, 744), fill="#c4c7bf", width=2)
    words_at((42, 764), "Les racines rapprochées dans le catalogue", 31, True)
    for idx, (key, fragment, title1, title2) in enumerate([
            ("grande_f18v", "212", "f18v · grande plante", "f102r2 · fragment 212"),
            ("grande_f23r", "213", "f23r · grande plante", "f102r2 · fragment 213")]):
        y = 825 + 338*idx
        for column,(k,title) in enumerate([(key,title1),(fragment,title2)]):
            x = 42+column*720
            words_at((x,y), title, 23, True)
            page,box=ROOTS[k]
            picture_center(page,box,x,y+36,695,262)
    words_at((44, 1511), "Yale, Beinecke Rare Book and Manuscript Library · MS 408. Les quatre dessins sont présentés à des échelles différentes.", 19, color=grey)
    board.save(HERE/"deux-phrases.jpg", quality=94)
    sources = {"sources": provenance, "coordonnees": "xyxy du JPEG natif, origine en haut à gauche, fin exclue.",
               "lignes_7": LINES, "mots_4_a_6": WORDS, "racines": ROOTS,
               "operation": "Rognage et redimensionnement proportionnel. Les mots isolés proviennent des deux lignes intactes présentées en haut.",
               "renvoi_catalogue": "https://www.voynich.nu/q19/index.html#f102r2"}
    (HERE/"deux-phrases-provenance.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
