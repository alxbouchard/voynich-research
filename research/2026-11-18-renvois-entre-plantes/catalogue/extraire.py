"""Extraire les renvois des deux notices sans lire les mots du manuscrit."""
import argparse
import json
import re
from collections import Counter, defaultdict
from hashlib import sha256
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
PAGE = r'f\d+[rv]\d*'
BLOCK = re.compile(r'<TH CLASS="Ph" ID="(' + PAGE + r')".*?</TH>(.*?)(?=<TH CLASS="[PF]h" ID=|</BODY>)', re.S | re.I)
ROW = re.compile(r'<i>(f\d+[rv]\d*), row (\d+)</i>\s*</p>\s*<table [^>]*>(.*?)</table>', re.S | re.I)
PARAGRAPH = re.compile(r'<p(?:\s+[^>]*)?>(.*?)</p>', re.S | re.I)
LINK = re.compile(r'<a\s+href="([^"]+)">(' + PAGE + r')</a>', re.I)


def clean(html):
    return " ".join(unescape(re.sub(r'<[^>]+>', ' ', html)).split())


def extract(paths):
    positions = {}
    sources, panels, mentions, other = {}, {}, [], []
    for quire, path in zip((15, 19), paths):
        base = f'https://www.voynich.nu/q{quire}/index.html'
        raw = path.read_bytes()
        sources[quire] = {"url": base, "sha256": sha256(raw).hexdigest()}
        for page, block in BLOCK.findall(raw.decode('utf-8')):
            rows = ROW.findall(block)
            if rows:
                n = re.search(r'(\d+) lines? of standard text', clean(block), re.I)
                assert n
                panels[page] = {"cahier": quire, "lignes_standard_catalogue": int(n[1]), "url": base + '#' + page}
            for row_page, row, table in rows:
                assert page == row_page
                for rank, number in enumerate(re.findall(r'<b>(\d+)</b>', table, re.I), 1):
                    assert int(number) not in positions
                    positions[int(number)] = (page, int(row), rank, quire)
            for para in PARAGRAPH.findall(block):
                links = LINK.findall(para)
                if not links:
                    continue
                start = 0
                for match in LINK.finditer(para):
                    phrase = clean(para[start:match.start()])
                    start = match.end()
                    url, target = match.groups()
                    if m := re.search(r'Fragment (\d+) (appears to be the same plant|shows some similarity)', phrase):
                        number = int(m[1])
                        category = 'meme_plante' if m[2].startswith('appears') else 'ressemblance'
                    elif re.search(r'and with the plant on$', phrase):
                        assert number == 150 and page == 'f101r'
                        category = 'ressemblance'
                    elif m := re.search(r'Item (\d+): Th.Petersen', phrase):
                        number = int(m[1])
                        category = 'petersen'
                    elif m := re.search(r'This plant shows some similarity with plant fragment #(\d+)', phrase):
                        mentions.append((int(m[1]), page, target, 'reciproque', base+'#'+page, urljoin(base,url)))
                        continue
                    else:
                        other.append((page,target))
                        continue
                    mentions.append((number,target,page,category,base+'#'+page,urljoin(base,url)))

    grouped = defaultdict(list)
    for number,target,notice,category,source,url in mentions:
        grouped[number,target].append(dict(classe=category,notice=notice,source=source,lien_imprime=url))
    out = []
    for (number,target), entries in sorted(grouped.items()):
        page,row,rank,q = positions[number]
        direct = [m for m in entries if m['classe']!='reciproque']
        assert direct
        category = next(m['classe'] for m in direct if m['classe']!='petersen') if any(m['classe']!='petersen' for m in direct) else 'petersen'
        authoritative = next(m for m in direct if m['classe']==category)
        # Deux chemins défectueux dans la notice. La donnée utilisée est le folio affiché.
        corrected = {'f40v':'https://www.voynich.nu/q05/index.html#f40v',
                     'f33r':'https://www.voynich.nu/q05/index.html#f33r'}
        out.append(dict(fragment=number,panneau=page,plante=target,cahier=q,classe=category,
                        rangee=row,rang_dans_rangee=rank,recensements=entries,
                        source=panels[page]["url"],
                        cible_source=corrected.get(target,authoritative['lien_imprime'])))
    assert sorted(other)==sorted([('f90r1','f3v'),('f102r2','f18v'),('f102r2','f23r')]), other
    assert len(out)==35 and Counter(x['classe'] for x in out)=={'meme_plante':9,'ressemblance':22,'petersen':4}
    return dict(sources=sources,panneaux=panels,liens=out,
                incidents=[
                    {"numero":31,"notice":"f89r2","panneau_physique":"f89r1","effet":"doublon de f33r"},
                    {"numero":39,"notice":"f89r2","effet":"numéro sauté, aucun dessin"},
                    {"numero":59,"notice":"f89v2","effet":"seconde ligne d’étiquette réattribuée au recto par transparence en 2025 ; aucun renvoi"},
                    {"numero":228,"notice":"f102v2","effet":"numéro sauté, aucun dessin"},
                    {"numero":30,"notice":"f89r1","effet":"identification de chardon proposée, sans renvoi à une grande plante du manuscrit"},
                    {"notice":"f90r1","cible":"f3v","effet":"deux grandes plantes, aucun fragment numéroté"},
                    {"notice":"f102r2","numeros":[212,213],"effet":"voisinage répété sur un même bifeuillet, déjà compté sous chaque numéro"},
                    {"notice":"f101r","effet":"les deux panneaux historiques du dépliant forment une seule face de texte"},
                    {"notice":"f101v","effet":"les deux panneaux historiques du dépliant forment une seule face de texte ; une ligne centrée"}])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('q15', type=Path)
    p.add_argument('q19', type=Path)
    args=p.parse_args()
    result=extract([args.q15,args.q19])
    (HERE/'RENVOIS.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')
