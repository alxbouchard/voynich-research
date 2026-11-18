"""Extraire les mots de chaque fragment continu du feuillet 17 du MS.626."""
import csv
import json
from pathlib import Path
import re

dossier = Path(__file__).resolve().parent
segments = {}
with (dossier / "lecture.tsv").open() as source:
    for ligne in csv.DictReader(source, delimiter="\t"):
        identifiant = ligne["segment"]
        if identifiant in segments:
            raise ValueError(identifiant)
        lecture = ligne["lecture"].replace("= / ", "").replace(" / ", " ").lower()
        mots = lecture.split()
        if not mots or any(not re.fullmatch("[a-z]+", mot) for mot in mots):
            raise ValueError(lecture)
        segments[identifiant] = mots
(dossier / "corpus.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2) + "\n")
print(len(segments), "fragments,", sum(map(len, segments.values())), "mots")
