"""Présenter une deuxième fois tous les pieds à résolution supérieure, jusqu'au bord du cliché."""
import hashlib
import json
from pathlib import Path
import random
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent


def main(cache):
    selection = json.loads((HERE/"SELECTION.json").read_bytes())["cas"]
    order = list(selection)
    random.Random(7253920).shuffle(order)
    key = {}
    (HERE/"D").mkdir(exist_ok=True)
    for index, old in enumerate(order, 1):
        rec = selection[old]
        source = cache / (rec["page"]+".jpg")
        assert hashlib.sha256(source.read_bytes()).hexdigest()==rec["sha256"]
        page = Image.open(source)
        w,h = page.size
        region = (0,int(.72*h),w,h)
        crop = page.crop(region).convert("RGB")
        crop.thumbnail((1150,590))
        new = f"D{index}"
        crop.save(HERE/"D"/(new+".jpg"),quality=93)
        key[new] = {"premiere_carte":old,"region":region}
    (HERE/"DETAILS.json").write_text(json.dumps(key,indent=1)+"\n")


if __name__=="__main__":
    main(Path(sys.argv[1]))
