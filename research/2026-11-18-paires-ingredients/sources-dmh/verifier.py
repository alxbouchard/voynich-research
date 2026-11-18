"""Check only the two published claims frozen in CLAIMS.md, using public IVTFF data."""
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "voynich_phase14" / "data"
TARGETS = {
    "f105r.6": ["par", "arody"],
    "f105v.29": ["karody"],
    "f112v.39": ["teodarody"],
    "f114v.37": ["tar", "arody"],
    "f115v.13": ["pchdarody"],
    "f116r.19": ["qotar", "ar", "arody"],
}
SOURCE = ["otar", "arody"]


def segment(body, split_commas):
    body = body.replace("<->", ".").replace("<~>", ".")
    body = re.sub(r"<[^>]*>", "", body)
    body = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", body)
    body = body.replace("{", "").replace("}", "")
    body = body.replace(",", "." if split_commas else "")
    return [word for word in body.split(".") if word]


def positions(words, seq):
    return [index + 1 for index in range(len(words) - len(seq) + 1)
            if words[index:index + len(seq)] == seq]


def audit(filename, split_commas):
    current = []
    source = {}
    target = {}
    source_repeats = {}
    source_repeats_in_paragraph = {}
    all_words = Counter()
    page = ""
    in_q20 = False
    for line in (DATA / filename).read_text(encoding="latin-1").splitlines():
        header = re.match(r"<(f\w+)>", line)
        if header:
            assert not current
            page = header[1]
            in_q20 = "$Q=T" in line and "$I=S" in line
            continue
        match = re.match(r"<(f\w+\.\d+),.(\w\w)>\s*(.*)", line)
        if not match:
            continue
        locus, kind, body = match.groups()
        if page == "f88v" and kind in ("Lc", "Lf"):
            source[locus] = segment(body, split_commas)
        if not in_q20 or not kind.startswith("P"):
            continue
        words = segment(body, split_commas)
        all_words.update(words)
        if (found := positions(words, SOURCE)):
            source_repeats[locus] = found
        assert body.startswith("<%>") == (not current)
        current.append((locus, words))
        if body.endswith("<$>"):
            paragraph_words = [word for _, w in current for word in w]
            if (found := positions(paragraph_words, SOURCE)):
                source_repeats_in_paragraph[current[0][0]] = found
            for index, (key, row_words) in enumerate(current, 1):
                if key in TARGETS:
                    target[key] = {"attendu": TARGETS[key], "positions_segment": positions(row_words, TARGETS[key]),
                                   "segments_ligne": len(row_words), "ligne_du_paragraphe": index,
                                   "lignes_du_paragraphe": len(current), "premier_segment": row_words[0]}
            current = []
    assert not current and target.keys() == TARGETS.keys()
    labels = [(key, word) for key, words in source.items() for word in words]
    matches = [[key, word, all_words[word]] for key, word in labels if all_words[word]]
    return {"source_f88v_4": source["f88v.4"], "cibles_publiees": target,
            "paire_source_occurrences_dans_ligne": source_repeats,
            "paire_source_occurrences_dans_paragraphe": source_repeats_in_paragraph,
            "nombre_etiquettes": len(source), "nombre_segments_etiquettes": len(labels),
            "segments_repris": len(matches), "reprises_et_frequences": matches}


def main():
    output = {}
    for edition, filename in {"H": "IT2a-n.txt", "ZL": "ZL3b-n.txt"}.items():
        output[edition] = {code: audit(filename, split_commas)
                           for code, split_commas in (("virgules_coupees", True), ("virgules_jointes", False))}
    (HERE / "verification.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
