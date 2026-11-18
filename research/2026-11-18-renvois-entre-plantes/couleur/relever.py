"""Fréquences olky et croquis photographiques. Exécuter sans argument pour le texte."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import MODES, corpus, parse

SITES = {
    "f99v": (1006247, (1980, 1910)),
    "f9v": (1006093, (1473, 1204)),
    "f20r": (1006112, (1549, 3288)),
    "f32r": (1006136, (1956, 1938)),
    "f29r": (1006130, (1624, 3230)),
}


def save(name, rows):
    (HERE / name).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")


def numbers():
    editions, _ = corpus()
    rows = {}
    for ed, cut in MODES:
        values = {}
        for place, (page, kind, _, raw) in editions[ed].items():
            if kind not in {"Lf", "P0"}:
                continue
            # Les numéros ajoutés par le catalogueur désignent les illustrations.
            if kind == "Lf":
                raw = re.sub(r"^<![0-9]+>", "", raw)
            words = [w for block in parse(raw, cut)[1] for w in block]
            key = "legendes_Lf" if kind == "Lf" else "prose_P0"
            for category in ([key, "prose_f99v"] if kind == "P0" and page == "f99v" else [key]):
                cnt = values.setdefault(category, {"lignes": 0, "mots_lus": 0, "rangs_olky": [],
                                                   "formes_qui_contiennent_olky": []})
                cnt["lignes"] += 1
                cnt["mots_lus"] += sum(bool(re.fullmatch(r"[a-z]+", w)) for w in words)
                for i, w in enumerate(words, 1):
                    if w == "olky":
                        cnt["rangs_olky"].append([place, i])
                    if kind == "Lf" and "olky" in w and w != "olky":
                        cnt["formes_qui_contiennent_olky"].append([place, i, w])
        rows[f"{ed}/{cut}"] = values
    save("frequences.json", rows)


def photographies(cache):
    from PIL import Image, ImageDraw, ImageStat
    images = {}
    source = {}
    for page, (identifier, xy) in SITES.items():
        name = cache / (page + ".jpg")
        images[page] = Image.open(name).convert("RGB")
        def median_at(point):
            x, y = point
            return ImageStat.Stat(images[page].crop((x-30, y-30, x+31, y+31))).median
        source[page] = {"url": f"https://collections.library.yale.edu/iiif/2/{identifier}/full/full/0/default.jpg",
                        "sha256": sha256(name.read_bytes()).hexdigest(), "dimensions": images[page].size,
                        "centre": xy, "mediane_RGB_61": median_at(xy)}
        if page == "f99v":
            source[page].update(parchemin_xy=[1800, 1910], parchemin_mediane_RGB_61=median_at((1800, 1910)))

    old = Image.new("RGB", (1024, 1280))
    hashes = {}
    for r in range(9, 14):
        for c in range(13, 17):
            tile = cache / f"112-{r}-{c}.webp"
            old.paste(Image.open(tile), ((c-13)*256, (r-9)*256))
            hashes[f"{r}/{c}"] = sha256(tile.read_bytes()).hexdigest()
    source["f99v_2004"] = {"source": "https://voynich.jasondavies.com/f99v/5/{y}/{x}.webp",
                            "x": [13, 16], "y": [9, 13], "sha256_y_x": hashes}
    save("sources-et-mesures.json", source)

    # Montage à échelle comparable. Les pixels de la trace restent intacts.
    pair = Image.new("RGB", (970, 804), "white")
    draw = ImageDraw.Draw(pair)
    panels = [
        ("2014 - Yale", images["f99v"].crop((1760, 1550, 2250, 2280)), (175, 375)),
        ("2004 - Beinecke, via Jason Davies", old.crop((200, 80, 970, 1227)).resize((490, 730), Image.Resampling.LANCZOS), (143, 326)),
    ]
    for i, (label, panel, _) in enumerate(panels):
        x = i * 486
        draw.text((x + 5, 5), label, fill="black")
        pair.paste(panel.resize((470, 700), Image.Resampling.LANCZOS), (x, 27))
    draw.text((8, 742), "Fragment 112, f99v. Trace sombre au milieu de la partie gauche de la racine.", fill="black")
    draw.text((8, 764), "Les deux numerisations sont en lumiere visible.", fill="black")
    pair.save(HERE / "f99v-deux-cliches.jpg", quality=95)
    witnesses = Image.new("RGB", (850, 710), "white")
    pen = ImageDraw.Draw(witnesses)
    for i, page in enumerate(["f9v", "f20r", "f32r", "f29r"]):
        x,y = SITES[page][1]
        left,top = (i%2)*425,(i//2)*350
        pen.text((left+6,top+4), f"{page} - centre ({x}, {y})",fill="black")
        witnesses.paste(images[page].crop((x-200,y-152,x+200,y+152)), (left+5,top+26))
    witnesses.save(HERE / "quatre-comparaisons.jpg", quality=95)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--photos", type=Path, help="dossier avec f99v.jpg, f9v.jpg, f20r.jpg, f32r.jpg, f29r.jpg et 112-{y}-{x}.webp")
    args = cli.parse_args()
    numbers()
    if args.photos:
        photographies(args.photos)
