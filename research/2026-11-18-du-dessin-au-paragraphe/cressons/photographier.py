"""Reproduire la vue d'ensemble des deux dernières étiquettes du rang supérieur."""
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GEOMETRY = ROOT / "research/2026-11-18-noms-dans-une-phrase/enumeration/verticale"
sys.path.insert(0, str(GEOMETRY))
from reperer import boite, recaler


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(cache):
    native = cache / "99v-yale.jpg"
    reference = cache / "99v-ref.jpg"
    chart = cache / "f99v.json"
    sources = json.loads((ROOT / "voynich_resources/yale/image_index.json").read_text())
    source = next(item for item in sources if "/1006247/" in item["url"])
    assert digest(native) == source["sha256"]
    matrix, precision = recaler(reference, native)
    dictionary, layout = json.loads(chart.read_bytes())
    estimates = {}
    for word in ("arol", "otoky"):
        occurrences = [entry for entry in layout if dictionary[entry[0]][0] == word]
        assert len(occurrences) == 1
        estimates[word] = boite(occurrences[0], matrix)

    # The viewer gives approximate word locations. Leave the image free of overlays.
    original = Image.open(native)
    bottom = max(box[3] for box in estimates.values())
    region = (0, 0, original.width, min(original.height, bottom + 725))
    plate = original.crop(region).convert("RGB")
    plate.thumbnail((1500, 950))
    plate.save(HERE / "f99v-rang-superieur.jpg", quality=90)
    metadata = {
        "source": source["url"], "empreinte": digest(native),
        "reference": "https://www.voynichese.com/2/data/folio/image/glance/color/large/f99v.jpg",
        "empreinte_reference": digest(reference),
        "carte": "https://www.voynichese.com/2/data/folio/script/f99v.js",
        "empreinte_carte": digest(chart),
        "region": region, "positions_approximatives_visualiseur": estimates,
        "calage": precision,
    }
    (HERE / "PHOTO.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
