"""Contrôles sur une phrase créée et sur un passage authentique chiffré."""
from collections import Counter
from hashlib import sha256
import json
from random import Random
from string import ascii_lowercase, ascii_uppercase

from phrase import confirm, predict, save
from corpus_sources import LATIN


def project(units, key):
    return "".join(key[unit] for unit in units)


def synthetic():
    key = dict(ch="b", o="a", d="i", y="l", e="e", r="t", a="r", l="e",
               q="m", i="o", n="n")
    out = []
    for mark in (False, True):
        truth = dict(key, ch="" if mark else "b")
        seed1 = project(("ch", "o", "d", "y"), truth)
        seed2 = project(("ch", "e", "o", "r"), truth)
        third = project(("ch", "e", "y"), truth)
        fifth = project(tuple("qoaiin"), truth)
        words = [project(tuple("dal"), truth), seed1, seed2, third, fifth, seed1]
        pristine = {"six": words}
        for width in (2, 3):
            predictions = predict(pristine, width, mark)
            assert len(predictions) == 1 and predictions[0]["predicted"] == [third]
            assert third not in predictions[0]["displaced"]
            cases = {
                "intact": words,
                "dernier_corrompu": [*words[:-1], "faux"],
                "II_distinct": [*words[:4], "maroxn", seed1],
                "retour_deplace": [*words[:4], seed1, words[4]],
            }
            for case, row in cases.items():
                found = confirm({"six": row}, predictions, width, set())
                n = found["counts"]
                assert n["predicted_right"] == n["predicted_with_left"] == 1
                assert not n["displaced_right"]
                assert bool(n["predicted_repeat_at_6"]) == (case in {"intact", "II_distinct"})
                assert bool(n["predicted_full_repeat_at_6_i+i"]) == (case == "intact")
                assert bool(n["predicted_full_repeat_at_6_II"]) == (case in {"intact", "II_distinct"})
                assert bool(n["predicted_full_repeat_at_5_i+i"]) == (case == "retour_deplace")
                if case == "intact":
                    full = found["third_word_recovered"][0]["repeat_at_6_i+i"]
                    assert truth in full
                out.append(dict(marque=mark, largeur=width, cas=case, mots=row,
                                catalogue=predictions, verification=found))
    return out


def first_seed(sections):
    for title, row in sections.items():
        for i in range(len(row)-2):
            x, y, z = row[i:i+3]
            letters = set(z)
            if (len(z) >= 3 and z not in (x, y) and letters <= set(x+y) and
                    letters.intersection(x) and letters.intersection(y)):
                return title, i
    raise ValueError("Le répertoire ne contient aucun triplet admissible")


def key_for_pair(cipher, plain):
    key = {}
    reverse = {}
    for coded, decoded in zip(cipher, plain):
        if len(coded) != len(decoded):
            return None
        for x, y in zip(coded, decoded):
            if key.get(x, y) != y or reverse.get(y, x) != x:
                return None
            key[x] = y
            reverse[y] = x
    return key


def candidates(sections, cipher):
    found = []
    windows = 0
    for title, row in sections.items():
        for i in range(len(row)-2):
            windows += 1
            key = key_for_pair(cipher[:2], row[i:i+2])
            if key is not None:
                # Le voisin clair du corpus ne participe à aucune de ces lectures.
                third = project(cipher[2], key)
                found.append(dict(notice=title, index=i, amorce=row[i:i+2], cle=key, predit=third))
    return windows, found


def signature(words):
    ids = {}
    return tuple(tuple(ids.setdefault(x, len(ids)) for x in w) for w in words)


def macer():
    assert sha256(LATIN.read_bytes()).hexdigest() == "c251598bbab3f9f93de40a72d4e039c17f52ce079dd95e86c7322f9a2283893b"
    sections = json.loads(LATIN.read_text())
    title, i = first_seed(sections)
    row = sections[title]
    letters = list(ascii_uppercase)
    seed = 89092
    Random(seed).shuffle(letters)
    encode = str.maketrans(ascii_lowercase, "".join(letters))
    coded = [w.translate(encode) for w in row]
    cipher = coded[i:i+3]
    windows, before = candidates(sections, cipher)
    correct = (title, i)
    assert correct in [(r["notice"], r["index"]) for r in before]
    after = []
    for r in before:
        plain = sections[r["notice"]][r["index"]+2]
        r["observé"] = plain
        r["conforme"] = plain == r["predit"]
        if r["conforme"]:
            after.append(r)
    real = next(r for r in after if (r["notice"], r["index"]) == correct)
    for size, matches in [(2, before), (3, after)]:
        # Calcul indépendant par les motifs d'égalité, en tenant les espaces ensemble.
        sig = signature(cipher[:size])
        recalc = {(t,j) for t, words in sections.items() for j in range(len(words)-2)
                  if signature(words[j:j+size]) == sig}
        assert recalc == {(r["notice"],r["index"]) for r in matches}
    # Le mot suivant illustre la couverture à clé figée. Il est hors des trois mots.
    mask = "".join(real["cle"].get(ch, "?") for ch in coded[i+3])
    reversed_cipher = list(cipher[:2]) + [cipher[2][::-1]]
    _, reversed_options = candidates(sections, reversed_cipher)
    reverse_hits = [v for v in reversed_options if v["predit"] == sections[v["notice"]][v["index"]+2]]
    assert len(reversed_options) == len(before) and not reverse_hits
    return dict(notice=title, rang_initial=i+1, chiffre=cipher, vrai_triplet=row[i:i+3],
                controle_inversion=dict(chiffre=reversed_cipher, propositions=[v["predit"] for v in reversed_options],
                    concordances=len(reverse_hits)),
                rng=seed, positions_interrogees=windows, positions_avant=len(before),
                positions_apres=len(after), lectures_distinctes_avant=dict(Counter(r["predit"] for r in before)),
                candidats=before, paires_apres=[(r["notice"],r["index"]+1) for r in after],
                cle_partielle=real["cle"], lettres_inconnues=26-len(real["cle"]),
                controle_mot_suivant=dict(chiffre=coded[i+3],cle_seule=mask, vrai=row[i+3]),
                sha256_notice_chiffree=sha256(" ".join(coded).encode()).hexdigest())


if __name__ == "__main__":
    save("ETALON.json", dict(synthetique=synthetic(), macer=macer()))
