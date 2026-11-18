"""Look up preregistered pairs in local and held paragraphs in separate stages."""
import argparse
import itertools
import json
import random
import re
from collections import Counter, defaultdict
from functools import lru_cache

from predire import ALG, DATA, EDITIONS, GEOMETRY, HERE, sha

POT = ("okol", "otoldy")
PRIMARY = "accord/joint/strict"
N_RANDOM = 9999
HEADER = re.compile(r"^<((f\w+)\.(\d+)),[^>](P\w)>")


def raw_text(pages):
    out = {}
    for ed, name in EDITIONS.items():
        table = {}
        for line in (DATA/name).read_text().splitlines():
            h = HEADER.match(line)
            if h and h[2] in pages:
                assert h[1] not in table
                table[h[1]] = line[h.end():].strip()
        out[ed] = table
    return out


@lru_cache(maxsize=None)
def tokens(body, split):
    s = re.sub(r"<![^>]*>|<@[^>]*>|<[%$]>|!", "", body)
    s = re.sub(r"<[~-]>", ".", s)
    assert "<" not in s and ">" not in s
    fields = [p for p in s.replace(",", "." if split else "").split(".") if p]
    return [w if re.fullmatch("[a-z]+", w) else None
            for w in (p.replace("{","").replace("}","") for p in fields)]


def slice_local(loci, table):
    blocks, run = [], []
    for loc in loci:
        raw = table.get(loc)
        if raw is None or "<%>" in raw:
            if run:
                blocks.append(run)
            run = []
        if raw is not None:
            run.append(loc)
            if "<$>" in raw:
                blocks.append(run)
                run = []
    if run:
        blocks.append(run)
    return blocks


def passages(rows, scope, edition, raw):
    if scope == "notices":
        markup = json.loads((HERE/"notices/paragraphes.json").read_text())
        return {"notices": [[x.split(",")[0] for x in seq] for seq in markup[edition]]}
    out = {}
    for key,row in rows.items():
        loci = [row["page"]+"."+str(n) for n in row["prose"]]
        groups = {ed:slice_local(loci,table) for ed,table in raw.items()}
        out[key] = ([seq for seq in groups["H"] if seq in groups["ZL"]]
                    if edition=="accord" else groups[edition])
    return out


@lru_cache(maxsize=None)
def units(w):
    return tuple(ALG["EVA"].findall(w))


def signatures(w):
    u = units(w)
    return {prefix for prefix in (u,u[:-1]) if len(prefix)>=4}


def word_map(vocab, relaxed):
    by_stem = defaultdict(set)
    if relaxed:
        for q in vocab:
            for stem in signatures(q):
                by_stem[stem].add(q)

    @lru_cache(maxsize=None)
    def tags(w):
        hits = {w} if w in vocab else set()
        if relaxed:
            for stem in signatures(w):
                hits.update(by_stem[stem])
        return hits
    return tags


def match_records(block, edition, raw, split, tags, window):
    seq, singles, matches = [], set(), {}
    for locus in block:
        ws = tokens(raw[edition][locus], split)
        for i,w in enumerate(ws, 1):
            found = tags(w) if w else set()
            here = (len(seq),locus,i,w,found)
            if found:
                singles.update((q,locus,w) for q in found)
                for off,prev_locus,prev_index,prev_word,prev_tags in seq[-window:] if window else seq:
                    for a in prev_tags:
                        for b in found:
                            if a == b:
                                continue
                            key = (a,b,prev_locus,locus,prev_word,w)
                            record = (prev_index,i,len(seq)-off)
                            matches.setdefault(key,[]).append(record)
            seq.append(here)
    return singles, matches


def pairs_in(blocks, edition, raw, split, tags, window):
    eds = list(EDITIONS) if edition=="accord" else [edition]
    all_hits, available, volumes = defaultdict(list), set(), {}
    for block in blocks:
        trials = {ed:match_records(block,ed,raw,split,tags,window) for ed in eds}
        singles = set.intersection(*(s for s,_ in trials.values()))
        available.update(q for q,_,_ in singles)
        positions = set.intersection(*(set(m) for _,m in trials.values()))
        for pos in sorted(positions):
            a,b,l,r,actual1,actual2 = pos
            pair = tuple(sorted((a,b)))
            all_hits[pair].append({"notice":block[0],"ordre":[a,b],"lignes":[l,r],
                                   "graphies":[actual1,actual2],
                                   "positions_distance":{ed:trials[ed][1][pos] for ed in eds}})
        for ed in eds:
            slots = [w for loc in block for w in tokens(raw[ed][loc],split)]
            v = volumes.setdefault(ed,[0,0])
            v[0]+=len(slots)
            v[1]+=sum(w is not None for w in slots)
    return all_hits, available, volumes


def labels_per_page(rows):
    pages = defaultdict(list)
    for key,row in rows.items():
        pages[row["page"]].append(key)
    return pages


def permute(rows, sets, scope):
    pages = labels_per_page(rows)
    seen_groups = {key:0 for key in rows}
    data = []
    for page,keys in pages.items():
        parts = []
        included = set()
        for k in keys:
            objects = rows[k]["objets"]
            assert not included.intersection(objects), (page,k)
            included.update(objects)
            parts.append(list(objects.values()))
        flat = [item for row in parts for item in row]
        indexes = list(range(len(flat)))
        tests = []
        for k,part in zip(keys,parts):
            hits = sets["notices" if scope=="notices" else k]
            edges = {(i,j) for i,j in itertools.combinations(indexes,2)
                     if any(tuple(sorted((a,b))) in hits for a in flat[i] for b in flat[j] if a!=b)}
            tests.append((k,len(part),edges))
        data.append((indexes,tests))
    rng = random.Random(1429)
    hist = Counter()
    for rep in range(N_RANDOM+1):
        score = 0
        for idx, tests in data:
            if rep:
                rng.shuffle(idx)
            lo=0
            for k,n,edges in tests:
                inside = set(idx[lo:lo+n])
                positive = any(i in inside and j in inside for i,j in edges)
                score += positive
                if not rep:
                    seen_groups[k] = int(positive)
                lo+=n
        if not rep:
            actual=score
        else:
            hist[score]+=1
    return {"rangs_observes":actual, "rangs":seen_groups, "tirages":N_RANDOM, "graine":1429,
            "histogramme":dict(sorted(hist.items())),
            "proportion_corrigee":(1+sum(n for v,n in hist.items() if v>=actual))/(N_RANDOM+1)}


def render_pairs(records, allowed):
    return {" ".join(key):records[key] for key in sorted(records.keys() & allowed)}


def analyse(rows,scope,edition,split,raw,window,relaxed,primary,check_null):
    groups = passages(rows,scope,edition,raw)
    own = {k:{tuple(p) for p in row["paires"]} for k,row in rows.items()}
    own_all = set().union(*own.values())
    vocab = {w for row in rows.values() for words in row["objets"].values() for w in words} | set(POT)
    tags = word_map(vocab,relaxed)
    found, sets, all_available = {},{},{}
    for k,blocks in groups.items():
        hits,available,volume = pairs_in(blocks, edition, raw, split,tags,window)
        allowed = own_all if scope=='notices' else own[k]
        detail = render_pairs(hits,allowed)
        sets[k] = hits.keys()
        all_available[k] = available
        localpot = scope=='notices' or (rows[k]["page"]=="f89r2" and 9 in rows[k]["pots"])
        found[k]={"paragraphes":len(blocks),"positions_totales_et_lisibles":volume,
                  "candidats_presents":sorted(vocab & available),
                  "paires_deux_mots_presents":sum(a in available and b in available for a,b in allowed),
                  "paires_retrouvees":sorted(detail),"pot_fragment":hits.get(POT,[]) if localpot else None}
        if primary:
            found[k]["rencontres"]=detail
        elif detail:
            found[k]["premier_exemple_par_paire"]={key:v[0] for key,v in detail.items()}
    out={"paires_distinctes":len(own_all),"blocs":found}
    if scope=="notices":
        hits=sets["notices"]
        positives=own_all & hits
        cross=set()
        pages=labels_per_page(rows)
        for keys in pages.values():
            for a,b in itertools.combinations(keys,2):
                for la in rows[a]["objets"].values():
                    for lb in rows[b]["objets"].values():
                        cross.update(tuple(sorted((x,y))) for x in la for y in lb if x!=y)
        out["entre_rangs_differents"]={"paires":len(cross),"positives":sorted(cross&hits),
                                     "aussi_dans_un_meme_rang":sorted(positives&cross)}
        out["rangs_positifs"]=[k for k,pairs in own.items() if pairs & hits]
    else:
        out["rangs_positifs"]=[k for k in rows if own[k] & sets[k]]
    if check_null:
        out["permutations"]=permute(rows,sets,scope)
        assert out["permutations"]["rangs_observes"]==len(out["rangs_positifs"])
    return out


def execute(scope, extended=False):
    suffix = "_pots_elargis" if extended else ""
    geometry = HERE/"rangees/pots_elargis.tsv" if extended else GEOMETRY
    p = HERE/("predictions"+suffix+".json")
    pred = json.loads(p.read_text())
    assert pred["geometrie_sha256"] == sha(geometry)
    assert all(sha(DATA/f)==pred["ivtff_sha256"][ed] for ed,f in EDITIONS.items())
    if scope=="notices":
        paragraphs=json.loads((HERE/"notices/paragraphes.json").read_text())
        pages={x.split(".")[0] for v in paragraphs.values() for seq in v for x in seq}
        local_path=HERE/("local"+suffix+".json")
        local=json.loads(local_path.read_text())
        assert local["prediction_sha256"]==sha(p)
    else:
        pages={r["page"] for r in pred["conditions"][PRIMARY].values()}
    raw=raw_text(pages)
    result={"prediction_sha256":sha(p),"analyses":{}}
    if scope=="notices":
        result["local_sha256"]=sha(local_path)
    for cond,rows in pred["conditions"].items():
        ed,space,kind=cond.split("/")
        # Primary analysis and prespecified one-factor sensitivities, plus
        # the expanded, unrestricted inventory for each individual edition.
        if cond not in (PRIMARY,"accord/separe/strict","accord/joint/elargi",
                        "H/joint/strict","ZL/joint/strict","H/separe/strict","ZL/separe/strict",
                        "H/joint/elargi","ZL/joint/elargi"):
            continue
        configs=[(8,False)]
        if cond==PRIMARY:
            configs.extend([(0,False),(8,True),(0,True)])
        for window,relaxed in configs:
            primary=cond==PRIMARY and window==8 and not relaxed
            key=cond+("/proche" if window else "/entier")+("/base" if relaxed else "/exact")
            check_null=cond==PRIMARY or (cond=="accord/joint/elargi" and window==8)
            run=analyse(rows,scope,ed,space=="separe",raw,window,relaxed,primary,check_null)
            if scope=="notices":
                frozen={pair for block in local["analyses"][key]["blocs"].values()
                        for pair in block["paires_retrouvees"]}
                run["issues_du_local"]=sorted(frozen)
                run["local_puis_notices"]=sorted(frozen & set(run["blocs"]["notices"]["paires_retrouvees"]))
            result["analyses"][key]=run
    (HERE/(scope+suffix+".json")).write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n")


if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("scope",choices=["local","notices"])
    args.add_argument("--pots-elargis", action="store_true")
    args=args.parse_args()
    execute(args.scope,args.pots_elargis)
