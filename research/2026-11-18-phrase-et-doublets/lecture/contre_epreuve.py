"""Retester les suites avec des groupes capturants et des rappels dans le moteur re."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

from corpus_sources import HERE, load_all

# Les majuscules P et S sont ici deux signes, les composés EVA ch et sh.
FORMS = ("opPeor", "opPeol", "Sody", "Soldy")
MODES = ("fixe", "l_contextuel", "position")
SEP = "\x1f"


def positions(mode):
    words = []
    for form in FORMS:
        row = []
        for i, glyph in enumerate(form):
            suffix = "" if mode != "position" else ("I" if i == 0 else "F" if i == len(form)-1 else "M")
            if mode == "l_contextuel" and glyph == "l" and i < len(form)-1:
                suffix = "M"
            row.append((glyph, suffix))
        words.append(row)
    return words


def alternatives(words, mute):
    choices = {frozenset()}
    cells = {cell for word in words for cell in word}
    if mute:
        for letter, suffix in cells:
            choices.add(frozenset({(letter, suffix)}))
            choices.add(frozenset(c for c in cells if c[0] == letter))
    return sorted(choices, key=lambda s: sorted(s))


def patterns(mode, mute, length):
    words = positions(mode)
    variants = set()
    for silent in alternatives(words, mute):
        seen = set()
        parts = []
        for w in words[:length]:
            fragments = []
            for cell in w:
                if cell in silent:
                    continue
                name = "g" + "".join(cell)
                if name in seen:
                    fragments.append("(?P=" + name + ")")
                else:
                    fragments.append("(?P<" + name + ">[^" + SEP + "]{1,3})")
                    seen.add(name)
            parts.append("".join(fragments))
        variants.add(SEP.join(parts))
    return [re.compile(p) for p in sorted(variants)]


def fits(patterns_, phrase):
    return any(p.fullmatch(phrase) for p in patterns_)


def known_answer():
    abc = SEP.join(("herba", "herbae", "tam"))
    fourth = ("herba","herbae","tam","teram","terram")
    out = {}
    for mode in MODES:
        for mute in (False, True):
            rule = patterns(mode, mute, 4)
            out[key(mode,mute)] = [w for w in fourth if fits(rule, abc + SEP + w)]
    assert out["l_contextuel-1"] == ["teram","terram"]
    assert not out["fixe-1"] and not out["l_contextuel-0"]
    return out


def key(mode, mute):
    return f"{mode}-{int(mute)}"


def evaluate(corpus, sizes, pred, readback):
    totals = {}
    expected_windows = sum(max(0,len(row)-3) for row in corpus.values())
    for mode in MODES:
        for mute in (False, True):
            model = key(mode, mute)
            pair, triple, quad = [patterns(mode, mute, n) for n in (2,3,4)]
            windows = 0
            n_pair = 0
            triplets, solutions = [], []
            for chapter, row in corpus.items():
                for i, (a,b,c,d) in enumerate(zip(row,row[1:],row[2:],row[3:]),1):
                    windows += 1
                    prefix = SEP.join((a,b))
                    # The first pair is tested at every position, without a shared-prefix filter.
                    if not fits(pair,prefix):
                        continue
                    n_pair += 1
                    prefix += SEP + c
                    if fits(triple, prefix):
                        triplets.append([chapter,i])
                        if fits(quad,prefix + SEP + d):
                            solutions.append([chapter,i])
            exp_triples = sorted([r["segment"], r["rang"]] for r in pred[model]["triplets"])
            exp_solutions = sorted([r["segment"],r["rang"]] for r in readback[model]["sites"]
                                   if r["comparaison"]["attendu"]["trouve"])
            assert sizes["segments"] == len(corpus)
            assert expected_windows == windows == pred[model]["fenetres"]
            assert n_pair == pred[model]["paires_ajustees"], (model,n_pair,pred[model]["paires_ajustees"])
            assert sorted(triplets) == exp_triples, (model,triplets,exp_triples)
            assert sorted(solutions) == exp_solutions, (model,solutions,exp_solutions)
            totals[model] = {"fenetres": windows, "paires": n_pair, "triplets": len(triplets),
                             "quadruplets": len(solutions), "loci_quadruplets": sorted(solutions)}
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml",type=Path)
    parser.add_argument("--ridges",type=Path,default=HERE/"RIDGES.json")
    args = parser.parse_args()
    corpora = load_all(args.xml,args.ridges)
    pred_file, ver_file = HERE/"PREDICTIONS.json", HERE/"VERIFICATION.json"
    pred, ver = [json.loads(path.read_bytes()) for path in (pred_file,ver_file)]
    assert set(corpora) == set(pred["essais"]) == set(ver)
    output = {"controle_construit_quatrieme_dans_le_lexique": known_answer(), "corpus": {},
              "predictions_sha256": sha256(pred_file.read_bytes()).hexdigest(),
              "verification_sha256": sha256(ver_file.read_bytes()).hexdigest()}
    for name, body in corpora.items():
        output["corpus"][name] = evaluate(body, pred["sources"][name], pred["essais"][name], ver[name])
        print(name, {k: (v["triplets"],v["quadruplets"]) for k,v in output["corpus"][name].items()}, flush=True)
    (HERE/"CONTRE-EPREUVE.json").write_text(json.dumps(output, indent=2,sort_keys=True,ensure_ascii=False)+"\n")


if __name__ == "__main__":
    main()
