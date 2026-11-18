"""Publier les quatre attentes textuelles sans consulter les images réservées."""
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
ROOT = RESEARCH.parent
sys.path.insert(0, str(RESEARCH / "2026-11-18-noms-dans-une-phrase/contexte"))
from contexte import MODES, corpus, sequence, units

REGISTRY = RESEARCH / "2026-11-18-ordre-des-noms/panneaux/RANGEES.json"
RULES = (("mot", "arol"), ("fin", "rol"), ("fin", "ol"), ("debut", "ar"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def features(words):
    result = set()
    for word in words:
        result.add(("mot", word))
        glyphs = units(word, False)
        for n in (2, 3):
            if len(glyphs) > n:
                result.update((("fin", "".join(glyphs[-n:])), ("debut", "".join(glyphs[:n]))))
    return result


def words_at(table, loci, cut):
    items = []
    for loc in loci:
        if loc not in table or table[loc][1] != "Lf":
            return None
        parts = [word for _, word in sequence(table[loc][3], cut)]
        if not parts or any(not re.fullmatch("[a-z]+", w) for w in parts):
            return None
        items.extend(parts)
    return items or None


def main():
    editions, _ = corpus()
    entries = []
    for row in json.loads(REGISTRY.read_bytes()):
        page = row["page"]
        if not re.fullmatch(r"f(?:88|89|100|102)[rv][12]?", page):
            continue
        for position in row["positions"]:
            loci = [f"{page}.{n}" for n in position["loci"]]
            views = [words_at(table, loci, cut) for table in editions.values() for cut in MODES]
            common = views[0] if all(v == views[0] for v in views) else None
            predictions = [rule in features(common) for rule in RULES] if common else None
            entries.append({"fragment":position["fragment"], "page":page, "rang":row["rang"],
                            "lot":"A" if row["cahier"] == 15 else "B", "attache":row["niveau"],
                            "loci":loci, "lectures":views, "commun":common, "predictions":predictions})
    assert len(entries) == len({entry['fragment'] for entry in entries}) == 135
    out = {"regles":RULES, "lectures":["H joints","H séparés","ZL joints","ZL séparés"],
           "sha256_registre":digest(REGISTRY), "sha256_transcriptions":{
               p:digest(ROOT / "voynich_20261028/data" / p) for p in ("IT2a-n.txt","ZL3b-n.txt")},
           "annonces":entries}
    write("ANNONCES.json", out)


if __name__ == "__main__":
    main()
