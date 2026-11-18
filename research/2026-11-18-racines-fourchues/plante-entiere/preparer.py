"""Sélection textuelle des témoins puis construction des cartes anonymes."""
import argparse
import json
import hashlib
from pathlib import Path
import random
import re
import sys

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from annoncer import ROOT, corpus, sequence

TARGET = "f40v"


def choose():
    corpus_file = ROOT / "voynich_20261028/data/ZL3b-n.txt"
    faces = set()
    for line in corpus_file.read_text().splitlines():
        header = re.match(r"^<(f\d+[rv])>", line)
        if header:
            meta = dict(re.findall(r"\$(\w)=(\w+)", line))
            if all(meta.get(k) == v for k, v in dict(Q="E", L="B", H="2", I="H").items()):
                faces.add(header[1])
    editions, _ = corpus()
    sizes = {f:0 for f in faces}
    for page, kind, _, raw in editions["H"].values():
        if page in sizes and kind == "P0":
            sizes[page] += len(sequence(raw, "joints"))
    occurrences = json.loads((HERE.parent / "hors-herbier/TOUS-LES-LIEUX.json").read_bytes())
    present = {entry["locus"].split(".")[0] for entry in occurrences if "P0" in entry["types"]}
    assert TARGET in present and TARGET in sizes
    seen = {"f40"}
    controls = []
    for f in sorted(faces - present, key=lambda n:(abs(sizes[n]-sizes[TARGET]),n)):
        leaf = f[:-1]
        if leaf in seen or sizes[f] == 0:
            continue
        controls.append(f)
        seen.add(leaf)
        if len(controls) == 4:
            break
    assert controls
    inventory = json.loads((ROOT / "voynich_resources/yale/image_index.json").read_bytes())
    chosen = sorted([TARGET, *controls])
    random.Random(463581).shuffle(chosen)
    records = {}
    for i,face in enumerate(chosen,1):
        (source,) = [r for r in inventory if r["label"] == face[1:]]
        records[f"C{i:02d}"] = {"page":face, "mots_H":sizes[face],
            "url":source["url"], "sha256":source["sha256"], "prediction":face == TARGET}
    return {"cas":records, "candidats_et_longueurs":dict(sorted(sizes.items()))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache",type=Path)
    args = parser.parse_args()
    data = choose()
    (HERE / "SELECTION.json").write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n")
    if not args.cache:
        print(*((k,v["page"],v["url"]) for k,v in data["cas"].items()), sep="\n")
        return
    folder = HERE / "C"
    folder.mkdir(exist_ok=True)
    for code,rec in data["cas"].items():
        original = args.cache / (rec["page"]+".jpg")
        assert hashlib.sha256(original.read_bytes()).hexdigest() == rec["sha256"]
        im = Image.open(original).convert("RGB")
        # Keep the lower 60% of the page, trim the binding, and obscure fine pen strokes.
        w,h = im.size
        cut = im.crop((int(.06*w),int(.40*h),int(.96*w),int(.96*h)))
        cut.thumbnail((405,350))
        cut = cut.filter(ImageFilter.GaussianBlur(radius=1.55))
        cut.save(folder / (code+".jpg"),quality=88)


if __name__ == "__main__":
    main()
