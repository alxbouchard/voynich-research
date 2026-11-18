"""Recompute the preregistered image-recognition gates from locked answers."""
import json
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECIDED = {"moyenne", "haute"}
LEVELS = DECIDED | {"faible", "abstention"}


def read(name):
    return json.loads((HERE / name).read_text())


def canonical(name):
    if not name:
        return None
    return unicodedata.normalize("NFKC", name).strip().casefold()


def assess(series, size):
    readers = [read(f"lecteurs/{reader}_{series}.json") for reader in ("A", "B")]
    items = read(f"evaluation/{series}.json")
    expected = {f"{series}{index:02d}" for index in range(1, size+1)}
    assert set(items) == expected
    assert all(set(reader) == expected for reader in readers)
    confirmed, decided, unchecked = [], [], []
    any_named, both_agree = [], []
    independent = [Counter(), Counter()]
    for code, item in sorted(items.items()):
        decisions = [reader[code] for reader in readers]
        mapped = []
        for index, response in enumerate(decisions):
            assert response["confiance"] in LEVELS and len(response["traits"]) >= 2
            name = canonical(response["nom"])
            equiv = item.get("equivalences", {})
            standard = equiv.get(name, name)
            mapped.append(standard)
            tally = independent[index]
            tally[response["confiance"]] += 1
            if name:
                tally["nom_propose_toute_confiance"] += 1
                if series == "H" and item["reference"] and standard == item["reference"]:
                    tally["nom_juste_toute_confiance"] += 1
            if response["confiance"] in DECIDED:
                assert name
                independent[index]["decision"] += 1
                if series == "H" and item["reference"]:
                    independent[index]["decisions_verifiables"] += 1
                    if standard == item["reference"]:
                        independent[index]["juste"] += 1
        if any(name is not None for name in mapped):
            any_named.append(code)
        if mapped[0] is not None and mapped[0] == mapped[1]:
            both_agree.append(code)
        if (all(v["confiance"] in DECIDED for v in decisions)
                and mapped[0] is not None and mapped[0] == mapped[1]):
            decided.append(code)
            if series == "H":
                if item["reference"] is None:
                    unchecked.append(code)
                elif mapped[0] == item["reference"]:
                    confirmed.append(code)
            elif item.get("ancre_documentee"):
                assert item["graphie_historique"] and item["source"] and item["attache_lisible"]
                confirmed.append(code)
    result = {
        "cartes": size,
        "au_moins_un_nom": any_named,
        "meme_nom_toute_confiance": both_agree,
        "decisions_individuelles": [dict(x) for x in independent],
        "accords_moyens_ou_hauts": decided,
        "accords_confirmes": confirmed,
        "accords_non_verifiables": unchecked,
    }
    if series == "H":
        n = len(decided) - len(unchecked)
        result["accords_verifiables"] = n
        result["accords_verifiables_exacts"] = len(confirmed)
        result["fraction"] = len(confirmed) / n if n else None
        result["seuil_atteint"] = len(confirmed) >= 3 and 3 * len(confirmed) >= 2 * n
        strict = [code for code in decided if items[code]["reference"] and not items[code].get("groupe_historique_large")]
        strict_correct = [code for code in strict if code in confirmed]
        result["genre_moderne_strict"] = {
            "accords_verifiables": strict, "confirmes": strict_correct,
            "seuil_atteint": len(strict_correct) >= 3 and 3 * len(strict_correct) >= 2 * len(strict)}
    else:
        names = {items[code]["graphie_historique"] for code in confirmed}
        result["noms_historiques_distincts"] = sorted(names)
        result["seuil_atteint"] = len(names) >= 3
    return result


if __name__ == "__main__":
    results = {"herbier": assess("H",8), "fragments": assess("V",22)}
    results["ajustement_autorise_par_protocole"] = all(entry["seuil_atteint"] for entry in results.values())
    if not results["ajustement_autorise_par_protocole"]:
        results["lecture"] = {"etat": "arrêt avant ajustement", "regle": None, "predictions_f99": [],
                              "f99": "non testé", "permutation": "non applicable", "prose": "non testée"}
    print(json.dumps(results, indent=2, ensure_ascii=False))
