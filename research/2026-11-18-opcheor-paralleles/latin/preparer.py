"""Reprend les 77 notices du Macer et conserve leurs frontières et repères de vers."""
import csv
import gzip
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / '2026-11-18-noms-secteurs' / 'herbier'))
from mesurer import HEADING, MACER, MACER_HASH, checked, macer_source, words


def main():
    notices = macer_source()
    corpus = {title: body for title, body in notices}
    assert len(corpus) == len(notices) == 77
    assert all(word.isascii() and word.isalpha() for body in corpus.values() for word in body)

    source = checked(gzip.decompress(MACER.read_bytes()), MACER_HASH)
    headers = list(HEADING.finditer(source))
    line_number = 0
    lines = []
    discrepant_markers = {}
    for i, (header, (title, tokens)) in enumerate(zip(headers, notices)):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(source)
        poem = re.fullmatch(r'\s*<poem>\s*(.*?)\s*</poem>\s*', source[header.end():end], re.S)
        assert poem and header[2] == title
        first_word = 1
        for line in poem[1].splitlines():
            line_number += 1
            markers = re.findall(r'\{\{Versus\|(\d+)\}\}', line)
            assert len(markers) == (1 if line_number % 5 == 0 else 0)
            marker = markers[0] if markers else ''
            if marker and int(marker) != line_number:
                discrepant_markers[line_number] = int(marker)
            clean = re.sub(r'\{\{Versus\|\d+\}\}', '', line).strip()
            row_words = words(clean)
            last_word = first_word + len(row_words) - 1
            assert row_words and row_words == tokens[first_word-1:last_word]
            lines.append((i + 1, title, line_number, marker, first_word, last_word, clean))
            first_word = last_word + 1
        assert first_word - 1 == len(tokens)
    assert discrepant_markers == {55: 65, 1125: 1126, 1570: 1510, 1575: 1515, 1750: 1150}
    assert line_number == 2269

    with (HERE / 'vers.tsv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('notice', 'titre', 'rang_du_vers', 'numero_dans_la_source', 'premier_mot_notice', 'dernier_mot_notice', 'texte_edite'))
        writer.writerows(lines)
    (HERE / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(len(corpus), 'notices,', len(lines), 'vers,', sum(map(len, corpus.values())), 'mots')


if __name__ == '__main__':
    main()
