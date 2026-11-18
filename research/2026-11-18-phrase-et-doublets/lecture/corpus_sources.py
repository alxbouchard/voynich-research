"""Corpus documentés de la lecture positionnelle ; frontières conservées."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import re

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
CELSUS_SHA = "a4a5194ba38a7efd5192d20f2a7b696f4fa64105010eb629aa7c35255a935145"
GERMAN = RESEARCH / "2026-11-18-mots-et-dessins/herbier_1485/corpus.json"
LATIN = RESEARCH / "2026-11-18-opcheor-paralleles/latin/corpus.json"


def latin_text(node):
    name = node.tag.split("}")[-1]
    if name in ("foreign", "figure"):
        return " | "
    if name in ("note", "del", "sic"):
        return ""
    if name == "choice":
        return latin_text(node.find("{*}corr"))
    return (node.text or "") + "".join(latin_text(child) + (child.tail or "") for child in node)


def celsus(path):
    assert sha256(path.read_bytes()).hexdigest() == CELSUS_SHA
    root = ET.parse(path)
    corpus = {}
    for book in root.findall(".//{*}div[@subtype='book']"):
        for chapter in book.findall("{*}div"):
            for i, para in enumerate(chapter.findall("{*}p"), 1):
                raw = latin_text(para).lower().replace("æ", "ae").replace("œ", "oe")
                # Séparer les séries grecques, chiffres et symboles de mesure résiduels.
                runs = re.split(r"[^a-z\s.,;:!?()«»\-–—'’]+", raw)
                for j, run in enumerate(runs, 1):
                    words = re.findall("[a-z]+", run)
                    if words:
                        locus = f"{book.get('n')}.{chapter.get('n')}.p{i}.{j}"
                        corpus[locus] = words
    return corpus


def gart():
    series = {}
    for notice in json.loads(GERMAN.read_text())["items"]:
        words = notice["body"].split()
        stops = set(notice["uncertain_word_positions"]) | set(notice["missing_initial"])
        buffer = []
        for pos, word in enumerate(words, 1):
            clean = "".join(c for c in word.lower().replace("ſ", "s") if c.isalpha())
            if clean and pos not in stops:
                buffer.append(clean)
            else:
                if buffer:
                    series[f"{notice['id']}.avant{pos}"] = buffer
                buffer = []
        if buffer:
            series[notice["id"] + ".fin"] = buffer
    return series


def load_all(xml, ridges=None):
    corpora = {"Macer": json.loads(LATIN.read_text()), "Celse": celsus(xml), "Gart1485": gart()}
    if ridges:
        corpora["RIDGES"] = json.loads(ridges.read_text())
        assert all(isinstance(row, list) and all(isinstance(w, str) and w.isalpha() and w==w.lower()
                                                  for w in row) for row in corpora["RIDGES"].values())
    return corpora
