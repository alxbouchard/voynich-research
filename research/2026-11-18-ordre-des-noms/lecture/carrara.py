"""Extraire les noms cités entre guillemets de la notice institutionnelle Egerton 2020."""
from html import unescape
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    raw = Path(sys.argv[1]).read_text()
    section = raw.split("The plants depicted are:", 1)[1].split("Plant names are listed", 1)[0]
    section = unescape(re.sub(r"<[^>]+>", "", section))
    sequence = list(dict.fromkeys(re.findall(r'f\.\s*(\d+[rv]):\s*“([^”]+)”', section)))
    assert len(sequence) == 53
    result = []
    for folio, title in sequence:
        name = re.sub(r"^(?:de l[’']|de (?:la|lo|li|le) |del |dei |de )", "", title.lower())
        result.append(dict(folio=folio, titre=title, nom=name))
    (HERE/"CARRARA.json").write_text(json.dumps(result,indent=1,ensure_ascii=False)+"\n")
