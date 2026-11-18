"""Chercher les deux mots puis croiser les faces avec les votes antérieurs."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / "2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import aligned, corpus, metadata, MODES, parse


def order(page):
    m = re.fullmatch(r"f(\d+)([rv])(\d*)", page)
    return int(m[1]), m[2], int(m[3] or 0)


def main():
    herbs = metadata()
    ed, _ = corpus()
    path = RESEARCH / "2026-11-18-fleurs/corolles"
    ballot = {}
    for file in ("A.json", "BC.json"):
        ballot.update(json.loads((path/file).read_bytes()))
    def consensus(v):
        return v[0] if v[0] == v[1] and v[0] in ("oui", "non") else "indetermine"
    targets = {"ctheor", "ctheol"}
    sites, individually = [], defaultdict(dict)
    cover = Counter()
    sizes = Counter()
    for locus, (page, kind, _, _) in ed["H"].items():
        if kind != "P0" or herbs.get(page, {}).get("I") != "H" or order(page)[0] == 52:
            continue
        if locus not in ed["ZL"] or ed["ZL"][locus][1] != kind:
            continue
        for e, mode in MODES:
            _, parts = parse(ed[e][locus][3],mode)
            hits = [w for part in parts for w in part if w in targets]
            if hits: individually[locus][e+"/"+mode] = hits
        for r in aligned(ed, locus, page, "H", order(page)[0], cover):
            sizes[page] += 1
            if r['mot'] in targets:
                sites.append({k:r[k] for k in ("page", "lieu", "mot", "troncon", "rangs_quatre")})
    leaves = sorted({r['page'] for r in sites}, key=order)
    known = [p for p in leaves if p in ballot]
    new = [p for p in leaves if p not in ballot]
    rows = {p:{"placements_admis":sizes[p], "mots":[r for r in sites if r['page']==p],
               "votes":ballot.get(p)} for p in leaves}
    voted = {p:v for p,v in ballot.items() if p in sizes}
    out = dict(secteur="H", feuillet_exclu=52, pages_avec_positions=len(sizes),
               positions=sum(sizes.values()), registre_des_positions=sizes,
               consensus_lot_cote=Counter(consensus(v) for v in voted.values()), ensemble_votes=voted,
               consensus_parmi_cibles_cotees=Counter(consensus(ballot[p]) for p in known),
               cibles_cotees=known, nouvelles_cibles=new, photographies_a_verifier=new[:3],
               occurrences_par_face=rows, occurrences_par_lecture_y_compris_discutees=individually)
    (HERE/"RESULTATS.json").write_text(json.dumps(out,sort_keys=True,indent=1,ensure_ascii=False)+"\n")
    for key in ('pages_avec_positions','positions','consensus_lot_cote','consensus_parmi_cibles_cotees','cibles_cotees','nouvelles_cibles','photographies_a_verifier','occurrences_par_face'):
        print(key,out[key])


if __name__ == "__main__":
    main()
