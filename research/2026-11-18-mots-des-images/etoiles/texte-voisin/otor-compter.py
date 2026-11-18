"""Rejoue le seul mot otor dans six classes de loci. Python 3, bibliothèque standard."""
import hashlib
import itertools
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[3] / "voynich_phase8" / "data"
FILES = {
    "ZL3b": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
    "IT2a": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
}
PANELS = set("f70v2 f70v1 f71r f71v f72r1 f72r2 f72r3 f72v3 f72v2 f72v1 f73r f73v".split())
CLASSES = ("Lz", "C", "Lf", "Lc", "Ln", "Lt")
TARGET = "otor"
ROW = re.compile(r"^<(f\w+)\.(\d+),(.)([A-Za-z0-9]+)>\s*(.*)$")

def records(ed):
    raw = (DATA / (ed+"-n.txt")).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FILES[ed]
    rows = {k:{} for k in CLASSES}
    excluded = {}
    for line in raw.decode().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        page, num, sep, kind, payload = m.groups()
        group = "C" if page in PANELS and kind.startswith("C") else kind
        if group not in rows or (group=="Lz" and page not in PANELS):
            continue
        locus = f"{page}.{num},{sep}{kind}"
        if sep=="!":
            excluded[locus] = payload
            continue
        assert not payload.endswith("/") and locus not in rows[group]
        rows[group][locus] = payload
    return rows,excluded

def words(raw,join):
    w = re.sub(r"<![^>]*>|<[%$]>", "",raw).replace("<->",".")
    assert "<" not in w and " " not in w
    return [t for t in w.replace(",","" if join else ".").split(".") if t]

def possible(word):
    # Pour otor, les quatre unités sont des signes EVA simples. Un caractère
    # illisible ? peut remplir une de ces positions. ??? indique une longueur inconnue.
    bare = word.replace("{","").replace("}","")
    parts = re.split(r"\[([^\]]*)\]", bare)
    choices = [(s,) if i%2==0 else tuple(s.split(":")) for i,s in enumerate(parts)]
    for variant in itertools.product(*choices):
        reading = "".join(variant)
        components = re.split(r"(\?\?\?|\?)", reading)
        regex = "".join(".+" if s=="???" else "." if s=="?" else re.escape(s) for s in components)
        if re.fullmatch(regex,TARGET):
            return True
    return False

def census(rows,join):
    all_groups = certain_groups = ambiguous_groups = matched_loci = 0
    hits,uncertain = [],[]
    for key, raw in rows.items():
        token_list = words(raw,join)
        matched = False
        for i,token in enumerate(token_list,1):
            all_groups+=1
            ambiguous = "?" in token or "[" in token
            if ambiguous:
                ambiguous_groups+=1
                uncertain.append({"locus":key,"groupe":i,"forme":token,"compatible":possible(token),"texte":raw})
            elif token.replace("{","").replace("}","")==TARGET:
                matched = True
                certain_groups+=1
                hits.append({"locus":key,"groupe":i,"forme":token,"texte":raw})
        matched_loci+=matched
    uncertain_loci={u["locus"] for u in uncertain}
    compatible=[u for u in uncertain if u["compatible"]]
    return {"loci":len(rows),"loci_avec_otor":matched_loci, "groupes":all_groups,"groupes_otor":certain_groups,
            "groupes_lisibles":all_groups-ambiguous_groups,"loci_incertains":len(uncertain_loci),
            "groupes_incertains":ambiguous_groups,"ambigus_compatibles":compatible,
            "rencontres":hits,"lectures_incertaines":uncertain}

def main():
    assert possible("o?or") and possible("ot[o:a]r") and possible("o???r")
    assert not possible("ot[a:e]r") and not possible("otor[a:y]") and not possible("of???")
    report={"mot":TARGET,"protocole_sha256":hashlib.sha256((HERE/"TRANSFERT-OTOR.md").read_bytes()).hexdigest(),
            "sources_sha256":FILES,"panneaux":sorted(PANELS),"editions":{}}
    for ed in FILES:
        rows,excluded=records(ed)
        assert [len(rows[k]) for k in CLASSES] == [299,36,194,40 if ed=="ZL3b" else 37,63,47]
        by_spaces = {}
        for name,join in (("separes",False),("joints",True)):
            by_spaces[name]={kind:census(rows[kind],join) for kind in CLASSES}
        report["editions"][ed]={"loci_fictifs_exclus":excluded,"espaces":by_spaces}
    (HERE/"otor-resultats.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")

if __name__=="__main__":
    main()
