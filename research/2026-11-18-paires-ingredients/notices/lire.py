"""Compare IVTFF paragraph membership and count delimiters without recording words."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_phase14" / "data"
PAGE = re.compile(r"<(f\w+)>")
LOCUS = re.compile(r"<((f\w+)\.([0-9]+),.(P[0-9a-z]))>\s*(.*)")
FILES = {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}


def count_segments(body):
    # Count delimiters only. Both official files have no spacing within alternatives
    # on the selected pages. Inline comments may contain arbitrary punctuation.
    body = body.replace("<->", ".").replace("<~>", ".")
    body = re.sub(r"<[^<>]*>", "", body)
    assert body and "/" not in body
    assert not re.search(r"\[[^\]]*[.,][^\]]*\]", body)
    assert not re.search(r"^[.,]|[.,]$|[.,]{2}", body)
    joined = 1 + body.count(".")
    return joined, joined + body.count(",")


def read(name):
    selected = False
    paragraphs, counts = [], {}
    current = None
    for line in (DATA / name).read_text(encoding="latin-1").splitlines():
        page = PAGE.match(line)
        if page:
            assert current is None
            page_id = page[1]
            values = dict(re.findall(r"\$(\w)=(\w+)", line))
            selected = (values.get("Q"), values.get("I")) == ("T", "S")
        elif selected and line.startswith("<"):
            row = LOCUS.fullmatch(line)
            assert row and row[2] == page_id, line.partition(">")[0]
            locus, body = row[1], row[5]
            assert locus not in counts
            starts, ends = body.startswith("<%>"), body.endswith("<$>")
            assert starts == (current is None), locus
            assert body.count("<%>") == int(starts) and body.count("<$>") == int(ends), locus
            if starts:
                current = []
            current.append(locus)
            counts[locus] = count_segments(body)
            if ends:
                paragraphs.append(tuple(current))
                current = None
        elif selected:
            assert not line.startswith("/"), "unexpected wrapped locus"
    assert current is None
    assert sum(map(len, paragraphs)) == len(counts)
    return paragraphs, counts


def page_id(paragraph):
    return paragraph[0].split(".")[0]


def summarize(paragraphs, counts):
    lines = [locus for paragraph in paragraphs for locus in paragraph]
    return [len(paragraphs), len(lines),
            sum(counts[locus][0] for locus in lines),
            sum(counts[locus][1] for locus in lines)]


def main():
    paragraphs, counts = {}, {}
    for version, name in FILES.items():
        paragraphs[version], counts[version] = read(name)
    zl = set(paragraphs["ZL"])
    paragraphs["accord"] = [row for row in paragraphs["H"] if row in zl]
    with (HERE / "paragraphes.json").open("w", encoding="utf-8") as output:
        # One paragraph per line, complete official locus IDs without angle brackets.
        groups = [f'  "{key}": [\n' + ",\n".join("    " + json.dumps(p) for p in rows) + "\n  ]"
                  for key, rows in paragraphs.items()]
        output.write("{\n" + ",\n".join(groups) + "\n}\n")
    pages = list(dict.fromkeys(page_id(p) for p in paragraphs["H"]))
    with (HERE / "comptes.tsv").open("w", encoding="utf-8", newline="") as output:
        table = csv.writer(output, delimiter="\t", lineterminator="\n")
        table.writerow(["page", "unites", "edition", "paragraphes", "loci", "segments_virgules_jointes",
                        "segments_virgules_coupees"])
        for page in pages + ["TOTAL"]:
            for mode in ("tous", "accord"):
                for version in FILES:
                    rows = paragraphs[version if mode == "tous" else "accord"]
                    sample = [p for p in rows if page == "TOTAL" or page_id(p) == page]
                    table.writerow([page, mode, version, *summarize(sample, counts[version])])
    for version, rows in paragraphs.items():
        singletons = [p[0] for p in rows if len(p) == 1]
        types = Counter(locus.split(",")[1][1:] for p in rows for locus in p)
        print(version, len(rows), "paragraphs,", sum(types.values()), "loci,", dict(types),
              "singletons", singletons)


if __name__ == "__main__":
    main()
