"""Extraire Hm (PPEA, 2008) dans un espace de travail privé.

Source : https://piers.chass.ncsu.edu/texts/xml/HmWhole.xml
La ponctuation éditoriale sépare les unités. Le signe & reste une unité propre.
La substitution masque les lettres aux fonctions de prédiction. Ce n'est pas
un chiffrement à publier : le XML, les mots masqués et le corrigé restent locaux.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unicodedata
import xml.etree.ElementTree as ET

SOURCE_SHA256 = "fdc424ffc5ed72857e3ee1bd8fcf60e0a92da0cc8f0f2f685b4b1b53d81801e6"
IGNORED = {"note", "rdg", "corr", "reg", "del", "anchor", "handShift", "addSpan"}
INLINE = {"l", "hi", "foreign", "sic", "orig", "lem", "add"}

class UnusableVerse(ValueError):
    """Un passage ambigu invalide le vers entier, sans recoller ses voisins."""

def pieces(node):
    tag = node.tag
    if tag in IGNORED:
        return
    if tag == "app":
        readings = [child for child in node.findall("lem") if "Hm" in child.get("wit", "").split()]
        if len(readings) != 1:
            raise UnusableVerse("apparat Hm ambigu")
        yield from pieces(readings[0])
        return
    if tag == "expan":
        value = node.text or ""
        if node.get("abbr") or len(node) or not value.isalpha():
            raise UnusableVerse("expansion de remplacement, composée ou incertaine")
        yield value, False
        return
    if tag == "seg" and node.get("type") == "shadowHyphen":
        yield " ", True
        return
    if tag not in INLINE:
        # Inclut lacunes, dégâts, sauts physiques et éléments inattendus.
        raise UnusableVerse("balisage exclu " + tag)
    if tag == "add" and node.get("place") not in {"inline", "supralinear"}:
        raise UnusableVerse("addition hors ligne")
    yield node.text or "", True
    for child in node:
        yield from pieces(child)
        yield child.tail or "", True

def units(node):
    result = []
    visible, full = [], []
    def flush():
        if full:
            if not visible:
                raise UnusableVerse("mot sans lettre visible")
            result.append(("".join(visible), "".join(full)))
            visible.clear()
            full.clear()
    for piece, supplied_on_page in pieces(node):
        for char in unicodedata.normalize("NFC", piece).lower():
            if char.isalpha():
                full.append(char)
                if supplied_on_page:
                    visible.append(char)
            elif char.isdecimal():
                raise UnusableVerse("chiffre dans le vers")
            else:
                flush()
                if char == "&":
                    result.append(("&", "&"))
    flush()
    return result

class Alphabet:
    def __init__(self):
        self.used = {}
        self.table = {}

    def word(self, letters):
        for char in letters:
            if char in self.table:
                continue
            digest = hashlib.sha256(("Hm opaque v1|" + char).encode()).digest()
            code = chr(0xF0000 + int.from_bytes(digest[:4], "big") % 0xFFFE)
            if code in self.used:
                raise ValueError("Collision de la substitution de signes")
            self.used[code] = char
            self.table[char] = code
        return "".join(self.table[char] for char in letters)

def write(folder, name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

def extract(source, out, train_only):
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Empreinte du XML différente de celle de l'édition figée")
    alphabet = Alphabet()
    train, reserve, answers = [], [], {}
    dropped = {"train": Counter(), "reserve": Counter()}
    identifiers = set()
    for _, verse in ET.iterparse(source, events=("end",)):
        if verse.tag != "l":
            continue
        identifier = verse.get("id", "")
        parts = identifier.split(".")
        if len(parts) < 3 or parts[0] != "Hm":
            raise ValueError("Identifiant de vers inattendu")
        passus = 0 if parts[1] == "P" else int(parts[1])
        if train_only and passus >= 10:
            break
        if 10 <= passus <= 12 or not 0 <= passus <= 20:
            verse.clear()
            continue
        if identifier in identifiers:
            raise ValueError("Identifiant de vers dupliqué")
        identifiers.add(identifier)
        group = "train" if passus < 10 else "reserve"
        try:
            words = units(verse)
            if not words:
                raise UnusableVerse("vers vide")
        except UnusableVerse as error:
            dropped[group][str(error)] += 1
            verse.clear()
            continue
        item = {"id": identifier, "passus": passus, "words": [alphabet.word(short) for short, _ in words]}
        if group == "train":
            train.append(item)
        else:
            reserve.append(item)
            answers[identifier] = [alphabet.word(long) for _, long in words]
        verse.clear()
    out.mkdir(mode=0o700, parents=True, exist_ok=True)
    write(out, "train.json", train)
    if not train_only:
        write(out, "reserve.json", reserve)
        write(out, "corrige.json", answers)
    write(out, "extraction.json", {"source_sha256": SOURCE_SHA256, "vers_retenus": {"train": len(train), "reserve": len(reserve)}, "exclus": dropped})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("sortie", type=Path)
    parser.add_argument("--train-only", action="store_true", help="arrête la lecture des vers au début du passus 10")
    args = parser.parse_args()
    extract(args.source, args.sortie, args.train_only)
