#!/usr/bin/env python3
"""Calcule les appariements de deux témoins du Liber de coquina. Python 3, beautifulsoup4."""
import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
MODES = ("exact", "flexion", "graphies", "synonyme")


def words(text):
    return TOKEN.findall(text.casefold())


def read_recipes(path):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    groups = []
    for group in soup.select("#testo > .ricetta"):
        numbered = {}
        active = None
        for child in group.find_all(recursive=False):
            if "head" in child.get("class", []):
                title = child.get_text(" ", strip=True)
                match = re.search(r"\b([0-9]+(?:bis)?)\.?\s*$", title)
                active = match[1] if match else None
                if active and active.isdecimal():
                    active = int(active)
                if active is not None:
                    assert active not in numbered
                    numbered[active] = {"title": title, "bodies": []}
            elif child.name == "p":
                assert active in numbered
                for marker in child.select("span.pagina"):
                    marker.decompose()
                numbered[active]["bodies"].append(child.get_text(" ", strip=True))
        groups.append(numbered)
    return groups


def compiled(rule, literal, lexeme, mode):
    if mode == "exact":
        return re.compile(re.escape(literal))
    all_forms = [lexeme]
    if mode == "synonyme" and "alias" in rule[lexeme]:
        all_forms.append(rule[lexeme]["alias"])
    patterns = []
    for name in all_forms:
        entry = rule[name]
        initial = entry["base"] if mode == "flexion" else entry.get("var", entry["base"])
        patterns.append(initial + entry["end"])
    pattern = re.compile("|".join(patterns))
    assert pattern.fullmatch(literal), (lexeme, mode, literal)
    return pattern


def write_tsv(destination, rows):
    with destination.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0], delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("a", type=Path, nargs="?", help="HTML AtLiTeG du témoin A")
    ap.add_argument("o", type=Path, nargs="?", help="HTML AtLiTeG du témoin O")
    ap.add_argument("--rejouer", type=Path, help="Index de formes déjà extrait des témoins A et O")
    ap.add_argument("--sortie", type=Path, default=HERE)
    args = ap.parse_args()
    args.sortie.mkdir(exist_ok=True, parents=True)
    plan_bytes = (HERE / "protocole.json").read_bytes()
    digest = hashlib.sha256(plan_bytes).hexdigest()
    plan = json.loads(plan_bytes)
    if args.rejouer:
        index = json.loads(args.rejouer.read_text())
        assert index["protocole_sha256"] == digest
        target = {int(n): sequence for n, sequence in index["O"].items()}
    else:
        if not (args.a and args.o):
            ap.error("Fournir les deux pages HTML, ou bien --rejouer INDEX.")
        first = read_recipes(args.a)
        later = read_recipes(args.o)
        assert all(len(r["bodies"]) == 1 for grp in later for r in grp.values())
        assert sum(map(len, later)) == 168
        target = {n: words(rec["bodies"][0]) for grp in later for n, rec in grp.items()}
        for a_num, o_num, x, y, *_ in plan["queries"]:
            grp = first[5 if o_num < 100 else 99]
            source_words = words(" ".join(grp[a_num]["bodies"]))
            assert x in source_words and y in source_words[source_words.index(x) + 1:]
        recognizers = [compiled(plan["lexemes"], query[k], query[k+2], mode)
                       for query in plan["queries"] for k in (2,3) for mode in MODES]
        retained = {w for sequence in target.values() for w in sequence
                    if any(p.fullmatch(w) for p in recognizers)}
        compact = {n: [w for w in sequence if w in retained] for n, sequence in target.items()}
        index = dict(protocole_sha256=digest, O=compact)
        (args.sortie / "index_O.json").write_text(json.dumps(index, ensure_ascii=False, indent=1)+"\n")
    assert set(target) == set(range(1, 169))
    hits = []
    totals = defaultdict(list)
    candidates = defaultdict(set)
    for a_num, o_num, x, y, lex1, lex2, relation in plan["queries"]:
        for mode in MODES:
            patterns = (compiled(plan["lexemes"], x, lex1, mode), compiled(plan["lexemes"], y, lex2, mode))
            scans = {"sans_ordre": [], "ordre_A": []}
            for idx, sequence in target.items():
                p1, p2 = ([i for i, word in enumerate(sequence) if pat.fullmatch(word)] for pat in patterns)
                for word, positions in ((x, p1), (y, p2)):
                    candidates[(mode, word)].update(sequence[i] for i in positions)
                if p1 and p2:
                    scans["sans_ordre"].append(idx)
                    if min(p1) < max(p2):
                        scans["ordre_A"].append(idx)
            for order, ids in scans.items():
                ids.sort()
                totals[(mode, order)].append((o_num, ids))
                hits.append(dict(A=a_num, O=o_num, terme_1=x, terme_2=y, relation_A=relation,
                                 mode=mode, ordre=order, candidats=len(ids), cible_presente=int(o_num in ids),
                                 cible_unique=int(ids == [o_num]), numeros_O=" ".join(map(str, ids))))
    write_tsv(args.sortie / "appariements.tsv", hits)
    stats = []
    for (mode, order), rows in totals.items():
        for name, chosen in (("toutes",rows),("hors_alternative",[r for r in rows if r[0]!=149])):
            nhit = sum(len(ids) for _, ids in chosen)
            tp = sum(a in ids for a, ids in chosen)
            uniq = sum(ids == [a] for a, ids in chosen)
            stats.append(dict(mode=mode, ordre=order, ensemble=name, requetes=len(chosen), recettes=168,
                              comparaisons=len(chosen)*168, resultats=nhit, cibles=tp,
                              concurrents=nhit-tp, cibles_uniques=uniq))
    write_tsv(args.sortie / "totaux.tsv", stats)
    forms = [dict(mode=m,forme_A=w,formes_detectees_O=" ".join(sorted(forms))) for (m,w),forms in candidates.items()]
    write_tsv(args.sortie / "formes.tsv", forms)
    if not args.rejouer:
        print("A", hashlib.sha256(args.a.read_bytes()).hexdigest())
        print("O", hashlib.sha256(args.o.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
