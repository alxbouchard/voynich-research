"""Vérifier les identifiants et conserver les boîtes du texte sans les graphies de prose."""
from collections import Counter
from difflib import SequenceMatcher
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-noms-dans-une-phrase/contexte"))
from contexte import MODES, corpus, sequence, units


def save(name, data):
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode()
    if name.endswith(".gz"):
        raw = gzip.compress(raw, mtime=0)
    (HERE / name).write_bytes(raw)


def load(name):
    raw = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith(".gz") else raw)


def assign(witness, viewer):
    operations = SequenceMatcher(None, witness, viewer, autojunk=False).get_opcodes()
    mapping = {}
    for j,(tag,start,end,ws,we) in enumerate(operations):
        anchored = (0 < j < len(operations)-1 and operations[j-1][0] == "equal"
                    and operations[j+1][0] == "equal")
        if tag == "equal" or (tag == "replace" and end-start == we-ws and anchored):
            for k in range(start,end):
                mapping[k] = (ws+k-start, tag)
    return mapping


def paragraph_ranges(rows, page):
    found = []
    current = []
    for loc, (p,kind,_,raw) in rows.items():
        if p != page or kind != "P0":
            continue
        if "<%>" in raw:
            current = []
        if current or "<%>" in raw:
            current.append(loc)
        if "<$>" in raw and current:
            found.append(tuple(current))
            current = []
    return found


def local_caption(loc, editions):
    views = [tuple(w for _,w in sequence(rows[loc][3],cut))
             for rows in editions.values() if loc in rows and rows[loc][1]=="Lf" for cut in MODES]
    if len(views)!=4 or len(set(views))!=1 or len(views[0])!=1:
        return None
    word = views[0][0]
    return word if re.fullmatch("[a-z]+",word) and len(units(word,False))>=3 else None


def make(page, raw_map, editions):
    dic, boxes = json.loads(raw_map)
    viewer = [dic[a[0]][0] for a in boxes]
    flat, ledger = [], []
    for loc,(p,kind,pos,raw) in editions["H"].items():
        if p != page:
            continue
        vals = sequence(raw,"joints")
        ledger.append((loc,kind,pos,len(flat),len(vals)))
        flat.extend(w for _,w in vals)
    mapping = assign(flat, viewer)
    partial = Counter()
    lines, labels = {}, {}
    for j,(loc,kind,pos,start,n) in enumerate(ledger):
        if kind not in ("P0","Lf"):
            continue
        if kind=="Lf" and (pos=="+" or (j+1<len(ledger) and ledger[j+1][1:3]==("Lf","+"))):
            partial["lf_multilignes"]+=1
            continue
        if not n or any(i not in mapping for i in range(start,start+n)):
            partial[kind+"_boites_incompletes"]+=1
            continue
        ids=[mapping[i][0] for i in range(start,start+n)]
        if ids!=list(range(ids[0],ids[0]+n)):
            partial[kind+"_boites_non_contigues"]+=1
            continue
        coords=[boxes[k][1:5] for k in ids]
        if any(x+w/2 >= u+v/2 for (x,_,w,_),(u,_,v,_) in zip(coords,coords[1:])):
            partial[kind+"_ordre_x"]+=1
            continue
        if kind=="P0":
            lines[loc]=coords
        else:
            word=local_caption(loc,editions)
            if word and n==1 and word==viewer[ids[0]]:
                labels[loc]={"mot":word,"boite":coords[0]}
            elif word:
                partial["lf_graphie_visualiseur"]+=1
            else:
                partial["lf_doute_ou_longueur"]+=1
    by_ed=[paragraph_ranges(rows,page) for rows in editions.values()]
    concordant=[list(v) for v in by_ed[0] if v in by_ed[1]]
    admitted=[group for group in concordant if all(loc in lines for loc in group)]
    coverage={"paragraphes_par_edition":list(map(len,by_ed)),"paragraphes_concordants":len(concordant),
              "paragraphes_geometrie_complete":len(admitted),"exclusions":dict(partial),
              "mots_H":len(flat),"boites":len(boxes),"accords_exacts":sum(k=="equal" for _,k in mapping.values())}
    merged = []
    for block in sorted(set(by_ed[0]) | set(by_ed[1]), key=lambda v:int(v[0].split(".")[1])):
        overlapping = [v for v in merged if set(v) & set(block)]
        combined = set(block)
        for prev in overlapping:
            merged.remove(prev)
            combined.update(prev)
        merged.append(sorted(combined,key=lambda loc:int(loc.split(".")[1])))
    covered = [{loc for block in groups for loc in block} for groups in by_ed]
    both = covered[0] & covered[1]
    alt = {"H":[list(v) for v in by_ed[0]],"ZL":[list(v) for v in by_ed[1]],
           "reunis":[v for v in merged if set(v)<=both]}
    layouts = {key:[v for v in sets if all(loc in lines for loc in v)] for key,sets in alt.items()}
    return dict(lignes=lines,legendes=labels,paragraphes={"strict":admitted,**layouts},couverture=coverage)


def main(cache):
    ed,sections=corpus()
    data,concordance={},{}
    for page in sorted(p for p,topic in sections.items() if topic=="P" and p!="f101r"):
        raw=(cache/(page+".json")).read_bytes()
        name="f101v2" if page=="f101v" else page
        concordance[page]={"url":f"https://www.voynichese.com/2/data/folio/script/{name}.js",
                           "sha256":sha256(raw).hexdigest()}
        data[page]=make(page,raw,ed)
    assert len(data)==15
    save("SOURCES.json",concordance)
    save("CARTE-MASQUEE.json.gz",data)


if __name__=="__main__":
    main(Path(sys.argv[1]))
