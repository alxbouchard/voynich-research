"""Locate just opchy and otol within eight token positions inside an IVTFF paragraph."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_phase14/data"
TARGETS = {"opchy", "otol"}


def read(filename, split):
    active = False
    paragraph = []
    for line in (DATA / filename).read_text(encoding="latin-1").splitlines():
        if re.match(r"<f\w+>", line):
            assert not paragraph
            active = "$Q=T" in line and "$I=S" in line
            continue
        locus = re.match(r"<(f\w+\.\d+),.P\w>\s*(.*)", line)
        if not active or not locus:
            continue
        name, text = locus.groups()
        assert text.startswith("<%>") == (not paragraph)
        body = re.sub(r"<[~-]>", ".", text)
        body = re.sub(r"<[^>]+>|!", "", body)
        body = body.replace("{", "").replace("}", "").replace(",", "." if split else "")
        words = [word for word in body.split(".") if word]
        paragraph.append((name, words))
        if text.endswith("<$>"):
            yield paragraph
            paragraph = []
    assert not paragraph


def scan(paragraphs):
    matches = []
    for paragraph in paragraphs:
        group = {row[0] for row in paragraph}
        seq = [(w, locus, i) for locus, words in paragraph for i, w in enumerate(words, 1)]
        for i, (left, left_id, left_pos) in enumerate(seq):
            if left not in TARGETS:
                continue
            for j in range(i + 1, min(len(seq), i + 9)):
                right, right_id, right_pos = seq[j]
                if {left, right} == TARGETS:
                    matches.append({"paragraph": [row[0] for row in paragraph],
                                    "positions": [[left, left_id, left_pos], [right, right_id, right_pos]],
                                    "distance": j - i, "between": [w for w, _, _ in seq[i + 1:j]]})
                    assert left_id in group and right_id in group
    return matches


def main():
    results = {}
    for split in (False, True):
        joint = {}
        for edition, filename in (("H", "IT2a-n.txt"), ("ZL", "ZL3b-n.txt")):
            joint[edition] = scan(read(filename, split))
        overlaps = []
        for h in joint["H"]:
            for z in joint["ZL"]:
                if [p[:2] for p in h["positions"]] != [p[:2] for p in z["positions"]]:
                    continue
                shared = [locus for locus in h["paragraph"] if locus in z["paragraph"]]
                assert all(token[1] in shared for token in h["positions"])
                overlaps.append(shared)
        joint["common_paragraph_overlap"] = overlaps
        results["commas_split" if split else "commas_joined"] = joint
    (HERE / "positions.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
