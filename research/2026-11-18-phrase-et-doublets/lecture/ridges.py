"""Extraire les graphies historiques lisibles des six extraits RIDGES de 1482 et 1487."""
from collections import Counter
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import argparse
import json
import re
import unicodedata

HERE = Path(__file__).resolve().parent
URL = 'https://www.laudatio-repository.org/download/format/3/35/9.0'
INNER = 'excel/Excel_9-0.zip'
INNER_SHA = '9e3e18cb568eb439458eeda8236491a476c28ecb183a2159d4b45b3e0b78482c'


def write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')) + '\n')


def merged_ranges(sheet, columns):
    spans = {c:{} for c in columns}
    for merge in sheet.findall('./{*}mergeCells/{*}mergeCell'):
        sides = re.fullmatch(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', merge.get('ref'))
        if not sides or sides[1] != sides[3] or sides[1] not in spans:
            continue
        begin, end = int(sides[2]), int(sides[4])
        for row in range(begin,end+1):
            spans[sides[1]][row] = (begin,end)
    return spans


def extract(name, raw):
    with ZipFile(BytesIO(raw)) as wb:
        strings = [''.join(t.text or '' for t in s.findall('.//{*}t'))
                   for s in ET.fromstring(wb.read('xl/sharedStrings.xml'))]
        sheet = ET.fromstring(wb.read('xl/worksheets/sheet1.xml'))
    matrix = {}
    for row in sheet.findall('./{*}sheetData/{*}row'):
        values = {}
        for cell in row.findall('{*}c'):
            val = cell.findtext('{*}v','')
            if val:
                col = re.sub(r'\d+$','',cell.get('r'))
                values[col] = strings[int(val)] if cell.get('t')=='s' else val
        matrix[int(row.get('r'))] = values
    head = {value:col for col,value in matrix[1].items()}
    clean, title, uncertain = [head[key] for key in ('clean','head','unclear')]
    merged = merged_ranges(sheet, (clean,title,uncertain))

    def has_annotation(row,col):
        origin = merged[col].get(row,(row,row))[0]
        return bool(matrix.get(origin,{}).get(col))

    corpus, buffer, counts = {}, [], Counter()
    def flush():
        if buffer:
            first, last = buffer[0][0],buffer[-1][1]
            corpus[f'{name}:{first}-{last}'] = [word for _,_,word in buffer]
            buffer.clear()

    for row in range(2,max(matrix)+1):
        start, end = merged[clean].get(row, (row,row))
        if start != row:
            continue
        token = unicodedata.normalize('NFC',matrix.get(row,{}).get(clean,'')).lower()
        if any(has_annotation(i,title) or has_annotation(i,uncertain) for i in range(start,end+1)):
            counts['rubrique_ou_lecture_incertaine'] += 1
            flush()
        elif not token.isalpha():
            counts['vide_ponctuation_chiffre_ou_alternance'] += 1
            flush()
        else:
            buffer.append((row,end,token))
            counts['mots'] += 1
    flush()
    return corpus, dict(counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path, help=URL)
    path = parser.parse_args().archive
    with ZipFile(path) as outer:
        raw = outer.read(INNER)
    assert sha256(raw).hexdigest() == INNER_SHA
    corpus, stats = {}, {}
    with ZipFile(BytesIO(raw)) as inner:
        docs = sorted(n for n in inner.namelist() if re.fullmatch(r'Excel/RIDGES_Herbology/[^/]*(?:1482|1487)[^/]*\.xlsx',n))
        assert len(docs)==6
        for n in docs:
            name = Path(n).stem
            workbook = inner.read(n)
            chunks, counts = extract(name, workbook)
            corpus.update(chunks)
            stats[name] = counts | {'fragments':len(chunks), 'sha256_xlsx':sha256(workbook).hexdigest()}
    write(HERE/'RIDGES.json',corpus)
    write(HERE/'RIDGES-SOURCES.json',{'corpus':'RIDGES Herbology version 9.0','annee_publication':2020,
        'editeurs':['Anke Lüdeling','Carolin Odebrecht','Thomas Krause','Gohar Schnelle','Catharina Fischer'],
        'notice':'https://www.laudatio-repository.org/browse/corpus/PySSCnMB7CArCQ9CNKFY/corpora',
        'metadonnees':'https://www.laudatio-repository.org/api/elasticapi/v1/corpora/PySSCnMB7CArCQ9CNKFY/corpora',
        'manuel':'https://ridges.pages.cms.hu-berlin.de/corpus/dokumente/dokumente.html',
        'licence':'CC BY 3.0 Unported','lien_licence':'https://creativecommons.org/licenses/by/3.0/',
        'url_archive':URL,'zip_interieur':INNER,'sha256_zip_interieur':INNER_SHA,
        'transformations':'Première feuille du classeur. Couche orthographique clean, minuscules NFC. Les mots fusionnés occupent une ligne logique. Rupture aux rubriques, lectures incertaines, marques de paragraphe, ponctuations, alternatives et toute cellule non alphabétique. Chaque lieu donne le nom du classeur et les lignes Excel, première et dernière incluses.',
        'documents':stats})
    print(len(corpus), 'fragments', sum(map(len,corpus.values())),'mots')


if __name__=='__main__':
    main()
