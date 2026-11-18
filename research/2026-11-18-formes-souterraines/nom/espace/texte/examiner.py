"""Compare les mots finaux des étiquettes de fragments voisins à la prose du panneau."""
from collections import Counter, defaultdict
from csv import DictReader
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / "second"))
from transfert import corpus, tokens

TABLE = HERE.parents[3] / "2026-11-18-paires-ingredients/rangees/rangees.tsv"
SHA = "584a27515c49c4c2cb4a527c0c54c30c02f7a34893001cdeeb1e047514afc5a4"
SEED_PAGE = "f89r2"


def certain(w):
    return bool(re.fullmatch("[a-z]+", w))


def size(w):
    return len(re.findall(r"c[kptf]h|ch|sh|.", w))


def futures(words):
    for i, a in enumerate(words):
        for j in range(i+1, min(i+4, len(words))):
            yield a, words[j], i+1, j+1


def geometry():
    assert sha256(TABLE.read_bytes()).hexdigest() == SHA
    with TABLE.open() as f:
        return list(DictReader(f, delimiter="\t"))


def terminals(rows, page, geometry_row, split):
    fragments = []
    for number in geometry_row["fragments"].split(","):
        words = []
        loci = []
        for line in number.split("+"):
            locus = f"{page}.{line}"
            assert rows[locus][1] == "Lf"
            words.extend(tokens(rows[locus][3],split))
            loci.append(locus)
        assert words
        fragments.append({"loci":loci, "derniere_position":len(words), "groupes":words, "dernier":words[-1]})
    return fragments


def run(rows, geo, split):
    pages = {r["page"] for r in geo}
    lines = {p:{} for p in pages}
    for locus,(p,kind,_,raw) in rows.items():
        if p in pages and kind == "P0":
            lines[p][locus] = tokens(raw,split)
    pair_rows, matches = [], []
    for row in geo:
        p = row["page"]
        local = {f"{p}.{n}" for n in row["prose"].split(",") if n}
        assert local <= set(lines[p])
        fragments = terminals(rows,p,row,split)
        for left,right in zip(fragments,fragments[1:]):
            a,b = left["dernier"],right["dernier"]
            key = left["loci"][0] + "/" + right["loci"][0]
            if not (certain(a) and certain(b)):
                eligibility = "dernier_groupe_incertain"
            elif min(size(a),size(b)) < 3:
                eligibility = "moins_de_trois_unites"
            elif a == b:
                eligibility = "memes_mots"
            else:
                eligibility = "admissible"
            pair = {"paire":key,"page":p,"rangee":int(row["rang"]),"gauche":left,"droite":right,
                    "statut":eligibility,"paragraphe_geometrique":sorted(local)}
            pair_rows.append(pair)
            if eligibility != "admissible":
                continue
            for locus,words in lines[p].items():
                for x,y,i,j in futures(words):
                    if (x,y) == (a,b) or (x,y) == (b,a):
                        matches.append({"paire":key,"mots":[a,b],"page":p,"rangee":int(row["rang"]),
                                        "ligne":locus,"rangs":[i,j],"intermediaires":words[i:j-1],
                                        "ordre":"direct" if x==a else "inverse","local":locus in local})
    assert len({r["paire"] for r in pair_rows}) == len(pair_rows)
    summary = {}
    for scope, ps in (("autres_panneaux", pages-{SEED_PAGE}), ("panneau_source",{SEED_PAGE}), ("ensemble",pages)):
        parts = [r for r in geo if r["page"] in ps]
        chosen = [r for r in pair_rows if r["page"] in ps]
        testable = [r for r in chosen if r["statut"] == "admissible"]
        found = [m for m in matches if m["page"] in ps]
        totals = {"panneaux":len(ps), "rangees":len(parts), "fragments":sum(len(r["fragments"].split(",")) for r in parts),
                  "paires_physiques":len(chosen),"statuts":dict(Counter(r["statut"] for r in chosen)),
                  "paires_admissibles_sur_panneau_avec_P0":sum(bool(lines[r["page"]]) for r in testable),
                  "rangees_avec_paragraphe":sum(bool(r["prose"]) for r in parts),
                  "paires_admissibles_avec_paragraphe":sum(bool(r["paragraphe_geometrique"]) for r in testable)}
        local_ids = {f"{r['page']}.{i}" for r in parts for i in r["prose"].split(",") if i}
        for label, keep in (("panneau",None), ("local",local_ids)):
            eligible_lines = {loc:seq for p in ps for loc,seq in lines[p].items() if keep is None or loc in keep}
            all_windows = [w for seq in eligible_lines.values() for w in futures(seq)]
            applicable = [m for m in found if label=="panneau" or m["local"]]
            occupied = {p["paire"] for p in testable if (lines[p["page"]] if keep is None else p["paragraphe_geometrique"])}
            pair_line_tests = sum(len(lines[r["page"]]) if keep is None else len(r["paragraphe_geometrique"]) for r in testable)
            totals[label] = {"lignes_distinctes":len(eligible_lines), "positions":sum(map(len,eligible_lines.values())),
                             "fenetres":len(all_windows),"fenetres_extremites_lisibles":sum(certain(a) and certain(b) for a,b,_,_ in all_windows),
                             "paires_admissibles_testables":len(occupied),"comparaisons_paire_ligne":pair_line_tests}
            for direction in ("direct","inverse"):
                sel=[m for m in applicable if m["ordre"]==direction]
                totals[label][direction]={"reprises":len(sel),"paires":len({m["paire"] for m in sel}),"lignes":len({m["ligne"] for m in sel})}
        summary[scope]=totals
    return {"toutes_paires":pair_rows,"toutes_les_reprises":matches,"effectifs":summary,
            "ligne_source_f89r2_22":lines[SEED_PAGE][SEED_PAGE+".22"]}


def consensus(world):
    def key(m):
        return (m["paire"],tuple(m["mots"]),m["ordre"],m["ligne"])
    idxs = {e:defaultdict(list) for e in world}
    for e,d in world.items():
        for m in d["toutes_les_reprises"]:
            idxs[e][key(m)].append(m)
    common = []
    for k in sorted(idxs["H"].keys() & idxs["ZL"].keys()):
        common.append({"paire":k[0],"mots":k[1],"ordre":k[2],"ligne":k[3],
                       "temoins":{e:idxs[e][k] for e in idxs}})
    comparable = {}
    for scope, is_inside in (("autres_panneaux", lambda row:row["page"]!=SEED_PAGE),
                             ("panneau_source",lambda row:row["page"]==SEED_PAGE)):
        a,b = (world[e]["toutes_paires"] for e in ("H","ZL"))
        assert [x["paire"] for x in a] == [x["paire"] for x in b]
        both = [(x,y) for x,y in zip(a,b) if is_inside(x) and x["statut"]==y["statut"]=="admissible"]
        same = [x for x,y in both if all(x[s]["dernier"]==y[s]["dernier"] for s in ("gauche","droite"))]
        comparable[scope] = {"paires_admissibles_deux_editions": len(both),"memes_deux_mots": len(same),
                             "memes_deux_mots_avec_paragraphe":sum(bool(x["paragraphe_geometrique"]) for x in same)}
    return {"reprises_memes_mots_ligne_ordre_et_etiquettes":common,"denominateurs":comparable}


if __name__ == "__main__":
    editions,_ = corpus()
    geo = geometry()
    out={}
    for split in ("joints","separes"):
        result={ed:run(rows,geo,split) for ed,rows in editions.items()}
        out[split] = dict(result, concordance=consensus(result))
    print(json.dumps(out, ensure_ascii=False, indent=1))
