"""Tester l'égalité de la première ou dernière unité graphique à un intervalle de dix positions."""
import csv
import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("vocabulaire", HERE.parent / "vocabulaire/comparer.py")
vocab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vocab)
N = 9999
SIGNS = tuple(vocab.PANELS)
TAIL = SIGNS[-3:]
HEAD = SIGNS[:-3]
REBUILT = "neuf_positions_peripheriques"
PRIMARY = "neuf_series_30_Lz"
WITHIN = "interne_lineaire"
METHODS = (PRIMARY, REBUILT, WITHIN, "interne_circulaire", "origine_midi", "origine_demi_anneau",
           "anneaux_inverses_par_panneau", "sens_alterne", "huit_signes_30_lieux", "dix_avec_centre_et_case_vide")
WALKS = ("origine_midi", "origine_demi_anneau", "anneaux_inverses_par_panneau", "sens_alterne")
METHODS += tuple("ivtff_" + method for method in WALKS)
ZL = vocab.DATA / "ZL3b-n.txt"


def layout():
    result, hours, ring, n = {}, {}, None, 0
    for row in ZL.read_text().splitlines():
        m = vocab.LABEL.match(row)
        if m is None:
            continue
        page, num, mark, raw = m.groups()
        if mark == "@":
            n += 1
            ring = (page, n)
        assert ring[0] == page
        loc = page + "." + num
        result[loc] = ring
        stamp = re.match(r"<!(\d+):(\d+)>", raw)
        if stamp:
            h, minute = map(int, stamp.groups())
            hours[loc] = 60 * (h % 12) + minute
    return result, hours


def collect(rows, edge, rings):
    groups = {}
    for sign, labels in rows.items():
        batches = defaultdict(list)
        for loc, variants in labels:
            values = {next(iter(vocab.values(v, edge))) for v in variants}
            value = next(iter(values)) if len(values) == 1 and "?" not in values else None
            batches[rings[loc]].append((loc, value))
            if loc == "f72r2.19":
                batches[rings[loc]].append(("f72r2.19+figure_sans_nom", None))
        groups[sign] = list(batches.items())
    return groups


def pairs_in_sign(batches, method, d, hours):
    """Chaque couple non orienté est compté une fois, y compris au demi-tour."""
    bands = [list(row) for key, row in batches]
    use_ivtff = method == PRIMARY or method.startswith("ivtff_")
    if method.startswith("ivtff_"):
        method = method[len("ivtff_"):]
    if not use_ivtff and method != "dix_avec_centre_et_case_vide":
        bands = [[x for x in band if x[0] != "f70v2.33"] for band in bands]
        bands = [band for band in bands if band]
    if method in ("interne_lineaire", "interne_circulaire"):
        pairs = []
        for band in bands:
            n = len(band)
            if d >= n:
                continue
            if method == "interne_lineaire":
                pairs.extend((band[i], band[i+d]) for i in range(n-d))
            else:
                # For short rows outside the ring a circular closing edge would be invented.
                if band[0][0] in ("f72r2.1", "f73r.1", "f73v.1"):
                    pairs.extend((band[i], band[i+d]) for i in range(n-d))
                    continue
                for i, j in sorted({tuple(sorted((i, (i+d) % n))) for i in range(n)}):
                    pairs.append((band[i], band[j]))
        return pairs
    n = sum(map(len, bands))
    if n != 30 or ((use_ivtff or method == "huit_signes_30_lieux") and any(x[0].startswith("f72r2.") for b in bands for x in b)):
        return []
    if method == "dix_avec_centre_et_case_vide" or method == "huit_signes_30_lieux":
        method = PRIMARY
    if method == "anneaux_inverses_par_panneau":
        reordered = []
        for page in dict.fromkeys(b[0][0].split(".")[0] for b in bands):
            reordered.extend(reversed([b for b in bands if b[0][0].split(".")[0] == page]))
        bands = reordered
    transformed = []
    for i, b in enumerate(bands):
        if method == "origine_demi_anneau":
            cut = len(b) // 2
            b = b[cut:] + b[:cut]
        elif method == "origine_midi":
            cut = min(range(len(b)), key=lambda j: min(hours.get(b[j][0], 720), 720-hours[b[j][0]]) if b[j][0] in hours else 721)
            b = b[cut:] + b[:cut]
        elif method == "sens_alterne" and i % 2 == 1:
            b = b[::-1]
        transformed.extend(b)
    return [(transformed[i], transformed[j]) for i,j in sorted({tuple(sorted((i, (i+d) % n))) for i in range(n)})]


def summaries(groups, hours, want_profiles=True):
    items = [x for batches in groups.values() for _, band in batches for x in band]
    ids = {loc:i for i,(loc,_) in enumerate(items)}
    assert len(items)==len(ids)
    alphabet = sorted({v for _,v in items if v is not None})
    code = {v:i+1 for i,v in enumerate(alphabet)}
    original = np.array([code.get(v, 0) for _,v in items], dtype=np.uint16)
    perm = np.tile(original, (N,1))
    rng = np.random.default_rng(1450)
    for sign,batches in groups.items():
        for _,band in batches:
            fixed = [ids[loc] for loc,s in band if s is not None]
            if fixed:
                perm[:,fixed] = rng.permuted(perm[:,fixed],axis=1)
    tables, profiles, examples = {}, {}, []
    for method in METHODS:
        by_sign, perms = {}, {}
        for sign, batches in groups.items():
            by_sign[sign] = {}
            distances = range(1,16) if want_profiles and method in (PRIMARY,REBUILT,WITHIN) else (10,)
            for d in distances:
                pairs = pairs_in_sign(batches,method,d,hours)
                known = [(ids[a[0]],ids[b[0]]) for a,b in pairs if a[1] is not None and b[1] is not None]
                left, right = ([i for i,j in known], [j for i,j in known])
                hits = int((original[left]==original[right]).sum())
                stat = dict(accords=hits, lisibles=len(known), paires=len(pairs))
                by_sign[sign][d] = stat
                if d==10:
                    permuted=(perm[:,left] == perm[:,right]).sum(axis=1)
                    perms[sign]=permuted
                    if method in (PRIMARY, REBUILT, WITHIN) and want_profiles:
                        examples.extend((method,sign,a[0],b[0],a[1],b[1]) for a,b in pairs)
                    stat.update(p_mc=float((1+np.count_nonzero(permuted>=hits))/(1+N)), attendu=float(permuted.mean()))
        tables[method] = {}
        for category, signs in [('ensemble',SIGNS),('sept_premiers',HEAD),('trois_derniers',TAIL)]:
            obs=sum(by_sign[s][10]['accords'] for s in signs)
            draws=sum(perms[s] for s in signs)
            tail=int(np.count_nonzero(draws>=obs))
            tables[method][category]=dict(accords=obs,lisibles=sum(by_sign[s][10]['lisibles'] for s in signs),
                    paires=sum(by_sign[s][10]['paires'] for s in signs),attendu=float(draws.mean()),
                    quantiles_nuls=[int(q) for q in np.quantile(draws,[.025,.5,.975])],tirages_au_moins=tail,p_mc=(1+tail)/(1+N))
        if want_profiles and method in (PRIMARY,REBUILT,WITHIN):
            profiles[method]=by_sign
    return tables, profiles, examples


def roman(n, additive):
    tokens = [(10,'X'),(5,'V'),(1,'I')] if additive else [(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    output=''
    for digit,symbol in tokens:
        quotient,n=divmod(n,digit)
        output+=symbol*quotient
    return output


def controls(groups,hours):
    out={}
    for label,encode in [('decimal',str),('romain_additif',lambda i:roman(i,True)),('romain_soustractif',lambda i:roman(i,False))]:
        for edge in (0,-1):
            control={}
            for sign,batches in groups.items():
                count=0; fake=[]
                for key,band in batches:
                    row=[]
                    for loc,val in band:
                        count+=1
                        row.append((loc, encode(count)[edge] if val is not None else None))
                    fake.append((key,row))
                control[sign]=fake
            observed,_,_=summaries(control,hours,False)
            out[label+('_initial' if edge==0 else '_final')]={m:observed[m]['ensemble'] for m in (PRIMARY,REBUILT,WITHIN)}
    return out


def main():
    rings,hours=layout()
    output={"graine":1450,"permutations":N,"numpy":np.__version__,"sources":{},"editions":{},"temoins":{}}
    with (HERE/'PAIRES-10.tsv').open('w') as f:
        writer=csv.writer(f, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow(['edition','bord','parcours','signe','locus_A','locus_B','unite_A','unite_B'])
        for book,name in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]:
            path=vocab.DATA/name
            output['sources'][name]=hashlib.sha256(path.read_bytes()).hexdigest()
            runs={}
            for edge in ('final','initial'):
                rows=vocab.parse(path,False);groups=collect(rows,edge,rings)
                # Joining or separating spaces can alter whole-group equality.
                # The externalmost unit must survive both conventions identically before reuse.
                assert groups==collect(vocab.parse(path,True),edge,rings)
                tables,profiles,examples=summaries(groups,hours)
                runs[edge]=dict(resultats=tables,profils=profiles,espaces_joint_et_separe_identiques=True)
                for record in examples:
                    writer.writerow((book,edge,*record))
                if book=='ZL' and edge=='final':
                    output['temoins']=controls(groups,hours)
            output['editions'][book]=runs
    (HERE/'RESULTATS.json').write_text(json.dumps(output,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main()
