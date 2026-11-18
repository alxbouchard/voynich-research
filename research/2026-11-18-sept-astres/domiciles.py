"""Count possible rulers in every twelve-sector wheel with seven occupied positions."""
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIGNS = "Bélier Taureau Gémeaux Cancer Lion Vierge Balance Scorpion Sagittaire Capricorne Verseau Poissons".split()
RULERS = "Mars Vénus Mercure Lune Soleil Mercure Vénus Mars Jupiter Saturne Saturne Jupiter".split()
OBSERVED = (1,3,5,6,7,8,11)


def check(mask):
    fits = []
    for first in range(1,13):
        for step in (1,-1):
            index = [((s-first)*step)%12 for s in mask]
            rulers = [RULERS[j] for j in index]
            if len(set(rulers))==7:
                fits.append({"secteur_du_belier":first,"sens":step,
                             "signes":[SIGNS[j] for j in index],"astres":rulers})
    return fits


if __name__ == "__main__":
    counts = Counter(len(check(m)) for m in itertools.combinations(range(1,13),7))
    assert sum(counts.values()) == 792 and len(check(OBSERVED)) == 2
    report = {"secteurs":OBSERVED,"solutions":check(OBSERVED),"distribution_sur_792":dict(sorted(counts.items())),
              "masques_avec_solution":792-counts[0]}
    (HERE/"domiciles.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
