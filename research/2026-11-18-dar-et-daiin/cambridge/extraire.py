"""Extraire séparément les citations manuscrites des deux TEI de Cambridge."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
import argparse
import gzip
import json
import re
import unicodedata

HERE = Path(__file__).resolve().parent
IDS = {"SJC": "MS-SJC-B-00015", "GON": "MS-GONVILLE-AND-CAIUS-00457-00395"}
# Attribution manuelle de la langue du passage (et non de la notice entière).
LATIN = {
    "SJC": {10,12,14,20,29,30,31,46,47,56,57,59,*range(64,76),85,86,89,
            92,93,94,95,96,97,98,*range(101,109),116,117,118,122,123,*range(126,132)},
    "GON": {4,9,10,20,21,22,37,72,73,78,81,82,91,99,100,101,102},
}
MIXED = {"SJC":{8,19,28,32,33,34,53,55,61,87,109,124,125,132,133},
         "GON":{0,3,12,24,38,41,42,46,67,70,75,76}}
EXCLUDE = {"SJC":{119}, "GON":set()}
TAGS = {"incipit","explicit","q","quote"}


def tag(e):
    return e.tag.split("}")[-1]


def letters(s):
    return re.findall(r"[^\W\d_]+",unicodedata.normalize("NFC",s.lower()))


def manuscript_text(e):
    text = e.text or ""
    for child in e:
        if tag(child) in {"hi","name","orgName"}:
            text += manuscript_text(child)
        else:
            text += "|"
        text += child.tail or ""
    return text


def passages(s):
    # Une lettre initiale suppléée est incluse. Les gloses, lacunes, chiffres
    # arabes, unités et limites de phrase ne créent jamais de voisin artificiel.
    s = re.sub(r"\[([A-Za-z]{1,2})\]",r"\1",s)
    s = s.replace("[sic]","")
    s = re.sub(r"\[[^\]]*\]|\.{2,}|[\d℥♡⸬]|\([^)]*\)","|",s)
    return [words for part in re.split(r"[|.;:!?/«»‘’“”'\n]|\s[-–—]\s",s)
            if (words:=letters(part))]


def extract(name, path):
    root = ET.parse(path).getroot()
    parent = {child:e for e in root.iter() for child in e}
    out = defaultdict(dict)
    inventory = []
    seen = set()
    for i, node in enumerate(e for e in root.iter() if tag(e) in TAGS):
        item = node
        while item in parent and tag(item)!="msItem":
            item = parent[item]
        if tag(item)!="msItem" or i in EXCLUDE[name]:
            continue
        place = " ".join(l.text or "" for l in node.findall(".//{*}locus"))
        itlocus = item.find("./{*}locus")
        if not place and itlocus is not None:
            place = "notice " + " ".join(itlocus.itertext())
        lang = "latin" if i in LATIN[name] else "mixte" if i in MIXED[name] else "anglais"
        key = name+"-"+lang
        # Retirer blancs de mise en page de l'XML avant les divisions textuelles.
        value = " ".join(manuscript_text(node).split())
        spans = passages(value)
        number = f"{i:03d}"
        for j,words in enumerate(spans,1):
            sig = (id(item),tuple(words))
            if sig in seen:
                continue
            seen.add(sig)
            location = f"{number}.{j:02d} | notice {item.get('n','?')} | {place} | {tag(node)}"
            out[key][location] = words
        inventory.append({"extrait":i,"notice":item.get("n"),"localisation":place,
                          "balise":tag(node),"classe_linguistique":lang})
    return out,inventory


def encode(data):
    return (json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tei",nargs=2,type=Path)
    args=parser.parse_args()
    output={};manifest={}
    for (name,id_),p in zip(IDS.items(),args.tei):
        books,items=extract(name,p)
        output.update(books)
        manifest[name]={"url":f"https://services.cudl.lib.cam.ac.uk/v1/metadata/tei/{id_}/",
                        "sha256":sha256(p.read_bytes()).hexdigest(),"id":id_,"extraits":items,
                        "fiche":f"https://cudl.lib.cam.ac.uk/view/{id_}/1",
                        "manifeste":f"https://cudl.lib.cam.ac.uk/iiif/{id_}"}
    (HERE/"CORPUS.json.gz").write_bytes(gzip.compress(encode(output),mtime=0))
    (HERE/"SOURCES.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=1)+"\n")
    for n,book in output.items():
        print(n,len(book),sum(map(len,book.values())))
