"""Séparer les feuillets et livrer des contextes de prose masqués, à rang fixe."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re


LOCUS = re.compile(
    r"^<(?P<id>f(?P<folio>[0-9]+)[rv][a-zA-Z0-9]*\.[0-9]+),"
    r".(?P<type>[A-Z][a-z0-9])(?:;[^>])?>(?P<texte>.*)$"
)
EVA = re.compile(r"[a-z]+")
V101 = re.compile(r"[a-zA-Z0-9]+")
FEUILLETS_EXEMPLES = {1, 14, 18, 19, 23, 49, 84, 102}


def tirage(cle, modulo):
    return int.from_bytes(sha256(cle.encode("ascii")).digest(), "big") % modulo


def decouper(texte):
    texte = texte.strip().replace("<%>", "").replace("<$>", "")
    if "," in texte:
        return None, "espace_incertain"
    if "<->" in texte:
        return None, "interruption"
    if "<" in texte or ">" in texte:
        return None, "autre_balise"
    if texte.endswith("/"):
        # Ne jamais exploiter une ligne physique IVTFF incomplète.
        return None, "ligne_continuee"
    mots = texte.split(".")
    if "" in mots:
        return None, "champ_vide"
    return mots, None


def lire(path):
    brut = path.read_bytes()
    lignes = {}
    # Les symboles non ASCII restent non admissibles dans les deux alphabets.
    for ligne in brut.decode("latin-1").splitlines():
        match = LOCUS.match(ligne)
        if match is None or match["type"] != "P0":
            continue
        ident = match["id"]
        if ident in lignes:
            raise ValueError(f"Locus de prose en double dans {path.name} : {ident}")
        mots, refus = decouper(match["texte"])
        lignes[ident] = (int(match["folio"]), mots, refus)
    if not lignes:
        raise ValueError(f"Aucune ligne de prose reconnue dans {path.name}")
    return lignes, sha256(brut).hexdigest()


def simple(mot, alphabet):
    return mot if mot is not None and alphabet.fullmatch(mot) else None


def ecrire(path, objet):
    path.write_text(json.dumps(objet, ensure_ascii=True, sort_keys=True,
                               separators=(",", ":")) + "\n", encoding="utf-8")


def preparer(it_path, zl_path, gc_path, sortie):
    it, it_hash = lire(it_path)
    zl, zl_hash = lire(zl_path)
    gc, gc_hash = lire(gc_path)
    train, reserve = [], []
    reponses = {}
    exclus, etat_gc = Counter(), Counter()
    for ident in sorted(it.keys() | zl.keys()):
        folio = (it.get(ident) or zl[ident])[0]
        if folio in FEUILLETS_EXEMPLES:
            exclus["feuillet_exemple_deja_discute"] += 1
            continue
        if ident not in it or ident not in zl:
            exclus["absent_IT_P0" if ident not in it else "absent_ZL_P0"] += 1
            continue
        _, mots_it, refus_it = it[ident]
        _, mots_zl, refus_zl = zl[ident]
        if refus_it or refus_zl:
            motifs = [prefixe + raison for prefixe, raison in (("IT_", refus_it), ("ZL_", refus_zl)) if raison]
            exclus["+".join(motifs)] += 1
            continue
        if len(mots_it) != len(mots_zl):
            exclus["nombres_de_groupes_EVA_differents"] += 1
            continue

        _, mots_gc, raison_gc = gc.get(ident, (folio, None, "absent_GC_P0"))
        if not raison_gc and len(mots_gc) != len(mots_it):
            raison_gc = "nombre_de_groupes_different"
        etat_gc[raison_gc or "rang_aligne"] += 1
        if raison_gc:
            mots_gc = [None] * len(mots_it)

        en_reserve = tirage("voynich-suites-v1|folio|" + str(folio), 4) == 0
        decalage = tirage("voynich-suites-v1|ligne|" + ident, 5)
        mots, masques, corrige = [], [], {}
        for i, (a, b, c) in enumerate(zip(mots_it, mots_zl, mots_gc)):
            a, b, c = simple(a, EVA), simple(b, EVA), simple(c, V101)
            if en_reserve and i % 5 == decalage:
                masques.append(i)
                mots.append(None)
                corrige[str(i)] = [a, b, c]
            else:
                mots.append([a if a == b else None, c])
        ligne = {"id": ident, "folio": folio, "words": mots, "mask": masques}
        if en_reserve:
            reserve.append(ligne)
            reponses[ident] = corrige
        else:
            train.append(ligne)

    def taille(lignes):
        return {"lignes": len(lignes), "feuillets": len({l["folio"] for l in lignes}),
                "positions": sum(len(l["words"]) for l in lignes),
                "masques": sum(len(l["mask"]) for l in lignes)}

    bilan = {
        "sha256": {"IT": it_hash, "ZL": zl_hash, "GC": gc_hash},
        "lignes_prose_P0": {"IT": len(it), "ZL": len(zl), "GC": len(gc)},
        "union_locus_P0_IT_ZL": len(it.keys() | zl.keys()), "exclusions": exclus,
        "etat_GC_sur_lignes_retenues": etat_gc,
        "train": taille(train), "reserve": taille(reserve),
        "formes": {"EVA": "IT et ZL identiques, a-z seulement",
                   "GC": "a-z, A-Z, 0-9 seulement, sensible à la casse ; autres codes v101 indéterminés"},
    }
    sortie.mkdir(parents=True, exist_ok=True)
    for nom, donnees in (("train", train), ("reserve", reserve), ("reponses", reponses),
                         ("extraction", bilan)):
        ecrire(sortie / (nom + ".json"), donnees)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for nom in ("it", "zl", "gc", "sortie"):
        p.add_argument(nom, type=Path)
    args = p.parse_args()
    preparer(args.it, args.zl, args.gc, args.sortie)
