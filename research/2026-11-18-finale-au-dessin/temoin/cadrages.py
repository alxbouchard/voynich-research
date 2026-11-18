"""Compose deux planches de contrôle à partir des vues intégrales Wellcome (Pillow)."""
import csv
from pathlib import Path
from PIL import Image, ImageDraw

ICI = Path(__file__).resolve().parent
with (ICI / "bouts.tsv").open(encoding="utf-8") as src:
    lignes = list(csv.DictReader(src, delimiter="\t"))
with (ICI / "mots.tsv").open(encoding="utf-8") as src:
    candidats = {(m["folio"], m["vers"]) for m in csv.DictReader(src, delimiter="\t")}

for folio in ("f3r", "f4v"):
    with Image.open(ICI / f"{folio}.jpg") as original:
        facteur = original.height / 1070
        donnees = [r for r in lignes if (r["folio"], r["vers"]) in candidats and r["folio"] == folio]
        marge_gauche, marge_droite = (128, 588) if folio == "f3r" else (200, 656)
        feuille = Image.new("RGB", (1040, len(donnees)*76), "white")
        legende = ImageDraw.Draw(feuille)
        for index, ligne in enumerate(donnees):
            centre = int(ligne["y_centre_repere"])
            zone = (marge_gauche, centre - 17, marge_droite, centre + 22)
            bande = original.crop(tuple(round(x * facteur) for x in zone))
            bande.thumbnail((990, 76), Image.Resampling.LANCZOS)
            feuille.paste(bande, (50, index * 76))
            legende.text((7, index*76 + 27), ligne["vers"], fill="black")
        feuille.save(ICI / f"lecture-{folio}.jpg", quality=90)
