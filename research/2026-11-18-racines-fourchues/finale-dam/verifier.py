"""Chercher les lieux Lf hors cotation prédits par la terminaison découverte sur f89r1."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from annoncer import MODES, corpus, features, sequence


def main():
    data = json.loads((HERE.parent/"ANNONCES.json").read_bytes())["annonces"]
    pages = {row["page"] for row in data}
    editions, _ = corpus()
    tables = list(editions.values())
    labels = []
    prose = []
    coverage = {}
    for loc in dict.fromkeys([*tables[0], *tables[1]]):
        page = loc.split(".")[0]
        kinds = [ed[loc][1] if loc in ed else None for ed in tables]
        reads = [[w for _,w in sequence(ed[loc][3],m)] if loc in ed else []
                 for ed in tables for m in MODES]
        if "Lf" in kinds and page not in pages:
            coverage[page] = coverage.get(page,0)+1
            hits = [[w for w in ws if w.isascii() and w.isalpha() and ("fin","dam") in features([w])]
                    for ws in reads]
            if any(hits):
                common = sorted(set.intersection(*(set(ws) for ws in hits)))
                labels.append({"locus":loc, "lectures":reads, "candidats_communs":common,
                               "legende_concordante":all(w==reads[0] for w in reads) and bool(common)})
        if "P0" in kinds and page=="f89r1" and any(set(words) & {"oldam","saldam"} for words in reads):
            prose.append({"locus":loc, "lectures":reads})
    out={"lignes_Lf_par_face_hors_lot":coverage,"legendes":labels,"prose_sur_f89r1":prose}
    (HERE/"LIEUX.json").write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
    print(coverage, labels, [x["locus"] for x in prose])


if __name__=="__main__":
    main()
