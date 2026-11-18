"""Compter les lectures de la racine et imprimer le concordancier OCR avec coordonnées."""
from collections import Counter
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'lectures.json').read_text())
with ZipFile(HERE / 'ocr-53-65.zip') as source:
    pages = {page: ET.fromstring(source.read(f'{page}.html')).findall('.//*[@class="ocr_line"]')
             for page in range(53, 66)}

report = {}
for chap in data['chapters']:
    examples = [r for r in data['root_candidates'] if r['chapter'] == int(chap)]
    counts = Counter(r['role'] for r in examples)
    report[chap] = dict(racine_longue=len(examples) - counts['ingredient_ambigu'] - counts['forme_courte'],
                        racine_courte=counts['forme_courte'], compose_ambigu=counts['ingredient_ambigu'],
                        von_nom=counts['von_nom'], von_article_nom=counts['von_article_nom'],
                        nom_racine=counts['nom_racine'], demonstratif=counts['demonstratif'],
                        autre_plante=counts['autre_plante'])

def concordance(r):
    line = pages[r['page']][r['line'] - 1]
    box = list(map(int, line.attrib['title'].split(';')[0].split()[1:]))
    return dict(r, rectangle_ocr=box, texte_ocr=' '.join(''.join(w.itertext()) for w in line))

print(json.dumps(dict(par_notice=report, occurrences=[concordance(r) for r in data['root_candidates']],
                      jus=[concordance(r) for r in data['juice_examples']]), ensure_ascii=False, indent=2))
