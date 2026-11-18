"""Hasard conditionnel exact pour les successeurs du groupe chedy."""

from collections import Counter, defaultdict
from fractions import Fraction
from math import comb


def accord_chedy(lectures):
    it, zl, gc = lectures
    return bool(it and it == zl and gc and ((it == "chedy") == (gc == "1c89")))


def classe(precedent, cible):
    """None pour une comparaison indécidable, sinon chedy, qokeey ou autre."""
    if not accord_chedy(precedent) or not accord_chedy(cible):
        return None
    it, _, gc = cible
    if (it == "qokeey") != (gc == "4ohC9"):
        return None
    if it in {"chedy", "qokeey"}:
        return it
    return "autre"


def poids_hypergeometriques(n, k, m):
    """Poids entiers : somme = nombre de sous-ensembles de m cases parmi n."""
    return {
        succes: comb(k, succes) * comb(n - k, m - succes)
        for succes in range(max(0, m - (n - k)), min(k, m) + 1)
    }


def mesurer(lignes, annonces, strate="face"):
    """Redistribuer qokeey dans chaque strate en gardant les chedy fixes."""
    if strate not in {"face", "ligne"}:
        raise ValueError("Une strate est une face ou une ligne.")
    par_strate = defaultdict(Counter)
    vus = set()
    for ligne in lignes:
        lieu, mots = ligne["id"], ligne["words"]
        if lieu in vus:
            raise ValueError(f"Identifiant de ligne dupliqué {lieu}")
        vus.add(lieu)
        bloc = lieu if strate == "ligne" else lieu.rsplit(".", 1)[0]
        for i in range(1, len(mots)):
            qualite = classe(mots[i - 1], mots[i])
            if qualite is None:
                continue
            cle = (bloc, "fin" if i == len(mots) - 1 else "interieur")
            c = par_strate[cle]
            annonce = (lieu, i) in annonces
            c["lisibles"] += 1
            c["annonces"] += annonce
            if qualite == "chedy":
                c["chedy_fixes"] += 1
                c["annonces_chedy_fixes"] += annonce
            else:
                c["population"] += 1
                c["tires"] += annonce
                c["qokeey"] += qualite == "qokeey"
                c["succes"] += annonce and qualite == "qokeey"

    # Les distributions entières sont multipliées avant une unique normalisation.
    distribution = {0: 1}
    decalage = 0
    esperance = Fraction()
    nb_informatives = 0
    nb_avec_annonce = 0
    details = []
    for (bloc, position), c in sorted(par_strate.items()):
        n, k, m = c["population"], c["qokeey"], c["tires"]
        if not c["annonces"]:
            continue
        nb_avec_annonce += 1
        moyenne = Fraction(k * m, n) if n else Fraction()
        esperance += moyenne
        poids = poids_hypergeometriques(n, k, m)
        if len(poids) == 1:
            decalage += next(iter(poids))
        else:
            nb_informatives += 1
            conv = Counter()
            for x, w in distribution.items():
                for y, v in poids.items():
                    conv[x + y] += w * v
            distribution = conv
        details.append({
            "bloc": bloc, "position": position,
            "n": n, "k_qokeey": k, "m_annonces_permutables": m,
            "annonces_chedy_fixes": c["annonces_chedy_fixes"],
            "succes_observes": c["succes"], "attendus": float(moyenne),
        })

    total = Counter()
    for compte in par_strate.values():
        total.update(compte)
    obs = total["succes"]
    den = sum(distribution.values())
    hist = {s + decalage: w for s, w in sorted(distribution.items())}
    if obs not in hist:
        raise ValueError("Le score observé est hors du support conditionnel.")
    p = Fraction(sum(w for s, w in hist.items() if s >= obs), den)
    evaluable = bool(total["annonces"])
    return {
        "strate": strate, "positions_lisibles": total["lisibles"],
        "annonces_total": len(annonces), "annonces_lisibles": total["annonces"],
        "annonces_indeterminees": len(annonces) - total["annonces"],
        "succes_observes": obs, "total_qokeey": total["qokeey"],
        "positions_non_annoncees_lisibles": total["lisibles"] - total["annonces"],
        "qokeey_non_annonces": total["qokeey"] - obs,
        "positions_chedy_fixes": total["chedy_fixes"],
        "annonces_chedy_fixes": total["annonces_chedy_fixes"],
        "positions_permutables": total["population"],
        "annonces_permutables": total["tires"],
        "attendus": float(esperance) if evaluable else None,
        "esperance_exacte": str(esperance) if evaluable else None,
        "p_unilateral": float(p) if evaluable else None,
        "p_exacte": str(p) if evaluable else None,
        "support_min": min(hist) if evaluable else None,
        "support_max": max(hist) if evaluable else None,
        "loi_constante": len(hist) == 1 if evaluable else None,
        "histogramme": {str(s): float(Fraction(w, den)) for s, w in hist.items()} if evaluable else {},
        "nombre_strates_lisibles": len(par_strate),
        "nombre_strates_avec_annonce": nb_avec_annonce,
        "nombre_strates_informatives": nb_informatives,
        "strates": details,
    }
