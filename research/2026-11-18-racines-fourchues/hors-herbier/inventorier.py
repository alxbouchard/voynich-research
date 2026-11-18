"""Vérifier toutes les occurrences autonomes de la forme cible, y compris les désaccords."""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from annoncer import corpus, MODES, sequence


def main():
    editions, _ = corpus()
    h, z = editions.values()
    rows = []
    for loc in dict.fromkeys([*h, *z]):
        readings, types = [], []
        for ed in (h, z):
            types.append(ed[loc][1] if loc in ed else None)
            for cut in MODES:
                readings.append([w for _, w in sequence(ed[loc][3], cut)] if loc in ed else [])
        if not any("arol" in words for words in readings):
            continue
        rows.append({"locus":loc,"types":types,"lectures":readings,
                     "mot_dans_quatre_lectures":all("arol" in w for w in readings),
                     "seul_mot_quatre_lectures":all(w == ["arol"] for w in readings)})
    (HERE / "TOUS-LES-LIEUX.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n")
    for row in rows:
        print(row["locus"], row["types"], row["mot_dans_quatre_lectures"], row["seul_mot_quatre_lectures"])


if __name__ == "__main__":
    main()
