"""Repérer les id est sans communiquer les mots qui les suivent avant évaluation."""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent


def normalize(word):
    return re.sub(r"[^a-zäöüß]", "", word.lower().replace("ſ", "s"))


def extract(payload, view):
    page = ET.fromstring(payload)
    lines = page.findall('.//*[@class="ocr_line"]')
    items = []
    for n, line in enumerate(lines, 1):
        for w in line:
            token = normalize(w.text or "")
            if token:
                box = [int(x) for x in w.attrib["title"].split()[1:5]]
                items.append((token,n,box))
    records = []
    for i in range(len(items)-3):
        if [x[0] for x in items[i:i+2]] != ["id","est"]:
            continue
        before = [x[0] for x in items[max(0,i-5):i]]
        records.append(dict(vue=view, ligne_ocr=items[i][1], avant=before,
                            capitel=bool(set(before) & {"capitel","capitulo"}),
                            box_id=items[i][2], box_reponse=items[i+2][2],
                            reponse_ocr=items[i+2][0], temoin_ocr=items[i+3][0]))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--devoiler", action="store_true")
    opts = parser.parse_args()
    with zipfile.ZipFile(HERE / "ocr-51-70.zip") as archive:
        matches = []
        for view in range(51,71):
            matches.extend(extract(archive.read(f"{view}.html"), view))
    if not opts.devoiler:
        for r in matches:
            del r["reponse_ocr"], r["temoin_ocr"]
    print(json.dumps(matches,indent=2,ensure_ascii=False))


if __name__ == "__main__":
    main()
