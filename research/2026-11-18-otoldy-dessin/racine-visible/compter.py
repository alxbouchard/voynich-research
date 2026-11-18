import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHOTOS = HERE.parent / "photos"
votes = {r:json.loads((HERE / f"votes-{r}.json").read_text()) for r in ("A","B")}
keys = json.loads((PHOTOS / "CLE-CARTES.json").read_text())
pairs = json.loads((PHOTOS / "ECHANTILLON.json").read_text())["paires"]
assert len(keys) == 13 and all(set(v) == set(keys) for v in votes.values())
by_face = {value["face"]: {"carte":key, **{r:v[key] for r,v in votes.items()}} for key,value in keys.items()}
paired = {p[k] for p in pairs for k in ("cible","témoin")}
results = {"paires":[{k:{"face":p[k],**by_face[p[k]]} for k in ("cible","témoin")} for p in pairs],
           "fragments":{f:v for f,v in by_face.items() if f not in paired}}
(HERE/"resultats.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
