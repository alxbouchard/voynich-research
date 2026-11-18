"""Extraire uniquement la colonne médiévale ou le corps des recettes."""
from hashlib import sha256
from pathlib import Path
import json
import re
import unicodedata
from lxml import html

HERE = Path(__file__).resolve().parent
MED = HERE.parents[1]/'2026-11-18-gestes-des-bains/francais/CORPUS.json'
URLS = {'viandier':'https://histolf.ulb.be/index.php/textes-gh/260-1450-viandier-taillevent-ms-vaticane-texte-et-traduction',
        'martino':'https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/martino2.htm'}


def norm(s):
    s = unicodedata.normalize('NFD',s.lower().replace('œ','oe').replace('æ','ae'))
    return ''.join(c for c in s if not unicodedata.combining(c))


def martino(path):
    doc = html.fromstring(path.read_bytes().decode('utf8'))
    container=doc.get_element_by_id('parent-fieldname-text')
    ref=None
    recipe=0
    for node in container:
        if node.tag=='h3':
            recipe+=1
            ref=f"recette {recipe}"
        elif ref and node.tag=='hr':
            break
        elif ref and node.tag=='p':
            clean=re.sub(r'<<\d+>>|\[[^][]*\]',' ',node.text_content())
            yield ref,clean


def viandier(path):
    doc=html.fromstring(path.read_bytes().decode('utf8'))
    tables=doc.xpath('//div[contains(@class,"article-details")]//table')
    assert len(tables)==1
    active=False
    for i,row in enumerate(tables[0].xpath('.//tr'),1):
        text=row.xpath('./td')[0].text_content()
        if "Cy aprés s'ensuit comment on fait les choses" in text:
            active=True
        elif active:
            yield f"entrée {i}",text


def load_book(records):
    result=[]
    for ref,text in records:
        for index,piece in enumerate(re.split(r'[.!?;:]',norm(text)),1):
            words=tuple(re.findall(r'[a-z]+',piece))
            if words: result.append((f"{ref} §{index}",words))
    return result


def sources(fr,it):
    records=json.loads(MED.read_bytes())
    return {'regime':load_book((r['ref'],r['texte']) for r in records),
            'viandier':load_book(viandier(fr)), 'martino':load_book(martino(it))}


def fingerprint(book):
    return sha256(json.dumps(book, ensure_ascii=False).encode()).hexdigest()
