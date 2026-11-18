"""Apprendre deux mots, prédire le troisième, puis vérifier la fin de la ligne."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
SOURCES = RESEARCH / "2026-11-18-phrase-et-doublets/lecture"
sys.path.insert(0, str(SOURCES))
sys.path.insert(0, str(RESEARCH / "2026-11-18-carte-sept-etoiles/lecture"))
from corpus_sources import load_all
from essai import tables

B = ("ch","o","d","y")
C = ("ch","e","o","r")
SIGNS = ("ch","o","d","y","e","r")
LAST = {"i+i":tuple("qoaiin"),"II":("q","o","a","II","n")}


def corpus(xml):
    data = load_all(xml, SOURCES/"RIDGES.json")
    data["Simples"] = json.loads((RESEARCH/"2026-11-18-opcheor-paralleles/francais/corpus.json").read_text())
    return data


def save(name, data):
    content = json.dumps(data, ensure_ascii=False, separators=(",",":")).encode() + b"\n"
    output = HERE/name
    if output.suffix == ".gz":
        output.write_bytes(gzip.compress(content, mtime=0))
    else:
        output.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def windows(sections):
    for section, words in sections.items():
        for start in range(len(words)-5):
            yield section, start, words


def fit(first, second, width, marker=False):
    first_units, second_units = (B[1:], C[1:]) if marker else (B, C)
    n = len(first_units)
    if (not marker and first[0] != second[0]) or any(not n <= len(w) <= n*width for w in (first,second)):
        return
    for key in tables(first_units, first, width):
        for other in tables(second_units, second, width, key):
            if marker:
                other["ch"] = ""
            yield [other[s] for s in SIGNS]


def predict(sections, width, marker=False):
    pairs = sorted({(words[i+1], words[i+2]) for _, i, words in windows(sections)})
    output = []
    for first, second in pairs:
        keys = list(fit(first, second, width, marker))
        if keys:
            pred = sorted({k[0]+k[4]+k[3] for k in keys})
            ctrl = sorted({k[0]+k[3]+k[4] for k in keys})
            output.append(dict(seed=[first,second], keys=keys, predicted=pred, displaced=ctrl))
    return output


def confirm(sections, catalogue, width, rubrics):
    lookup = {tuple(record["seed"]):record for record in catalogue}
    counts = Counter()
    contexts = []
    simple = []
    for section, i, words in windows(sections):
        a,b,c,d,e,f = words[i:i+6]
        counts["windows"] += 1
        initials = b[0] == c[0] == d[0]
        counts["triple_initial"] += initials
        counts["repeat"] += (b==f)
        if initials and b==f:
            simple.append(dict(section=section, index=i, words=words[i:i+6]))
        record = lookup.get((b,c))
        if not record:
            continue
        counts["fit_two"] += 1
        counts["unique_prediction"] += (len(record["predicted"])==1)
        for which in ("predicted","displaced"):
            if d not in record[which]:
                continue
            counts[which+"_right"] += 1
            if which == "predicted":
                contexts.append(dict(section=section,index=i,words=words[i:i+6],
                    predictions=record[which], repeat=b==f, preceding_initial_possible=False,
                    fixed_left=False, macer_title=b in rubrics))
            for rep, extra, label in ((f,e,"repeat_at_6"),(e,f,"repeat_at_5")):
                if rep == b:
                    counts[which+"_"+label] += 1
            hits = defaultdict(set)
            for values in record["keys"]:
                key = dict(zip(SIGNS,values))
                mid = key["e"]+key["y"] if which == "predicted" else key["y"]+key["e"]
                if d != key["ch"]+mid:
                    continue
                if which=="predicted" and a.startswith(key["d"]):
                    contexts[-1]["preceding_initial_possible"] = True
                for left in tables(tuple("dal"),a,width,key):
                    hits["left"].add(tuple(sorted(left.items())))
                    for rep, extra, label in ((f,e,"repeat_at_6"),(e,f,"repeat_at_5")):
                        if rep != b:
                            continue
                        for units, signword in LAST.items():
                            for full in tables(signword,extra,width,left):
                                hits[label+"_"+units].add(tuple(sorted(full.items())))
            if hits["left"]:
                counts[which+"_with_left"] += 1
                if which=="predicted":
                    contexts[-1]["fixed_left"] = True
            for mode, keys in hits.items():
                if mode!="left":
                    counts[which+"_full_"+mode] += 1
                    if which=="predicted":
                        contexts[-1][mode] = [dict(k) for k in sorted(keys)]
    return dict(counts=counts, only_initials_and_repeat=simple, third_word_recovered=contexts)


def main():
    data = corpus(Path(sys.argv[2]))
    marker = len(sys.argv) == 4 and sys.argv[3] == "marque"
    tag = "-MARQUE" if marker else ""
    filename = "PREDICTIONS" + tag + ".json.gz"
    if sys.argv[1] == "predire":
        save(filename, {name:{str(w):predict(sections,w,marker) for w in (2,3)}
                        for name,sections in data.items()})
    elif sys.argv[1] == "verifier":
        stored = json.loads(gzip.decompress((HERE/filename).read_bytes()))
        rubrics = {title.lower() for title in data["Macer"]}
        save("VERIFICATION" + tag + ".json", {name:{w:confirm(data[name],rows,int(w),rubrics)
                                          for w,rows in bywidth.items()}
                                   for name,bywidth in stored.items()})
    else:
        raise ValueError("mode attendu : predire ou verifier")


if __name__ == "__main__":
    main()
