"""Construit cinq modèles fixes avec les seules entrées Hipparcos locales."""
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLEIADES = [(17702, "Alcyone"), (17847, "Atlas"), (17499, "Electra"),
            (17573, "Maia"), (17608, "Merope"), (17531, "Taygeta"),
            (17851, "Pleione"), (17489, "Celaeno"), (17579, "Asterope")]
BIG = [(54061, "Dubhe"), (53910, "Merak"), (58001, "Phecda"),
       (59774, "Megrez"), (62956, "Alioth"), (65378, "Mizar"), (67301, "Alkaid")]
LITTLE = [(11767, "Polaris"), (72607, "Kochab"), (75097, "Pherkad"),
          (85822, "Yildun"), (82080, "Epsilon UMi"), (77055, "Zeta UMi"), (79822, "Eta UMi")]
ADDITIONAL = [(17588, "22 Tau (Sterope II)")]
names = dict(PLEIADES + BIG + LITTLE + ADDITIONAL)
with (HERE / "hipparcos-esa.csv").open() as src:
    records = {int(r["hip"]): r for r in csv.DictReader(src)}
assert set(records) == set(names)
stars = {}
for hip, name in names.items():
    r = records[hip]
    stars[name] = dict(id=f"HIP {hip}", name=name,
                       ra_deg=float(r["ra"]), dec_deg=float(r["de"]), mag=float(r["vmag"]))
def seven(stars_):
    return sorted(stars_, key=lambda s: (s["mag"], s["id"]))[:7]

def vector(star):
    ra, dec = map(math.radians, (star["ra_deg"], star["dec_deg"]))
    return (math.cos(dec) * math.cos(ra), math.cos(dec) * math.sin(ra), math.sin(dec))

def combined(first, second):
    a, b = vector(first), vector(second)
    weights = [10 ** (-0.4 * s["mag"]) for s in (first, second)]
    x, y, z = [weights[0] * u + weights[1] * v for u, v in zip(a, b)]
    return dict(id=first["id"] + "+" + second["id"], name=first["name"] + "+" + second["name"],
                ra_deg=round(math.degrees(math.atan2(y, x)) % 360, 9),
                dec_deg=round(math.degrees(math.atan2(z, math.hypot(x, y))), 9),
                mag=round(-2.5 * math.log10(sum(weights)), 6))

def separation(first, second):
    dot = sum(u * v for u, v in zip(vector(first), vector(second)))
    return round(math.degrees(math.acos(max(-1, min(dot, 1)))) * 60, 6)

pool = [stars[n] for _, n in PLEIADES]
sisters = [s for s in pool if s["name"] not in {"Atlas", "Pleione"}]
parents = combined(stars["Atlas"], stars["Pleione"])
models = {"pleiades_bright7": seven(pool),
          "grande_ourse": [stars[n] for _, n in BIG],
          "petite_ourse": [stars[n] for _, n in LITTLE],
          "pleiades_sisters": seven(sisters),
          "pleiades_blend": seven(sisters + [parents])}
assert all(len(m) == len({s["id"] for s in m}) == 7 for m in models.values())
doc = dict(frame="ICRS", epoch="J1991.25", mag_band="Johnson V",
           source="ESA, 1997, Hipparcos, SP-1200, main catalogue (I/239/hip_main)",
           models=models, catalog_entries=list(stars.values()),
           diagnostics={"atlas_pleione_separation_arcmin": separation(stars["Atlas"], stars["Pleione"]),
                        "asterope_22tau_separation_arcmin": separation(stars["Asterope"], stars["22 Tau (Sterope II)"]),
                        "asterope_22tau_combined_v_for_context_only": combined(stars["Asterope"], stars["22 Tau (Sterope II)"])["mag"]})
(HERE / "modeles.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
with (HERE / "modeles.tsv").open("w") as dst:
    writer = csv.DictWriter(dst, delimiter="\t", fieldnames=["model", "id", "name", "ra_deg", "dec_deg", "mag"], lineterminator="\n")
    writer.writeheader()
    for key, members in models.items():
        writer.writerows(dict(model=key, **s) for s in members)
print(doc["diagnostics"])
for key, members in models.items():
    print(key, ", ".join(star["name"] for star in members))
