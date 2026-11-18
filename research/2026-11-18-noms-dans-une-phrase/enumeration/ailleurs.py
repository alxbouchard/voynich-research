"""Contrôle sur la prose extérieure à tous les folios de fragments étiquetés."""
from collections import Counter, defaultdict
import json
from enumerer import HERE, describe, manuscript
from contexte import MODES, corpus, folio, sequence
import re


def compare_views(editions, excluded, vocab):
    inventories = {}
    for ed, rows in editions.items():
        for cut in MODES:
            counts = Counter()
            patterns = Counter()
            for loc, (p,kind,_,raw) in rows.items():
                if kind != "P0" or folio(p) in excluded:
                    continue
                ws = sequence(raw,cut)
                for i in range(len(ws)-3):
                    span = ws[i:i+4]
                    if span[0][0] != span[-1][0] or any(not re.fullmatch("[a-z]+", w) for _,w in span):
                        continue
                    counts["fenetres"] += 1
                    a,x,b,y = [w for _,w in span]
                    if a == b == "daiin":
                        patterns[loc,x,y] += 1
                        counts["motifs"] += 1
                        if x in vocab:
                            counts["x_dans_index"] += 1
                            counts["y_dans_index_et_distinct"] += int(y in vocab and y != x)
            inventories[ed+"/"+cut] = (counts,patterns)
    sets = [set(pp) for _,pp in inventories.values()]
    examples = [dict(lieu=l,x=x,y=y,x_indexe=x in vocab,y_indexe=y in vocab,
            lectures={key:counts[l,x,y] for key,(_,counts) in inventories.items()})
            for l,x,y in sorted(set.union(*sets))]
    return dict(totaux={key:counts for key,(counts,_) in inventories.items()},
                occurrences_hors_rang=sum(min(row["lectures"].values()) for row in examples),lieux=examples)


def independent_check(segments, lex):
    stats = Counter()
    groups = defaultdict(Counter)
    for p, loc, words, offset in segments:
        for i in range(3, len(words)):
            a, x, b, y = words[i-3:i+1]
            if None in (a, x, b, y):
                continue
            stats["quatre"] += 1
            if a != b:
                continue
            groups[a]["motif"] += 1
            if x in lex:
                groups[a]["x_dans_index"] += 1
                if y in lex and y != x:
                    groups[a]["y_dans_index_et_distinct"] += 1
    return stats, dict(sorted(groups.items()))


def main():
    gallery, _, rec = manuscript()
    known = {folio(p) for p in gallery}
    vocab = set.union(*gallery.values())
    editions, topics = corpus()
    spans = []
    all_pages = set()
    for p, loc, ss in rec:
        if folio(p) in known:
            continue
        all_pages.add(p)
        offset = 0
        for words in ss:
            spans.append((p,loc,words,offset))
            offset += len(words)
    g = {p:vocab for p in all_pages}
    result = describe(spans,g,"daiin")
    tables = result["comptes"]
    counts, repeated = independent_check(spans,vocab)
    assert sum(c["fenetres"] for c in tables.values()) == counts["quatre"]
    assert repeated["daiin"]["motif"] == tables.get("conjonction",{}).get("fenetres",0)
    assert repeated["daiin"]["x_dans_index"] == tables.get("conjonction",{}).get("x_legende",0)
    for entry in result["expressions"]:
        p,loc,rank=entry["page"],entry["lieu"],entry["rang"]
        entry["section"]=topics.get(p)
        entry["verifications"]={}
        for ed, rows in editions.items():
            for mode in MODES:
                full=sequence(rows[loc][3],mode)
                raw=[w for _,w in full[rank-1:rank+3]]
                assert raw==["daiin",entry["x"],"daiin",entry["y"]]
                entry["verifications"][ed+"/"+mode]=raw
    # Test the tenth word also against all Lf, including those below the three-unit cutoff.
    raw_labels = {}
    for w in ("ckhy","ckhol","okeoly"):
        raw_labels[w]={ed+"/"+mode:[loc for loc,(_,kind,_,raw) in rows.items() if kind=="Lf"
                                     and w in {word for _,word in sequence(raw,mode)}]
                       for ed,rows in editions.items() for mode in MODES}
    output=dict(vocabulaire=sorted(vocab),feuillets_exclus=sorted(known),panneaux_avec_prose=len(all_pages),
                resultats=tables,motifs_repetes=repeated,positions_daiin=result["expressions"],
                lignes_de_legendes_sans_minimum=raw_labels, variantes=compare_views(editions,known,vocab))
    (HERE/"AILLEURS.json").write_text(json.dumps(output,ensure_ascii=False,indent=1,sort_keys=True)+"\n")
    print({k:v for k,v in tables.items() if k!="sans_repetition"})
    print("pages",len(all_pages),"vocab",len(vocab),"tous",counts)
    print("cibles",[(v["lieu"],v["x"],v["y"]) for v in result["expressions"] if v["premier_indexe"]])


if __name__=="__main__":
    main()
