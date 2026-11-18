"""Construire des cartes des deux cibles avec contrôle de classe, de main et de longueur."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from annoncer import ROOT


def main(cache):
    pages = json.loads((HERE/"F55-TEXTE.json").read_bytes())["pages"]
    c = json.loads((HERE.parent/"plante-entiere/SELECTION.json").read_bytes())["cas"]
    excluded = {v["page"][:-1] for v in c.values()} | {"f55","f34"}
    eligible = [p for p,rows in pages.items() if not any(x["fin_dam_meme_ligne"] for x in rows)]
    lengths = {p:sum(r["longueurs"][0] for r in rows) for p,rows in pages.items()}
    pool = []
    for case in ("f34r","f55r"):
        control = min((p for p in eligible if p[:-1] not in excluded),
                      key=lambda p:(abs(lengths[p]-lengths[case]),p))
        pool.extend([case,control])
        excluded.add(control[:-1])
    random.Random(251118).shuffle(pool)
    meta = json.loads((ROOT/"voynich_resources/yale/image_index.json").read_bytes())
    key = {}
    for i,p in enumerate(pool,1):
        source = next(s for s in meta if s["label"]==p[1:])
        code = f"F{i}"
        key[code] = {"page":p,"mots":lengths[p],"prediction":p in ("f34r","f55r"),
                     "sha256":source["sha256"],"url":source["url"]}
        if cache:
            path = cache/(p+".jpg")
            assert hashlib.sha256(path.read_bytes()).hexdigest()==source["sha256"]
            photo = Image.open(path).convert("RGB")
            w,h = photo.size
            cut = photo.crop((0,round(.65*h),w,h))
            cut.thumbnail((1000,530))
            folder = HERE/"F"
            folder.mkdir(exist_ok=True)
            cut.save(folder/(code+".jpg"),quality=91)
    (HERE/"DEUX-PAGES.json").write_text(json.dumps(key,indent=1)+"\n")
    print([(rec["page"],rec["url"]) for rec in key.values()])


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache",type=Path)
    main(parser.parse_args().cache)
