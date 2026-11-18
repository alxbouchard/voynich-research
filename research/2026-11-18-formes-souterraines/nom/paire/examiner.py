"""Rejouer le test prospectif du commit cfe9a2b. Sortie JSON sur stdout."""
from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / "second"))
from transfert import corpus, labels, tokens

R, L = "opcheor", "opcheol"
SOURCE = "f89r2"
ANCHOR = SOURCE + ".22"
EDS = ("H", "ZL")


def certain(word):
    return re.fullmatch("[a-z]+", word) is not None


def units(word):
    return re.findall(r"c[kptf]h|ch|sh|.", word)


def entries(d):
    """Une entrée par locus et mots ordonnés, en conservant toutes les positions."""
    out = []
    for (loc, *words), eds in sorted(d.items()):
        out.append({"lieu": loc, "mots": words, "temoins": dict(eds)})
    return out


def counts(rows):
    both = [r for r in rows if set(r["temoins"]) == set(EDS)]
    return {"H": sum(len(r["temoins"].get("H", [])) for r in rows),
            "ZL": sum(len(r["temoins"].get("ZL", [])) for r in rows),
            "communs": sum(min(len(r["temoins"][e]) for e in EDS) for r in both),
            "union": sum(max(map(len, r["temoins"].values())) for r in rows)}


def store(storage, key, ed, val):
    storage.setdefault(key, {}).setdefault(ed, []).append(val)


def raw_groups(raw, split):
    clean = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)
    clean = re.sub(r"<[-~]>", ".", clean)
    protected = {}
    def protect(m):
        code = chr(0xE000 + len(protected))
        protected[code] = m[0]
        return code
    clean = re.sub(r"\[[^\]]*\]", protect, clean)
    clean = clean.replace(",", "." if split == "separes" else "")
    return [word.translate({ord(k): v for k, v in protected.items()}) for word in clean.split(".") if word]


def latent(word):
    """Recenser les alternatives éditoriales explicites, sans inventer les signes ?."""
    if "[" not in word:
        return []
    parts = re.split(r"(\[[^\]]*\])", word.replace("{", "").replace("}", ""))
    choices = [s[1:-1].split(":") if s.startswith("[") else [s] for s in parts]
    return sorted({"".join(xs) for xs in product(*choices)}.intersection({R, L}))


def candidate_context(raw, split, seq, i, j):
    # Les espaces marqués par un dessin sont traités comme des espaces dans le protocole.
    # Remplacer les ruptures graphiques explicites par un mot sentinelle donne leurs limites.
    flagged = re.sub(r"<[-~]>|<!(?:gap|tear|plant|drawing|crease|fold)[^>]*>", ".zzgapzz.", raw,
                     flags=re.IGNORECASE)
    marked = tokens(flagged, split)
    filtered = [w for w in marked if w != "zzgapzz"]
    if tuple(filtered) != seq:
        return "commentaire_interieur_non_aligne"
    idx = [k for k, w in enumerate(marked) if w != "zzgapzz"]
    return "rupture_graphique" if "zzgapzz" in marked[idx[i]:idx[j] + 1] else "continu"


def run(eds, split):
    denominators = {}
    singles, near, pairs, borderline, alternate = {}, {}, {}, {}, {}
    lf_by_ed = {ed: labels(rows, split) for ed, rows in eds.items()}
    assert set(lf_by_ed["H"]) == set(lf_by_ed["ZL"])
    lf_words = {}
    for ed, inscriptions in lf_by_ed.items():
        for loc, seq in inscriptions.items():
            for i, w in enumerate(seq, 1):
                if certain(w):
                    store(lf_words, (loc, w), ed, {"rang": i, "entiere": len(seq) == 1})
    for ed, rows in eds.items():
        totals = defaultdict(Counter)
        for loc, (page, kind, _, raw) in rows.items():
            seq = tokens(raw, split)
            original = raw_groups(raw, split)
            assert len(original) == len(seq), (loc, raw)
            for group in ("manuscrit", kind, kind + ("_source" if page == SOURCE else "_hors_panneau")):
                c = totals[group]
                c["lignes"] += 1
                c["positions"] += len(seq)
                c["lisibles"] += sum(map(certain, seq))
                if kind == "P0":
                    c["voisinages_adjacents"] += max(0, len(seq) - 1)
                    c["adjacents_lisibles"] += sum(certain(a) and certain(b) for a, b in zip(seq, seq[1:]))
                    c["jusqua_trois_intercalaires"] += sum(max(0, len(seq)-distance) for distance in range(1, 5))
                    c["jusqua_trois_intercalaires_extremites_lisibles"] += sum(
                        certain(a) and certain(b) for k in range(1,5) for a,b in zip(seq,seq[k:]))
            for i, w in enumerate(seq):
                if w in {R, L}:
                    store(singles, (loc, w), ed, {"rang": i+1, "classe": kind})
                if w == "opchear":
                    store(alternate, (loc,w), ed, {"rang":i+1,"classe":kind,
                          "opcheol_meme_ligne":L in seq})
                raw_word = original[i]
                if w not in {R, L} and (any(x in raw_word for x in (R, L)) or latent(raw_word)):
                    store(borderline, (loc, raw_word), ed, {"rang": i+1, "classe": kind,
                                                           "alternatives_cible": latent(raw_word)})
                if kind != "P0" or not certain(w):
                    continue
                for j in range(i+1, min(i+5, len(seq))):
                    v = seq[j]
                    if {v, w} == {R, L}:
                        store(near, (loc, w, v), ed, {"rangs":[i+1,j+1], "intercalaires":j-i-1})
                if i+1 == len(seq):
                    continue
                v = seq[i+1]
                if certain(v) and {v[-1],w[-1]} == {"r","l"} and v[:-1] == w[:-1] and len(units(w[:-1])) >= 3:
                    store(pairs, (loc, w, v), ed, {"rangs":[i+1,i+2], "frontiere":candidate_context(raw,split,seq,i,i+1),
                                                  "ligature":any("{" in word for word in original[i:i+2])})
        denominators[ed] = dict(totals)
    result_pairs = entries(pairs)
    assert all(len(v) == 1 for matches in (pairs, singles, near)
               for eds_per_locus in matches.values() for v in eds_per_locus.values())
    witnesses_lf = entries(lf_words)
    for row in result_pairs:
        row["liens_Lf"] = [l for l in witnesses_lf if l["mots"][0] in row["mots"]]
    aggregates = {}
    for name, subset in (("hors_panneau", [r for r in result_pairs if r["lieu"].split(".")[0] != SOURCE]),
                         ("hors_ligne_source", [r for r in result_pairs if r["lieu"] != ANCHOR])):
        agg = {}
        for order in ("r-l", "l-r"):
            items = [r for r in subset if r["mots"][0][-1] == order[0]]
            common = [r for r in items if set(r["temoins"]) == set(EDS)]
            whole = []
            for r in common:
                if any(set(lf["temoins"]) == set(EDS) and
                       all(any(pos["entiere"] for pos in lf["temoins"][e]) for e in EDS) for lf in r["liens_Lf"]):
                    whole.append(r["lieu"])
            agg[order] = {"occurrences": counts(items), "formes_distinctes_communes": len({tuple(r["mots"]) for r in common}),
                          "formes_distinctes_union":len({tuple(r["mots"]) for r in items}),
                          "lieux_communs_avec_Lf_entiere_concordante": whole,
                          "lieux_communs_avec_Lf_mot_concordant": [
                              r["lieu"] for r in common if any(set(lf["temoins"]) == set(EDS) for lf in r["liens_Lf"])]}
        aggregates[name] = agg
    lf_target = [r for r in witnesses_lf if r["mots"][0] in {L, R}]
    lf_count = {}
    for ed, rows in lf_by_ed.items():
        external = [s for loc, s in rows.items() if not loc.startswith(SOURCE+".")]
        lf_count[ed] = {"total": len(rows), "hors_panneau":len(external),
                        "hors_panneau_entierement_lisibles":sum(all(map(certain,s)) for s in external),
                        "hors_panneau_lisibles_monolexicaux":sum(len(s)==1 and certain(s[0]) for s in external)}
    common_lf = [loc for loc in lf_by_ed["H"] if not loc.startswith(SOURCE+".")
                 and all(all(map(certain, lf_by_ed[ed][loc])) for ed in EDS)]
    lf_count["communs_lisibles_hors_panneau"] = len(common_lf)
    p0 = {ed:{loc for loc,(page,kind,_,_) in rows.items() if kind=="P0" and page!=SOURCE}
          for ed,rows in eds.items()}
    denom_common = len(p0["H"] & p0["ZL"])
    target_pairs = entries(near)
    targets = {"Lf_entiere_opcheol_hors_panneau":[x for x in lf_target if x["mots"] == [L]
                   and not x["lieu"].startswith(SOURCE+".") and all(
                       any(v["entiere"] for v in x["temoins"].get(ed,[])) for ed in EDS)],
               "paire_directe_autre_ligne":[x for x in target_pairs if x["lieu"] != ANCHOR
                   and x["mots"] == [R,L] and all(
                       any(v["intercalaires"] == 0 for v in x["temoins"].get(ed,[])) for ed in EDS)],
               "paire_deux_ordres_0_a_3_intercalaires_autre_ligne":[x for x in target_pairs if x["lieu"] != ANCHOR]}
    return {"denominateurs":denominators, "denominateurs_Lf":lf_count,
            "lignes_P0_communes_hors_panneau":denom_common,"epreuves":targets,
            "occurrences_exactes":entries(singles),"inscriptions_Lf_cibles":lf_target,
            "variante_opchear":entries(alternate),
            "graphies_voisines_exclues":entries(borderline),"paires_cibles":entries(near),
            "controle":aggregates,"paires_r_l_toutes_lignes":result_pairs}


if __name__ == "__main__":
    rows, _ = corpus()
    print(json.dumps({s: run(rows,s) for s in ("joints","separes")},indent=1,ensure_ascii=False))
