"""Épreuve du composant dar entre un fragment légendé et la grande plante associée."""
import csv
import json
import re
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
sys.path.insert(0, str(STUDY))
from croiser import CAT, MODES, adjacent, corpus, leaf, load, loc, segment, texts
from corpus_dam import WORD, parse

REGISTER = STUDY.parent / "2026-11-18-noms-dans-les-notices/registre/registre.csv"


def evaluate(rows):
    words = [loc(row) for row in rows if row[0] == "dar"]
    windows = []
    for i, row in enumerate(rows):
        if row[0] != "daiin":
            continue
        following = []
        for j in range(i + 1, min(i + 4, len(rows))):
            if not adjacent(rows[j - 1], rows[j]):
                break
            following.append(rows[j][0])
        windows.append({"lieu": loc(row), "suite": following})
    return {"positions": len(rows), "dar": words, "fenetres": windows,
            "trois_lisibles": sum(len(w["suite"]) == 3 for w in windows),
            "occasions_lisibles": sum(bool(w["suite"]) for w in windows),
            "proche": sum("dar" in w["suite"] for w in windows)}


def internal(word):
    units = segment(word)
    return any(units[i:i + 3] == ("d", "a", "r") for i in range(1, len(units) - 3))


def single_label(editions, locus, fragment):
    forms = []
    for edition, mode in MODES:
        row = editions[edition].get(locus)
        if not row or row[1] != "Lf":
            return None
        # ZL préfixe certaines légendes du numéro éditorial du dessin.
        raw = re.sub(rf"^<!{fragment}>", "", row[3])
        _, parts = parse(raw, mode)
        if len(parts) != 1 or len(parts[0]) != 1 or not WORD.fullmatch(parts[0][0]):
            return None
        forms.append(parts[0][0])
    return forms[0] if len(set(forms)) == 1 else None


def other_labels(links, editions):
    with REGISTER.open() as stream:
        register = list(csv.DictReader(stream))
    linked = []
    for link in links:
        page, target, number = link["panneau"], link["plante"], link["fragment"]
        if leaf(page) == 102 or leaf(target) in {18, 23}:
            continue
        loci = sorted({r["locus"] for r in register if r["source_page"] == page
                       and r["drawing_target"] == target and int(r["fragment"]) == number and r["locus"]})
        assert any(r["source_page"] == page and r["drawing_target"] == target
                   and int(r["fragment"]) == number for r in register)
        labels = {locus: single_label(editions, locus, number) for locus in loci}
        # Une légende de plusieurs lignes ne constitue pas l’étiquette d’un seul mot annoncée.
        word = labels[loci[0]] if len(loci) == 1 else None
        linked.append({"fragment": number, "panneau": page, "grande_plante": target,
                       "lectures": labels, "mot": word, "dar_interieur": bool(word and internal(word))})
    return linked


def raw_counts(editions, page):
    out = {}
    for edition, mode in MODES:
        words, occurrences, windows = 0, [], []
        for locus, (face, kind, _, raw) in editions[edition].items():
            if face != page or kind != "P0":
                continue
            _, parts = parse(raw, mode)
            for block in parts:
                words += sum(bool(WORD.fullmatch(w)) for w in block)
                occurrences.extend(locus for word in block if word == "dar")
                for rank, word in enumerate(block):
                    if word == "daiin":
                        windows.append({"ligne": locus, "rang_troncon": rank + 1, "suite": block[rank + 1:rank + 4]})
        out[f"{edition}_{mode}"] = {"positions": words, "dar": occurrences, "daiin": windows}
    return out


def compute():
    assert internal("koldarod") and internal("odalydary")
    assert not any(internal(w) for w in ("dar", "oldar", "dary", "otary"))
    links = [r for r in load(CAT)["liens"] if r["classe"] != "petersen"]
    all_pages = texts("plantes", True)
    results = {p: evaluate(all_pages[p]) for p in sorted({r["plante"] for r in links})}
    editions, _ = corpus()
    assert single_label(editions, "f102r2.21", 212) == "koldarod"
    assert single_label(editions, "f102r2.22", 213) == "odalydary"
    reference_size = results["f23r"]["positions"]
    other = [p for p in results if p not in ("f18v", "f23r")]
    comparable = [p for p in other if 3 * reference_size <= 4 * results[p]["positions"] <= 5 * reference_size]
    return {"pages": results, "contre_epreuves": {"autres": other, "longueur_proche": comparable},
            "editions_f23r": raw_counts(editions, "f23r"), "etiquettes": other_labels(links, editions)}


if __name__ == "__main__":
    (HERE / "RESULTATS.json").write_text(json.dumps(compute(), ensure_ascii=False, indent=1) + "\n")
