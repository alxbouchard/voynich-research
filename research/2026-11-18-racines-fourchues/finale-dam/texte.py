"""Chercher les trois formes et la finale dans le recto prévu et les faces comparables."""
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from annoncer import ROOT, MODES, corpus, features, sequence

NAMES = {"oldam","saldam","doldam"}


def main():
    codes = {}
    for line in (ROOT/"voynich_20261028/data/ZL3b-n.txt").read_text().splitlines():
        h = re.match(r"^<(f\w+)>",line)
        if h:
            attrs = dict(re.findall(r"\$(\w)=(\w+)",line))
            codes[h[1]] = tuple(attrs.get(k) for k in ("I","L","H"))
    ref = codes["f55r"]
    assert ref[0] == "H"
    editions, _ = corpus()
    h,z = editions.values()
    output = {}
    for page in sorted(p for p,v in codes.items() if v==ref):
        lines = []
        for loc in h:
            if h[loc][:2]!=(page,"P0") or loc not in z or z[loc][1]!="P0":
                continue
            views=[[w for _,w in sequence(table[loc][3],mode)] for table in (h,z) for mode in MODES]
            reliable = [(i,seq[0]) for i,seq in enumerate(zip(*views),1)
                        if all(w==seq[0] for w in seq) and re.fullmatch("[a-z]+",seq[0])]
            by_line = set.intersection(*(set(v) for v in views))
            ends = sorted(w for w in by_line if re.fullmatch("[a-z]+", w) and ("fin","dam") in features([w]))
            lines.append({"locus":loc, "longueurs":[len(v) for v in views], "rangs_lisibles":len(reliable),
                          "fin_dam_meme_rang":[(i,w) for i,w in reliable if ("fin","dam") in features([w])],
                          "fin_dam_meme_ligne":ends,"exact_meme_ligne":sorted(by_line & NAMES)})
        if lines:
            output[page]=lines
    out={"classe_image_currier_main":ref,"pages":output}
    (HERE/"F55-TEXTE.json").write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
    for key, subset in (("f55r",output["f55r"]),("autres",[r for p,rows in output.items() if p!="f55r" for r in rows])):
        with_end=[(x["locus"],x["fin_dam_meme_rang"]) for x in subset if x["fin_dam_meme_rang"]]
        print(key, len(subset),sum(x["rangs_lisibles"] for x in subset),with_end[:12],len(with_end))
    print('panels',len(output))


if __name__=="__main__":
    main()
