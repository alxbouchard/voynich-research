"""Vérifier les pixels des deux cartes à partir du JPEG original de Yale."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


def verifier(source):
    dossier = Path(__file__).resolve().parent
    masques = json.loads((dossier / "MASQUES.json").read_text())
    if hashlib.sha256(source.read_bytes()).hexdigest() != masques["photographie"]["sha256_archive_jpeg"]:
        raise ValueError("Le fichier diffère du JPEG Yale vérifié.")

    with Image.open(source) as original:
        for carte in masques["cartes"]:
            boite = carte["boite"]
            image = original.crop(boite).convert("RGB")
            masque = Image.new("L", image.size)
            dessin = ImageDraw.Draw(masque)
            for champ, valeur in [("inclure", 255), ("exclure", 0)]:
                for polygone in carte[champ]:
                    points = [(x - boite[0], y - boite[1]) for x, y in polygone]
                    dessin.polygon(points, fill=valeur)
            zone_ecriture = (1480 - boite[0], 363 - boite[1], 1655 - boite[0], 456 - boite[1])
            if masque.crop(zone_ecriture).getbbox():
                raise ValueError("L’inscription f88v.3 touche le masque.")
            fond = Image.new("RGB", image.size, tuple(carte["fond_rgb"]))
            attendu = Image.composite(image, fond, masque)
            fichier = dossier / "cartes" / (carte["carte"] + ".png")
            if hashlib.sha256(fichier.read_bytes()).hexdigest() != carte["sha256_png"]:
                raise ValueError(f"{fichier.name} a changé.")
            with Image.open(fichier) as observe:
                if observe.size != attendu.size or observe.mode != "RGB" or observe.info:
                    raise ValueError(f"Dimensions, mode ou métadonnées inattendus dans {fichier.name}.")
                if ImageChops.difference(attendu, observe).getbbox():
                    raise ValueError(f"Écart photographique dans {fichier.name}.")
            print(f"{fichier.name} vérifiée pixel par pixel. Zone de la légende entièrement masquée.")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("jpeg_yale", type=Path)
    verifier(arguments.parse_args().jpeg_yale)
