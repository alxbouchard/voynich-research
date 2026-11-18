"""Quantify the four possible joint readings of two localized inscriptions."""
import itertools
import json

from compter import HERE, KNOWN, TARGETS, condition, exact_randomization, sources, summary


def run():
    faces, _ = sources()
    panels, _, corpus = condition(faces, "accord", False)
    comparable = {face for face, counts in panels.items() if counts["readable_mix"]}
    results = {}
    for leaf, jar in itertools.product(("otol", "okol"), ("otold", "otoldy")):
        rows = dict(corpus)
        for locus, word in (("f102v2.7", leaf), ("f89r2.9", jar)):
            face, folio, category, words = rows[locus]
            assert face in comparable and words is None
            rows[locus] = face, folio, category, [word]
        trials = {}
        for subset in ("toutes", "hors_origine"):
            read = {loc: row for loc, row in rows.items()
                    if row[0] in comparable and row[3] and (subset == "toutes" or row[1] not in KNOWN)}
            trials[subset] = {
                "effectifs": {cat: summary({loc: row for loc, row in read.items() if row[2] == cat})
                             for cat in ("Lf", "Lc")},
                "par_face": exact_randomization(read, set(TARGETS), False),
                "par_face_et_longueur": exact_randomization(read, set(TARGETS), True),
            }
        results[f"{leaf}/{jar}"] = trials
    return results


if __name__ == "__main__":
    (HERE / "variantes_photo.json").write_text(json.dumps(run(), ensure_ascii=False, indent=2) + "\n")
