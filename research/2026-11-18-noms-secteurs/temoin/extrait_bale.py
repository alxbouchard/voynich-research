"""Bâle O.IV.4. Dérive les sept fenêtres depuis une copie HTML de l'édition PAL."""
import argparse
import hashlib
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EDITION = "https://ptolemaeus.badw.de/ms/601/878/text/1"
# Ces notes décrivent la collation de D. Juste, pas un contrôle photographique de L.
LYON = {
    "Saturnus": {"notes": [2, 3, 4], "difference": "Les deux mots biffés dans B sont absents dans L. Le verbe au mot 16 est au singulier."},
    "Iupiter": {"notes": [8, 9], "difference": "L insère et avant le verbe au mot 16 de B."},
    "Mars": {"notes": [16, 17], "difference": "L omet hec signa et inverse l’ordre des deux signes ; leurs positions suivent le nom planétaire."},
    "Sol": {"notes": [26, 27, 28, 29], "difference": "Variante du nom de l’autorité au mot 3. La note 28 présente un lemme dont l’ordre diffère du texte imprimé en ligne pour B. La note 29 signale une lacune des deux témoins."},
    "Venus": {"notes": [38], "difference": "Aucune variante du texte courant dans les 16 premiers mots n’est donnée."},
    "Mercurius": {"notes": [43], "difference": "Aucune variante du texte courant dans les 16 premiers mots n’est donnée."},
    "Luna": {"notes": [54, 55], "difference": "Une variante touche le groupe verbal de trois mots au sujet du domicile, à partir du mot 9."},
}
HEAD = re.compile(r'<h3 id="(I\.[1-7])">(.*?)</h3>', re.S)
NOTES = re.compile(r'<span class="note">.*?</small></span>', re.S)
MARKUP = re.compile(r'<[^>]+>')


def clean(html):
    return unescape(MARKUP.sub("", NOTES.sub("", html)))


def extract(html):
    headings = list(HEAD.finditer(html))
    if len(headings) != 7:
        raise ValueError(f"Rubriques attendues : 7 ; trouvées : {len(headings)}")
    rows = []
    for i, h in enumerate(headings):
        locus, heading = h.groups()
        title = re.sub(r'〈\d+〉', '', clean(heading)).strip()
        stop = headings[i + 1].start() if i < 6 else html.index('</section>', h.end())
        body = clean(html[h.end():stop])
        body = re.sub(r'\[[^\]]*\]|〈[^〉]*〉', '', body)
        words = re.findall(r'[A-Za-z]+', body)[:16]
        if len(words) != 16 or sum(w.lower() == 'sub' for w in words) != 1:
            raise ValueError(f"Fenêtre ambiguë pour {locus}")
        sub = next(j for j, w in enumerate(words) if w.lower() == 'sub')
        folio = '11v' if i < 6 else '12r'
        rows.append({
            "locus": locus,
            "folio": folio,
            "transcription": EDITION + '#' + locus,
            "facsimile": f'https://ptolemaeus.badw.de/ms/601/878/{folio}',
            "nominative": title,
            "ablative": words[sub+1],
            "sub_position_1based": sub+1,
            "name_position_1based": sub+2,
            "window16": words,
            "lyon_heading_present": False,
            "lyon_formula_variant_reported": False,
            "lyon_opening_apparatus": LYON[title],
        })
    return rows


def encode(rows):
    # Le vocabulaire unique et les indices préservent les fenêtres sans réimprimer les notices.
    vocabulary = sorted({word for row in rows for word in row["window16"]}, key=lambda w: (w.casefold(), w))
    mapping = {word: i for i, word in enumerate(vocabulary)}
    encoded = []
    for row in rows:
        data = row.copy()
        words = data.pop("window16")
        data["window16_vocabulary_indices_0based"] = [mapping[word] for word in words]
        data["window16_sha256"] = hashlib.sha256(" ".join(words).encode("utf-8")).hexdigest()
        encoded.append(data)
    return {
        "witness": "Basel, Universitätsbibliothek, O.IV.4, f. 11v–12r",
        "copy_date": 1429,
        "transcription_credit": "David Juste, Ptolemaeus Arabus et Latinus, 18.08.2023 ; corpus de textes CC BY 4.0.",
        "source": EDITION,
        "window_length": 16,
        "vocabulary": vocabulary,
        "notices": encoded,
    }


def decode(data):
    for row in data['notices']:
        words = [data['vocabulary'][j] for j in row['window16_vocabulary_indices_0based']]
        if hashlib.sha256(" ".join(words).encode()).hexdigest() != row['window16_sha256']:
            raise ValueError(f"Empreinte de fenêtre incorrecte pour {row['locus']}")
        yield (row['locus'], row['nominative'], words)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", type=Path, help="source HTML PAL à utiliser pour reconstruire le JSON")
    ap.add_argument("--windows", action="store_true", help="afficher les fenêtres décodées")
    args = ap.parse_args()
    if args.html:
        data = encode(extract(args.html.read_text(encoding='utf-8')))
    else:
        data = json.loads((ROOT / "bale1429.json").read_text(encoding="utf-8"))
    if args.windows:
        for locus, title, words in decode(data):
            print(locus, title, " ".join(words), sep="\t")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
