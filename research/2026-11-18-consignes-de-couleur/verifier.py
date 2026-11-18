"""Contre-calcul autonome depuis IVTFF et les extraits archivés (Python standard)."""
import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CODES = {"g": "ios", "r": "an", "n": "on"}
MOTIFS = ("ios", "an", "on", "iosan", "iosanon")
NAMES = {"f2v.1": ["nenufar"], "f35v.1": ["edera", "nigra"], "f99v.2": ["veratrum"]}


def load_ivtff(path):
    pages, loci = {}, {}
    for line in path.read_text().splitlines():
        if not line.startswith("<f"):
            continue
        label, rest = line.split(">", 1)
        if "," not in label:
            page = label[1:]
            pages[page] = dict(re.findall(r"\$(\w)=([^\s>]+)", rest))
            continue
        locus, code = label[1:].split(",")
        page = locus.split(".")[0]
        assert page in pages and locus not in loci
        loci[locus] = (page, code[1:], rest.strip())
    return pages, loci


def fields(raw, split):
    raw = re.sub(r"<![^>]*>|<@[^>]*>|<%>|<\$>|!", "", raw)
    raw = raw.replace("<->", ".").replace("<~>", ".").replace(",", "." if split else "")
    return [part for part in raw.split(".") if part]


def encode(field, eva):
    if not re.fullmatch("[a-z]+", field):
        return "#"
    # Un seul caractère de substitution suffit : aucun motif obligatoire ne le contient.
    return re.sub("c[kptf]h|[cs]h", "X", field) if eva else field


def sources():
    records = {}
    for line in (ROOT / "research/2026-11-18-noms-dans-les-notices/historique/corpus.jsonl").read_text().splitlines():
        row = json.loads(line)
        records[row["id"]] = row["tokens"][:20]
    gart = ROOT / "research/2026-11-17-plantes-repetees/historique/corpus.json"
    for row in json.loads(gart.read_text())["items"]:
        skip = {*row["missing_initial"], *row["uncertain_word_positions"]}
        records[row["id"]] = [w for i, w in enumerate(row["body"].split()[:20], 1) if i not in skip]
    assert len(records) == 52
    return {key: "".join(re.findall("[grn]", "".join(words).lower())) for key, words in records.items()}


def name_regex(word, unknown):
    return "".join(CODES.get(c, unknown) for c in word)


def check_names(loci, split, eva, report):
    counts = {}
    for loc, names in NAMES.items():
        tokens = [encode(w, eva) for w in fields(loci[loc][2], split)]
        strict, loose = [], []
        for i in range(len(tokens)):
            window = tokens[i:i+len(names)]
            if len(window) == len(names) and all(re.fullmatch(name_regex(name, "[^#]+"), word) for name, word in zip(names, window)):
                strict.append(i+1)
            for end in range(i+1, len(tokens)+1):
                if re.fullmatch(name_regex("".join(names), "[^#]*"), "".join(tokens[i:end])):
                    loose.append([i+1,end])
        assert (strict, loose) == (report[loc]["debuts_stricts"], report[loc]["intervalles_assouplis"])
        counts[loc] = {"strict": len(strict), "assoupli": len(loose)}
    return counts


def count_codes(text):
    return {letter: text.count(code) for letter, code in CODES.items()}


def main():
    published = json.loads((HERE / "RESULTATS.json").read_text())["editions"]
    signatures = sources()
    hashes = {}
    for src in (ROOT / "research/2026-11-18-noms-dans-les-notices/historique/corpus.jsonl",
                ROOT / "research/2026-11-17-plantes-repetees/historique/corpus.json",
                ROOT / "voynich_20261028/data/IT2a-n.txt", ROOT / "voynich_20261028/data/ZL3b-n.txt"):
        hashes[src.name] = hashlib.sha256(src.read_bytes()).hexdigest()
    assert hashes == json.loads((HERE / "RESULTATS.json").read_text())["sources_sha256"]
    results = {"sources_sha256": hashes, "extraits": {"nombre": len(signatures), "avec_g": sum("g" in s for s in signatures.values()),
                            "effectifs_extraits_sans_g": {k:dict(Counter(s)) for k,s in signatures.items() if "g" not in s},
                            "minimum_par_lettre": {c:min(s.count(c) for s in signatures.values()) for c in CODES}},
               "editions": {}}
    for edition, filename in (("H", "IT2a-n.txt"), ("ZL", "ZL3b-n.txt")):
        pages, loci = load_ivtff(ROOT / "voynich_20261028/data" / filename)
        variants = results["editions"][edition] = {}
        for split in (True, False):
            for eva in (True, False):
                variant = ("separes" if split else "joints") + ("_EVA" if eva else "_ascii")
                ref = published[edition][variant]
                prose = defaultdict(list)
                inventory = defaultdict(Counter)
                seen_pages = defaultdict(set)
                ios = []
                exclusions = Counter()
                for loc, (page, kind, raw) in loci.items():
                    if pages[page]["Q"] == "A":
                        continue
                    cat = "prose_herbier" if pages[page]["I"] == "H" and kind.startswith("P") else "fragment" if kind == "Lf" else "autres"
                    tokens = fields(raw, split)
                    seq = [encode(f, eva) for f in tokens]
                    line = "".join(seq)
                    if cat == "prose_herbier":
                        prose[page].append(line)
                        marks = {"?":"interrogation", "[":"variantes", "{":"ligature", "@":"signe_etendu", "'":"apostrophe"}
                        for word, encoded in zip(tokens, seq):
                            if encoded == "#":
                                reason = "+".join(desc for mark,desc in marks.items() if mark in word)
                                exclusions[reason or "autre"] += 1
                    seen_pages[cat].add(page)
                    counts = inventory[cat]
                    counts["lignes"] += 1
                    counts["positions"] += len(seq)
                    counts["incertaines"] += seq.count("#")
                    counts["unites_lisibles"] += len(line) - line.count("#")
                    for m in MOTIFS:
                        # Aucune de ces chaînes n'a de chevauchement avec elle-même.
                        counts[m,"groupes_entiers"] += seq.count(m)
                        counts[m,"interieur_occurrences"] += sum(f.count(m) for f in seq)
                        counts[m,"ligne_jointe_occurrences"] += line.count(m)
                        counts[m,"lignes_avec_motif"] += int(m in line)
                    if "ios" in line:
                        ios.append({"categorie":cat, "locus":loc, "debut_unites_1":line.index("ios")+1,
                                    "groupes_avec_ios":[w for w in fields(raw, split) if "ios" in encode(w, eva)]})
                for cat, counted in inventory.items():
                    expected = ref["inventaire"][cat]
                    assert len(seen_pages[cat]) == expected["pages"]
                    for k, total in counted.items():
                        assert total == (expected["motifs"][k[0]].get(k[1],0) if isinstance(k,tuple) else expected[k]), (cat,k,total)
                bodies = {p:"".join(lines) for p,lines in prose.items()}
                complete = sorted(p for p,body in bodies.items() if "#" not in body)
                supply = {p:count_codes(body) for p,body in bodies.items()}
                unique_supply = Counter(tuple(s[c] for c in CODES) for s in supply.values())
                subsets = (("toutes", sorted(bodies)), ("sans_champ_ecarte", complete))
                stats = {}
                for key, group in subsets:
                    pairs, ordered = 0, 0
                    failing = Counter()
                    for doc, sig in signatures.items():
                        assert sig == ref["passages"][doc]["signature"]
                        wanted = Counter(sig)
                        pattern = re.compile(".*?".join(CODES[c] for c in sig))
                        control = "k".join(CODES[c] for c in sig)
                        assert pattern.search(control)
                        found = []
                        for p in group:
                            missing = [c for c in CODES if wanted[c] > supply[p][c]]
                            failing.update(missing)
                            pairs += int(not missing)
                            if pattern.search(bodies[p]):
                                assert not missing
                                found.append(p)
                        assert sorted(found) == sorted(set(group) & set(ref["passages"][doc]["faces_compatibles"]))
                        ordered += len(found)
                    stats[key] = {"faces": len(group), "comparaisons":len(group)*len(signatures),
                                  "couples_compatibles_effectifs_seuls":pairs, "couples_compatibles_ordre_impose":ordered,
                                  "couples_insuffisants_par_lettre": dict(failing)}
                selected = {p for p,meta in pages.items() if meta["I"] == "H" and meta["Q"] != "A"}
                variants[variant] = {"statistiques":stats, "marquages_des_champs_de_prose_ecartes":dict(sorted(exclusions.items())), "faces_sans_champ_ecarte":complete,
                                     "faces_botaniques_sans_prose":sorted(selected-set(prose)),
                                     "offre_maximale_par_face":{c:max(s[c] for s in supply.values()) for c in CODES},
                                     "distribution_offre_g_r_n":{" ".join(map(str,k)):v for k,v in sorted(unique_supply.items())},
                                     "loci_ios_inventaire_par_ligne":ios, "noms":check_names(loci, split, eva, ref["noms"])}
    (HERE / "SENSIBILITE.json").write_text(json.dumps(results, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__":
    main()
