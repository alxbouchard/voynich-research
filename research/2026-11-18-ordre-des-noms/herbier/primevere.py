"""Comparer les deux premiers mots aux trois propositions de nom de plante."""
from collections import Counter
from itertools import product
import json
import re
import sys
from transitions import HERE, RESEARCH, UNIT, tokens, write
sys.path.insert(0,str(RESEARCH/"2026-11-18-carte-sept-etoiles/lecture"))
from essai import tables, project

FACES = ("f39v","f40r")
NAMES = ("primula veris","premula veris","herba paralisis")


def spellings():
    result = {}
    for spaces in ("joints","separes"):
        for ed, readings in tokens(FACES,spaces).items():
            words = tuple(tuple(w for _,w in readings[face][:2]) for face in FACES)
            assert all(w for pair in words for w in pair)
            result.setdefault(words,[]).append(f"{ed}_{spaces}")
    return result


def glyphs(word, compound, marker):
    signs=tuple(UNIT.findall(word) if compound else re.findall("c[ktpf]h|sh|.",word))
    if marker and len(signs)>1 and signs[0]=="p":
        return signs[1:]
    return signs


def initial_keys(first, second, name, width):
    return [k for p in tables(first,name,width) for k in tables(second,name,width,p)]


def score(words, source, width, compound, marker):
    (first, second),(third,fourth) = [[glyphs(w,compound,marker) for w in pair] for pair in words]
    name, rest = source.split()
    paired = initial_keys(first,third,name,width)
    proposals = []
    after = Counter()
    for k in paired:
        a = list(tables(second,rest,width,k))
        b = list(tables(fourth,rest,width,k))
        both = [v for partial in a for v in tables(fourth,rest,width,partial)]
        after["compatible_f39v"]+=bool(a)
        after["compatible_f40r"]+=bool(b)
        after["compatibles_ensemble"]+=bool(both)
        if both:
            proposals+=both
    return {"tables_f39v":sum(1 for _ in tables(first,name,width)),
            "tables_f40r":sum(1 for _ in tables(third,name,width)),"sur_les_deux":len(paired),
            "exemple_table":paired[0] if paired else None,
            "exemple_lecture_partielle":[project(second,paired[0]),project(fourth,paired[0])] if paired else [],
            "premieres_tables_compatibles":dict(after),"nombre_de_tables_finales":len(proposals),
            "premieres_lectures":[project(second,k) for k in paired[:5]],
            "exemple_table_finale":proposals[0] if proposals else None}


def main():
    titles=[title.lower() for title in json.loads((RESEARCH/"2026-11-18-opcheor-paralleles/latin/corpus.json").read_text()) if title.isascii() and title.isalpha()]
    output=[]
    for words,eds in spellings().items():
        for width,compound,marker in product((2,3),(True,False),(False,True)):
            initial=[glyphs(p[0],compound,marker) for p in words]
            alternatives={title:n for title in titles if (n:=len(initial_keys(*initial,title,width)))}
            result={src:score(words,src,width,compound,marker) for src in NAMES}
            output.append(dict(lectures=eds,mots=words,longueur=width,banc_compose=compound,
                           p_initial_sans_lettres=marker,noms=result,n_titres_temoins=len(titles),
                           titres_qui_conviendraient_aux_deux=alternatives))
    write("PRIMEVERE.json",output)


if __name__=="__main__":
    main()
