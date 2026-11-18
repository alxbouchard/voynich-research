# Reproduction du chiffre publié de 0,58 %

L’exemplaire téléchargé le 18 novembre 2026 porte l’en-tête IVTFF Eva- 1.7, version **ZL 1r du 11 avril 2020**. Son SHA-256 est `1632f3269b8b79e813bd9904daf6589cf860b22fb88a9addb47e1dedde523467` (fichier original, fins de ligne CRLF). Les trois filtres publiés par oshfdk rendent les trois effectifs annoncés. [Fichier d’origine](https://www.voynich.nu/data/previous/ZL_ivtff_1r.txt) · [Méthode publiée par oshfdk](https://github.com/oshfdk/f67r2planets/blob/9cdd099422878e1524b9a5be6ba7674359999ba6/meaning.md#prefix-probabilities-in-a-text)

| Ce que le filtre compte | Résultat retrouvé |
|---|---:|
| Occurrences du motif « espace, point ou chevron, suivi d’une lettre minuscule » sur les lignes commençant par `<f` | 35 949 |
| Lignes dont l’en-tête satisfait au filtre de légende de l’auteur | 1 033 |
| Occurrences de `op` immédiatement après un espace, un point ou un chevron dans ces lignes | 53 |

Dans cette édition, les 53 occurrences se trouvent dans 53 légendes distinctes. Après retrait de l’en-tête de locus et des commentaires IVTFF, **52** de ces légendes commencent par `op`. Dans f75v.50, le texte est `otal.opal` et le préfixe appartient au second mot. Les trois occurrences de `ytoa` sont toutes initiales dans une légende entière (f2r.14, f67r2.37, f72r3.30). Il en va de même pour les trois occurrences initiales de `yfa` (f67r2.47, f72r3.28, f73v.15). [Transcription vérifiée](https://www.voynich.nu/data/previous/ZL_ivtff_1r.txt)

## Arithmétique et événement étudié

L’auteur retire les sept légendes sources de f67r2. Il compte deux emplacements restants de l’ancre `ytoa`, deux exemplaires de `yfa` et six places voisines pour chaque ancre. Il obtient **2 × 6 × 2 / 1 025 = 2,34146 %**. Pour `op`, il multiplie ensuite ce nombre par **5 × (53 − 1) / 1 024**. Avec le 2,3 % arrondi utilisé dans son texte, le produit donne **0,583984375 %**. En conservant la première fraction exacte, le même produit donne **0,5945121951 %**. Les deux étapes sont des approximations d’occupation. [Calcul dans la version d’octobre 2023](https://github.com/oshfdk/f67r2planets/blob/9cdd099422878e1524b9a5be6ba7674359999ba6/meaning.md#prefix-probabilities-in-a-text)

La recherche historique avait déjà rencontré `ytoar` grâce à `ytoaiin`. L’un des deux emplacements qu’intègre le facteur 2 est la feuille botanique f2r.14, l’autre est f72r3.30 dans l’anneau du Cancer. En conditionnant sur **ce dernier anneau déjà choisi et son ancre fixée**, on demande seulement si une étiquette en `yfa` et une en `op` se rencontrent dans les six autres positions. Si l’on veut rejouer toute la découverte, il faut aussi préciser quels groupes et quels préfixes auraient pu conduire au choix d’un autre panneau. Ni cette sélection ni les sept appariements ni le sens des mots n’entrent dans le produit publié. [Récit de sélection du panneau](https://github.com/oshfdk/f67r2planets/blob/a79c3f8523344d53c9df24032d98ad7265d220a2/noteon72r3.md)

## Commandes de reproduction

Depuis le répertoire où se trouve le fichier, les trois commandes reprennent les expressions régulières publiées, avec `grep -E` et `grep -Eo`. L’ordre des sorties est celui du premier tableau.

```sh
export LC_ALL=C
grep -E '^<f' ZL_ivtff_1r.txt | grep -Eo '[ .>][a-z]' | wc -l
grep -E '^<f[^>]+L[^.]*?> ' ZL_ivtff_1r.txt | wc -l
grep -E '^<f[^>]+L[^.]*?>' ZL_ivtff_1r.txt | grep -Eo '[.> ]op' | wc -l
```

Cette vérification additionnelle mesure la position de `op` dans la légende complète. Les deux sorties sont 52 et la ligne f75v.50.

```python
import re
from pathlib import Path

lignes = Path("ZL_ivtff_1r.txt").read_text(encoding="latin-1").splitlines()
legendes = [ligne for ligne in lignes if re.match(r"^<f[^>]+L[^.]*?> ", ligne)]
debuts = 0
autres = []
for ligne in legendes:
    entete, corps = ligne.split(">", 1)
    corps = re.sub(r"<![^>]*>", "", corps).strip()
    if corps.startswith("op"):
        debuts += 1
    elif re.search(r"[.> ]op", ligne):
        autres.append((entete + ">", corps))
print(debuts)
print(autres)
```
