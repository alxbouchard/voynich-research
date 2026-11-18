"""Ouvrir les finales puis comparer chaque règle aux mêmes positions lisibles."""
from collections import Counter, defaultdict
from corpus_dam import (corpus, group, h_rows, metadata, position_key,
                        read, save, split_word, strict_rows)


def opening():
    editions, _ = corpus()
    meta = metadata()
    cov = Counter()
    strict, source = {}, {}
    for loc,(page,kind,_,raw) in editions["H"].items():
        lot = group(page,kind,meta)
        if lot not in {"dernier_cahier","bains","legendes"}:
            continue
        for part,idx,word,_ in h_rows(raw):
            source[position_key(loc,part,idx)] = word
        for part,idx,word,_ in strict_rows(editions,loc,meta[page].get("I",""),cov):
            strict[position_key(loc,part,idx)] = word
    result = []
    for item in read("ANNONCES.json.gz"):
        pos = item["lieu"]
        word = source[pos]
        base,tail = split_word(word)
        assert base == item["base"] and strict.get(pos) in (None,word)
        result.append({**item,"vrai":word,"finale":tail,"accord":pos in strict})
    return result


def score(items,level,scope,tail_filter):
    candidates = [x for x in items if (scope=="court")== (x["base"]=="da")
                  and (tail_filter=="multiple" or x["finale"]!="iin")
                  and (tail_filter!="rm" or x["finale"] in ("r","m"))]
    rows = [x for x in candidates if level=="H" or x["accord"]]
    scores = {}
    for name, subset in (("toutes",rows),("fin",[x for x in rows if x["fin"]]),
                         ("autres",[x for x in rows if not x["fin"]])):
        scores[name] = {"n":len(subset),"vraies_finales":dict(Counter(x["finale"] for x in subset)),
                        "succes":dict(Counter({rule:sum(x["mots"][rule]==x["vrai"] for x in subset)
                               for rule in ("r_m","r_constant","base","base_et_position","l_m","iin_m")}))}
    return {"annonces":len(candidates),"score":scores}


def main():
    rows = opening()
    save("OUVERTURES.json.gz", rows)
    results = {}
    for lot in sorted({x["lot"] for x in rows}):
        items = [x for x in rows if x["lot"]==lot]
        for level in ("H","accord"):
            for scope in ("long","court"):
                for endings in ("simple","rm","multiple"):
                    results["/".join([lot,level,scope,endings])] = score(items,level,scope,endings)
    save("RESTITUTIONS.json",results)


if __name__ == "__main__":
    main()
