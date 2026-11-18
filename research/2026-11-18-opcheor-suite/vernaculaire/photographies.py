"""Cadrer les deux mots italiens de 17r et les trois groupes du Voynich f19r.2."""
from hashlib import sha256
from pathlib import Path
import json,sys
from PIL import Image
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/"2026-11-18-d-initial-et-formules/deux-lignes/photos"))
from planche import entries

def main(jp2,cache):
    digest=sha256(jp2.read_bytes()).hexdigest()
    assert digest=="a45478fc9c389b4996090272ae5b1591055eeae7caacc85273991534bcb521c1"
    box=[310,1580,1670,1830]
    with Image.open(jp2) as native:
        native.crop(box).save(HERE/"martino-f17r.jpg",quality=95,subsampling=0)
    index={item["label"]:item for item in json.loads((RESEARCH.parent/"voynich_resources/yale/image_index.json").read_bytes())}
    data=entries("f19r",2,cache,index)
    groups=[row["boite"] for row in data["groupes"] if row["rang"] in (2,3,4)]
    assert len(groups)==3
    xmin=min(g[0] for g in groups)-23;ymin=min(g[1] for g in groups)-24
    xmax=max(g[2] for g in groups)+26;ymax=max(g[3] for g in groups)+24
    data["trois_groupes"]=[xmin,ymin,xmax,ymax]
    with Image.open(cache/"f19r-n.jpg") as native:
        native.crop(data["trois_groupes"]).save(HERE/"voynich-f19r.jpg",quality=96,subsampling=0)
    out={"italien":{"source":"https://tile.loc.gov/storage-services/service/rbc/rbc0001/2017/2017medren60856/0037.jp2",
                    "sha256":digest,"cadre":box},"voynich":data}
    (HERE/"PHOTOGRAPHIES.json").write_text(json.dumps(out,indent=1,ensure_ascii=False)+"\n")

if __name__=="__main__":main(*map(Path,sys.argv[1:]))
