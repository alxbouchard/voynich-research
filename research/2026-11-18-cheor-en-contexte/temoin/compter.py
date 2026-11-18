"""Reproduire le classement des notices XIII–XX du Gart der Gesundheit."""
import json
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Coordonnées verticales du premier et du dernier bloc de texte courant,
# exprimées en pixels du fac-similé de Munich. Les rubriques sont exclues.
Y_BOUNDS = {
    37: (3370, 3755), 38: (660, 3580), 39: (3390, 3780), 40: (660, 3230),
    41: (3300, 3695), 42: (600, 2330), 43: (3345, 3740), 44: (640, 3310),
    45: (3365, 3760), 46: (680, 2645), 47: (3270, 3660), 48: (630, 1685),
    49: (3220, 3750), 50: (735, 3195), 51: (3340, 3735), 52: (710, 3015),
}


def normalize(s):
    s = unicodedata.normalize('NFC', s.lower().replace('ſ', 's'))
    return s.strip('.,;:!?/()[]–-“”«»·-')


def body(archive, page):
    root = ET.fromstring(archive.read(f'{page}.html'))
    y_min, y_max = Y_BOUNDS[page]
    groups = []
    for index, line in enumerate(root.findall('.//*[@class="ocr_line"]'), 1):
        x, y = (int(v) for v in line.attrib['title'].split()[1:3])
        if 500 <= x <= 3000 and y_min <= y <= y_max:
            words = [(int(w.attrib['title'].split()[1]), normalize(''.join(w.itertext())))
                     for w in line]
            groups.append((y, index, words))
    # Certains fragments d'une même ligne physique ont deux identifiants OCR.
    merged = []
    for y, index, words in sorted(groups):
        if merged and y - merged[-1][0] <= 32:
            merged[-1][2].extend(words)
        else:
            merged.append([y, index, list(words)])
    return [(f'{page}.{index}', [s for _, s in sorted(words) if any(c.isalpha() for c in s)])
            for _, index, words in merged]


def score(lines):
    order = {}
    locations = defaultdict(list)
    position = 0
    for label, words in lines:
        for word in words:
            position += 1
            order.setdefault(word, position)
            if not locations[word] or locations[word][-1] != label:
                locations[word].append(label)
    repeated = {w: {'premiere_position': order[w], 'lignes': loc}
                for w, loc in locations.items() if sum(c.isalpha() for c in w) >= 4 and len(loc) >= 3}
    eligible = [w for w in repeated if order[w] <= 12]
    return {'premiers_mots': [w for _, line in lines for w in line][:12],
            'prediction': next(iter(eligible), None), 'eligibles': eligible, 'repetes': repeated}


def main():
    with zipfile.ZipFile(HERE / 'ocr-37-52.zip') as archive:
        chapters = {}
        for chapter, first in enumerate(range(37, 52, 2), 13):
            rows = body(archive, first) + body(archive, first + 1)
            raw = score(rows)
            fixes = json.loads((HERE / 'corrections.json').read_text()).get(str(chapter), {})
            for label, words in rows:
                for original, replacement in fixes.get(label, {}).items():
                    if original not in words:
                        raise ValueError((label, original, words))
                    words[words.index(original)] = replacement
            chapters[chapter] = {'ocr': raw, 'avec_relectures': score(rows)}
        print(json.dumps(chapters, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
