"""Inspecter la source des deux fragments lus comme um et mesurer leur effet."""
from collections import Counter
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

from phrase import HERE, confirm, corpus, predict, save


def repaired(xml):
    chapters = corpus(xml)["Celse"]
    source = ET.parse(xml)
    def paragraph(book, chapter, idx):
        section = source.find(f".//{{*}}div[@subtype='book'][@n='{book}']/{{*}}div[@n='{chapter}']")
        return "".join(section.findall("{*}p")[idx-1].itertext())

    assert "qüum magnam" in paragraph(6,6,1)
    assert "il!um esse spinosum" in paragraph(7,26,3)
    first, second = "6.6.p1.1", "6.6.p1.2"
    assert chapters[first][-1]=="q" and chapters[second][0]=="um"
    chapters[first] = chapters[first][:-1] + ["quum"] + chapters.pop(second)[1:]
    locus = "7.26.p3.1"
    words = chapters[locus]
    idx, = [i for i in range(len(words)-1) if words[i:i+2]==["il","um"]]
    chapters[locus] = words[:idx]
    chapters[locus+"-apres"] = words[idx+2:]
    return chapters


def main():
    fixed = repaired(Path(sys.argv[1]))
    lexicon = {w for row in fixed.values() for w in row}
    assert "um" not in lexicon
    pages = json.loads((HERE/"TRANSFERT.json").read_text())["pages"]
    generated = Counter()
    for page in pages.values():
        for word,r in page["readings"].items():
            generated[(word, r["form"])] += r["n"]
    output = {
        "forms": [{"voynich":w,"read":d,"occurrences":n,"after_cleaning":d in lexicon}
                  for (w,d),n in sorted(generated.items())],
        "recheck": []
    }
    for marker in (False,True):
        for width in (2,3):
            candidates = predict(fixed,width,marker)
            result = confirm(fixed,candidates,width,set())
            output["recheck"].append({"initial_marker":marker,"width":width,
                         "summary":result["counts"],"matches":result["third_word_recovered"]})
    save("SENSIBILITE.json",output)


if __name__=="__main__":
    main()
