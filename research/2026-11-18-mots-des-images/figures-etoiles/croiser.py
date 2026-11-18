"""Exploratory cross-context lookup of whole signs groups around composite drawings."""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_20261028/data"
INITIAL = {"f71v", "f72r1"}
STAR = {"f68r1", "f68r2"}
PATTERN = re.compile(r"^<((f(\d+)[rv]\d*)\.\d+),.([A-Za-z0-9]{2})>\s+(.*)$")


def inventory(path, split):
    rows = {}
    for line in path.read_text().splitlines():
        m = PATTERN.match(line)
        if not m:
            continue
        loc, face, leaf, kind, raw = m.groups()
        if face in STAR and kind == "Ls":
            category = "etoiles"
        elif 70 <= int(leaf) <= 73 and kind == "Lz":
            category = "zodiaque_deux" if face in INITIAL else "zodiaque_dix"
        elif 75 <= int(leaf) <= 84 and kind in ("Ln","Lt"):
            category = "figures_bains" if kind == "Ln" else "objets_bains"
        else:
            continue
        raw = re.sub(r"<![^>]*>|<[%$]>|!", "", raw)  # Editorial comments include clock positions.
        raw = re.sub(r"<[-~]>", ".", raw).strip(".").replace(",", "." if split else "")
        # Exclude a whole line for any unresolved sign or annotation.
        words = raw.split(".") if re.fullmatch("[a-z]+(?:[.][a-z]+)*",raw) else None
        assert loc not in rows
        rows[loc] = (face,category,words)
    return rows


def analyze(rows):
    both = set.intersection(*({face for face,cat,w in rows.values() if cat==kind and w}
                              for kind in ("figures_bains","objets_bains")))
    counts = defaultdict(lambda: {"toutes":0,"lisibles":0,"groupes":0})
    index = defaultdict(lambda: defaultdict(list))
    for loc,(face,cat,words) in sorted(rows.items()):
        if cat in ("figures_bains","objets_bains") and face not in both:
            continue
        counts[cat]["toutes"] += 1
        if words is None:
            continue
        counts[cat]["lisibles"] += 1
        counts[cat]["groupes"] += len(words)
        for word in set(words):
            index[cat][word].append(loc)
    result = {}
    for src in ("etoiles","figures_bains"):
        ref = index[src]
        candidates = sorted(w for w,loci in ref.items() if len({l.split(".")[0] for l in loci}) >= 2)
        common_initial = sorted(ref.keys() & index["zodiaque_deux"].keys())
        common_ten = sorted(ref.keys() & index["zodiaque_dix"].keys())
        def profile(w):
            return {cat:index[cat].get(w,[]) for cat in sorted(counts)}
        result[src] = {"candidats_deux_faces":{w:profile(w) for w in candidates},
                       "intersections_sans_seuil_deux":{w: profile(w) for w in common_initial},
                       "intersections_sans_seuil_dix":{w: profile(w) for w in common_ten}}
    return {"denominateurs":dict(counts),"faces_bains_mixtes":sorted(both),"tests":result}


def main():
    paths = {"H":DATA/"IT2a-n.txt","ZL":DATA/"ZL3b-n.txt"}
    report = {"sha256":{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},"lectures":{}}
    for split in (False,True):
        tables = {k:inventory(p,split) for k,p in paths.items()}
        # A conservative common panel uses the same line and the same full group sequence.
        h,z = tables.values()
        shared = {}
        for loc in h.keys() | z.keys():
            row = h.get(loc) or z[loc]
            if loc in h and loc in z:
                assert h[loc][:2] == z[loc][:2]
            shared[loc] = row if h.get(loc) == z.get(loc) else (row[0],row[1],None)
        tables["accord"] = shared
        for name,rows in tables.items():
            report["lectures"][name+("_separe" if split else "_joint")] = analyze(rows)
    (HERE/"resultats.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")


if __name__ == "__main__":
    main()
