"""Déterminer si un voisin de la reprise de f89r2 annonce d'autres légendes."""
from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH/"2026-11-18-legendes-et-paragraphes"))
from comparer import MODES, common_words, inventory
sys.path.insert(0, str(RESEARCH/"2026-11-18-opcheor-paralleles/variantes"))
from compter import corpus, runs

MARK = "sheey"
FIRST = "qokeoefy"


def counts(raw, cut, n):
    out = Counter()
    for span in runs(re.sub(r"\{[^}]*\}", "?", raw), cut):
        ws = [w for _,w in span]
        out.update(zip(*(ws[j:] for j in range(n))))
    return out


def agreed(editions):
    result = {}
    for loc in sorted(set.intersection(*(set(v) for v in editions.values()))):
        if any(ed[loc][1]!="P0" for ed in editions.values()):
            continue
        shared = []
        for n in (1,2,3):
            first,*others = [counts(editions[ed][loc][3], cut, n) for ed,cut in MODES]
            for other in others:
                first &= other
            shared.append(first)
        result[loc] = shared
    return result


def marker_trial(mark, corpus, labels, genre, pages):
    hits = []
    for loc, ngrams in corpus.items():
        page = loc.split(".")[0]
        if page not in pages:
            continue
        for sequence,count in ngrams[len(mark)].items():
            if sequence[:-1] != mark:
                continue
            nxt=sequence[-1]
            control = {p: labels[p][nxt] for p in sorted(pages) if genre[p]==genre[page] and nxt in labels[p]}
            hits.append({"locus":loc,"suivant":nxt, "n":count, "legendes_propres":labels[page].get(nxt,[]),
                         "panneaux_compatibles":control})
    return hits


def main():
    tables,_ = corpus()
    pages, quires, views = inventory()
    labels = {p:common_words([views[m][0][p] for m in MODES]) for p in pages}
    # Un panneau dont les étiquettes concordent mal reste inclus au dénominateur.
    reserve = {p for p in pages if p != "f101r" and not p.startswith("f89")}
    data = agreed(tables)
    assert any(r["suivant"]=="opcheor" and r["legendes_propres"]==["f89r2.5"]
               for r in marker_trial((FIRST,MARK),data,labels,quires,{"f89r2"}))
    result = {"panneaux":sorted(reserve), "denominateurs":{}, "hypotheses":{}, "reprises":{},
              "transfert_autres_predecesseurs":{}}
    for p in sorted(reserve):
        bucket = {loc:ng for loc,ng in data.items() if loc.partition(".")[0]==p}
        result["denominateurs"][p] = {"lignes":len(bucket),
            "mots_au_meme_lieu":sum(sum(ng[0].values()) for ng in bucket.values()),
            "legendes_lieux_admissibles":len({loc for loci in labels[p].values() for loc in loci}),
            "mots_legendes":len(labels[p])}
        for loc, (words,pairs,_) in bucket.items():
            for (name,), n in words.items():
                if name in labels[p]:
                    result["reprises"].setdefault(loc,{})[name] = {
                        "n":n,"legendes":labels[p][name],
                        "precedents":{a:k for (a,b),k in pairs.items() if b==name}}
    for marker in [(FIRST,MARK),(MARK,)]:
        index=len(marker)-1
        def totals(allowed):
            return sum(row[index][marker] for loc,row in data.items() if allowed(loc.split(".")[0]))
        result["hypotheses"][" ".join(marker)] = {
            "marqueur_dans_prose_entiere":totals(lambda p:True),
            "marqueur_hors_f89":totals(lambda p:not p.startswith("f89")),
            "marqueur_panneaux_reserves":totals(reserve.__contains__),
            "annonces":marker_trial(marker,data,labels,quires,reserve)}
    seeds = defaultdict(list)
    for loc,names in result["reprises"].items():
        for name, detail in names.items():
            for prev in detail["precedents"]:
                seeds[prev].append((loc,name))
    for prev, seed in sorted(seeds.items()):
        hits = marker_trial((prev,),data,labels,quires,reserve)
        predictions = []
        for hit in hits:
            leaf = re.match(r"f\d+",hit["locus"])[0]
            learn = [(loc,name) for loc,name in seed if re.match(r"f\d+",loc)[0]!=leaf]
            if learn:
                predictions.append({"locus":hit["locus"],"suivant":hit["suivant"],"n":hit["n"],
                                    "legendes":hit["legendes_propres"],"apprentissage":learn,
                                    "juste_nom_different":bool(hit["legendes_propres"] and
                                             any(hit["suivant"]!=name for _,name in learn))})
        result["transfert_autres_predecesseurs"][prev] = {"departs":seed, "annonces":predictions}
    (HERE/"RESULTATS.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("panneaux",len(reserve),"mots",sum(v["mots_au_meme_lieu"] for v in result["denominateurs"].values()))
    for k,rec in result["hypotheses"].items(): print(k,rec)
    print("reprises",len(result["reprises"]),sum(v["n"] for row in result["reprises"].values() for v in row.values()))
    transfer=result["transfert_autres_predecesseurs"]
    print("autres apprentissages",len(transfer),"nb annonces",sum(len(x["annonces"]) for x in transfer.values()))
    print("justes",[(k,r) for k,v in transfer.items() for r in v["annonces"] if r["juste_nom_different"]])


if __name__=="__main__":
    main()
