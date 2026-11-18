"""Vérifier les empreintes du catalogue Yale et refaire trois planches à partir des JPEG natifs."""
from hashlib import sha256
from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FILES = {"f18v": "18v", "f102r2": "101v (part) and 102r", "f89r1": "88v and 89r",
         "f30r": "30r", "f3r": "3r", "f23v": "23v"}

# Coordonnées sur les vues entières, origine en haut à gauche, droite et bas exclus.
PLATES = {
    "qokol-oky.jpg": [
        ("f18v", (1420, 923, 2680, 1045), "f18v.7   ychol dor chod [qokol daiin qokol] dar dy"),
        ("f102r2", (5480, 2255, 7510, 2475), "f102r2.18   fin de la ligne, avec pli vertical dans le premier oky"),
        ("f102r2", (6540, 2290, 7460, 2470), "Detail de la fin   sheey [qokol daiin oky oky]"),
        ("f102r2", (5410, 2100, 7530, 3270), "Paragraphe et deux fragments   212 a gauche, 213 a droite"),
    ],
    "qokechy.jpg": [
        ("f30r", (330, 735, 1320, 900), "f30r.4   [qokechy] qoko, au debut de la ligne"),
        ("f89r1", (3110, 1055, 5080, 1240), "f89r1.8   cheody [qokechy] daiin, dans la troisieme ligne du paragraphe"),
        ("f89r1", (3040, 920, 5130, 1845), "Paragraphe et fragments 27, 28, 29. Le 28 est la racine fine au centre."),
    ],
    "interruptions.jpg": [
        ("f3r", (1210, 1980, 2260, 2170), "f3r.16   [qokol daiin] / tige / [soleeg]"),
        ("f3r", (1120, 1500, 2320, 2420), "Contexte de la tige. La ligne cible est la deuxieme du paragraphe median."),
        ("f23v", (1170, 852, 2480, 1035), "f23v.7   [qokol daiin] / partie basse de la fleur / [sol] daiin ylg"),
        ("f23v", (900, 525, 2500, 1250), "Contexte floral. La ligne cible est la deuxieme du second paragraphe."),
    ],
}


def run(source):
    index = json.loads((ROOT / "voynich_resources/yale/image_index.json").read_text())
    images, provenance = {}, {}
    for page, label in FILES.items():
        record, = (entry for entry in index if entry["label"] == label)
        jpg = source / (page + ".jpg")
        digest = sha256(jpg.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            raise ValueError(f"JPEG différent de l'original indexé de Yale: {page}")
        images[page] = Image.open(jpg)
        provenance[page] = {k: record[k] for k in ["label", "url", "sha256", "width", "height"]}

    metadata = {"sources": provenance, "fenetres_xyxy": PLATES}
    (HERE / "coordonnees.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    for name, rows in PLATES.items():
        blocks = []
        for page, box, label in rows:
            im = images[page].crop(box)
            im.thumbnail((1195, 570), Image.Resampling.LANCZOS)
            blocks.append((im, label))
        height = sum(im.height+53 for im, _ in blocks)
        canvas = Image.new("RGB", (1220, height), "white")
        pen = ImageDraw.Draw(canvas)
        y = 0
        for im, label in blocks:
            pen.text((12, y+5), label, fill="black", font=ImageFont.load_default(size=19))
            canvas.paste(im, (12, y+34))
            y += im.height+53
        canvas.save(HERE / name, quality=93)


if __name__ == "__main__":
    run(Path(sys.argv[1]))
