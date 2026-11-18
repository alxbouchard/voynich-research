"""Accès aux quatre lectures et à leur géométrie, communes aux épreuves."""
from importlib.util import module_from_spec, spec_from_file_location
import gzip
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# Le dépôt comprend deux modules intitulés mesurer.py avec des rôles différents.
spec = spec_from_file_location("bords_du_dessin", HERE.parent / "2026-11-18-finale-au-dessin/corpus/mesurer.py")
bords = module_from_spec(spec)
spec.loader.exec_module(bords)
MODES, WORD, aligned, corpus = bords.MODES, bords.WORD, bords.aligned, bords.corpus
parse, positions, segment = bords.parse, bords.positions, bords.segment


def save(name, data):
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (HERE / name).write_bytes(gzip.compress(raw, mtime=0) if name.endswith(".gz") else raw)


def read(name):
    data = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(data) if name.endswith(".gz") else data)


def metadata():
    sections = {}
    for line in (ROOT / "voynich_20261028/data/ZL3b-n.txt").read_text().splitlines():
        m = re.match(r"^<(f\w+)>", line)
        if m:
            sections[m[1]] = dict(re.findall(r"\$(\w)=(\w+)", line))
    return sections


def group(page, kind, sections):
    meta = sections.get(page, {})
    leaf = re.match(r"f(\d+)", page)
    n = int(leaf[1]) if leaf else None
    if kind == "Lf" and n not in (89,99):
        return "legendes"
    if kind != "P0":
        return None
    if meta.get("Q") == "T":
        return "dernier_cahier"
    if meta.get("I") == "B":
        return "bains"
    if meta.get("I") == "H" and n not in (34,55):
        return "apprentissage"
    return None


def split_word(word):
    # Le prédicteur ne reçoit ni le dernier signe ni le nombre de traits masqués.
    if not WORD.fullmatch(word):
        return None
    glyphs = segment(word)
    if glyphs[-3:] == ("i","i","n"):
        base, tail = glyphs[:-3], "iin"
    else:
        base, tail = glyphs[:-1], glyphs[-1]
    if base[-2:] != ("d","a"):
        return None
    return "".join(base), tail


def h_rows(raw):
    _, parts = parse(raw, "joints")
    for block,words in enumerate(parts,1):
        for idx,word in enumerate(words,1):
            yield block,idx,word,positions(block-1,len(parts),idx-1,len(words))


def label_rows(editions,loc):
    views = [parse(editions[ed][loc][3], cut) for ed,cut in MODES]
    if any(len(parts)!=1 for _,parts in views):
        return
    groups = [parts[0] for _,parts in views]
    for i,ws in enumerate(zip(*groups)):
        role = positions(0,1,i,len(groups[0]))
        if (all(w==ws[0] for w in ws) and WORD.fullmatch(ws[0]) and
                all(positions(0,1,i,len(v))==role for v in groups[1:])):
            yield 1, i+1, ws[0], role


def strict_rows(editions,loc,section,cov):
    page, kind, *_ = editions["H"][loc]
    if loc not in editions["ZL"] or editions["ZL"][loc][1] != kind:
        return
    if kind == "Lf":
        yield from label_rows(editions,loc)
        return
    if kind != "P0":
        return
    for row in aligned(editions,loc,page,section,page,cov):
        yield row["troncon"],row["rang_troncon_IT"],row["mot"],set(row["positions"])


def position_key(loc,block,idx):
    return f"{loc}/{block}/{idx}"
