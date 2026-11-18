"""Réutilise les règles du premier protocole sur une autre prédiction et un cahier réservé."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "protocole_initial"))
import fleurs


def run(args):
    train = fleurs.read(args.apprendre)
    prediction_path = args.sortie / "PREDICTIONS.json"
    frozen = fleurs.read(prediction_path) if args.evaluer else None
    decisions, evaluation = {}, {}
    for tx, fn in fleurs.EDITIONS.items():
        for split in (False, True):
            key = tx + ("_separe" if split else "_joint")
            pages = fleurs.charger(args.donnees / fn, split, ("A", "B", "C"))
            target = sorted(f for f, obj in pages.items() if obj.cahier == "A")
            fit_pages = set(pages) - set(target)
            assert len(fit_pages) == 30 and len(target) == 15
            fleurs.valider_avis(train, fit_pages)
            model = fleurs.entrainer(pages, fleurs.consensus(train))
            estimates = fleurs.predire(pages, model, target)
            decisions[key] = {"modele": model[0], "predictions": estimates,
                              "sha256_donnees": fleurs.empreinte(args.donnees / fn),
                              "sha256_avis_apprentissage": fleurs.empreinte(args.apprendre)}
            if args.evaluer:
                assert decisions[key] == frozen[key]
                gold = fleurs.read(args.evaluer)
                fleurs.valider_avis(gold, set(target))
                agreed = fleurs.consensus(gold)
                evaluation[key] = {"mesures": {m: fleurs.matrice(estimates, agreed, m) for m in fleurs.MODELES},
                                   "controle": {m: fleurs.controle_apparie(pages, estimates, agreed, m) for m in fleurs.MODELES},
                                   "accord_positif_negatif": agreed,
                                   "exclusions": {f: pair for f, pair in gold.items() if f not in agreed},
                                   "sha256_avis_epreuve": fleurs.empreinte(args.evaluer)}
    if args.evaluer:
        fleurs.dump(args.sortie / "RESULTATS.json", evaluation)
    else:
        fleurs.dump(prediction_path, decisions)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--apprendre", required=True, type=Path)
    cli.add_argument("--evaluer", type=Path)
    cli.add_argument("--donnees", required=True, type=Path)
    cli.add_argument("--sortie", required=True, type=Path)
    run(cli.parse_args())
