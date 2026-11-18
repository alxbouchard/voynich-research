"""Où trouve-t-on également le candidat fixé dans la prose ordinaire P0 ?"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from etiquettes import DATA, FILES, HERE, ROW


def locate(path, word):
    counts = defaultdict(Counter)
    examples = defaultdict(list)
    section = "?"
    for line in path.read_text().splitlines():
        header = re.match(r"^<f\d+[rv]\d*>\s+(.*)", line)
        if header:
            key = re.search(r"\$I=(.)", header[1])
            section = key[1] if key else "?"
            continue
        row = ROW.match(line)
        if not row:
            continue
        locus, _, leaf, _, _, kind, raw = row.groups()
        if kind != "P0" or int(leaf) in (80, 81):
            continue
        body = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)
        body = re.sub(r"<[-~]>", ".", body).strip().replace(",", "")
        words = [w for w in body.split(".") if re.fullmatch(r"[a-z]+", w)]
        counts[section]["lisibles"] += len(words)
        counts[section]["occurrences"] += words.count(word)
        if word in words:
            examples[section].append(locus)
    return {key: {**values, "lignes": examples[key]} for key, values in counts.items()}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--donnees", type=Path, default=DATA)
    options = cli.parse_args()
    word = json.loads((HERE / "PREDICTIONS.json").read_text())["accord_joint"]["Lf"]["mot"]
    result = {tx: locate(options.donnees / file, word) for tx, file in FILES.items()}
    (HERE / "OKOL_DANS_LA_PROSE.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
