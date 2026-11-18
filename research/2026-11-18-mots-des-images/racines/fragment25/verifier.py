"""Search the prespecified exact EVA form within f57r. Standard library."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[3] / "voynich_20261028/data"
LINE = re.compile(r"^<(f57r\.\d+|f89r1\.[1-5]),.([A-Za-z0-9]{2})>\s+(.*)$")


def tokenize(body, comma, choice):
    body = re.sub(r"<[-~]>", ".", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = re.sub(r"\[([^\]]+)\]", lambda m: m[1].split(":")[choice], body)
    body = body.replace(",", comma).replace("{", "").replace("}", "")
    return [w for w in body.split(".") if w]


def read_page(path):
    labels = {}
    target = {}
    for line in path.read_text().splitlines():
        match = LINE.match(line)
        if match:
            locus, kind, text = match.groups()
            group = target if locus.startswith("f57r.") else labels
            group[locus] = {"type": kind, "raw": text}
    assert len(labels) == 5 and len(target) == 11
    assert labels["f89r1.4"] == {"type": "Lf", "raw": "otoldy"}
    summary = {}
    for comma_name, comma in [("split", "."), ("join", "")]:
        for choice_name, choice in [("first", 0), ("last", -1)]:
            total = 0
            hits = []
            for locus, row in target.items():
                tokens = tokenize(row["raw"], comma, choice)
                total += len(tokens)
                for i, token in enumerate(tokens, start=1):
                    if token == "otoldy":
                        hits.append({"locus": locus, "position": i, "type": row["type"]})
            summary[f"{comma_name}_{choice_name}"] = {"n_groups": total,
                                                     "n_loci": len(target), "hits": hits}
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "labels": labels,
            "target": target, "runs": summary}


if __name__ == "__main__":
    result = {name: read_page(DATA / (name + ".txt")) for name in ["ZL3b-n", "IT2a-n"]}
    (HERE / "resultats.json").write_text(json.dumps(result, indent=2) + "\n")
    for k, dataset in result.items():
        print(k, dataset["runs"])
