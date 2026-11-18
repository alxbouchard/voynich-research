"""Refait la recherche avec les rubriques de la copie de 1478 et vérifie la forme avec article."""
import gzip
import json
from comparer import HERE, corpus, maps, normal, prepare, read, save, units, verify
from verifier_independant import audit


def catalogue():
    rows = read(HERE / "macer1478" / "RUBRIQUES.json")
    return {"Macer1478": {
        r["rang"]: (r["folio"], normal(r["nom"])) for r in rows
        if r["nom"] and not r["incertain"]
    }}


def rubrique_carrara():
    predictions = json.loads(gzip.decompress((HERE / "PREDICTIONS.json.gz").read_bytes()))
    key, = [record["key"] for block in predictions for record in block["models"].get("1", [])
            if record["book"] == "Carrara"]
    # The original diplomatic titles include the article. Fix both word boundaries.
    rows = []
    for width in (1, 2, 3):
        for label, prior in [("amorce", key), ("libre", {})]:
            full = any(next(maps(units("arody"), "molom", width, first), None) is not None
                       for first in maps(units("otar"), "del", width, prior))
            singles = {word: next(maps(units(word), "molom", width, prior), None)
                       for word in ("otar", "arody")}
            rows.append(dict(width=width, table=label, full=full, single=singles))
    return rows


if __name__ == "__main__":
    editions, _ = corpus()
    catalog = catalogue()
    predictions = prepare(editions, catalog)
    results = verify(editions, catalog, predictions)
    checks = audit(catalog, predictions, results)
    save("COPIE-1478.json.gz", dict(predictions=predictions, resultats=results,
         nombre_controles=checks, article=rubrique_carrara()))
