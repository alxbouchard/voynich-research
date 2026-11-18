"""Sensitivity to disagreements between editions within a single panel."""
import json
from tables import FULL, MODELS, HERE, MONTHS, SIGNS, groups, inscriptions, normalize, scan


def main():
    sources = [inscriptions(edition)[0] for edition in ("IT2a-n","ZL3b-n")]
    lists = {"mois":MONTHS,"signes":SIGNS, **json.loads((HERE/"sources/listes-historiques.json").read_text())}
    result = []
    for kind,base in (("rubriques",1),("visages",52)):
        for alphabet in ("EVA","ASCII"):
            merged = []
            agreed = []
            for i in FULL:
                raw = [src.get(i+base) for src in sources]
                variants = [groups(r,alphabet,spacing) for r in raw for spacing in ("split","join")]
                if any(v is None for v in variants):
                    merged.append(None)
                else:
                    merged.append(tuple(sorted({s for v in variants for s in v})))
                # Completely remove red locus 2 for the photographic spacing disagreement.
                # Retain only identical raw strings in the strict common-text stress test.
                eligible = raw[0] == raw[1] and not (kind == "rubriques" and i == 1)
                agreed.append(merged[-1] if eligible else None)
            for scenario,panel in (("choix_local_des_editions",merged),("seules_graphies_identiques",agreed)):
                for source,names in lists.items():
                    for form in ("entier","trois"):
                        order = [normalize(w) if form == "entier" else normalize(w)[:3] for w in names]
                        for model in MODELS:
                            res = scan(panel,order,model)
                            result.append({"serie":kind,"alphabet":alphabet,"scenario":scenario,"liste":source,"forme":form,
                                           "modele":model,"secteurs_retenus":[i+1 for i in FULL if panel[i] is not None],
                                           "apprentissage_evaluable":res["apprentissage_evaluable"],
                                           "reserve_evaluable":res["reserve_evaluable"],
                                           "orientations_apprentissage":len(res["orientations_apprentissage"]),
                                           "orientations_compatibles":sum(h["serie_compatible"] for h in res["orientations_apprentissage"])})
    (HERE/"variantes.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
